<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<html>
<head>
	<title>moo!</title>
</head>

<?php
 $file=array();
 $i=0;

 if(empty($flat) == 0)
  {
   printf("<body background=\"%s\">\n", $flat);
   printf("<table><tr><td bgcolor=black text=white>\n");
   printf("<a href=\"%s\"><font color=#ffffff>Back to image index</font></a><br>\n", $PHP_SELF);   
   printf("</td></tr></table>\n");
  }
 else {
   printf("<body>\n");
   $handle=opendir('.');
   while($filex = readdir($handle)) {
    $file[$i]=$filex;
	$i++;
   }
  
  for($j=0; $j != $i; $j++)
   {
    if(strstr($file[$j], ".gif") == true)
	 printf("<a href=\"%s?flat=%s\">%s</a><br>\n", $PHP_SELF, $file[$j], $file[$j]);
   }
   closedir($handle);
  }
?>

</body>
</html>

