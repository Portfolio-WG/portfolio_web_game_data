#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# 共通掲示板 Created by Merino
#=================================================
&get_data;

$this_title  = "$title掲示板";
$this_file   = "$logdir/bbs_public";
$this_script = 'bbs_public.cgi';
$this_sub_title = qq|<br>書き込み権限のある人しか書き込めません。バグ報告は<a href="letter.cgi?id=$id&pass=$pass&send_name=ｱﾙﾋﾞｽ">こちら</a>へ<br>挨拶は交流へ|;
@writer_member = ($admin_name, $admin_sub_name, $admin_support_name);

#=================================================
&run;
&footer;
exit;
