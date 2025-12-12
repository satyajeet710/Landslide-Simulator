<?php 
    session_start();
    include 'head.php';
    unset($_SESSION['process']);
    
    // Validate required session variables
    $required_sessions = [
        'invest', 
        'checkOne', 
        'checkTwo', 
        'checkThree', 
        'daily_income', 
        'final_money_array', 
        'day', 
        'final_money', 
        'time_span'
    ];
    
    foreach ($required_sessions as $sess) {
        if (!isset($_SESSION[$sess])) {
            $_SESSION[$sess] = 0; // Set default value
        }
    }
    ?>
<!-- Game page when landslide does not occur -->
<!DOCTYPE html>
<html lang="en">
    
<body>
    <!--HEADER, no header needed -->
    
    <!-- BODY -->
    <div class="container-fluid">
        <div class="row">
            <div class="jumbotron">
                <h2 class="text-center"><i class="fa fa-smile-o"></i> Landslide did not Occur! 
                 <!--   <?php echo  $_SESSION['scenario_id']; ?> -->
                </h2>
                <br><br>
<p>You made <strong><?php echo  $_SESSION['invest'];?></strong> investment against landslides and you spent <strong><?php echo  $_SESSION['checkOne']+$_SESSION['checkTwo']+$_SESSION['checkThree'];?></strong> in buying different types of insurance </p>
<!--               <?php if(isset($_SESSION['nbr_pay']) ) { ?>
                <p><strong>Your friend invested: <?php echo $_SESSION['nbr_pay']; ?> </strong></p>
<?php }
?> -->
                <p>Overall, your income stays at <strong><?php echo round($_SESSION['daily_income'],1);?></strong>.</p>
            
                <p>Overall, your property wealth stays at <strong><?php echo $_SESSION['final_money_array'][$_SESSION['day']-1] ;?></strong>.</p>
                <p>Your total wealth is <strong><?php echo round($_SESSION['final_money'],1); ?></strong>.</p>
            <br>
                <?php if($_SESSION['day']-1 == $_SESSION['time_span']) {echo "<a href='end.php'><button class='btn btn-warning'>Return To Game</button></a>";} else { echo "<a href='game.php'><button class='btn btn-warning'>Return To Game</button></a>"; } ?><br><br>
                
                </div>
        </div>
    </div>
    <!-- FOOTER -->
    <?php include 'footer.php';?>
</body>
</html>