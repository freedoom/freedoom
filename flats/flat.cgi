#!/usr/bin/perl -w
# I am a perlscript

use CGI qw(param);

$flat = param("flat") or die "BAH";
$flat =~ s/deutex\/flats\///;
$backme = "/showflats.cgi";
print <<EOF ;

<!doctype html public "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>$flat</title></head>
<body background="$flat">
<table bgcolor="#000000"><tr><td><a href="$backme"><font color="#ffffff">Back</font></a></td></tr></table>
</body></html>
EOF
