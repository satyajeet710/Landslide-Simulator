<?php

session_start();
error_reporting(0);

// VERIFY: CHANGE FROM HERE
$alpha = 3.5; // adjust sensitivity for smart_cubic
$beta = 1.2;  // for smart_linear (scaling factor)
// VERIFY: TILL HERE

if(!isset($_SESSION['uid'])) {
$_SESSION['process'] = 'false';
//header('Location: http://pratik.acslab.org/index.php');
header('Location: ./index.php');
    die();

} else if(!isset($_GET['decision']) || $_SESSION['process'] == 'true' || !isset($_SESSION['process'])) {
$_SESSION['process'] = 'false';
    //header('Location: http://pratik.acslab.org/game.php');
header('Location: ./game.php');
    die();

} else {

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
    return $data;}

if(!empty($_POST['invest'])) {
    $invest = test_input($_POST['invest']);
   // $planChosen = test_input($POST['chooseplan']);
    $_SESSION['invest'] = $invest;
} else { //header('Location: http://pratik.acslab.org/index.php'); 

$invest = test_input($_POST['invest']);
   // $planChosen = test_input($POST['chooseplan']);
    $_SESSION['invest'] = $invest;

//header('Location: http://localhost/pratik/index.php');
//die(); 
  }

echo json_encode($_POST, JSON_PRETTY_PRINT);
$V1 = test_input($_POST['invest-retaining_walls']);
echo $V1;
$_SESSION['invest-retaining_walls'] =  $V1;
$v2 = test_input($_POST['invest-drainage_systems']);
$_SESSION['invest-drainage_systems']= $v2;
echo $v2;
$v3 = test_input($_POST['invest-land_use_planning']);
$_SESSION['invest-land_use_planning'] = $v3;
echo $v3;
$v4 = test_input($_POST['invest-soil_classification']);
$_SESSION['invest-soil_classification'] = $v4;
echo $v4;
$v5= test_input($_POST['invest-tree_planting']);
$_SESSION['invest-tree_planting'] = $v5;
echo $v5;
$v6 = test_input($_POST['invest-water_management']);
$_SESSION['invest-water_management'] = $v6;
echo $v6;

$chkOne = test_input($_POST['checkOne']);
$chkTwo = test_input($_POST['checkTwo']);
$chkThree = test_input($_POST['checkThree']);

$_SESSION['checkOne'] = $chkOne;
$_SESSION['checkTwo'] = $chkTwo;
$_SESSION['checkThree'] = $chkThree;


$hinsur=$chkOne;
$linsur=$chkTwo;
$pinsur=$chkThree;

$day = $_SESSION['day'];
$unqid = $_SESSION['uid'];
$consent = $_SESSION['consent'];
$conn = new mysqli("localhost", "root", "", "linearsmart");
    
//inputs

/*if($planChosen == "lifeinsurance"){
  $_SESSION['daily_income'] = 1;
}

if($planChosen == "healtheinsurance"){
  $_SESSION['daily_income'] = 2;
}
if($planChosen == "propertyinsurance"){
  $_SESSION['daily_income'] = 3;
}
if($planChosen == "lifehealthinsurance"){
  $_SESSION['daily_income'] = 4;
}
if($planChosen == "healthpropertyinsurance"){
  $_SESSION['daily_income'] = 5;
}
if($planChosen == "lifepropertyinsurance"){
  $_SESSION['daily_income'] = 6;
}
if($planChosen == "lifepropertyhealthinsurance"){
  $_SESSION['daily_income'] = 7;
}*/


//$sqltest = "SELECT * FROM game WHERE id=".$unqid." AND day=".$day.";";
//if(mysqli_query($conn,$sqltest)) {
//header('Location: http://pratik.acslab.org/game.php');
//die();
//}
$_SESSION['cumulative_invest'] = $_SESSION['cumulative_invest'] + $invest;
$cumulative_invest = $_SESSION['cumulative_invest'];
$M = $_SESSION['return_mitigation'];
$money_ini = $_SESSION['money_ini'];
$d_f_inv = $_SESSION['d_f_inv'];
$wealth_property = $_SESSION['wealth_property'];

