#!/usr/bin/perl --
use Time::HiRes;
$load_time = Time::HiRes::time unless $load_time;
require './lib/system.cgi';
require './lib/move_player.cgi';
use File::Copy;
#================================================
# ﾌﾟﾚｲﾔｰ一覧HTML作成 + 期限切れﾌﾟﾚｲﾔｰ削除
# & Cookieｾｯﾄ(PCのみ) Created by Merino
#================================================

# ﾌﾟﾚｲﾔｰ一覧HTML更新周期(日) 1日〜
my $update_cycle_day = 1;

# Cookie保存期間(日)
my $limit_cookie_day = 30;


#================================================
&decode;
$in{is_cookie} ? &set_cookie($in{login_name},$in{pass},1) : &del_cookie unless $is_mobile;
require 'bj.cgi';

# 統一者あらわれず
if ($time > $w{limit_time}) {
	require './lib/reset.cgi';
	&time_limit;
}

#&summary_contribute;

# htmlﾌｧｲﾙ作成 & 期限切れﾌﾟﾚｲﾔｰ削除
for my $i (0 .. $w{country}) {
	if (-M "./html/$i.html" >= $update_cycle_day) {
#	if (-M "./html/$i.html" >= 0) {
		&write_players_html($i);
		last;
	}
}

my $chart_time = (stat "./html/chart_img.html")[9];
if($chart_time < $time - 3600){
	&chart_backup;
}

if (-M "./html/all.html" >= $update_cycle_day) {
#if (-M "./html/$i.html" >= 0) {
	&write_all_players_html;
	&backup_players;
}
#&make_player_name_list;
#&refresh_new_commer;

exit;

#=================================================
# ｸｯｷｰｾｯﾄ
#=================================================
sub set_cookie {
	my @cooks = @_;

	local($csec,$cmin,$chour,$cmday,$cmon,$cyear,$cwday) = gmtime(time + $limit_cookie_day * 24 * 60 * 60); # 24時間 * 60分 * 60秒
	local @mons = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	local @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	local $expirese_time = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$cwday],$cmday,$mons[$cmon],$cyear+1900,$chour,$cmin,$csec);

	for my $c (@cooks) {
		$c =~ s/(\W)/sprintf("%%%02X", unpack "C", $1)/eg;
		$cook .= "$c<>";
	}

	print "Set-Cookie: bj=$cook; expires=$expirese_time\n";
}

# ------------------
# ｸｯｷｰ削除
sub del_cookie {
	my $expires_time = 'Thu, 01-Jan-1970 00:00:00 GMT';
	print "Set-Cookie: bj=dummy; expires=$expires_time\n";
}


#=================================================
# 国ごとのhtmlﾌｧｲﾙ作成
#=================================================
# 表示する項目を増減する場合は、@rows と 130行目周辺を編集してね

