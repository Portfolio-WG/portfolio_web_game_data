#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# 同盟掲示板 Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]の方はご利用できません") if $m{country} eq '0';
&error("他の国と同盟を組んでいません") unless $union;
&error("牢獄中は同盟会議室には入れません") if $m{lib} eq 'prison';
my $u = &union($m{country}, $union);

$this_title  = "$cs{name}[$m{country}]+$cs{name}[$union] 同盟会議室";
$this_file   = "$logdir/union/$u";
$this_script = 'bbs_union.cgi';

#=================================================
&run;
&footer;
exit;