$_SESSION['income_unaffected_cumulative'] = $_SESSION['income_unaffected_cumulative'] + $_SESSION['daily_income'];
$income_unaffected_cumulative = $_SESSION['income_unaffected_cumulative'];
$p_property = $_SESSION['p_property'];
$p_injury = $_SESSION['p_injury'];
$p_fatality = $_SESSION['p_fatality'];
$daily_income = $_SESSION['daily_income'];
$w_i = $_SESSION['weight_invest'];
$inj_loss = $_SESSION['injury_daily_inc_loss'];
$fat_loss = $_SESSION['fatality_daily_inc_loss'];
//processing part
//outputs

$rand_property = round(mt_rand() / mt_getrandmax(),5);
$rand_fatality = round(mt_rand() / mt_getrandmax(),5);
$rand_injury = round(mt_rand() / mt_getrandmax(),5);
$p_temporal = $_SESSION['p_temporal'];

$p_spatial = $_SESSION['p_spatial'];
$p_rain = $p_temporal * $p_spatial; $p_rain = $_SESSION['p_rain'];

$p_investment = $_SESSION['p_invest'];

// VERIFY: DELTE FROM HERE
// $p_investment = 1 - $M * ($cumulative_invest / $income_unaffected_cumulative) * ( $cumulative_invest / $income_unaffected_cumulative) *  (  $cumulative_invest / $income_unaffected_cumulative); $_SESSION['p_invest'] = $p_investment;
// VERIFY: TILL HERE DELETE

// VERIFY: CHANGE FROM HERE
$investment_ratio = $cumulative_invest / $income_unaffected_cumulative;

// Smart linear scaling with cap at 1
$smart_effect = min(1, $beta * $investment_ratio);

$p_investment = 1 - $M * $smart_effect;

// VERIFY: TILL HERE 
$p_landslide = $p_rain * ( 1 - $w_i ) + $p_investment * ( $w_i );
    $_SESSION['p_landslide'] = $p_landslide;
$landslide_threshold = round(mt_rand() / mt_getrandmax(),5);;
    if($p_landslide >= $landslide_threshold)
    {  $landslide = 1;

     if($p_property >= $rand_property) 
      {  $damage_property =1 ;
      //$_SESSION['dmg_property']=$_SESSION['daily_income'];
      if ($_SESSION['checkThree']==0){
        $damage = $wealth_property * $money_ini;
        $_SESSION['money_ini'] = ( 1 - $wealth_property) * $_SESSION['money_ini'];
        } 
        else 
          {
            $damage_property =0;
            $damage = 0;
          }
       }
        
  if($p_fatality >= $rand_fatality) 
  { $damage_fatality =1;
    $_SESSION['dmg_fatality']=$_SESSION['daily_income'];
  if ($_SESSION['checkTwo']==0){
    $_SESSION['daily_income'] = (1 - $fat_loss) * $_SESSION['daily_income'];
    $_SESSION['dmg_fatality']=$_SESSION['dmg_fatality'] - $_SESSION['daily_income'];
    } 
    else 
      {
        $damage_fatality =0;
      }
   }
      
  if($p_injury >= $rand_injury) 
  {
    $damage_injury =1 ;
    $_SESSION['dmg_injury']=$_SESSION['daily_income'];
    if ($_SESSION['checkOne']==0){
      $_SESSION['daily_income'] = (1 - $inj_loss) * $_SESSION['daily_income'];
      $_SESSION['dmg_injury']=$_SESSION['dmg_injury'] - $_SESSION['daily_income'];
  } 
  else 
    {$damage_injury =0;
      
    }

    }
  }
    else 
      {    $landslide = 0;$damage_property = 0;$damage_fatality = 0;$damage_injury = 0;    
      }

    // if($damage_property == 1 && $_SESSION['checkThree']==0) {
    //     $damage = $wealth_property * $money_ini;$_SESSION['money_ini'] = ( 1 - $wealth_property) * $_SESSION['money_ini'];
    // } elseif($damage_property == 1 && $_SESSION['checkThree']!=0) {
    //     $damage = 0;} 
    //   elseif($damage_property == 0) {$damage = 0;}

