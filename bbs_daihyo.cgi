#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ��\��p�f���� Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]�̕��͓���܂���") if $m{country} eq '0';
&error("�S�����͕]�c��ɂ͓���܂���") if $m{lib} eq 'prison';
&error("���̑�\\�҂łȂ��Ɠ���܂���") unless &is_daihyo;

$this_title  = "�e����\\�]�c��";
$this_file   = "$logdir/bbs_daihyo";
$this_script = 'bbs_daihyo.cgi';

#=================================================
&run;
&footer;
exit;