sub write_players_html {
	my $country = shift;

	my @rows = (qw/名前 性別 階級 部隊 職業 種族 武器 ﾀﾏｺﾞ ﾍﾟｯﾄ 世代 Lv HP MP AT DF MAT MDF AG LEA CHA お金 ｺｲﾝ 更新時間 ﾒｯｾｰｼﾞ 参入日時/);

	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;

	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	open my $fh, "< $logdir/$country/member.cgi";
	while (my $player = <$fh>) {
		$player =~ tr/\x0D\x0A//d;

		# 同じ名前の人が複数いる場合
		next if ++$sames{$player} > 1;

		my $player_id = unpack 'H*', $player;

		# 存在しない場合はﾘｽﾄから削除
		unless (-f "$userdir/$player_id/user.cgi") {
			&move_player($player, $country, 'del');
			next;
		}

		my %p = &get_you_datas($player_id, 1);

		# 削除期限になり自動削除
		if ($time > $p{ltime} + $auto_delete_day * 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			# 自動削除延命ﾍﾟｯﾄを装備しているなら自動削除日＋24日は削除しない
			if ($pets[$p{pet}][2] eq 'life_up') {
				if ($time > $p{ltime} + ($auto_delete_day + 30) * 3600 * 24) {
					&move_player($player, $country, 'del');
					next;
				}
			}
			else {
				&move_player($player, $country, 'del');
				next;
			}
		}
		# ﾁﾗ見だけの人(１世代目のレベル１)を５日目で削除
		elsif ($p{lv} <= 1 && $p{sedai} <= 1 && $time > $p{ltime} + 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			&move_player($player, $country, 'del');
			next;
		}
		# ﾊﾞｸﾞなどで違う国の人が所属している場合
		elsif ($p{country} ne $country) {
			&move_player($player, $country, $p{country});
			next;
		}

		my $name = $p{name};
		$name .= "[$p{shogo}]" if $p{shogo};

		my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..5];
		my $start_date = sprintf("%d/%d/%d %02d:%02d", $year+1900, $mon+1, $mday, $hour, $min);

#		$html .= $count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
		#my $rank_name = &get_rank_name($p{rank}, $p{name});
		$html .= qq|<tr>|;
		$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
		$html .= qq|<td>$sexes[$p{sex}]</td>|;
		#$html .= qq|<td>$rank_name</td>|;
		$html .= qq|<td>$ranks[$p{rank}]</td>|;
		$html .= qq|<td>$units[$p{unit}][1]</td>|;
		$html .= qq|<td>$jobs[$p{job}][1]</td>|;
		$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
		$html .= qq|<td>$weas[$p{wea}][1]</td>|;
		$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
		$html .= qq|<td>$pets[$p{pet}][1]</td>|;
		$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
		$html .= qq|<td>$p{ldate}</td>|;
		$html .= qq|<td>$p{mes}</td>|;
		$html .= qq|<td>$start_date</td>|;
		$html .= qq|</tr>\n|;

		# 統計
		++$ranks{$p{rank}};
		++$weas{$weas[$p{wea}][2]};
		++$jobs{$p{job}};
		++$_seeds{$p{seed}};
		++$sexes{$p{sex}};
		++$units{$p{unit}};
		++$count;
	}
	close $fh;
	$html .= qq|</tbody></table>|;

	# 所属人数補正
	$cs{member}[$country] = $count;

	if ($country eq '1') {
		$w{playing} = int($w{playing} * 0.9); # 拘束入らず落ちる人を考慮して少し減らす
	}

	&write_cs if $country > 0;

	# 統計HTML
	my $html_chart  = $w{world} eq $#world_states && $country eq $w{country} ? qq|<hr size="1"><h1>$cs{name}[$country] の悪魔達</h1>| : qq|<hr size="1"><h1>$cs{name}[$country] の勇士達</h1>|;
	   $html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>所属人数</th><td>$count人|;

	$html_chart .= qq|<br></td></tr><tr><th>性別</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}人/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>階級</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>部隊</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>武器属性</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>職業</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>種族</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}

	$html_chart .= qq|<br></td></tr></table><br>|;

	# HTMLﾌｧｲﾙ作成
	open my $out, "> ./html/$country.html";
	print $out &header_players_html($country);
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;

	# 携帯用に統計HTML出力
	open my $out2, "> ./html/${country}_chart.html";
	print $out2 &header_chart_html($country);
	print $out2 $html_chart;
	print $out2 &footer_players_html;
	close $out2;
}

sub write_all_players_html {
	my @rows = (qw/名前 性別 階級 部隊 職業 種族 武器 ﾀﾏｺﾞ ﾍﾟｯﾄ 世代 Lv HP MP AT DF MAT MDF AG LEA CHA お金 ｺｲﾝ 更新時間 ﾒｯｾｰｼﾞ 参入日時/);

	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;

	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	for my $country (0..$w{country}){
		open my $fh, "< $logdir/$country/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;

			# 同じ名前の人が複数いる場合
			next if ++$sames{$player} > 1;

			my $player_id = unpack 'H*', $player;


			my %p = &get_you_datas($player_id, 1);

			my $name = $p{name};
			$name .= "[$p{shogo}]" if $p{shogo};

			my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..5];
			my $start_date = sprintf("%d/%d/%d %02d:%02d", $year+1900, $mon+1, $mday, $hour, $min);

			my $rank_name = &get_rank_name($p{rank}, $p{name});
			$html .= qq|<tr>|;
			$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
			$html .= qq|<td>$sexes[$p{sex}]</td>|;
			$html .= qq|<td>$rank_name</td>|;
			$html .= qq|<td>$units[$p{unit}][1]</td>|;
			$html .= qq|<td>$jobs[$p{job}][1]</td>|;
			$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
			$html .= qq|<td>$weas[$p{wea}][1]</td>|;
			$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
			$html .= qq|<td>$pets[$p{pet}][1]</td>|;
			$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
			$html .= qq|<td>$p{ldate}</td>|;
			$html .= qq|<td>$p{mes}</td>|;
			$html .= qq|<td>$start_date</td>|;
			$html .= qq|</tr>\n|;

			# 統計
			++$ranks{$p{rank}};
			++$weas{$weas[$p{wea}][2]};
			++$jobs{$p{job}};
			++$_seeds{$p{seed}};
			++$sexes{$p{sex}};
			++$units{$p{unit}};
			++$count;
		}
		close $fh;
	}
	$html .= qq|</tbody></table>|;

	# 統計HTML
	my $html_chart  = qq|<hr size="1"><h1>全国の勇士達</h1>|;
	$html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>所属人数</th><td>$count人|;

	$html_chart .= qq|<br></td></tr><tr><th>性別</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}人/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>階級</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>部隊</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>武器属性</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>職業</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>種族</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}

	$html_chart .= qq|<br></td></tr></table><br>|;

	# HTMLﾌｧｲﾙ作成
	open my $out, "> ./html/all.html";
	print $out &header_all_players_html;
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;

}

