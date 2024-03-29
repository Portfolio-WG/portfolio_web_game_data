#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/move_player.cgi';
require "$datadir/skill.cgi";
use File::Copy::Recursive qw(rcopy);
use File::Path;
my $this_script = 'admin.cgi';
#=================================================
# プレイヤー管理 Created by Merino
#=================================================

# 並び順名
my %e2j_sorts = (
	country	=> '国順',
	name	=> '名前順',
	ldate	=> '更新日時順',
	addr	=> 'ﾎｽﾄ名/IP順',
	agent	=> 'UA(ﾌﾞﾗｳｻﾞ)',
	check	=> '多重ﾁｪｯｸ',
	player	=> 'プレイヤーﾁｪｯｸ',
);

# ﾃﾞﾌｫﾙﾄの並び順
$in{sort} ||= 'addr';


#=================================================
# メイン処理
#=================================================
&header;
&decode;
&error('ﾊﾟｽﾜｰﾄﾞが違います') unless $in{pass} eq $admin_pass;
&read_cs;

if    ($in{mode} eq 'admin_delete_user') { &admin_delete_user; }
elsif ($in{mode} eq 'admin_get_depot_data')   { &admin_get_depot_data; }
elsif ($in{mode} eq 'admin_get_akindo_data')   { &admin_get_akindo_data; }
elsif ($in{mode} eq 'admin_get_bank_log')     { &admin_get_bank_log; }
elsif ($in{mode} eq 'admin_wt0')     { &admin_wt0; }
elsif ($in{mode} eq 'admin_refresh')     { &admin_refresh; }
elsif ($in{mode} eq 'admin_go_neverland')     { &admin_go_neverland; }
elsif ($in{mode} eq 'admin_violate')   { &admin_violate; }
elsif ($in{mode} eq 'admin_repaire')     { &admin_repaire; }
elsif ($in{mode} eq 'junk_sub')          { &junk_sub($in{j_del}); }
elsif ($in{mode} eq 'junk_show')          { &junk_show; }
elsif ($in{mode} eq 'country_reset')     { &country_reset; }
elsif ($in{mode} eq 'kinotake_god')      { &kinotake_god; }
elsif ($in{mode} eq 'bug_prize')      { &bug_prize; }
elsif ($in{mode} eq 'boss_make')         { &boss_make; }
elsif ($in{mode} eq 'all_reset_point')   { &all_reset_point; }
elsif ($in{mode} eq 'all_set_default')   { &all_set_default; }
elsif ($in{mode} eq 'reset_monster')   { &reset_monster; }
elsif ($in{mode} eq 'modify_cha')   { &modify_cha; }
elsif ($in{mode} eq 'admin_losstime')   { &admin_losstime; }
elsif ($in{mode} eq 'admin_summer_lot_list_up')   { &admin_summer_lot_list_up; }
elsif ($in{mode} eq 'admin_summer_end')   { &admin_summer_end; }
elsif ($in{mode} eq 'admin_summer_radio_end')   { &admin_summer_radio_end; }
elsif ($in{mode} eq 'admin_summer_reset')   { &admin_summer_reset; }
elsif ($in{mode} eq 'admin_expendable')   { &admin_expendable; }
elsif ($in{mode} eq 'admin_parupunte')   { &admin_parupunte; }
elsif ($in{mode} eq 'admin_compare')   { &admin_compare; }
elsif ($in{mode} eq 'migrate_reset')   { &migrate_reset; }
elsif ($in{mode} eq 'admin_all_pet_check')   { &admin_all_pet_check; }
elsif ($in{mode} eq 'admin_letter_log_check')   { &admin_letter_log_check; }
elsif ($in{mode} eq 'admin_incubation_log_check')   { &admin_incubation_log_check; }
elsif ($in{mode} eq 'admin_shopping_log_check')   { &admin_shopping_log_check; }
elsif ($in{mode} eq 'admin_hunt_log_check')   { &admin_hunt_log_check; }

&top;
&footer;
exit;

