<?php
session_start();

// Validate session
if(!isset($_SESSION['uid'])) {
    header('Location: ./index.php');
    exit();
}

// Add validation for required session variables
$required_sessions = [
    'invest', 
    'checkOne', 
    'checkTwo', 
    'checkThree',
    'daily_income',
    'money_ini',
    'dmg_injury',
    'dmg_fatality', 
    'dmg_property'
];

foreach($required_sessions as $sess) {
    if(!isset($_SESSION[$sess])) {
        $_SESSION[$sess] = 0; // Set default value
    }
}

// Initialize database connection
$conn = new mysqli("localhost", "root", "", "linearsmart");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch death images data
$query_death = "SELECT * FROM death_images";
$result_death = $conn->query($query_death);

// Check if query was successful
if ($result_death) {
    $rowdth1 = array();
    while ($row = $result_death->fetch_assoc()) {
        $rowdth1[] = $row;
    }
} else {
    // Handle query error
    $rowdth1 = array(); // Initialize empty array as fallback
}

// Validate before using array_rand
if (!empty($rowdth1)) {
    $random_death = array_rand($rowdth1);
} else {
    $random_death = 0; // Default value if no images found
}
?>
<!-- Game page when landslide occurs -->
<!DOCTYPE html>
<html lang="en">
    <?php include 'head.php';unset($_SESSION['process']); ?>
<body>
    <!--HEADER, no header needed -->
    
    <!-- BODY -->
    <div class="container-fluid">
        <div class="row">
            <div class="jumbotron">
                <h2 class="text-center"><i class="fa fa-exclamation-triangle"></i> Landslide Occurred!  
                   <!-- <?php echo  $_SESSION['scenario_id']; ?> -->
                </h2>
                <!--SAD MESSAGE START -->
                <br><br>
                <p>You made <strong><?php echo  $_SESSION['invest'];?></strong> investment against landslides and you spent <strong><?php echo  $_SESSION['checkOne']+$_SESSION['checkTwo']+$_SESSION['checkThree'];?></strong> in buying different types of insurance. </p>
<!--               <?php if(isset($_SESSION['nbr_pay']) ) { ?>
                <p><strong>Your friend invested: <?php echo $_SESSION['nbr_pay']; ?> </strong></p>
<?php }
?> -->
                <?php
               if($_SESSION['message_injury'] && $_SESSION['checkOne']!=0)
                {
                    echo "<p>Sorry, a wage-earner of your family got injured in a car accident while traveling with a friend. As you purchased health insurance, your monthly income was not affected and stays the same at "; echo "<strong>"; echo round($_SESSION['daily_income'],1); echo "</strong>.</p>";
                    
                }
                elseif ($_SESSION['message_injury'] && $_SESSION['checkOne']==0) { 

                    echo "<p>Sorry, a wage-earner of your family got injured in a car accident while traveling with a friend. As you did not purchase health insurance, your monthly income was  affected and it decreased to "; echo "<strong>"; echo round($_SESSION['daily_income'],1); echo "</strong>.</p>";
                    
                }
                else {echo "<p>Fortunately, no one in your family was injured.</p>"; echo "<p>Thus, your monthly income was not affected and stays at the same value.</p>";
                
				} 

				 if($_SESSION['message_fatality'] && $_SESSION['checkTwo']!=0)
                {
                    echo "<p>Sorry, a wage-earner of your family got buried under the debris of the mudslide. As you purchased life insurance, your monthly income was not affected and stays the same at"; echo "<strong>"; echo round($_SESSION['daily_income'],1); echo "</strong>.</p>";
                }
                elseif ($_SESSION['message_fatality'] && $_SESSION['checkTwo']==0) { 

                    echo "<p>Sorry, a wage-earner of your family got buried under the debris of the mudslide. As you did not purchase life insurance, your monthly income was affected and it decreased to "; echo "<strong>"; echo round($_SESSION['daily_income'],1); echo "</strong>.</p>";
                    
                }
                else {echo "<p>Fortunately, no one in your family died. Thus, your monthly income was not affected and stays at the same value.</p>";
                    
                }
                
                  ?>
                

            <?php    if($_SESSION['message_property'] && $_SESSION['checkThree']!=0)
                {       $_SESSION['invest']=0;
                    echo "<p>Sorry, your house was destroyed by the debris. As you purchased property insurance, the total damage occurred is "; echo "<strong>"; echo round($_SESSION['dmg_property'],1); echo "</strong>.</p>";
                    
             ?>
<p>Thus, your property wealth is <strong><?php echo round($_SESSION['final_money_array'][$_SESSION['day']-1],1) ;?></strong>.</p>
 <?php  }
