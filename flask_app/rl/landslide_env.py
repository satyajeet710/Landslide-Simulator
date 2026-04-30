import random
import numpy as np

# Default game parameters — mirrors what the param table holds
DEFAULT_PARAMS = {
    'daily_income':          8760.0,
    'money_ini':             500000.0,
    'time_span':             12,
    'return_mitigation':     0.8,
    'weight_invest':         0.5,
    'p_property':            0.5,
    'p_fatality':            0.3,
    'p_injury':              0.4,
    'wealth_property':       0.3,
    'injury_daily_inc_loss': 0.1,
    'fatality_daily_inc_loss': 0.5,
    # insurance costs (fixed, from game.html)
    'cost_health_insur':     1173.0,
    'cost_life_insur':       488.0,
    'cost_property_insur':   1884.0,
}

# p_temporal per month (mirrors the reference table, 12 months)
# index 0 = month 1, index 11 = month 12
P_TEMPORAL = [0.05, 0.05, 0.08, 0.10, 0.15, 0.20,
              0.25, 0.22, 0.18, 0.12, 0.08, 0.05]


class LandslideEnv:
    """
    Standalone simulation of one full game (time_span months).
    No Flask, no DB, no session — pure Python.

    STATE (7 values, all normalized 0-1):
        [day/time_span, income/income_ini, property/property_ini,
         p_rain, cumulative_invest/total_possible_invest,
         last_p_landslide, last_damage_flag]

    ACTION (single integer index):
        0  — invest nothing, no insurance
        1  — invest 10% of income
        2  — invest 20% of income
        3  — invest 30% of income
        4  — buy health insurance only
        5  — buy life insurance only
        6  — buy property insurance only
        7  — buy all three insurances
        8  — invest 10% + all insurances
        9  — invest 20% + all insurances

    REWARD:
        net change in total wealth this step
        minus a large penalty if uninsured damage occurs
    """

    ACTIONS = [
        # (invest_pct, health_ins, life_ins, prop_ins)
        (0.0,  False, False, False),  # 0 — do nothing
        (0.1,  False, False, False),  # 1 — invest 10%
        (0.2,  False, False, False),  # 2 — invest 20%
        (0.3,  False, False, False),  # 3 — invest 30%
        (0.0,  True,  False, False),  # 4 — health ins only
        (0.0,  False, True,  False),  # 5 — life ins only
        (0.0,  False, False, True),   # 6 — property ins only
        (0.0,  True,  True,  True),   # 7 — all insurances
        (0.1,  True,  True,  True),   # 8 — invest 10% + all ins
        (0.2,  True,  True,  True),   # 9 — invest 20% + all ins
    ]
    N_ACTIONS = len(ACTIONS)
    STATE_SIZE = 7

    def __init__(self, params=None):
        self.params = {**DEFAULT_PARAMS, **(params or {})}
        self.state = None
        self.reset()

    def reset(self):
        p = self.params
        self.day                       = 0
        self.daily_income              = p['daily_income']
        self.income_ini                = p['daily_income']
        self.money_ini                 = p['money_ini']
        self.property_ini              = p['money_ini']
        self.final_money               = p['money_ini']
        self.cumulative_invest         = 0.0
        self.income_unaffected_cumul   = 0.0
        self.p_spatial                 = round(random.random(), 2)
        self.last_p_landslide          = 0.0
        self.last_damage_flag          = 0.0
        self.done                      = False
        self.state                     = self._get_state()
        return self.state

    def step(self, action_idx):
        assert not self.done, "Game is over. Call reset()."
        p = self.params
        invest_pct, buy_health, buy_life, buy_prop = self.ACTIONS[action_idx]

        # --- costs this month ---
        invest   = invest_pct * self.daily_income
        chk_one  = p['cost_health_insur']   if buy_health else 0.0
        chk_two  = p['cost_life_insur']     if buy_life   else 0.0
        chk_three= p['cost_property_insur'] if buy_prop   else 0.0
        total_spend = invest + chk_one + chk_two + chk_three

        # cap spend to available income
        if total_spend > self.daily_income:
            invest = max(0.0, self.daily_income - chk_one - chk_two - chk_three)
            total_spend = invest + chk_one + chk_two + chk_three

        # --- landslide probability ---
        self.cumulative_invest       += invest
        self.income_unaffected_cumul += self.daily_income

        M            = p['return_mitigation']
        w_i          = p['weight_invest']
        inv_ratio    = self.cumulative_invest / (self.income_unaffected_cumul or 1)
        smart_effect = min(1.0, 1.2 * inv_ratio)
        p_investment = 1.0 - M * smart_effect

        month_idx    = min(self.day, len(P_TEMPORAL) - 1)
        p_temporal   = P_TEMPORAL[month_idx]
        p_rain       = self.p_spatial * p_temporal
        p_landslide  = p_rain * (1 - w_i) + p_investment * w_i
        self.last_p_landslide = p_landslide

        # --- damage resolution ---
        damage = 0.0
        damage_flag = 0.0
        if p_landslide >= random.random():
            damage_flag = 1.0
            if p['p_property'] >= random.random():
                if not buy_prop:
                    damage = p['wealth_property'] * self.money_ini
                    self.money_ini = (1 - p['wealth_property']) * self.money_ini
            if p['p_fatality'] >= random.random():
                if not buy_life:
                    self.daily_income *= (1 - p['fatality_daily_inc_loss'])
            if p['p_injury'] >= random.random():
                if not buy_health:
                    self.daily_income *= (1 - p['injury_daily_inc_loss'])

        self.last_damage_flag = damage_flag

        # --- wealth update ---
        net = self.daily_income - total_spend - damage
        self.final_money += net

        # --- reward ---
        # base reward = net wealth gained this step
        # extra penalty if damage happened and player had no insurance
        reward = net
        if damage_flag and not (buy_health or buy_life or buy_prop):
            reward -= damage * 0.5   # extra penalty for being completely unprotected

        # --- advance day ---
        self.day += 1
        self.done = self.day >= p['time_span']
        self.state = self._get_state()

        return self.state, reward, self.done

    def _get_state(self):
        p = self.params
        tspan = p['time_span']
        max_invest = self.income_ini * tspan
        return np.array([
            self.day / tspan,
            self.daily_income / (self.income_ini or 1),
            self.money_ini / (self.property_ini or 1),
            self.p_spatial * P_TEMPORAL[min(self.day, len(P_TEMPORAL)-1)],  # p_rain
            self.cumulative_invest / (max_invest or 1),
            self.last_p_landslide,
            self.last_damage_flag,
        ], dtype=np.float32)