$hinsur=$chkOne;
$linsur=$chkTwo;
$pinsur=$chkThree;

$final_money = $_SESSION['final_money'];
$net_money = $_SESSION['daily_income'] - $invest - $hinsur - $linsur - $pinsur - $damage; $final_money = $final_money + $net_money;
$_SESSION['final_money'] = $final_money;
$t_span = $_SESSION['time_span'];
//$daily_income = $_SESSION['daily_income'];
$_SESSION['invest'] = $invest;

$_SESSION['final_money_array'][$_SESSION['day']] = round($_SESSION['money_ini'],2);
$_SESSION['damage_array'][$_SESSION['day']] = round($damage,2);
$_SESSION['p_landslide_array'][$_SESSION['day']] = round($p_landslide,2);
$_SESSION['daily_income_array'][$_SESSION['day']] = round($daily_income,1);
$d_i_t = $_SESSION['day_initial_temporal'];
$_SESSION['message_property']=$damage_property;
$_SESSION['message_fatality']=$damage_fatality;
$_SESSION['message_injury']=$damage_injury;
$_SESSION['dmg_property']=$damage;



$invest_retaining_walls =        $_SESSION['invest-retaining_walls'];
$invest_drainage_systems =        $_SESSION['invest-drainage_systems'];
$invest_land_use_planning =        $_SESSION['invest-land_use_planning'];
$invest_soil_classification =        $_SESSION['invest-soil_classification'];
$invest_tree_planting =        $_SESSION['invest-tree_planting'];
$invest_water_management =        $_SESSION['invest-water_management'];

$sqlo = "INSERT INTO game (consent, id, day, invest,  `invest-retaining_walls`, `invest-drainage_systems`,  `invest-land_use_planning`, `invest-soil_classification`, `invest-tree_planting`, `invest-water_management`,hinsur, linsur, pinsur, cumulative_invest, weight_invest, daily_income, rand_property, rand_fatality, rand_injury, p_temporal, p_spatial, p_rain, p_investment, p_landslide, landslide_threshold, landslide, damage_property, damage_fatality, damage_injury, damage, net_money, final_money, return_mitigation, money_ini, time_span, dampening_factor_investment, wealth_property, p_property, p_fatality, p_injury, injury_daily_inc_loss, fatality_daily_inc_loss, day_initial_temporal)
VALUES('$consent','$unqid','$day','$invest','$invest_retaining_walls','$invest_drainage_systems','$invest_land_use_planning','$invest_soil_classification','$invest_tree_planting','$invest_water_management', '$hinsur', '$linsur', '$pinsur','$cumulative_invest','$w_i','$daily_income','$rand_property','$rand_fatality','$rand_injury','$p_temporal','$p_spatial','$p_rain','$p_investment','$p_landslide','$landslide_threshold','$landslide','$damage_property','$damage_fatality','$damage_injury','$damage','$net_money','$final_money','$M','$money_ini','$t_span','$d_f_inv','$wealth_property','$p_property','$p_fatality','$p_injury','$inj_loss','$fat_loss','$d_i_t')";
echo "Query: \n" . $sqlo;

$resulto=mysqli_query($conn,$sqlo);

 $_SESSION['process'] = 'true';
//if($_SESSION['day'] == $t_span) {
   //     header('Location: http://pratik.acslab.org/end.php'); die();
    //}

if(isset($_SESSION['nbr_pay'])) {
$sqlnbr = "SELECT pay FROM nbr_pay WHERE day=" . $_SESSION['day'] . ";" ;
 $resultnbr = mysqli_query($conn,$sqlnbr);
$rownbr=mysqli_fetch_array($resultnbr,MYSQLI_ASSOC);
$_SESSION['nbr_pay'] = $rownbr["pay"];
}

if($landslide == 1) {
$_SESSION['day'] += 1;
        //header('Location: http://pratik.acslab.org/landslide_positive.php'); 
        header('Location: ./landslide_positive.php');
        die();
}
    else{ $_SESSION['day'] += 1;
//header('Location: http://pratik.acslab.org/landslide_negative.php'); 
header('Location: ./landslide_negative.php');
die();}

mysqli_close($conn);
}
?>