elseif ($_SESSION['message_property'] && $_SESSION['checkThree']==0) {
    echo "<p>Sorry, your house was destroyed by the debris. As you did not purchase property insurance, the total damage occurred is "; echo "<strong>"; echo round($_SESSION['dmg_property'],1); echo "</strong>.</p>";
}
elseif (!$_SESSION['message_property']) {echo "<p>Fortunately, none of your property was harmed.</p>";
echo "<p>Thus, your property wealth was not affected and stays at the same value.</p>";
}
                ?>
                
                <p>Your total wealth is <strong><?php echo round($_SESSION['final_money'],1); ?></strong>.</p>
            <br>
                <?php if($_SESSION['day']-1 == $_SESSION['time_span']) {echo "<a href='end.php'><button class='btn btn-warning'>Return To Game</button></a>";} else { echo "<a href='game.php'><button class='btn btn-warning'>Return To Game</button></a>"; }?><br><br>
                <div class="row">
                <?php
                //code for images to be displayed
 $conn1 = new mysqli("localhost", "root", "","linearsmart");
$scenario_id = $_SESSION['scenario_id'];
if($_SESSION['message_fatality']) {
$sqldth = "SELECT image_source FROM death_images WHERE scenario_id='$scenario_id'";
    if($resultdth = mysqli_query($conn1,$sqldth)){
        
       $i = 0; 
       while($rowdth=mysqli_fetch_array($resultdth,MYSQLI_NUM))
        {
            $rowdth1[$i] = $rowdth[0];$i++;
        }
        $random_keys_dth = array_rand($rowdth1);
        $dth_img_src = $rowdth1[$random_keys_dth];
        
        echo "<div class='col-md-4'><embed height='400' width='100%' src='";echo $dth_img_src; echo "'></div>";
    }
}
if($_SESSION['message_injury']){
    $sqlinj = "SELECT image_source FROM injury_images WHERE scenario_id='$scenario_id'";
    if($resultinj = mysqli_query($conn1,$sqlinj)){
        $i =0 ;
        while($rowinj=mysqli_fetch_array($resultinj,MYSQLI_NUM)) {
            $rowinj1[$i] = $rowinj[0];$i++;
        }
        $random_keys_inj = array_rand($rowinj1);
        $inj_img_src = $rowinj1[$random_keys_inj];
        
        echo "<div class='col-md-4'><embed height='400' width='100%' src='";echo $inj_img_src; echo "'></div>";
    }
}
if($_SESSION['message_property']){
    $sqlprop = "SELECT image_source FROM property_images WHERE scenario_id='$scenario_id'";
    if($resultprop = mysqli_query($conn1,$sqlprop)){
        $i=0;
        while($rowprop=mysqli_fetch_array($resultprop,MYSQLI_NUM)) {
            $rowprop1[$i] = $rowprop[0];$i++;
        }
        
        $random_keys_prop = array_rand($rowprop1);
        $prop_img_src = $rowprop1[$random_keys_prop];
        
        echo "<div class='col-md-4'><embed height='400' width='100%' src='";echo $prop_img_src; echo "'></div>";
    }
}               
                mysqli_close($conn1);
                ?><br><br>
            </div>
                </div>
        </div>
    </div>
    <!-- FOOTER -->
    <?php include 'footer.php';?>
</body>
</html>