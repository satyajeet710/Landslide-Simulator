from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory
from flask import Response
from db import init_db_pool, get_conn
import uuid, hashlib
import os
import math
import random
import smtplib
from email.message import EmailMessage
from ml_model import get_ml_probabilities

app = Flask(__name__, static_folder='../')
app.secret_key = os.environ.get('FLASK_SECRET', 'change-me')

# DB config — matches original PHP defaults
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'linearsmart'
}

init_db_pool(DB_CONFIG)

# Serve existing repo static folders (so templates can reference /css/* and /js/* exactly as before)
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'js'), filename)

@app.route('/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'fonts'), filename)

@app.route('/<filename>.png')
def serve_root_images(filename):
    # serve simple root-level images like /23.png or /final.JPG referenced by templates
    return send_from_directory(os.path.join(app.root_path, '..'), f"{filename}.png")


@app.route('/<path:filename>.html')
def serve_root_html(filename):
    # serve root-level html files (e.g., /impress2.html)
    return send_from_directory(os.path.join(app.root_path, '..'), f"{filename}.html")


@app.route('/message_day/<path:filename>')
def serve_message_day(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'message_day'), filename)


@app.route('/<filename>.jpg')
def serve_root_jpg(filename):
    # try root first
    root_file = os.path.join(app.root_path, '..', f"{filename}.jpg")
    if os.path.exists(root_file):
        return send_from_directory(os.path.join(app.root_path, '..'), f"{filename}.jpg")
    # try message_day folder
    md_file = os.path.join(app.root_path, '..', 'message_day', f"{filename}.jpg")
    if os.path.exists(md_file):
        return send_from_directory(os.path.join(app.root_path, '..', 'message_day'), f"{filename}.jpg")
    return "", 404

# Helpers
def query_one(query, params=None):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params or ())
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

