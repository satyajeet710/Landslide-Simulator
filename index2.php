<?php

    session_start();
    $unqid = uniqid('',true);
    $_SESSION["uid"] = "$unqid";
    $cryptid = md5($unqid);
    $_SESSION["cid"] = "$cryptid";
    //header('Location: http://pratik.acslab.org/consent.php?id='.$cryptid);
header('Location: ./consent.php?id='.$cryptid);
    die();
?>