# ------------------
sub header_players_html {
	my $country = shift;

my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / $cs{name}[$country]</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>
<p>更新日時 $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= $i eq $country
			? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / |
			: qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |
			;
	}

	$html .= qq|<a href="all.html"><font color="#ffffff">全プレイヤー</font></a> / |;

	if ($is_backup_countries) {
		$html .= $country eq 'chart' ? qq|国力ﾁｬｰﾄ / | : qq|<a href="chart_img.html">国力ﾁｬｰﾄ</a> / |;
	}

	return $html;
}

sub header_all_players_html {
my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / 全プレイヤー</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>
<p>更新日時 $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |;
	}

	$html .= qq|<font color="#ffffff">全プレイヤー</font> / |;

	if ($is_backup_countries) {
		$html .= qq|<a href="chart_img.html">国力ﾁｬｰﾄ</a> / |;
	}

	return $html;
}
# ------------------
sub chart_backup {
	# ﾊﾞｯｸｱｯﾌﾟ処理
	if ($is_backup_countries && -d "./backup" && -s "$logdir/countries.cgi" > 300) {
		my @lines = ();
		open my $fh_b, "< $logdir/countries.cgi";
		while (my $line = <$fh_b>) {
			push @lines, $line;
		}
		close $fh_b;

		my($mhour,$wday) = (localtime($time))[2,6];
		my $hour_file = "./backup/" . $wday . "_" . $mhour . ".cgi";
		open my $fh_b2, "> $hour_file";
		print $fh_b2 @lines;
		close $fh_b2;

		my $del_start = $wday + 1;
		my $del_end = $wday + 6;

		for my $d ($del_start..$del_end){
			my $del_d = $d > 6 ? $d - 7 : $d;
			for my $h (0..23){
				my $hour_file = "./backup/" . $del_d . "_" . $h . ".cgi";
				if(-f "$hour_file"){
					unlink $hour_file;
				}
			}
		}

		&create_world_chart;
	}
}

sub header_chart_html {
	my $country = shift;

	my $html = '';
	$html .= qq|<html><head>|;
	$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	$html .= qq|<title>$title / $cs{name}[$country]</title>|;
	$html .= qq|</head><body $body>|;
	$html .= qq|<form method="$method" action="../$script_index"><input type="submit" value="ＴＯＰ"></form>|;
	$html .= qq|<form method="$method" action="../players.cgi"><input type="submit" value="戻る"></form>|;
	$html .= qq|<p>更新日時 $date</p>|;
	$html .= qq|<hr size="1"><h1>$cs{name}[$country]</h1>|;

	return $html;
}
# ------------------
sub footer_players_html {
	my $html = '';
	$html .= qq|<br><div align="right" style="font-size:11px">|;
	$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama楽.net</a><br>|;  # 著作表示:削除・非表示 禁止!!
	$html .= qq|$copyright|;
	$html .= qq|</div></body></html>|;

	return $html;
}

