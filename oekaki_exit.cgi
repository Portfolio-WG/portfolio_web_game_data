#!/usr/bin/perl --
require './lib/system.cgi';
#================================================
# お絵描き後処理(url_exit) Created by Merino
#================================================
&decode;

my $name = pack 'H*', $in{id};

my $image_type = -f "./user/$in{id}/picture/_$in{time}.png" ? 'png' : 'jpeg';
$mes .= qq|<img src="./user/$in{id}/picture/_$in{time}.$image_type"><br>絵を$nameのﾏｲﾋﾟｸﾁｬに保存しました<br>|;
require 'bj.cgi';
exit;

