#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# 共通掲示板 Created by Merino
#=================================================
&get_data;
&error("$cs{name}[$w{country}]の方は入れません") if $m{country} eq $w{country};
&error("NPC国と同盟の国は封印騎士団本部には入れません") if $w{"p_$m{country}_$w{country}"} eq '1';
#&error("牢獄中は封印騎士団本部には入れません") if $m{lib} eq 'prison';

$this_title  = "封印騎士団本部";
$this_file   = "$logdir/bbs_vs_npc";
$this_script = 'bbs_vs_npc.cgi';
$this_sub_title = "対NPC国軍";

#=================================================
&run;
&footer;
exit;
