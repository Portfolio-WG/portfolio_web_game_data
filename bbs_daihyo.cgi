#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# 代表専用掲示板 Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]の方は入れません") if $m{country} eq '0';
&error("牢獄中は評議会には入れません") if $m{lib} eq 'prison';
&error("国の代表\者でないと入れません") unless &is_daihyo;

$this_title  = "各国代表\評議会";
$this_file   = "$logdir/bbs_daihyo";
$this_script = 'bbs_daihyo.cgi';

#=================================================
&run;
&footer;
exit;