# ﾊﾞｯｸｱｯﾌﾟよりﾃﾞｰﾀを取得
sub create_world_chart {
	$touitu_strong = 0 if ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10')); # 世界情勢[深淵]

	# ﾊﾞｯｸｱｯﾌﾟﾌｧｲﾙを古いもの順にｿｰﾄ
	my @lines = ();
	opendir my $dh, "backup";
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;

		my $file_time = (stat "./backup/$file_name")[9];
		push @lines, "$file_name<>$file_time<>\n";
	}
	closedir $dh;

	@lines = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ]} @lines;

	# 国力を取得
	my $chxl_x = '';
	my @chds = ();
	my $count_day = 0;
	for my $line (@lines) {
		my($file_name, $file_time) = split /<>/, $line;

		my $i = 1;
		open my $fh, "< ./backup/$file_name";
		my $head_line = <$fh>;
		while (my $data_line = <$fh>) {
			if ($data_line =~ /<>is_die;1<>/) {
				$chds[$i] .= "0,";
			}
			else {
				my($strong)    = ($data_line =~ /<>strong;(\d+?)<>/);
				my $strong_par = $strong <= 0 || $touitu_strong <= 0 ? 0 : int($strong / $touitu_strong * 100);
				$strong_par = 100 if $strong_par > 100;
				$chds[$i] .= "$strong_par,";
			}
			++$i;
		}
		close $fh;

		my($mhour,$mday,$month) = (localtime($file_time))[2,3,4];
		++$month;
		$chxl_x .= "|$month/$mday $mhour:00";

		++$count_day;
	}
	my $chg_x = $count_day <= 2 ? 25 : int(50 / ($count_day-1) * 100) * 0.01;

	my $name = '';
	my $chco = '';
	my $chd = '';
	for my $i (1 .. $w{country}) {
		$chco .= "$cs{color}[$i],";
		chop $chds[$i]; # 後尾の,をとる
		$chd  .= "$chds[$i]|";

		$name .= qq|<font color="$cs{color}[$i]">■【 統一 <b>$cs{win_c}[$i]</b> 】$cs{name}[$i]</font><br>|;
	}
	$chco =~ tr/#//d; # #を除く
	chop $chco; # 後尾の,をとる
	chop $chd;  # 後尾の|をとる

	my $one_tenth = int($touitu_strong * 0.1);
	my $count_scale = 0;
	my $scale = 0;
	my $chxl_y = '';
	for my $i (1 .. 15) {
		$chxl_y .= "|$scale";
		$scale += int($one_tenth * 0.01) * 100;
		++$count_scale;
		last if $scale >= $touitu_strong*0.95;
	}
	$chxl_y .= "|$touitu_strong";
	$chg_y = $count_scale <= 0 ? 25 : int(100 / $count_scale * 100) * 0.01;

	my $html = qq|<hr size="1"><h1>$world_name大陸国力ﾁｬｰﾄ</h1>|;
	$html .= qq{<img src="http://chart.apis.google.com/chart?cht=lc&chs=500x350&chco=$chco}
		  .  qq{&chd=t:$chd&chxt=x,y,r&chxl=0:$chxl_x|1:$chxl_y|2:|Die|Harf|Win}
		  .  qq{&chg=$chg_x,$chg_y&chtt=World+Force+Chart&chf=c,lg,110,003366,0.7,000000,0|bg,s,CCCCCC">};

	my $limit_day = int( ($w{limit_time} - $time) / (3600 * 24) );
	$html .= qq|<p>$name</p>|;
	$html .= qq|$world_name暦【 $w{year}年 】/ 世界情勢【 $world_states[$w{world}] 】/ 統一期限【 残り$limit_day日 】/<br>|;
	$html .= qq|難易度【 Lv.$w{game_lv} 】/ 統一$e2j{strong}【 $touitu_strong 】/ | unless ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10'));

	my($c1, $c2) = split /,/, $w{win_countries};
	$html .= $c2 ? qq|統一国【 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>同盟 】<br>|
		   : $c1 ? qq|統一国【 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font> 】<br>|
		   :       qq|<br>|
		   ;

	# HTMLﾌｧｲﾙ作成
	open my $out, "> ./html/chart_img.html";
	print $out &header_players_html('chart');
	print $out $html;
	print $out &footer_players_html;
	close $out;
}

sub backup_players {
	mkdir "./snap_shot/snap_shot_$time";
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my $user_from = "$userdir/$pid/user.cgi";
		my $user_to = "./snap_shot/snap_shot_$time/user_$pid.cgi";

		copy($user_from, $user_to);
	}
	closedir $dh;

	my $countries_from = "$logdir/countries.cgi";
	my $countries_to = "./snap_shot/snap_shot_$time/countries.cgi";
	copy($countries_from, $countries_to);

	opendir my $rdh, "./snap_shot" or &error("ﾊﾞｯｸｱｯﾌﾟﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $backup_name = readdir $rdh) {
		if ($backup_name =~ /snap_shot_(\d+)/) {
			if ($1 < $time - 3 * 24 * 60 * 60) {
				rmtree(["./snap_shot/$backup_name"]);
			}
		}
	}
	closedir $rdh;
}