#=================================================
# top
#=================================================
sub top {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;

	print qq|<form method="$method" action="admin_country.cgi">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="国管理" class="button1">|;
	print qq|</form>|;

	print qq|<form method="$method" action="admin_log.cgi">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="解析" class="button1">|;
	print qq|</form>|;

	print qq|<table border="0"><tr>|;
	print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value=""><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="全ﾕｰｻﾞｰ" class="button_s"></form></td>|;
	for my $i (0 .. $w{country}) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$i"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="$cs{name}[$i]" class="button_s"></form></td>|;
	}
	print qq|</tr></table>|;

	print qq|<table border="0"><tr>|;
	while (my($k,$v) = each %e2j_sorts) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$in{country}"><input type="hidden" name="pass" value="$in{pass}">\n|;
		print qq|<input type="hidden" name="sort" value="$k"><input type="submit" value="$v" class="button_s"></form></td>\n|;
	}
	print qq|</tr></table>|;

	print qq|<a href="#util">機能\へ</a>|;

	print qq|<div class="mes">$mes</div><br>| if $mes;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="mode" value="admin_delete_user"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="country" value="$in{country}"><input type="hidden" name="sort" value="$in{sort}">|;
	print qq|ﾘｾｯﾄは、画面に何も表\示されなくなったり、Nextループにはまった状態を修正します。<br>|;
	print qq|<table class="table1"><tr>|;

	for my $k (qw/削除 ﾛｸﾞｲﾝ 倉庫 商人の店 銀行ﾛｸﾞ 名前 ﾌｫﾙﾀﾞ ﾘｾｯﾄ 無所属へ 国 IPｱﾄﾞﾚｽ ﾎｽﾄ名 UserAgent(ﾌﾞﾗｳｻﾞ) 更新時間 ｱｸｾｽﾁｪｯｸ/) {
		print qq|<th>$k</th>|;
	}
	print qq|</tr>|;

	# プレイヤー情報を取得
	my @lines = $in{country} eq '' ? &get_all_users : &get_country_users($in{country});

	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $count = 0;
	my $pre_line = '';
	my $is_duplicated = 0;
	for my $line (@lines) {
		my($id, $name, $pass, $country, $addr, $host, $agent, $ldate) = split /<>/, $line;

		# もしホスト名が同じなら赤表示
		if ( ($host !~ /admin_login/ && $addr eq $b_addr && $host eq $b_host && $agent eq $b_agent)
			|| ($agent eq $b_agent && ($agent =~ /DoCoMo/ || $agent =~ /KDDI|UP\.Browser/ || $agent =~ /J-PHONE|Vodafone|SoftBank/)) ) {
				unless ($is_duplicated) {
					my($pid, $pname, $ppass, $pcountry, $paddr, $phost, $pagent, $pldate) = split /<>/, $pre_line;
					print qq|<tr class="stripe2">|;
					print qq|<td><input type="checkbox" name="delete" value="$pid"></td>|;
					print qq|<td><input type="button" class="button_s" value="ﾛｸﾞｲﾝ" onClick="location.href='$script?id=$pid&pass=$ppass';"></td>|;
					print qq|<td><input type="button" class="button_s" value="倉庫" onClick="location.href='?mode=admin_get_depot_data&pass=$in{pass}&id=$pid&name=$pname';"></td>|;
					print qq|<td>|;
					if (-f "$userdir/$pid/shop_sale_detail.cgi") {
						print qq|<input type="button" class="button_s" value="商人の店" onClick="location.href='?mode=admin_get_akindo_data&pass=$in{pass}&id=$pid&name=$pname';">|;
					}
					print qq|</td>|;
					print qq|<td>|;
					if (-f "$userdir/$pid/shop_bank_log.cgi") {
						print qq|<input type="button" class="button_s" value="銀行ﾛｸﾞ" onClick="location.href='?mode=admin_get_bank_log&pass=$in{pass}&id=$pid&name=$pname';">|;
					}
					print qq|</td>|;
					print qq|<td>$pname</td>|;
					print qq|<td>$pid</td>|;
					print qq|<td><input type="button" class="button_s" value="拘束0" onClick="location.href='?mode=admin_wt0&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td><input type="button" class="button_s" value="ﾘｾｯﾄ" onClick="location.href='?mode=admin_refresh&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td><input type="button" class="button_s" value="無所属へ" onClick="location.href='?mode=admin_go_neverland&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td>$cs{name}[$pcountry]</td>|;
					print qq|<td>$paddr</td>|;
					print qq|<td>$phost</td>|;
					print qq|<td>$pagent</td>|;
					print qq|<td>$pldate</td>|;
					print qq|<td><input type="button" class="button_s" value="ｱｸｾｽﾁｪｯｸ" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td></tr>|;
				}
				print qq|<tr class="stripe2">|;
				$is_duplicated = 1;
		}
		else{
			$is_duplicated = 0;
			if ($in{sort} ne 'check') {
				print ++$count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
			}
		}
		$b_addr  = $addr;
		$b_host  = $host;
		$b_agent = $agent;

		if ($in{sort} ne 'check' || $is_duplicated) {
			print qq|<td><input type="checkbox" name="delete" value="$id"></td>|;
			print qq|<td><input type="button" class="button_s" value="ﾛｸﾞｲﾝ" onClick="location.href='$script?id=$id&pass=$pass';"></td>|;
			print qq|<td><input type="button" class="button_s" value="倉庫" onClick="location.href='?mode=admin_get_depot_data&pass=$in{pass}&id=$id&name=$name';"></td>|;
			print qq|<td>|;
			if (-f "$userdir/$id/shop_sale_detail.cgi") {
				print qq|<input type="button" class="button_s" value="商人の店" onClick="location.href='?mode=admin_get_akindo_data&pass=$in{pass}&id=$id&name=$name';">|;
			}
			print qq|</td>|;
			print qq|<td>|;
			if (-f "$userdir/$id/shop_bank_log.cgi") {
				print qq|<input type="button" class="button_s" value="銀行ﾛｸﾞ" onClick="location.href='?mode=admin_get_bank_log&pass=$in{pass}&id=$id&name=$pname';">|;
			}
			print qq|</td>|;
			print qq|<td>$name</td>|;
			print qq|<td>$id</td>|;
			print qq|<td><input type="button" class="button_s" value="拘束0" onClick="location.href='?mode=admin_wt0&pass=$in{pass}&id=$id&country=$pcountry&sort=$in{sort}';"></td>|;
			print qq|<td><input type="button" class="button_s" value="ﾘｾｯﾄ" onClick="location.href='?mode=admin_refresh&pass=$in{pass}&id=$id&country=$in{country}&sort=$in{sort}';"></td>|;
			print qq|<td><input type="button" class="button_s" value="無所属へ" onClick="location.href='?mode=admin_go_neverland&pass=$in{pass}&id=$id&country=$in{country}&sort=$in{sort}';"></td>|;
			print qq|<td>$cs{name}[$country]</td>|;
			print qq|<td>$addr</td>|;
			print qq|<td>$host</td>|;
			print qq|<td>$agent</td>|;
			print qq|<td>$ldate</td>|;
			print qq|<td><input type="button" class="button_s" value="ｱｸｾｽﾁｪｯｸ" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td></tr>|;
		}

		$pre_line = $line;
	}
	print qq|</table><br>|;
	print qq|<input type="radio" name="is_delete" value="delete">削除|;
	print qq| <input type="checkbox" name="is_add_deny" value="1">登録禁止IP/UAに追加<br>|;
	print qq|<input type="radio" name="is_delete" value="exile" checked="checked">国外追放(3日拘束)|;
	print qq|<p style="color: #F00">プレイヤーを削除/追放する<br><input type="submit" value="処理" class="button_s"></p></form>|;

	print qq|<a name="util"></a>|;
	print qq|<br><br><br>|;
	print qq|<div class="mes">データ補正：以下の状態になった時に使用<ul>|;
	print qq|<li>実際の登録人数が違う|;
	print qq|<li>国メンバーに違う国の人が入ってる|;
	print qq|<li>国メンバーに同じ名前の人がいる|;
	print qq|<li>国メンバーにプレイヤー一覧には存在しない人がいる|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_repaire">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="データ補正" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">バグ報酬<ul>|;
	print qq|<form method="$method" action="$this_script"><p>送信先：<input type="text" name="send_name" class="text_box1"></p><input type="hidden" name="mode" value="bug_prize">|;
	my @prizes = (
		['孵化夢',	'2_3_999_0'],
		['孵化？',	'2_2_999_0'],
		['豆',	'3_62_0_0'],
		['ｶﾞﾌﾞ',	'3_21_0_0'],
		['ﾀｸﾐ',		'3_183_0_0'],
		['ﾌｧﾝﾄﾑ',		'3_9_15_0'],
		['ｺﾞｰｽﾄ',		'3_8_0_0'],
	);
	print qq|<select name="prize" class="menu1">|;
	for my $pz (@prizes) {
		print qq|<option value="$pz->[1]">$pz->[0]</option>|;
	}
	print qq|</select>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="バグ報酬" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">密輸監視：以下の状態になった時に使用<ul>|;
	print qq|<li>複垢密輸疑惑のあるプレイヤーがいる場合にジャンクショップのログを参照します|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="junk_sub">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="密輸監視" class="button_s"></p>|;
	print qq|<input type="radio" name="j_del" value="0">閲覧|;
	print qq|<input type="radio" name="j_del" value="1" checked>ログ削除</form>|;
	print qq|<li>ジャンクショップの中身を確認します|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="junk_show">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="閲覧" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">垢比較：二つの垢のログイン状況を比較する<ul>|;
	print qq|<li>複垢疑惑のあるプレイヤーがいる場合比較します|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_compare">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="複垢比較" class="button_s"></p>|;
	print qq|<input type="text" name="comp1" value="">|;
	print qq|<input type="text" name="comp2" value=""></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">ﾈﾊﾞｰﾗﾝﾄﾞ送り：以下の状態になった時に使用<ul>|;
	print qq|<li>混乱の誤作動でﾈﾊﾞｰﾗﾝﾄﾞ送りされなかった時（個人設定にかかわらず全員ﾈﾊﾞｰﾗﾝﾄﾞ送りにします）|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="country_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="ﾈﾊﾞﾗﾝ送り" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">改造ﾊﾟﾙﾌﾟﾝﾃ：強制的に情勢変更<ul>|;
	print qq|<li>祭り情勢のままだった場合などに使用する|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_parupunte">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="ﾌﾟﾝﾃ" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">不倶戴天緊急2<ul>|;
	print qq|<li>（仮）|;
	print qq|<form method="$method" action="$this_script"><p>送信先：<input type="text" name="send_name" class="text_box1"></p><input type="hidden" name="mode" value="kinotake_god">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="不倶戴天緊急2" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">ボス<ul>|;
	print qq|<li>現在のボス<br>|;
	open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
	my $line = <$bfh>;
	my ($bname, $bcountry, $bmax_hp, $bmax_mp, $bat, $bdf, $bmat, $bmdf, $bag, $bcha, $bwea, $bskills, $bmes_win, $bmes_lose, $bicon, $bwea_name) = split /<>/, $line;
	print qq|$bname HP:$bmax_hp MP:$bmax_mp<br>|;
	print qq|攻撃:$bat 魔攻:$bmat<br>|;
	print qq|防御:$bdf 魔防:$bmdf<br>|;
	print qq|素早:$bag 魅力:$bcha<br>|;
	print qq|武器:$weas[$bwea][1]<br>|;
	print qq|技:|;
	my @bskill = split /,/, $bskills;
	for(@bskill){
		print qq|$skills[$_][1],|;
	}
	print qq|<br>|;
	print qq|<form method="$method" action="$this_script"><p>新ボス作成</p><input type="hidden" name="mode" value="boss_make">|;
	print qq|<p>ボス名<input type="text" name="boss_name" class="text_box1"></p>|;
	print qq|<p>HP<input type="text" name="boss_hp" class="text_box1">MP<input type="text" name="boss_mp" class="text_box1"></p>|;
	print qq|<p>攻撃<input type="text" name="boss_at" class="text_box1">魔攻<input type="text" name="boss_mat" class="text_box1"></p>|;
	print qq|<p>防御<input type="text" name="boss_df" class="text_box1">魔防<input type="text" name="boss_mdf" class="text_box1"></p>|;
	print qq|<p>素早<input type="text" name="boss_ag" class="text_box1">魅力<input type="text" name="boss_cha" class="text_box1"></p>|;
	print qq|<p>武器<select name="boss_wea" class="menu1">|;
	for(0..$#weas){
		print qq|<option value="$_">$weas[$_][1]</option>|;
	}
	print qq|<p>武器名<input type="text" name="boss_weaname" class="text_box1"></p>|;
	print qq|</select></p>|;
	for my $i (1..5){
		print qq|<p>技$i<select name="boss_skill$i" class="menu1">|;
		for(0..$#skills){
			print qq|<option value="$_">$skills[$_][1]</option>|;
		}
		print qq|</select></p>|;
	}
	print qq|<p>撃破メッセージ<input type="text" name="boss_winmes" class="textarea1"></p>|;
	print qq|<p>敗北メッセージ<input type="text" name="boss_losemes" class="textarea1"></p>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="新ボス作成" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">リセット<ul>|;
	print qq|<li>（仮）|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="all_reset_point">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="リセット" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">初期値セット<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="all_set_default">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="初期値セット" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">モンスターリセット<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="reset_monster">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="リセットセット" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">魅力修正<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="modify_cha">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="魅力修正" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">延長<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_losstime">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="延長" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">サマージャンボリストアップ<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_lot_list_up">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="リスト化" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">夏イベ終了処理<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_end">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="終了" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">夏イベラジオ体操処理(終了処理よりも先に実行すること)<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_radio_end">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="終了" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">夏イベ初期化処理<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="終了" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">適当士官フラグリセット処理<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="migrate_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="リセット" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">臨時処理（連打しないこと、また処理終了後コメントアウトのこと）<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_expendable">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="text" name="to_name">|;
	print qq|<p><input type="submit" value="臨時処理" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">ﾍﾟｯﾄ流通状況調査<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_all_pet_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="調査" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">手紙送信履歴<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_letter_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="チェック" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">孵化履歴<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_incubation_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="チェック" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">購入履歴<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_shopping_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="チェック" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">討伐卵入手履歴<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_hunt_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="チェック" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	my @files = glob "$logdir/monster/*.cgi";
	for my $p_name (@files){
		if ($p_name =~ /boss/ || $p_name =~ /beginner/) {
			next;
		}
		print qq|<div class="mes">$p_name<br>|;
		print qq|<table><tr><th>名前</th><th>技</th><th>危険度</th></tr>|;
		open my $fh, "<$p_name" or &error("$p_nameﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			my @datas = split /<>/, $line;
			my $i = 0;
			my %y = ();
			for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
				$y{$k} = $datas[$i];
				++$i;
			}
			my $skill_st = 0;
			my $si = 0;
			my $skill_str = '';
			for my $skill (split /,/, $y{skills}) {
				$si++;
				if ($skills[$skill][2] eq $weas[$y{wea}][2]) {
					$skill_st += $skills[$skill][7];
					$skill_str .= $skills[$skill][1];
				} else {
					$skill_st += $skills[0][7];
					$skill_str .= $skills[0][1];
				}
			}
			for (my $j = $si; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			print qq|<tr><td>$y{name}</td><td>$skill_str</td><td>$skill_st</td></tr>|;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		print qq|</table></div>|;
	}
}

#=================================================
# 削除・追放処理
#=================================================
sub admin_delete_user {
	return unless @delfiles;

	require './lib/move_player.cgi';
	for my $delfile (@delfiles) {
		my %datas = &get_you_datas($delfile, 1);

		if ($in{is_delete} eq 'exile') { # 追放
			my $id = unpack 'H*', $datas{name};
			return unless -f "$userdir/$id/user.cgi";

			&move_player($datas{name}, $datas{country}, 0);
			$mes .= "$datas{name}を追放しました<br>";

			my @data = (
				['wt', 3 * 24 * 3600],
				['country', 0],
				['lib', ''],
				['tp', 0],
				['vote', ''],
			);
			&regist_you_array($datas{name}, @data);
		}
		elsif ($in{is_delete} eq 'delete') {
			&move_player($datas{name}, $datas{country}, 'del');
			$mes .= "$datas{name}を削除しました<br>";

			# 違反者リストに追加
			if ($in{is_add_deny}) {
				open my $fh, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgiﾌｧｲﾙが開けません");
				print $fh $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
					|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
				if(-f "$userdir/$id/access_log.cgi"){
					open my $fh2, "< $userdir/$id/access_log.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
					while (my $line_info_add = <$fh2>){
						($d{addr}, $d{host}, $d{agent}) = split /<>/, $line_info_add;
						print $fh ($d{agent} =~ /DoCoMo/ ||
							$d{agent} =~ /KDDI|UP\.Browser/ ||
							$d{agent} =~ /J-PHONE|Vodafone|SoftBank/) ? "$d{agent}\n" : "$d{addr}\n";
					}
				}
				close $fh;
			}
		}
	}
}

#=================================================
# ﾘｾｯﾄ処理：画面真っ黒　ハマった場合に使用(何かしらの異常ｴﾗｰ)
#=================================================
sub admin_wt0 {
	$mes .= "$in{id}の拘束時間をﾘｾｯﾄしました<br>";
	return unless $in{id};

	my $name = pack 'H*', $in{id};
	&regist_you_data($name, "wt", 0);

	$mes .= "$nameの拘束時間をﾘｾｯﾄしました<br>";
}

#=================================================
# ﾘｾｯﾄ処理：画面真っ黒　ハマった場合に使用(何かしらの異常ｴﾗｰ)
#=================================================
sub admin_refresh {
	return unless $in{id};

	local %m = &get_you_datas($in{id}, 1);
	$m{lib} = '';
	$m{wt} = $m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
	$id = $in{id};
	&write_user;

	$mes .= "$m{name}のlib,tpなどの値をﾘｾｯﾄしました<br>";
}

#=================================================
# 無所属処理：強制的に無所属にする
#=================================================
sub admin_go_neverland {
	return unless $in{id};

	require './lib/move_player.cgi';
	local %m = &get_you_datas($in{id}, 1);
	$m{lib} = '';
	$m{wt} = $m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
	$id = $in{id};
	&move_player($m{name}, $m{country}, 0);
	$m{country} = 0;
	&send_item($m{name}, 3, 134, 0, 0, 1);

	&regist_you_data($m{name}, "random_migrate", 0);

	&write_user;

	$mes .= "$m{name}の所属国をﾘｾｯﾄしました<br>";
}


#=================================================
# 国ごとのユーザーデータを取得
#=================================================
sub get_country_users {
	my $country = shift;
	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが読み込めません");
	while (my $name = <$fh>) {
		$name =~ tr/\x0D\x0A//d;

		my $id = unpack 'H*', $name;
		open my $fh2, "< $userdir/$id/user.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
		my $line_data = <$fh2>;
		my $line_info = <$fh2>;
		close $fh2;

		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}
		($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name pass country addr host agent ldate/) {
			$line .= "$m{$k}<>";
		}
		push @lines, "$line\n";
	}
	close $fh;

	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $a->[8] cmp $b->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }

	return @lines;
}


#=================================================
# 全ユーザーのデータを取得
#=================================================
sub get_all_users {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		next if ($in{sort} eq 'player' && $in{checkid} && $in{checkid} ne $id);

		open my $fh, "< $userdir/$id/user.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;

		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}

		if(-f "$userdir/$id/access_log.cgi" && ($in{sort} eq 'check' || ($in{sort} eq 'player' && $in{checkid}))){
			open my $fh2, "< $userdir/$id/access_log.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
			while (my $line_info_add = <$fh2>){
				($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info_add;
				my $line = "$id<>";
				for my $k (qw/name pass country addr host agent ldate/) {
					$line .= "$m{$k}<>";
				}
				unless($m{host} =~ /\.trendmicro\.com$|\.sjdc$|\.iad1$/){
					push @lines, "$line\n";
				}
			}
		}else{
			($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;
			my $line = "$id<>";
			for my $k (qw/name pass country addr host agent ldate/) {
				$line .= "$m{$k}<>";
			}
			push @lines, "$line\n";
		}
	}
	closedir $dh;

	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $b->[8] cmp $a->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'check')   { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'player')  { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] ||$a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }

	return @lines;
}


#=================================================
# データ補正：人数や国のﾒﾝﾊﾞｰなどがおかしいのを一旦白紙にしてから書き直す
#=================================================
sub admin_repaire {
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		push @{ $members{$m{country}} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;
	}

	&write_cs;
	$mes .= "<hr>人数や国のﾒﾝﾊﾞｰﾌｧｲﾙを修正しました<br>";
}


#=================================================
# 密輸監視
#=================================================
sub junk_sub {
	my $del = shift;
	open my $fh3, "+< $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgiﾌｧｲﾙが開けません");
	my @lines = <$fh3>;
	my @sell = ();
	my @buy = ();
	$mes .= qq|<table><tr>|;
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @lines;
	$mes .= qq|<td>アイテムソ\ート<table class="table1"><tr><th>アイテム</th><th>名前</th><th>売り/買い</th><th>時間</th></tr>|;
	for my $line (@lines){
		my($kind, $item_no, $item_c, $name, $jtime, $type) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($jtime);
		$year += 1900;
		$mon++;
		my $jtime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= "<td>";
		$mes .= &get_item_name($kind, $item_no);
		$mes .= "</td><td>$name</td>";
		$mes .= $type ? "<td>買い</td>" : "<td>売り</td>";
		$mes .= "<td>$jtime2<br></td></tr>";
	}
	$mes .= qq|</table></td>|;
	@lines = map { $_->[0] }
				sort { $a->[5] <=> $b->[5] }
					map { [$_, split /<>/ ] } @lines;
	$mes .= qq|<td>時間ソ\ート<table class="table1"><tr><th>アイテム</th><th>名前</th><th>売り/買い</th><th>時間</th></tr>|;
	for my $line (@lines){
		my($kind, $item_no, $item_c, $name, $jtime, $type) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($jtime);
		$year += 1900;
		$mon++;
		my $jtime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= "<td>";
		$mes .= &get_item_name($kind, $item_no);
		$mes .= "</td><td>$name</td>";
		$mes .= $type ? "<td>買い</td>" : "<td>売り</td>";
		$mes .= "<td>$jtime2<br></td></tr>";
	}
	$mes .= qq|</table></td>|;
	$mes .= qq|<tr></table>|;

	if($del){
		seek  $fh3, 0, 0;
		truncate $fh3, 0;
	}
	close $fh3;
}

#=================================================
# ｼﾞｬﾝｸｼｮｯﾌﾟの中身確認
#=================================================
sub junk_show {
	my $count = 0;
	my $mes_sub;
	open my $fh, "< $logdir/junk_shop.cgi" or &error("$logdir/junk_shop.cgiを開けませんでした");
	while (my $line = <$fh>) {
		$count++;
		my($kind, $item_no, $item_c) = split /<>/, $line;
		$mes_sub .= &get_item_name($kind, $item_no, $item_c)."<br>";
	}
	close $fh;
	$mes .= "$count個<br>".$mes_sub;
}

#=================================================
# ﾈﾊﾞｰﾗﾝﾄﾞ送り
#=================================================
sub country_reset {
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		&regist_you_data($m{name}, 'country', 0);
		for my $k (qw/war dom pro mil/) {
			&regist_you_data($name, $k."_c", $m{$k."_c_t"}+$m{$k."_c"});
		}
		&regist_you_data($m{name}, "random_migrate", 0);

		push @{ $members{0} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	for my $i (1..$w{country}) {
		for my $k (qw/ceo war dom pro mil/) {
			$cs{$k}[$i] = '';
			my $kc = $k . "_c";
			$cs{$kc}[$i] = 0;
		}
	}
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $country - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $country - 1 ? 0:$ave_c;
	}

	&write_cs;
	$mes .= "<hr>全員ﾈﾊﾞｰﾗﾝﾄﾞ送りにしました<br>";
}

#=================================================
# 不倶戴天緊急2
#=================================================
sub kinotake_god {
	my $pid = pack 'H*', $in{send_name};
	open my $fh, ">> $userdir/$pid/ex_c.cgi";
	print $fh "fes_c<>1<>\n";
	close $fh;

	&send_item($in{send_name}, 2, int(rand($#eggs)+1), 0, 0, 1);

#	require './lib/shopping_offertory_box.cgi';
#	&send_god_item(5, $in{send_name});
}

#=================================================
# 超ボス作成
#=================================================
sub boss_make {
	open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
	print $bfh "$in{boss_name}<>0<>$in{boss_hp}<>$in{boss_mp}<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$in{boss_wea}<>$in{boss_skill1},$in{boss_skill2},$in{boss_skill3},$in{boss_skill4},$in{boss_skill5}<>$in{boss_losemes}<>$in{boss_winmes}<>$default_icon<>$in{boss_weaname}<>\n";
	close $bfh;
}

#=================================================
# 全代表ポイントリセット
#=================================================
sub all_reset_point {
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		for my $k (qw/war dom pro mil/) {
			&regist_you_data($m{name}, $k."_c", 0);
		}
	}
	closedir $dh;
	$mes .= "<hr>全員の代表ポイントをリセットしました<br>";
}

#=================================================
# 初期値セット
#=================================================
sub all_set_default {
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		&regist_you_data($m{name}, "start_time", $time);
	}
	closedir $dh;
	$mes .= "<hr>全員の初期値をセットしました<br>";
}

#=================================================
# モンスター初期化
#=================================================
sub reset_monster {
	# 魔物から送られてくるﾀﾏｺﾞ
	my @egg_nos = (1..34,42..51);

	my @files = glob "$logdir/monster/*.cgi";
	for my $p_name (@files){
		if ($p_name =~ /boss/ || $p_name =~ /beginner/) {
			next;
		}
		$mes .= "$p_name<br>";
		my @lines = ();
		open my $fh, "+< $p_name" or &error("$p_nameﾌｧｲﾙが開けません");
		&dirflock($pname);
		while (my $line = <$fh>) {
			# 魔物画像を返す処理
			next unless $default_icon;
			my($ymname, $ymes_win, $yicon, $yname) = (split /<>/, $line)[0,-5,-3,-2];
			next if $yicon eq $default_icon;
			next unless -f "$icondir/$yicon"; # 画像がない
			my $y_id  = unpack 'H*', $yname;
			next unless -d "$userdir/$y_id/picture"; # ﾌﾟﾚｲﾔｰが存在しない

			# 魔物から主への手紙
			my $m_message = $m_messages[ int( rand(@m_messages) ) ];
			$in{comment}  = qq|$places[$place][2]に住む魔物$ymnameの最後を見届けた$m{name}からの手紙<br><br>|;
			$in{comment} .= qq|$ymnameの最後の言葉『$m_message$ymes_win』<br>|;
			$in{comment} .= qq|$ymnameの画像はﾏｲﾋﾟｸﾁｬに戻りました<br>|;
			$in{comment} .= qq|$ymnameからﾀﾏｺﾞが贈られたようだ<br>|;

			&send_letter($yname);
			rename "$icondir/$yicon", "$userdir/$y_id/picture/$yicon";

			my $egg_no = $egg_nos[int(rand(@egg_nos))];
			&send_item($yname, 2, $egg_no, 0, 0, 1);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		&release_dirflock($pname);
	}
	$mes .= "<hr>魔物をリセットしました<br>";
}
#=================================================
# 魅力修正
#=================================================
sub modify_cha {
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		unless ($m{cha}) {
			my $ave_status = int(($m{max_hp} + $m{max_mp} + $m{max_hp} + $m{lea} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag}) /  8);
			&regist_you_data($m{name}, "cha", $ave_status);
		}
	}
	closedir $dh;
	$mes .= "<hr>全員の魅力を修正しました<br>";
}
#=================================================
# 延長
#=================================================
sub admin_losstime {
	$w{limit_time} = $time + 24 * 3600;
	&write_cs;
	$mes .= "<hr>残り時間を1日にしました<br>";
}
#=================================================
# 夏イベント終了 虫・ラジオ・日記・武器
#=================================================
sub admin_summer_end {
	require './lib/shopping_offertory_box.cgi';

	my @morning_glory = ();

	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;

		my %m = &get_you_datas($id, 1);

		# 夏祭り用
		unless (-f "$userdir/$id/summer.cgi") {
			open my $fh, "> $userdir/$id/summer.cgi";
			close $fh;
		}
		open my $fh, "< $userdir/$id/summer.cgi" or &error("そのような名前のﾌﾟﾚｲﾔｰが存在しません");
		my $line = <$fh>;
		close $fh;

		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$m{$k} = $v;
		}
		$m{dummy} = 0;

		if ($m{summer_blog} > 30) {
			&regist_you_data($m{name}, "shogo", '★★ｴﾆｯｷﾏｽﾀｰ');
			&send_money($m{name}, '絵日記優秀賞', 2000000);
			&send_god_item(5, $m{name});
		} elsif($m{summer_blog} > 20) {
			&send_money($m{name}, '絵日記努力賞', 500000);
			&send_god_item(1, $m{name});
		} elsif($m{summer_blog} > 10) {
			&send_money($m{name}, '絵日記参加賞', 20000);
		}

		push @morning_glory, "$m{name}<>$m{morning_glory}<>\n";
	}
	closedir $dh;

	@morning_glory = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @morning_glory;
	my $rank = 1;
	for my $line (@morning_glory) {
		my ($name, $height) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|朝顔成長第1位に$nameさんが輝きました|);
			&regist_you_data($name, "shogo", '★★ｱｻｶﾞｵﾏｲｽﾀｰ');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? $rank - 7 : 1;
		&send_money($name, "朝顔成長第 $rank 位", 100000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my @pop = ();
	open my $fh, "< $logdir/pop_vote.cgi" or &error('人気投票ファイルが開けません');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		push @pop, "$name<>$vote<>\n";
	}
	close $fh;
	@pop = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @pop;
	$rank = 1;
	for my $line (@pop) {
		my ($name, $vote) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|人気投票(銀)第1位に $name さんが輝きました|);
			&regist_you_data($name, "shogo", '★ｾﾝﾀｰ');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? $rank - 7 : 1;
		&send_money($name, "人気投票(銀)第 $rank 位", 100000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my %pop2 = ();
	open my $fh, "< $logdir/pop_vote2.cgi" or &error('人気投票ファイルが開けません');
	while (my $line = <$fh>) {
		my($pop_name, $vote_name) = split /<>/, $line;
		$pop2{$pop_name}++;
	}
	close $fh;
	@pop = ();
	foreach my $name (keys(%pop2)) {
		push @pop, "$name<>$pop2{$name}<>\n";
	}
	@pop = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @pop;
	$rank = 1;
	for my $line (@pop) {
		my ($name, $vote) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|人気投票(金)第1位に$nameさんが輝きました|);
			&regist_you_data($name, "shogo", '★★ｾﾝﾀｰ');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? ($rank - 7) * 3 : 2;
		&send_money($name, "人気投票(銀)第 $rank 位", 300000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my @lot_num = ();
	my $max_lot = 0;
	open my $fhn, "< $logdir/event_lot_name.cgi" or &error('宝くじﾌｧｲﾙが読み込めません');
	while (my $line = <$fhn>) {
		my($name, $lot) = split /<>/, $line;
		push @lot_num, $name;
	}
	close $fhn;

	my $name = $lot_num[int(rand(@lot_num))];
	$mes .= "aaa" . $name;
	my $lot_id = unpack 'H*', $name;
	if (-f "$userdir/$lot_id/user.cgi") {
		&write_world_big_news(qq|サマージャンボの当選者は $name さんでした|);
		&regist_you_data($name, "shogo", '★ｻﾏｰｼﾞｬﾝﾎﾞ★');
		&regist_you_data($name, "money_overflow", 1);
		my %p = &get_you_datas($lot_id, 1);
		&regist_you_data($name, 'money_limit',$p{money} + 50000000);
		&send_money($name, 'ｻﾏｰｼﾞｬﾝﾎﾞ当選金', 50000000);
	}
	my $this_vote_file = "$logdir/pop_vote.cgi";
	my $this_file = "$logdir/pop_vote_result_middle.cgi";

	my %sames = ();
	my @p_ranks;

	my @lines = ();
	open my $fh, "< $this_vote_file" or &error('人気投票ファイルが開けません');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		my $p_id = unpack 'H*', $name;
		if (-f "$userdir/$p_id/user.cgi") {
			%p = &get_you_datas($p_id, 1);
			push @lines, "$name<>$vote<>$p{country}<>\n";
		}
	}
	# 票が多い順に並び替え
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	close $fh;

	open my $rfh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;

	my $this_vote_file = "$logdir/pop_vote2.cgi";
	my $this_file = "$logdir/pop_vote2_result.cgi";

	my %ranks = ();

	open my $fh, "< $this_vote_file" or &error('人気投票ファイルが開けません');
	while (my $line = <$fh>) {
		my($pname, $name) = split /<>/, $line;
		my $p_id = unpack 'H*', $pname;
		if (-f "$userdir/$p_id/user.cgi") {
			$ranks{$pname}++;
		}
	}

	my @lines = ();
	for my $name (keys(%ranks)) {
		my $p_id = unpack 'H*', $name;
		my %p = &get_you_datas($p_id, 1);
#		my $rank_name = &get_rank_name($p{rank}, $name);
#		push @lines, "$name<>$rank_name<>$p{country}<>\n";
		push @lines, "$name<>$ranks{$name}<>$p{country}<>\n";
	}
	# 票が多い順に並び替え
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	close $fh;

	open my $rfh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;

=pod
	require 'pop_ranking_gold.cgi';
	&update_pop2_ranking;
	require 'pop_ranking_middle.cgi';
	&update_pop_ranking;
=cut
	$mes .= "<hr>夏イベントの終了処理をしました<br>";
}
#=================================================
# 夏イベント ラジオ体操終了、報酬処理　
#=================================================
sub admin_summer_radio_end {
	#ラジオ体操の報酬処理　連想配列は慣れてなくてあまり使いたくない

	#出席回数カウント
	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "< $this_radio_dir/$d.cgi" or &error('ラジオ体操ファイルが開けません');
			while (my $line = <$fh>) {
				my($name, $rtime) = split /<>/, $line;
				if(!-f "$userdir/$id/temp_radio.cgi"){
					open my $fh2, "> $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgiが作成できません");
					close $fh2;
				}
				open my $fh2, "< $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgiが開けません");
				my $line = <$fh2>;
				my($radio_num) = split /<>/, $line;
				close $fh2;

				$radio_num++;

				open my $fh2, "> $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgiが作成できません");
				print $fh2 "$radio_num\n";
				close $fh2;

			}
			close $fh;
		}
	}

	#出席回数より報酬処理実行
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;

		my %m = &get_you_datas($id, 1);
		open my $fh3, "< $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgiが開けません");
		my $line = <$fh3>;
		my($radio_num) = split /<>/, $line;
		close $fh3;

		if ($radio_num > 30) {
			&regist_you_data($m{name}, "shogo", '★★ﾗｼﾞｵ少年');
			&send_money($m{name}, 'ラジオ体操優秀賞', 1000000);
			&send_god_item(5, $m{name});
		} elsif($radio_num > 20) {
			&send_money($m{name}, 'ラジオ体操努力賞', 250000);
			&send_god_item(1, $m{name});
		} elsif($radio_num > 10) {
			&send_money($m{name}, 'ラジオ体操参加賞', 10000);
		}

	}
	closedir $dh;

	#出席回数ファイル削除

}

#=================================================
# 夏イベントデータ初期化　
#=================================================
sub admin_summer_reset {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
		my $summer_file = "$userdir/$pid/summer.cgi";
		my $summer_file_trash_dir = "$userdir/$pid/summer_trash";
		if (-f "$summer_file") {
			#summer_trashディレクトリが無い場合は作成
			mkdir "$summer_file_trash_dir" or &error("$summer_file_trash_dir ﾌｫﾙﾀﾞが作れませんでした") unless -d "$summer_file_trash_dir";
			#過去のsummer.cgiがtrashにあった場合
			if(-f "$summer_file_trash_dir/summer.cgi") {
				unlink "$summer_file_trash_dir/summer.cgi" or &error("$summer_file_trash_dir/summer.cgiﾌｧｲﾙを削除することができません");
			}
			#renameしてtrashに保存
			rename "$summer_file", "$summer_file_trash_dir/summer.cgi";
			#データ初期化
			open my $fh, "> $summer_file" or &error("$summer_file が読み込めません");
			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
			close $fh;
		}
	}
	closedir $dh;

	#過去のデータを保存
	my $summer_log_trash_dir = "$logdir/summer_trash";
	mkdir "$summer_log_trash_dir" or &error("$summer_log_trash_dir ﾌｫﾙﾀﾞが作れませんでした") unless -d "$summer_log_trash_dir";

	my $this_vote_file = "$logdir/pop_vote.cgi";
	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	my $this_lot_file = "$logdir/event_lot.cgi";
	my $this_lot2_file = "$logdir/event_lot_name.cgi";
	my $this_blog_vote_file = "$logdir/blog_vote.cgi";

	#過去のデータがあった場合
	if(-f "$summer_log_trash_dir/pop_vote.cgi") {
		unlink "$summer_log_trash_dir/pop_vote.cgi" or &error("$summer_log_trash_dir/pop_vote.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$summer_log_trash_dir/pop_vote2.cgi") {
		unlink "$summer_log_trash_dir/pop_vote2.cgi" or &error("$summer_log_trash_dir/pop_vote2.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$summer_log_trash_dir/event_lot.cgi") {
		unlink "$summer_log_trash_dir/event_lot.cgi" or &error("$summer_log_trash_dir/event_lot.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$summer_log_trash_dir/event_lot_name.cgi") {
		unlink "$summer_log_trash_dir/event_lot_name.cgi" or &error("$summer_log_trash_dir/event_lot_name.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$summer_log_trash_dir/blog_vote.cgi") {
		unlink "$summer_log_trash_dir/blog_vote.cgi" or &error("$summer_log_trash_dir/blog_vote.cgiﾌｧｲﾙを削除することができません");
	}
	#データ移動
	rename "$this_vote_file", "$summer_log_trash_dir/pop_vote.cgi";
	rename "$this_vote2_file", "$summer_log_trash_dir/pop_vote2.cgi";
	rename "$this_lot_file", "$summer_log_trash_dir/event_lot.cgi";
	rename "$this_lot2_file", "$summer_log_trash_dir/event_lot_name.cgi";
	rename "$this_blog_vote_file", "$summer_log_trash_dir/blog_vote.cgi";

	#新規作成
	open my $fh, "> $this_vote_file" or &error("$this_vote_file が読み込めません");
	close $fh;

	open my $fh2, "> $this_vote2_file" or &error("$this_vote2_file が読み込めません");
	close $fh2;

	open my $fh3, "> $this_lot_file" or &error("$this_vote2_file が読み込めません");
	close $fh3;

	open my $fh4, "> $this_lot2_file" or &error("$this_vote2_file が読み込めません");
	close $fh4;

#勿体無いので去年のも残す
#	my $this_horror_story_file = "$logdir/horror_story.cgi";
#	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file が読み込めません");
#	close $fh;
	open my $fh5, "> $this_blog_vote_file" or &error("$this_blog_vote_file が読み込めません");
	close $fh5;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('ラジオ体操ファイルが開けません');
			close $fh;
		}
	}
}
#=================================================
# サマージャンボリスト化
#=================================================
sub admin_summer_lot_list_up {
	my @list = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;

		my %m = &get_you_datas($pid, 1);
		# 関数が定義されていない
		# read_summer にﾛﾄ番号も読み込むようにすれば良いがﾌｧｲﾙｵｰﾌﾟﾝが一回増えるのでﾛﾄ番号だけを読み込む関数にしてしまった方がスマート
		my %s = &get_summer_datas($pid);
		my @lots = split /,/, $m{event_lot};
		if ($lots[0] ne '') {
			for my $lot (@lots) {
				push @list, "$m{name}<>$lot<>\n"
			}
		}
	}
	@list = map { $_->[0] } sort {$a->[2] <=> $b->[2]} map { [$_, split /<>/] } @list;
	$mes .= qq|<table><tr><th>名前</th><th>くじ</th></tr>|;
	my $next_lot = 1;
	for my $line (@list) {
		my ($name, $lot) = split /<>/, $line;
		$lot_n = $lot;
		$lot_n =~ s/^0*([1-9])(\d*)$/$1$2/;
		$mes .= qq|<tr>|;
		$mes .= qq|<td>$name</td>|;
		$mes .= qq|<td>|;
		if ($next_lot != $lot_n) {
			$mes .= qq|<font color="#FF0000">$lot</font>|;
		} else {
			$mes .= qq|$lot|;
		}
		$mes .= qq|</td>|;
		$mes .= qq|</tr>|;
		$next_lot = $lot_n + 1;
	}
	$mes .= qq|</table>|;
	closedir $dh;
}

#=================================================
# バグ発見報酬
#=================================================
sub bug_prize {
	my ($kind, $item_no, $item_c, $item_lv) = split /_/, $in{prize};

	my $item_mes = &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # 種類非表示

	&send_item($in{send_name}, $kind, $item_no, $item_c, $item_lv, 1);
	&write_send_news(qq|【バグ発見報酬】$in{send_name}に$item_mesを送ります。|);
	$mes .= "$in{send_name}に$item_mesを送ります。";
}

#=================================================
# 鯖内の全ﾍﾟｯﾄ表示
#=================================================
sub admin_all_pet_check {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my $depot_file = "$userdir/$pid/depot.cgi";
		my %pm = &get_you_datas($pid, 1);

		my $is_find = 0;
#		if ($pm{pet} && $pm{pet_c} >= 10) {
		if ($pm{pet} == 169) {
			push @lines, "$pm{name}<>3<>$pm{pet}<>$pm{pet_c}<>0<>\n";
			push @lines, "$pm{name}<>3<>$pm{pet}<>$pm{pet_c}<>0<>\n";
		}
		open my $fh, "< $depot_file" or &error("$depot_file が読み込めません");
		while (my $line = <$fh>) {
			next if $is_find;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
#			if ($kind eq '3' && $item_c >= 10) {
			if ($kind eq '3') {
				if ($item_no == 169) {
					push @lines, "$pm{name}<>$line";
					$is_find = 1;
				}
			}
		}
		close $fh;
	}
	@lines = map { $_->[0] } sort { $a->[2] <=> $b->[2] || $a->[3] <=> $b->[3] || $a->[4] <=> $b->[4] || $a->[1] cmp $b->[1] } map { [$_, split /<>/] } @lines;
	for my $line (@lines) {
		my($name, $kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$mes .= "$name:".&get_item_name($kind, $item_no, $item_c, $item_lv)."<br>";
	}
}

#=================================================
# 臨時処理(おそらく一度だけの処理の場合その都度ここで処理)
#=================================================
sub admin_expendable {
#	my $num = rmtree("./user/928381588adb");
#	$mes .= "$num";
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
		my $summer_file = "$userdir/$pid/summer.cgi";
		if (-f "$summer_file") {
			open my $fh, "> $summer_file" or &error("$summer_file が読み込めません");
			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
			close $fh;
		}
	}
	closedir $dh;
	my $this_vote_file = "$logdir/pop_vote.cgi";
	open my $fh, "> $this_vote_file" or &error("$this_vote_file が読み込めません");
	close $fh;

	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	open my $fh, "> $this_vote2_file" or &error("$this_vote2_file が読み込めません");
	close $fh;

	my $this_horror_story_file = "$logdir/horror_story.cgi";
	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file が読み込めません");
	close $fh;

	my $this_blog_vote_file = "$logdir/blog_vote.cgi";
	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file が読み込めません");
	close $fh;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('ラジオ体操ファイルが開けません');
			close $fh;
		}
	}
=pod
	&send_item("とーるぎす", 3, 8, 0, 0, 1);
	&send_item("とーるぎす", 3, 21, 0, 0, 1);
	&send_item("とーるぎす", 3, 21, 0, 0, 1);
	&send_item("とーるぎす", 3, 21, 0, 0, 1);
	&send_item("とーるぎす", 3, 22, 0, 0, 1);
	&send_item("とーるぎす", 3, 23, 0, 0, 1);
	&send_item("とーるぎす", 3, 24, 0, 0, 1);
	&send_item("とーるぎす", 3, 56, 0, 8, 1);
	&send_item("とーるぎす", 3, 136, 0, 0, 1);
	&send_item("とーるぎす", 3, 143, 0, 0, 1);
	&send_item("とーるぎす", 3, 143, 0, 0, 1);
	&send_item("とーるぎす", 3, 143, 0, 0, 1);
	&send_item("とーるぎす", 3, 143, 0, 0, 1);
	&send_item("とーるぎす", 3, 143, 0, 0, 1);
	&send_item("とーるぎす", 3, 200, 0, 0, 1);
=cut

#	my $from = "$userdir/6e616e616d6965";
#	my $to = "./user_backup/6e616e616d6965";
#	my $i = rcopy($from, $to);
#	my $num = rmtree($to);


#	unlink "$userdir/6e616e616d6965/letter_flag.cgi";
#	chmod '0666', "./user/82ad82a682d082b1/letter_flag.cgi";
#	open my $fh, "> ./user/82ad82a682d082b1/letter_flag.cgi" or &error("$!");
#	open my $fh, "> $userdir/82c6815b82e982ac82b7/shop_bank.cgi" or &error('ラジオ体操ファイルが開けません');
#	print $fh qq|500<>10<>10<>4999999<>\n304<>みかん<>2000000<>\n304<>みやこ<>2000000<>\n304<>大麻解禁<>2000000<>\n304<>フルーツ俺<>1900000<>\n304<>散るの<>2000000<>\n304<>とーるぎす<>4500000<>\n304<>睡魔<>4250000<>\n304<>ナナコ<>2000000<>\n304<>いちご<>2000000<>\n|;
#	close $fh;


#	my %p = &get_you_datas('Arthur', 0);
#	my $pt = $p{war_c} * 2;
#	&regist_you_data('めぐみん', 'seed', 'new_seed_151852970182df82ae82dd82f1');

#	$mes .= $p{seed};

=pod
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name}<br>";
		my $depot_log_file = "$userdir/$pid/depot_log.cgi";
		if (-f "$depot_log_file") {
			open my $fh, "< $depot_log_file" or &error("$depot_log_file が読み込めません");
			while (my $line = <$fh>) {
				$mes .= "$line<br>";
			}
			close $fh;
		}
	}
	closedir $dh;
=cut

#	&regist_you_data('とーるぎす', 'wt', 0);
	# 2258560
#	&regist_you_data('nanamie', 'coin', 811275);
#108122枚
#	&regist_you_data('あき', 'coin', 2258560);
#	&regist_you_data('VIPPER', 'coin', 2500000);
#	&regist_you_data('nanamie', 'coin', 2500000);
#	&regist_you_data('nanamie', "shogo", '★★ｾﾝﾀｰ');

#	open my $fh, "> $userdir/564950504552/casino_pool.cgi" or &error('ラジオ体操ファイルが開けません');
#	print $fh "11500000<>-325<>135<>\n";
#	close $fh;

#	require './lib/shopping_offertory_box.cgi';

=pod
	my $str = qq|ぽろん:3<>エゾシカ:1<>32:4<>ふわふわ:2<>vavaa:1<>あっしゅ:7<>謎の草:6<>のの:31<>ﾍﾞﾝｽﾞｱﾙﾃﾞﾋﾄﾞ:1<>すこ:1<>うっどげーと:1<>ドペニ:1<>さといも:1<>蔦:16<>吉良吉田:4<>検見川主殿頭:1<>サブリナ:1<>kotobuki:3<>LINKER:1<>睡魔:1<>偵察兵:31<>キリコ:1<>キリヱ:1<>1001:2<>レーニン:8<>トレーニー:1<>ステファ:1024<>ぴろん:6<>うんちして:1<>のけ者ﾌﾚﾝｽﾞ:1<>レタラ:1<>たんの:1<>かる:62<>su-:1<>パンツ:3<>でぶちん:13<>お米:10<>masa272:3<>ばりばり:1<>うりぼう:2<>21二世:1<>ぱらそる:1<>いかすみ:1<>素兎:1<>みやこ:5<>老回回:1<>誰:38<>プルプル:10<>カエル２:2<>オネーサン:10<>ヌゥ。:3<>片道:3<>白熱灯:1<>ものもらい:1<>もこみこ:10<>羊:5<>いけめんさま:1<>プルシュカ:1<>νavaa:1<>メルクリ:4<>部隊:1<>るじぇ:3<>ムラビトＮ:4<>ヨエル:50<>ぬんぱち:4<>地を這う豚:29<>ｱﾙﾋﾞｽ:1<>ヒアリ:1<>スネーク:23<>キリカ:1<>カリカリ:30<>orz:3<>Axis:2<>Forza:1<>六道:1<>大山椒魚:2<>不佞chan:30<>LokLok:6<>poppo:5<>ぬるぽん:15<>小神あきら:7<>くえひこ:1<>フルーツ俺:20<>アルン:2<>うにうに:1<>システム:1<>歌:1<>ぐう:1<>HalLunba:45<>ロイド:1<>Nep:2<>VIPPER:31<>あばばば保吉:5<>adad:10<>乃木まさよ:125<>ナナコ:9<>みなも:1<>マネヨーズ:10<>ぐったり:5<>くっさ:7<>ロボーん:42<>まおんこ:1<>レオン:1<>トトリ:1<>薄塩たらこ:16|;
	my @array = split /<>/, $str;
	my $num = 0;
	for my $i (0 .. $#array) {
		my ($name, $num2) = split /:/, $array[$i];
		$num += $num2;
	}

	my $j = int(rand($num));
	$mes .= "max num $num rand num $j<br>";

	$num = 0;
	for my $i (0 .. $#array) {
		my ($name, $num2) = split /:/, $array[$i];
		$mes .= "$name<br>" if $num <= $j && $j <= ($num+$num2);
		$num += $num2;
	}
=cut

#	my @plys = ('火粉', 'ザモイスキ', 'ブオーン', 'あき', '℃', '間黒男', 'あの細胞', '骨', '鉄仮面', 'nanamie');
#	my @goods = (500000, 400000, 300000, 200000, 100000, 80000, 60000, 40000, 20000, 10000);
#	for my $i (0 .. $#plys) {
#		my $name = $plys[$i];
#		&send_money($plys[$i], 'ｻﾏｰｼﾞｬﾝﾎﾞ当選金(小)', $goods[$i]);
#		my %datas = &get_you_datas($name);
#		my $v_coin = $datas{coin} + $goods[$i];
#		$v_coin = 2500000 < $v_coin ? 2500000 : $v_coin;
#		&regist_you_data($name, 'coin', $v_coin);
#	}

#火粉 500000
#ザモイスキ 400000
#ブオーン 300000
#あき 200000
#℃ 100000
#間黒男 80000
#あの細胞 60000
#骨  40000
#鉄仮面 20000
#nanamie 10000

#50000ｺｲﾝ
#ぶぶお 500000
#ムクガイヤ 400000
#田中 300000
#八百比丘尼 200000
#リノ 100000
#アイスさん 80000
#うごご 60000
#cheee 40000
#とーるぎす 20000
#オネーサン 10000

=pod
	my $this_file = "$logdir/event_lot_name";

	my %lot_name = ();

	if (-f "$this_file.cgi") {
		open my $fh, "< $this_file.cgi" or &error('ラジオ体操ファイルが開けません');
		while (my $line = <$fh>) {
			my ($mname, $mtime) = split /<>/, $line;
			$lot_name{$mname}++;
		}
		close $fh;
	}

	foreach my $k (keys(%lot_name)) {
		$mes .= "$k:$lot_name{$k}<br>";
	}
=cut
#		if (30 < $radio{$k}) {
#			if (&you_exists($k)) {
#うごご:13

#				&send_money('あさぎ', 'ﾗﾁﾞｵ体操皆勤賞', 2000000);
#				&send_god_item(5, 'あさぎ');
#				&write_world_big_news(qq|ﾗﾁﾞｵ体操ｶｰﾄﾞをすべて埋めた あさぎ さんが皆勤賞を成し遂げました|);
=pod
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
		elsif (20 < $radio{$k}) {
			if (&you_exists($k)) {
				&send_money($k, 'ﾗﾁﾞｵ体操努力賞', 500000);
				&send_god_item(1, $k);
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
		elsif (10 < $radio{$k}) {
			if (&you_exists($k)) {
=cut
#				&send_money('†えーのん†', 'ﾗﾁﾞｵ体操参加賞', 20000);
=pod
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
	}

	for my $i (0 .. $#top) {
		$mes .= $top[$i];
	}
	for my $i (0 .. $#middle) {
		$mes .= $middle[$i];
	}
	for my $i (0 .. $#bottom) {
		$mes .= $bottom[$i];
	}
=cut
#	for my $i (0 .. $#bottom2) {
#		$mes .= $bottom2[$i];
#	}


=pod
			my ($holy_strong, $dark_strong) = (0, 0);
			$holy_strong += $cs{strong}[$_] for (1 .. $w{country}-1);
			my $holy_strong_ave = int($holy_strong / ($w{country}-1));
			$dark_strong += $cs{strong}[$w{country}];

			# 基本仕様 暗黒国力が統一国力から遠いほどｶｳﾝﾀｰ率上昇
			my $divisor = $touitu_strong;
			# 暗黒の国力が増えるほどｶｳﾝﾀｰ率低下
			# 封印側の平均国力が増すほどｶｳﾝﾀｰ率低下するが、暗黒同盟国の国力として平均国力を足している（仮想同盟）
			# 仮想同盟として国力を足さない場合、おそらく暗黒が殴る殴られるで国力が変動したときにｶｳﾝﾀｰ率の変動も激しくなる
			my $dividend = $touitu_strong-($dark_strong+$holy_strong_ave);

			if ($dark_strong < $holy_strong_ave) { # 封印の平均国力よりも暗黒の国力が低い
				$divisor = 1; # 暗黒死にそう 修羅モード
			}
			elsif ($touitu_strong < 50000 && ($touitu_strong*0.5) < $dark_strong) { # 統一国力が5万切っていて、かつ暗黒の国力が統一国力の半分より高い
				# (統一国力 - (暗黒国力 + 封印平均国力)) / ((暗黒国力 + 封印平均国力) / 2 + 統一国力)
				$divisor = ($dark_strong+$holy_strong_ave) / 2 + $touitu_strong; # 暗黒とその仮想同盟の国力が高いほどｶｳﾝﾀｰ率下げる
			}
			elsif ($dark_strong < 30000) { # 暗黒の国力が3万切ったら本気モード
				$divisor -= $holy_strong_ave / 2; # 封印の平均国力が高いほど暗黒のｶｳﾝﾀｰ率上昇 本気モード
			}

#			$dividend = $divisor * 0.25 if ($holy_strong_ave / $dark_strong) < 0.6;
#			$dividend = $divisor * 0.5 if 0.5 < ($dividend / $divisor);

#			my $base = $dark_strong < 30000 ? $touitu_strong-$holy_strong_ave/2 : $touitu_strong ;
#			my $base = $touitu_strong ;
#			$base = 0 if $dark_strong < $holy_strong_ave;

			$mes .= "touitu_strong $touitu_strong holy_strong $holy_strong holy_strong_ave $holy_strong_ave dark_strong $dark_strong<br>";
			$mes .= "($touitu_strong - ($dark_strong+$holy_strong_ave)) / ($touitu_strong - ($holy_strong_ave/2))<br>";
			$mes .= "$dividend/$divisor<br>";
			$mes .= "% ".($dividend/$divisor)."<br>";
=cut

#	&regist_you_data('VIPPER', "coin", 2500000);
#	&regist_you_data('ライト', 'money_limit', 300000000);
#	&send_money('ライト', 'ｻﾏｰｼﾞｬﾝﾎﾞ当選金', 300000000);
#	require './lib/shopping_offertory_box.cgi';
#	&regist_you_data('マネヨーズ', "shogo", '★★ｴﾆｯｷﾏｽﾀｰ');
#	&send_money('マネヨーズ', '絵日記優秀賞', 2000000);
#	&send_god_item(5, 'マネヨーズ');

#my $summer_file = "$userdir/8356835883658380/summer.cgi";
#open my $fh, "> $summer_file" or &error("$summer_file が読み込めません");
#print $fh "radio_time;1503695737<>pop_vote;735<>blog_time;1503662907<>morning_glory;6<>morning_glory_time;1503668426<>summer_blog;25<>cicada_sound;<>dummy;0<>";
#close $fh;

#	my @tutorials = ('片道', 'ドペニ', 'ぐう', 'ぽろん', 'サブリナ', 'BlackBoxNPC', 'さといも', '露夢', 'Luxuria', 'レオン');

#	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
#	while (my $id = readdir $dh) {
#		next if $id =~ /\./;
#		next if $id =~ /backup/;

#		my %m = &get_you_datas($id, 1);

#		my $name = pack 'H*', $id;

		# 夏祭り用
#		unless (-f "$userdir/$id/summer.cgi") {
#			$mes .= "summer $name<br>";
#		}

#		unless (-f "$userdir/$id/tutorial.cgi") {
#			$mes .= "tutorial $name<br>";
#			my $output_file = "$userdir/$id/tutorial.cgi";
#			open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
#			close $fh;
#		}

#		open my $fh, "< $userdir/$id/summer.cgi" or &error("そのような名前のﾌﾟﾚｲﾔｰが存在しません");
#		my $line = <$fh>;
#		close $fh;

#		for my $hash (split /<>/, $line) {
#			my($k, $v) = split /;/, $hash;
#			$m{$k} = $v;
#		}
#		$m{dummy} = 0;

#		if ($m{summer_blog} > 30) {
#			&regist_you_data($m{name}, "shogo", '★★ｴﾆｯｷﾏｽﾀｰ');
#			&send_money($m{name}, '絵日記優秀賞', 2000000);
#			&send_god_item(5, $m{name});
#		} elsif($m{summer_blog} > 20) {
#			&send_money($m{name}, '絵日記努力賞', 500000);
#			&send_god_item(1, $m{name});
#		} elsif($m{summer_blog} > 10) {
#			&send_money($m{name}, '絵日記参加賞', 20000);
#		}

#		push @morning_glory, "$m{name}<>$m{morning_glory}<>\n";
#	}
#	closedir $dh;

=pod
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
#		my $summer_file = "$userdir/$pid/summer.cgi";
#		if (-f "$summer_file") {
#			open my $fh, "> $summer_file" or &error("$summer_file が読み込めません");
#			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#			close $fh;
#		}
	}
	closedir $dh;
=cut
#	require './lib/_rampart.cgi'; # 城壁
#	for my $i (1 .. 5) {
#		&change_barrier(6, -25);
#	}
#	&write_cs;
#		&regist_you_data('システム', 'wt', '0');
#		&regist_you_data('ふわふわ', 'c_turn', '0');
#		&regist_you_data('ザモイスキ', 'c_turn', '0');
=pod
	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			my @members = ();
			open my $fh, "+< $this_radio_dir/$d.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my ($mname, $mtime) = split /<>/, $line;
				if ($mname eq 'うんちして') {
					push @members, "システム<>$mtime<>\n";
				}
				else {
					push @members, "$mname<>$mtime<>\n";
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @members;
			close $fh;
		}
	}
=cut
#	open my $fh, "> $logdir/error.cgi" or &error("$this_vote_file が読み込めません");
#	close $fh;

#	&send_item('SOUTH', 3, 168, 0, 0, 1);

#my $this_lot_file = "$logdir/event_lot.cgi";
#my $this_lot_name_file = "$logdir/event_lot_name.cgi";

#my $this_blog_vote_result_file = "$logdir/blog_vote_result.cgi";
=pod
	my $this_vote_file = "$logdir/pop_vote.cgi";
	open my $fh, "> $this_vote_file" or &error("$this_vote_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	open my $fh, "> $this_vote2_file" or &error("$this_vote2_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_horror_story_file = "$logdir/horror_story.cgi";
	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_blog_vote_file = "$logdir/blog_vote.cgi";
	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('ラジオ体操ファイルが開けません');
			close $fh;
		}
	}
=cut
#	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#	close $fh;

#	my $summer_file = "$logdir/event_lot_name.cgi";
#	open my $fh, "> $summer_file" or &error("$summer_file が読み込めません");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#	close $fh;


=pod
	my $name = '誰';
	my %datas = &get_you_datas($name);
	my $v_coin = $datas{coin} + 1149320;
	$v_coin = $v_coin > 2500000 ? 2500000 : $v_coin;
	&regist_you_data($name, 'coin', $v_coin);

	my $name = '骨';
	my %datas = &get_you_datas($name);
	my $v_coin = $datas{coin} - 1149320;
	$v_coin = $v_coin > 2500000 ? 2500000 : $v_coin;
	&regist_you_data($name, 'coin', $v_coin);
=cut
=pod
	my @lines = ();
	open my $fh, "+< $userdir/818e/super.cgi" or &error("$target.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	push @lines, "26<>0<>3<>3<>0<>12<>からあげ砲<>1<>1463841347<>\n";
	push @lines, "46<>4<>0<>3<>0<>0<>からあげ砲<>1<>1468403883<>\n";
	push @lines, "66<>0<>1<>8<>0<>0<>からあげ砲<>1<>1473019609<>\n";
	push @lines, "86<>1<>13<>13<>0<>12<>からあげ砲<>0<>1478220558<>\n";
	push @lines, "106<>2<>13<>10<>0<>4<>からあげ砲<>1<>1482969513<>\n";
	push @lines, "126<>7<>12<>7<>0<>4<>からあげ砲<>1<>1487737021<>\n";
	push @lines, "146<>7<>19<>8<>0<>8<>つーか、これからっしょ！<>1<>1493892431<>\n";
	push @lines, "166<>1<>11<>8<>2<>14<>からあげ砲<>0<>1497424101<>\n";
	push @lines, "186<>15<>23<>10<>0<>14<>つーか、これからっしょ！<>0<>1500482540<>\n";

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
=cut

#26<>1<>6<>0<>0<>0<>お腹いたい<>1<>1463849463<>
#66<>0<>7<>1<>0<>15<>9021192182<>0<>1472933764<>
#86<>2<>27<>8<>2<>10<>ねむ<>2<>1478072043<>
#106<>1<>10<>4<>0<>2<>あ<>1<>1482963421<>
#126<>1<>22<>5<>0<>13<>あ<>1<>1487666060<>
#146<>0<>26<>11<>0<>3<>寿司食べたい<>1<>1493887062<>
#166<>6<>11<>5<>0<>1<>暑い<>1<>1497574264<>
#186<>8<>25<>10<>0<>0<>ビールまだー？<>0<>1500480513<>


=pod
	my @lines = ();
	my $money = 0;
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$money += $pm{money};

		my $bank_file = "$userdir/$pid/shop_bank.cgi";
		if (-f "$bank_file") {
			open my $fh, "< $bank_file" or &error("$bank_file が読み込めません");
			my $hl = <$fh>;
			while (my $line = <$fh>) {
				my @data = split /<>/, $line;
				$money += $data[2];
			}
			close $fh;
		}
	}
	closedir $dh;

	$mes .= $money;
=cut
=pod
	require './lib/_rampart.cgi'; # 城壁
	for my $i (1 .. 5) {
		&change_barrier($i, 100);
	}
	&write_cs;
=cut
}

#=================================================
# 複垢比較
#=================================================
sub admin_compare {
	my @lines = ();
	my @comp = ($in{comp1}, $in{comp2});
	my %addr = ();
	my %host = ();
	my %agent = ();
	my $bit = 1;
	for my $name (@comp) {
		my $id = unpack 'H*', $name;

		open my $fh2, "< $userdir/$id/access_log.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
		while (my $line_info_add = <$fh2>){
			my ($maddr, $mhost, $magent) = split /<>/, $line_info_add;
			if (($addr{$maddr} & $bit) == 0) {
				$addr{$maddr} |= $bit;
			}
			if (($host{$mhost} & $bit) == 0) {
				$host{$mhost} |= $bit;
			}
			if (($agent{$magent} & $bit) == 0) {
				$agent{$magent} |= $bit;
			}
		}
		$bit *= 2;
	}

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>アドレス</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $maddr (keys(%addr)) {
		my $mes_tr = qq|<td>$maddr</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($addr{$maddr} & $bit) {
				$mes_tr .= qq|○|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>ホスト名</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $mhost (keys(%host)) {
		my $mes_tr = qq|<td>$mhost</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($host{$mhost} & $bit) {
				$mes_tr .= qq|○|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>エージェント</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $magent (keys(%agent)) {
		my $mes_tr = qq|<td>$magent</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($agent{$magent} & $bit) {
				$mes_tr .= qq|○|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;
}

#=================================================
# 適当士官フラグリセット
#=================================================
sub migrate_reset {
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		$name = pack 'H*', $id;
		&regist_you_data($name, "random_migrate", '');
	}
	closedir $dh;

}
#=================================================
# 改造ﾊﾟﾙﾌﾟﾝﾃ
#=================================================
sub admin_parupunte {
	require "$datadir/parupunte.cgi";
	&{$effects[2]};
	$mes .= "<hr>改造ﾊﾟﾙﾌﾟﾝﾃを打ちました<br>";
}

#=================================================
# 手紙の送信履歴（プライバシーを考慮し、誰が誰に送信したかだけをロギングしている）
#=================================================
sub admin_letter_log_check {
	$mes .= qq|<table><tr><th>送信者</th><th>受信者</th><th>送信日時</th></tr>\n|;

	open my $fh, "< $logdir/letter_log.cgi" or &error("$logdir/letter_log.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($from_name, $to_name, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$from_name</td><td>$to_name</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# 卵の孵化履歴
#=================================================
sub admin_incubation_log_check {
	$mes .= qq|<table><tr><th>名前</th><th>卵</th><th>ﾍﾟｯﾄ</th><th>孵化日時</th></tr>\n|;

	open my $fh, "< $logdir/incubation_log.cgi" or &error("$logdir/incubation_log.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($name, $egg, $pet, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$name</td><td>$egg</td><td>$pet</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# アイテムの購入履歴
#=================================================
sub admin_shopping_log_check {
	$mes .= qq|<table><tr><th>購入者</th><th>経営者</th><th>ｱｲﾃﾑ</th><th>値段</th><th>購入日時</th></tr>\n|;

	open my $fh, "< $logdir/shopping_log.cgi" or &error("$logdir/shopping_log.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($m_name, $y_name, $item, $price, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$m_name</td><td>$y_name</td><td>$item</td><td>$price</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# 倉庫の中身確認
#=================================================
sub admin_get_depot_data {
	my $pid = $in{id};

	my $count = 0;
	my $mes_sub;
	$mes .= qq|$in{name}<br>\n|;
	open my $fh2, "< $userdir/$pid/depot.cgi" or &error("倉庫ﾌｧｲﾙを開けませんでした");
	while (my $line = <$fh2>) {
		$count++;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

		$mes_sub .= &get_item_name($kind, $item_no, $item_c, $item_lv)."<br>";
	}
	close $fh2;
	$mes .= "$count個<br>".$mes_sub;
#	print qq|$</table>\n|;
}

#=================================================
# 商人の店の販売履歴
#=================================================
sub admin_get_akindo_data {
	my $pid = $in{id};

	$mes .= qq|$in{name}<br>\n|;
	$mes .= qq|<table><tr><th>販売ｱｲﾃﾑ</th><th>購入者</th><th>購入日時</th></tr>\n|;
	open my $fh2, "< $userdir/$pid/shop_sale_detail.cgi" or &error("商人の店ﾌｧｲﾙを開けませんでした");
	while (my $line = <$fh2>) {

		my($item, $y_name, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= qq|<tr><td>$item</td><td>$y_name</td><td>$ltime2</td></tr>|;
	}
	close $fh2;
	$mes .= qq|</table>|;
}

#=================================================
# 銀行の取引履歴
#=================================================
sub admin_get_bank_log {
	my $pid = $in{id};

	$mes .= qq|$in{name}<br>\n|;
	$mes .= qq|<table><tr><th>銀行</th><th>金額</th><th>取引</th><th>取引日時</th></tr>\n|;
	open my $fh2, "< $userdir/$pid/shop_bank_log.cgi" or &error("銀行ﾛｸﾞﾌｧｲﾙを開けませんでした");
	while (my $line = <$fh2>) {

		my($y_name, $type, $money, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= qq|<tr><td>$y_name</td><td>$type</td><td>$money</td><td>$ltime2</td></tr>|;
	}
	close $fh2;
	$mes .= qq|</table>|;
}

#=================================================
# 討伐の卵入手履歴
#=================================================
sub admin_hunt_log_check {
	$mes .= qq|<table><tr><th>討伐者</th><th>討伐地</th><th>拾った卵</th><th>拾えたか</th><th>日時</th></tr>\n|;

	open my $fh, "< $logdir/hunt_log.cgi" or &error("$logdir/hunt_log.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($m_name, $place, $item, $is_get, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$m_name</td><td>$place</td><td>$item</td><td>$is_get</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}