def query_all(query, params=None):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def execute(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    # ensure parameter count matches number of %s placeholders to avoid mysql connector ProgrammingError
    if params is None:
        use_params = ()
    else:
        use_params = tuple(params)
    placeholder_count = query.count('%s')
    if len(use_params) != placeholder_count:
        if len(use_params) > placeholder_count:
            use_params = use_params[:placeholder_count]
        else:
            use_params = use_params + (None,) * (placeholder_count - len(use_params))
    try:
        cur.execute(query, use_params)
        conn.commit()
    except Exception as e:
        # add debug context for column/value mismatch or param issues
        placeholder_count = query.count('%s')
        msg = f"SQL execution failed: {e}; placeholders={placeholder_count}; params_provided={len(use_params)}; params={use_params}"
        cur.close(); conn.close()
        raise RuntimeError(msg)
    cur.close(); conn.close()

# Routes
@app.route('/')
def index():
    # reset session similar to PHP index.php
    session.clear()
    session['uid'] = str(uuid.uuid4()).replace('-', '')
    return render_template('index.html')

@app.route('/index2')
def index2():
    unqid = str(uuid.uuid4())
    session['uid'] = unqid
    cryptid = hashlib.md5(unqid.encode()).hexdigest()
    session['cid'] = cryptid
    return redirect(url_for('consent', id=cryptid))

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    id_param = request.args.get('id')
    if not id_param:
        return render_template('oops.html', message='Please go to start (index2)')

    # fetch latest scenario age restriction
    row = query_one('SELECT scenario_id FROM param')
    sno = row['scenario_id'] if row else 1
    row2 = query_one('SELECT age_restriction FROM param WHERE scenario_id=%s', (sno,))
    age_restriction = row2['age_restriction'] if row2 else 18

    if request.method == 'POST':
        cq1 = request.form.get('cq1')
        cq2 = request.form.get('cq2')
        cq3 = request.form.get('cq3')
        if cq1 and cq2 and cq3 and cq1=='1' and cq2=='1' and cq3=='1':
            session['consent'] = True
            return redirect(url_for('connect', id=session.get('cid')))
        else:
            flash('You must answer all consent questions and agree to continue', 'warning')
    return render_template('consent.html', age_restriction=age_restriction, id=id_param)

@app.route('/connect')
def connect():
    id_param = request.args.get('id')
    if not id_param:
        return render_template('oops.html', message='Missing id')
    try:
        # quick check for DB connectivity
        r = query_one('SELECT 1 as ok')
    except Exception as e:
        return render_template('oops.html', message='DB connection failed: ' + str(e))
    session['connect'] = True
    return redirect(url_for('demographic', id=session.get('cid'), connect='true'))

@app.route('/demographic', methods=['GET', 'POST'])
def demographic():
    if not request.args.get('id'):
        return render_template('oops.html', message='Please start from index2')
    if not request.args.get('connect'):
        return render_template('oops.html', message='Please connect first')
    if not session.get('consent'):
        return render_template('oops.html', message='Session expired or consent missing')

    if request.method == 'POST':
        # minimal validation and insertion
        uid = session.get('uid')
        age = request.form.get('age')
        gender = request.form.get('gender')
        ed = request.form.get('ed')
        occ = request.form.get('occ')
        major = request.form.get('major')
        email = request.form.get('email')
        city = request.form.get('city')
        # collect additional demographic fields to match PHP form
        live = request.form.get('live')
        liveno = request.form.get('liveno')
        livelong = request.form.get('livelong')
        livereason = request.form.get('livereason')
        dwell = request.form.get('dwell')
        dwellother = request.form.get('dwellother')
        household = request.form.get('household')
        owner = request.form.get('owner')
        source = request.form.get('source')
        sourceother = request.form.get('sourceother')
        income = request.form.get('income')
        know = request.form.get('know')

        # insert demographic (match PHP columns)
        sql = """INSERT INTO demographic (id, Age, Gender, Education, Occupation, Major, Email, city_belong_to, liveno_currently_live, live_long, livereason, dwell_type, household_size, owner, source_of_income, income, knowledge) 
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        execute(sql, (uid, age, gender, ed, occ, major, email, city, live, liveno, livelong, livereason, dwell, household, owner, source, income, know))
        # initialize game similar to PHP: fetch param
        row = query_one('SELECT * FROM param WHERE scenario_id=%s', (1,))
        if row:
            session['day']=0
            session['cumulative_invest']=0
            session['scenario_id'] = row['scenario_id']
            session['injury_daily_inc_loss'] = row.get('injury_daily_inc_loss')
            session['fatality_daily_inc_loss'] = row.get('fatality_daily_inc_loss')
            session['weight_invest'] = row.get('weight_invest')
            session['d_f_inv'] = row.get('dampening_factor_investment')
            session['wealth_property'] = row.get('wealth_property')
            session['daily_income'] = row.get('daily_income')
            session['money_ini'] = row.get('money_ini')
            session['return_mitigation'] = row.get('return_mitigation')
            session['time_span'] = row.get('time_span')
            session['p_property'] = row.get('p_property')
            session['p_fatality'] = row.get('p_fatality')
            session['p_injury'] = row.get('p_injury')
            # spatial interpolation (simplified)
            rand_spatial = round(random.random(),2)
            session['rand_spatial'] = rand_spatial
            session['final_money'] = session['money_ini']
            # initialize arrays used by the game charts (match PHP initialization)
            tspan = int(session.get('time_span', 0) or 0)
            # ensure numeric session values are plain floats
            session['daily_income'] = float(session.get('daily_income') or 0)
            session['money_ini'] = float(session.get('money_ini') or 0)
            session['final_money'] = float(session.get('final_money') or 0)
            session['city'] = city
            session['daily_income_array'] = [None] * (tspan + 1)
            session['daily_income_array'][0] = session['daily_income']
            session['final_money_array'] = [None] * (tspan + 1)
            session['final_money_array'][0] = session['money_ini']
            session['income_not_invested'] = [None] * (tspan + 1)
            session['damage_array'] = [0] * (tspan + 1)
            session['daychart'] = list(range(0, tspan + 1))
            # use None for future (unset) slots so charts show gaps instead of zeros
            session['p_landslide_array'] = [None] * (tspan + 1)
            # set current initial month to 0
            if len(session['p_landslide_array']) > 0:
                session['p_landslide_array'][0] = 0

            # store day_initial_temporal so later rows can use it
            session['day_initial_temporal'] = row.get('day_initial_temporal')

            # insert initial game row
            execute('''INSERT INTO game (rand_spatial,consent, id, day, weight_invest, daily_income, money_ini, return_mitigation, time_span, p_property, p_fatality, p_injury, p_spatial, dampening_factor_investment, wealth_property, injury_daily_inc_loss, fatality_daily_inc_loss, day_initial_temporal) 
                       VALUES (%s,%s,%s,0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (rand_spatial, session.get('consent'), uid, session['weight_invest'], session['daily_income'], session['money_ini'], session['return_mitigation'], session['time_span'], session['p_property'], session['p_fatality'], session['p_injury'], session['p_spatial'], session['d_f_inv'], session['wealth_property'], session['injury_daily_inc_loss'], session['fatality_daily_inc_loss'], row.get('day_initial_temporal')))
        return redirect(url_for('instruction', id=session.get('cid')))

    return render_template('demographic.html')

@app.route('/instruction')
def instruction():
    if not session.get('uid'):
        return redirect(url_for('index'))
    return render_template('instruction.html')

@app.route('/game', methods=['GET'])
def game():
    if not session.get('connect'):
        return redirect(url_for('connect'))

    day = session.get('day', 1)

    # Convert day → month
    month_num = ((day - 1) % 12) + 1

    # Get user city
    city = session.get('city', 'Mandi')

    # 🔥 ML Prediction
    p_spatial, p_temporal = get_ml_probabilities(city, month_num)

    # Store in session
    session['p_spatial'] = p_spatial
    session['p_temporal'] = p_temporal

    # Combined probability
    session['p_rain'] = p_spatial * p_temporal

    return render_template(
        'game.html',
        income=session.get('daily_income'),
        day=day,
        p_spatial=round(p_spatial, 3),
        p_temporal=round(p_temporal, 3)
    )
@app.route('/process', methods=['POST'])
def process():
    # ported simplified logic from process.php
    if not session.get('uid'):
        return redirect(url_for('index'))
    invest = float(request.form.get('invest', 0) or 0)
    chkOne = float(request.form.get('checkOne', 0) or 0)
    chkTwo = float(request.form.get('checkTwo', 0) or 0)
    chkThree = float(request.form.get('checkThree', 0) or 0)

    # persist choices into session so outcome pages can read them
    session['invest'] = invest
    session['checkOne'] = chkOne
    session['checkTwo'] = chkTwo
    session['checkThree'] = chkThree

    session['cumulative_invest'] = session.get('cumulative_invest',0) + invest
    income_unaffected_cumulative = session.get('income_unaffected_cumulative',0) + session.get('daily_income',0)
    session['income_unaffected_cumulative'] = income_unaffected_cumulative
    M = session.get('return_mitigation',1)
    w_i = session.get('weight_invest',0.5)

    cumulative_invest = session['cumulative_invest']
    investment_ratio = cumulative_invest / (income_unaffected_cumulative or 1)
    beta = 1.2
    smart_effect = min(1, beta * investment_ratio)
    p_investment = 1 - M * smart_effect
    p_rain = session.get('p_rain', 0.0)
    p_landslide = p_rain * (1 - w_i) + p_investment * w_i
    session['p_landslide'] = p_landslide

    rand_property = random.random()
    rand_fatality = random.random()
    rand_injury = random.random()
    p_property = session.get('p_property', 0.0)
    p_fatality = session.get('p_fatality', 0.0)
    p_injury = session.get('p_injury', 0.0)

    damage = 0
    damage_property = 0
    damage_fatality = 0
    damage_injury = 0

    if p_landslide >= random.random():
        if p_property >= rand_property:
            damage_property = 1
            if chkThree == 0:
                damage = session.get('wealth_property',0) * session.get('money_ini',0)
                session['money_ini'] = (1 - session.get('wealth_property',0)) * session.get('money_ini',0)
            else:
                damage_property = 0
        if p_fatality >= rand_fatality:
            damage_fatality = 1
            if chkTwo == 0:
                session['daily_income'] = (1 - session.get('fatality_daily_inc_loss',0)) * session['daily_income']
        if p_injury >= rand_injury:
            damage_injury = 1
            if chkOne == 0:
                session['daily_income'] = (1 - session.get('injury_daily_inc_loss',0)) * session['daily_income']

    final_money = session.get('final_money',0) + (session.get('daily_income',0) - invest - chkOne - chkTwo - chkThree - damage)
    session['final_money'] = final_money
    # store damage and outcome flags for landslide pages
    session['dmg_property'] = damage
    session['message_property'] = 1 if damage_property else 0
    session['message_fatality'] = 1 if damage_fatality else 0
    session['message_injury'] = 1 if damage_injury else 0

    # update chart arrays at current day index (match PHP behavior)
    day_idx = int(session.get('day', 0) or 0)
    # ensure arrays exist and are long enough
    def ensure_length(name, length, default=None):
        arr = session.get(name)
        if not isinstance(arr, list) or len(arr) < length:
            new = [default] * length
            if isinstance(arr, list):
                for i, v in enumerate(arr):
                    if i < len(new):
                        new[i] = v
            session[name] = new
        return session.get(name)

    ensure_length('final_money_array', day_idx + 1, None)
    ensure_length('p_landslide_array', day_idx + 1, None)
    ensure_length('daily_income_array', day_idx + 1, 0)
    ensure_length('income_not_invested', day_idx + 1, 0)
    ensure_length('damage_array', day_idx + 1, 0)

    # property wealth after possible damage
    session['final_money_array'][day_idx] = round(session.get('money_ini', 0), 2)
    session['damage_array'][day_idx] = round(damage, 2)
    session['p_landslide_array'][day_idx] = round(p_landslide, 2)
    session['daily_income_array'][day_idx] = round(session.get('daily_income', 0), 1)

    # update cumulative income not invested (NTM): previous + (daily_income - invest - insurances)
    prev_ntm = 0
    if day_idx > 0:
        prev_ntm = session.get('income_not_invested', [0])[day_idx - 1] or 0
    ntm_add = (session.get('daily_income', 0) - invest - chkOne - chkTwo - chkThree)
    session['income_not_invested'][day_idx] = round(prev_ntm + ntm_add, 1)

    # collect per-investment breakdown from the form to match PHP
    invest_retaining_walls = float(request.form.get('invest-retaining_walls', 0) or 0)
    invest_drainage_systems = float(request.form.get('invest-drainage_systems', 0) or 0)
    invest_land_use_planning = float(request.form.get('invest-land_use_planning', 0) or 0)
    invest_soil_classification = float(request.form.get('invest-soil_classification', 0) or 0)
    invest_tree_planting = float(request.form.get('invest-tree_planting', 0) or 0)
    invest_water_management = float(request.form.get('invest-water_management', 0) or 0)

    # landslide threshold used to decide occurrence (stored in DB)
    landslide_threshold = round(random.random(), 5)
    landslide_flag = 1 if p_landslide >= landslide_threshold else 0

    net_money = session.get('daily_income', 0) - invest - chkOne - chkTwo - chkThree - damage

    # ensure required non-null DB columns have sensible defaults
    day_initial_temporal_val = session.get('day_initial_temporal') if session.get('day_initial_temporal') is not None else 1

    # insert game row (columns match DB `game` table order; exclude auto timestamp/sno)
    execute('''INSERT INTO game (consent, id, day, invest, hinsur, linsur, pinsur, cumulative_invest, weight_invest, time_span, daily_income, return_mitigation, dampening_factor_investment, p_property, rand_property, p_fatality, rand_fatality, p_injury, rand_injury, p_temporal, rand_spatial, p_spatial, p_rain, p_investment, p_landslide, landslide_threshold, landslide, fatality_daily_inc_loss, damage_fatality, injury_daily_inc_loss, damage_injury, wealth_property, damage_property, money_ini, damage, net_money, final_money, day_initial_temporal, `invest-retaining_walls`, `invest-drainage_systems`, `invest-land_use_planning`, `invest-soil_classification`, `invest-tree_planting`, `invest-water_management`)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (
                session.get('consent'),            # consent
                session.get('uid'),                # id
                session.get('day'),                # day
                invest,                            # invest
                chkOne,                            # hinsur
                chkTwo,                            # linsur
                chkThree,                          # pinsur
                session['cumulative_invest'],     # cumulative_invest
                w_i,                               # weight_invest
                session.get('time_span'),          # time_span
                session.get('daily_income'),       # daily_income
                session.get('return_mitigation'),  # return_mitigation
                session.get('d_f_inv'),            # dampening_factor_investment
                session.get('p_property'),         # p_property
                rand_property,                     # rand_property
                session.get('p_fatality'),         # p_fatality
                rand_fatality,                     # rand_fatality
                session.get('p_injury'),           # p_injury
                rand_injury,                       # rand_injury
                session.get('p_temporal'),         # p_temporal
                session.get('rand_spatial', session.get('p_spatial')),  # rand_spatial (fallback)
                session.get('p_spatial'),          # p_spatial
                p_rain,                            # p_rain
                p_investment,                      # p_investment
                p_landslide,                       # p_landslide
                landslide_threshold,               # landslide_threshold
                landslide_flag,                    # landslide
                session.get('fatality_daily_inc_loss'), # fatality_daily_inc_loss
                damage_fatality,                   # damage_fatality
                session.get('injury_daily_inc_loss'),   # injury_daily_inc_loss
                damage_injury,                     # damage_injury
                session.get('wealth_property'),    # wealth_property
                damage_property,                   # damage_property
                session.get('money_ini'),          # money_ini
                damage,                            # damage
                net_money,                         # net_money
                final_money,                       # final_money
                day_initial_temporal_val, # day_initial_temporal
                invest_retaining_walls,            # invest-retaining-walls
                invest_drainage_systems,           # invest-drainage-systems
                invest_land_use_planning,          # invest-land-use-planning
                invest_soil_classification,        # invest-soil-classification
                invest_tree_planting,              # invest-tree-planting
                invest_water_management            # invest-water-management
            ))

    # if nbr_pay feature is enabled in session, refresh today's pay from DB (mirrors PHP behavior)
    if session.get('nbr_pay') is not None:
        try:
            row_nbr = query_one('SELECT pay FROM nbr_pay WHERE day=%s', (session.get('day'),))
            if row_nbr and row_nbr.get('pay') is not None:
                session['nbr_pay'] = row_nbr.get('pay')
        except Exception:
            # leave session value as-is on error
            pass

    session['process'] = True
    # choose redirect
    if p_landslide >= random.random():
        session['day'] = session.get('day',0) + 1
        return redirect(url_for('landslide_positive'))
    else:
        session['day'] = session.get('day',0) + 1
        return redirect(url_for('landslide_negative'))

@app.route('/landslide_positive')
def landslide_positive():
    scenario_id = session.get('scenario_id')
    death_img = None
    inj_img = None
    prop_img = None
    if scenario_id:
        try:
            if session.get('message_fatality'):
                rows = query_all('SELECT image_source FROM death_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    death_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
            if session.get('message_injury'):
                rows = query_all('SELECT image_source FROM injury_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    inj_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
            if session.get('message_property'):
                rows = query_all('SELECT image_source FROM property_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    prop_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
        except Exception:
            pass
    return render_template('landslide_positive.html', death_img=death_img, inj_img=inj_img, prop_img=prop_img)

@app.route('/landslide_negative')
def landslide_negative():
    scenario_id = session.get('scenario_id')
    death_img = None
    inj_img = None
    prop_img = None
    if scenario_id:
        try:
            if session.get('message_fatality'):
                rows = query_all('SELECT image_source FROM death_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    death_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
            if session.get('message_injury'):
                rows = query_all('SELECT image_source FROM injury_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    inj_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
            if session.get('message_property'):
                rows = query_all('SELECT image_source FROM property_images WHERE scenario_id=%s', (scenario_id,))
                if rows:
                    prop_img = random.choice([r['image_source'] for r in rows if r.get('image_source')])
        except Exception:
            pass
    return render_template('landslide_negative.html', death_img=death_img, inj_img=inj_img, prop_img=prop_img)


# Diagnostic route `/__diag/game_schema` removed

@app.route('/end')
def end():
    return render_template('end.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    # show any existing session-banner then clear it (mirrors PHP session banner behavior)
    if request.method == 'GET':
        banner = session.pop('banner', None)
        if banner:
            flash(banner, 'success')
        return render_template('contact.html')

    # POST: process form and optionally send email using SMTP env vars
    name = request.form.get('name')
    email_addr = request.form.get('email')
    body = request.form.get('body')

    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = int(os.environ.get('SMTP_PORT', '0') or 0)
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    smtp_use_tls = os.environ.get('SMTP_USE_TLS', 'true').lower() in ('1', 'true', 'yes')
    contact_recipient = os.environ.get('CONTACT_RECIPIENT') or smtp_user or 'admin@example.com'

    subject = f"Contact form message from {name}"
    msg_text = f"From: {name} <{email_addr}>\n\n{body}"

    sent_ok = False
    send_error = None
    if smtp_host and smtp_port and smtp_user and smtp_pass:
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = contact_recipient
            msg.set_content(msg_text)

            if smtp_use_tls:
                server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
                server.starttls()
                server.login(smtp_user, smtp_pass)
            else:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            sent_ok = True
        except Exception as e:
            send_error = str(e)

    # set session banner like PHP so it's shown after redirect
    if sent_ok:
        session['banner'] = f"Message sent. Thank you, {name}"
    else:
        # if SMTP not configured, still set success banner but note not sent; if error occurred, show warning
        if smtp_host:
            session['banner'] = f"Message NOT sent due to error: {send_error or 'unknown'}"
        else:
            session['banner'] = f"Message received. (Email not configured on this server.) Thank you, {name}"

    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)
