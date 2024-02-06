#================================================
# メイン画面 Created by Merino
#================================================

# お店の売上金の税金(0(税金なし)～0.99まで)
my $shop_sale_tax = 0.2;
# ギルドマスターの税金免除率(0(税金なし)～0.99まで)
my $guild_master_tax_rate = 1.0;
# 活発なギルドの税金免除率(0(税金なし)～1.0まで)
my $guild_prior_tax_rate = 1.0;
# その他のギルドの税金免除率(0(税金なし)～1.0まで)
my $guild_ferior_tax_rate = 1.0;

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['更新',		''],
	['ｼｮｯﾋﾟﾝｸﾞﾓｰﾙ',	'shopping'],
	['預かり所',	'depot'],
	['国庫',	'depot_country'],
	['ﾏｲﾙｰﾑ',		'myself'],
	['修行',		'training'],
	['討伐',		'hunting'],
	['国情報',		'country'],
	['内政',		'domestic'],
	['外交',		'promise'],
	['軍事',		'military'],
	['戦争',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['孵化', 'incubation'];
}
if (&on_summer) {
	push @menus, ['夏祭り', 'summer_festival'];
}
elsif(&on_may_june){
	push @menus, ['秋イベ', 'boardgame_splend_test'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# ﾒｲﾝｼｽﾃﾑ
#================================================
sub main_system {
	if(&on_december_end){
		&winter_xmas_end;#クリスマス終了処理
	}
	if(!&on_new_year && !&on_december && -f "$userdir/$id/greeting_card.cgi"){
		require './lib/greeting_card_lot.cgi';
		&lot_delete;
		if(-f "$logdir/greeting_card_summary.cgi"){#lot_deleteで削除できなかったので
			unlink "$logdir/greeting_card_summary.cgi" or &error("$logdir/greeting_card_summary.cgiﾌｧｲﾙを削除することができません");
		}
	}
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '卵士';
			push @menus, ['孵化', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# ﾀﾏｺﾞ成長
	elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "持っていた$eggs[$m{egg}][1]が光だしました!<br>";

		# ﾊｽﾞﾚｴｯｸﾞ専用処理
		if ( $eggs[$m{egg}][1] eq 'ﾊｽﾞﾚｴｯｸﾞ' && rand(7) > 1 && $m{egg} != 53) {
			if (rand(6) > 1) {
				$mes .= "なんと、$eggs[$m{egg}][1]の中から $eggs[$m{egg}][1]が産まれました<br>";
			}
			else {
				$mes .= "なんと、$eggs[$m{egg}][1]の中は空っぽでした…<br>";
				$m{egg} = 0;
			}
		}
		# ﾀｷｵﾝｴｯｸﾞ
		elsif ($eggs[$m{egg}][1] eq 'ﾀｷｵﾝｴｯｸﾞ') {
			$m{egg_c} = 0;
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];

			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			if (rand(3) < 1) {
				$m{egg} = 0;
			} else {
				$mes .= "$eggs[$m{egg}][1]が時を逆行した<br>";
			}
		}
		# ｱﾋﾞﾘﾃｨｴｯｸﾞ専用処理(曜日により変わる)
		elsif ( $eggs[$m{egg}][1] eq 'ｱﾋﾞﾘﾃｨｴｯｸﾞ' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];

			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];

			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('incubation');
		}
	}
	# ｵｰｸｼｮﾝ代、お店の売上金、送金系の受け取り
	elsif (-s "$userdir/$id/money.cgi") {
		if($m{guild_number}){
			open my $fhg1, "< $logdir/guild_shop1_sale.cgi";
			my $lineg1 = <$fhg1>;
			my($g1_sale_c, $g1_sale_money, $g1_update_t) = split /<>/, $lineg1;
			close $fhg1;

			open my $fhg2, "< $logdir/guild_shop2_sale.cgi";
			my $lineg2 = <$fhg2>;
			my($g2_sale_c, $g2_sale_money, $g2_update_t) = split /<>/, $lineg2;
			close $fhg2;
			if(($m{guild_number} == 1 && $g1_sale_c > $g2_sale_c) || ($m{guild_number} == 2 && $g2_sale_c > $g1_sale_c)){
				$shop_sale_tax *= $guild_prior_tax_rate;
			}else{
				$shop_sale_tax *= $guild_ferior_tax_rate;
			}

			open my $fhg, "< $logdir/bbs_akindo_$m{guild_number}_allmember.cgi";
			my $headline = <$fhg>;
			while (my $line = <$fhg>) {
				my($mname, $vote, $master) = split /<>/, $line;
				if ($master) {
					if($mname eq $m{name}){
						$shop_sale_tax *= $guild_master_tax_rate;
					}
					last;
				}
			}
			close $fhg;
		}

		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;

			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$nameに $money Gを支払いました<br>";

				# 銀行経営者が資金マイナスになった場合は銀行は倒産
#				if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
#					unlink "$userdir/$id/shop_bank.cgi";
#					unlink "$userdir/$id/shop_sale_bank.cgi";
#					&mes_and_send_news("<b>経営する銀行は赤字経営のため倒産しました</b>", 1);
#				}
			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '商人' || $pets[$m{pet}][2] eq 'tax_free') {
					$mes .= "$nameから $money Gの売上金を受け取りました<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$nameから $money Gの売上金を受け取り、$v G税金として取られました<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			elsif ($is_shop_sale eq '2') {
				$mes .= "$nameから $money を受け取りました<br>";
			}
			else {
				$m{money} += $money;
				$mes .= "$nameから $money Gを受け取りました<br>";
			}
		}
		# 銀行経営者が資金マイナスになった場合は銀行は倒産
		# ↑修正、資金マイナス、かつ、銀行預金が100万以下の時倒産
		if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
			my $shop_id = unpack 'H*', $m{name};

			my $last_year = 0;
			my $save_money = 0;
			open my $fh2, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
			my $head_line = <$fh2>;
			while (my $line = <$fh2>) {
				my($year, $name, $money) = split /<>/, $line;
				if ($m{name} eq $name) {
					$save_money = $money;
					$last_year = $year;
					last;
				}
			}
			close $fh2;
			if ($save_money < 1000000) {
				unlink "$userdir/$id/shop_bank.cgi";
				unlink "$userdir/$id/shop_sale_bank.cgi";
				&mes_and_send_news("<b>経営する銀行は赤字経営のため倒産しました</b>", 1);
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/ex_c.cgi") {
		open my $fh, "+< $userdir/$id/ex_c.cgi" or &error("$userdir/$id/ex_c.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($c, $number) = split /<>/, $line;
			&c_up($c) for(1..$number);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/cataso_res.cgi") {
		if (!$m{cataso_ratio}) {
			$m{cataso_ratio} = 1500;
		}
		open my $fh, "+< $userdir/$id/cataso_res.cgi" or &error("$userdir/$id/cataso_res.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($compare, $value) = split /<>/, $line;
			my %c_data = &get_you_datas($compare, 1);
			if (!$c_data{cataso_ratio}) {
				$c_data{cataso_ratio} = 1500;
			}
			my $dr = int(16 + ($c_data{cataso_ratio} - $m{cataso_ratio}) * 0.04 + 0.5);
			if ($dr < 1) {
				$dr = 1;
			} elsif ($dr > 32) {
				$dr = 32;
			}
			$m{cataso_ratio} += int($dr * $value);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif ((-s "$userdir/$id/head_hunt.cgi") && $m{random_migrate} ne $w{year}) {
		if ($in{head_hunt} ne '1') {
			open my $fh, "< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgiﾌｧｲﾙが開けません");
			while (my $line = <$fh>) {
				my($hname, $hcountry) = split /<>/, $line;
				$mes .= "$hnameから $cs{name}[$hcountry] への勧誘を受けています<br>";
			}
			close $fh;

			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="hidden" name="head_hunt" value="1">|;
			$mes .= qq|<input type="submit" value="勧誘を受ける" class="button1"></form>|;
		}
		else {
			$mes .= "勧誘を受けることにしました<br>";
			$m{lib} = 'country_move';
			$m{tp} = 100;
			&n_menu;
		}
	}
	# 国に所属している場合
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "日頃の国への貢献が認められ、$m{name}の階級が$rank_nameに昇進しました<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				my $rank_name = &get_rank_name($m{rank}, $m{name});
				$mes .= "$m{name}の階級が$rank_nameに降格しました<br>";
				if($m{super_rank}){
					$mes .= "しかし$m{rank_name}は名誉職なので名称はそのままです<br>";
				}
			}
		}
		# 給与
		elsif ($m{country} && $time >= $m{next_salary}) {
			if($m{salary_switch} && $in{get_salary} ne '1'){
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
				$mes .= qq|<input type="submit" value="給料を受け取る" class="button1"></form>|;
			}else{
				$m{egg_c} += int(rand(50)+100) if $m{egg};
				&salary;
			}
		}
	}

	if($m{shogo_t} ne '' || $m{icon_t} ne ''){
		if($time >= $m{trick_time}){
			if($m{shogo_t} ne ''){
				$m{shogo} = $m{shogo_t} unless ($m{shogo} eq $shogos[1][0]);
				$m{shogo_t} = '';
			}
			if($m{icon_t} ne ''){
				if($m{icon} ne $default_icon){
					unlink "$icondir/$m{icon}" or &error("$m{icon}が存在しません");
				}
				$m{icon} = $m{icon_t};
				$m{icon_t} = '';
			}
		}
	}
	if(-s "$userdir/$id/fx.cgi"){
		require './lib/fx_func.cgi';
		$mes .= &check_losscut;
	}

	$y{country} = 0 if $y{country} eq '';
#	$m{act} = 0 if $config_test;
	&run_tutorial_quest('tutorial_full_act_1') if $m{act} > 99;
	if($m{start_time} eq ''){
		$m{start_time} = $time - 3600 * 24 * 306;
	}
}

#================================================
# 給与
#================================================
sub salary {
	# 給与税
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );

	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;

	my $v = int( $salary_base * &tax ) + 1000;

	# 君主なら給料2.0倍、国の代表者なら給料1.5倍
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$v *= 2.0;
	} elsif (&is_daihyo) {
		$v *= 1.5;
	}

	# 統一国ならﾎﾞｰﾅｽ
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# 同盟なしで統一なら2倍
		$v *= defined $c2 ? 1.75 : 2;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}

	# 滅亡時
	$v *= 0.5 if $cs{is_die}[$m{country}];

	# 商人ならﾎﾞｰﾅｽ
	$v += 5000 if $jobs[$m{job}][1] eq '商人';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_mから $v Gの給与があたえられました<br>";
	&write_yran('sal', $v, 1) if $v > 0;
}


#================================================
# 世代交代/ﾚﾍﾞﾙｱｯﾌﾟ
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};

	# 世代交代
#	my $sedai_max = &seed_bonus('sedai_lv', 100);
	my $sedai_max = 100;#seed_bonus関数のreturnを1にしたためバグる、一時的修正
	if ($m{lv} >= $sedai_max) {
		$m{lv} = 1;
		&c_up('sedai');

		# 結婚していた場合
		if ($m{marriage} || $m{sox_kind} eq '11' && (&on_december_end || !&on_december)) {
			if($m{marriage}){
				&mes_and_world_news("$m{marriage}との間にできた$m{sedai}代目の子供に意志が引き継がれました", 1);
			}
			else{
				&mes_and_world_news("聖ｴﾝｼﾞｪﾙの力により受胎した$m{sedai}代目の子供に意志が引き継がれました", 1);
				$m{sox_kind} = 0;#冬イベの効果は一世代限り
			}

			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}

			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));
			$m{super_rank} = 0;
			$m{rank_name} = '';

			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # 覚えている技を保存
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;

					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# 覚えていないｽｷﾙなら追加
						unless ($line =~ /,\Q$skill\E,/) {
							$is_rewrite = 1;
							$line .= "$skill,";
						}
					}
					if ($is_rewrite) {
						$line  = join ",", sort { $a <=> $b } split /,/, $line;
						$line .= ',';

						seek  $fh, 0, 0;
						truncate $fh, 0;
						print $fh $line;
					}
					close $fh;
				}

				if ($pets[$m{pet}][2] eq 'copy_pet' && $datas{pet}) {
					$mes .= "$pets[$m{pet}][1]★$m{pet_c}は$datas{name}のﾍﾟｯﾄの$pets[$datas{pet}][1]をｺﾋﾟｰしました<br>";
					$m{pet} = $datas{pet};
					#&get_icon_pet;
				}

			}
		}
		# 結婚していないとき
		else {
			if($m{job} ne '24'){
				&mes_and_world_news("$m{sedai}代目へと意志が引き継がれました", 1);
			}else{
				&mes_and_world_news("$m{sedai}代目へと意志が引き継がれました魔法少女$m{name}のソ\ウルジェムが真っ黒に染まった！", 1);
				open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
				$line = <$bfh>;
				my $boss_name = (split /<>/, $line)[0];
				close $bfh;
				if($boss_name eq '負けイベント'){
					$in{boss_at} = $m{at} + 500;
					$in{boss_df} = $m{df} + 500;
					$in{boss_mat} = $m{mat} + 500;
					$in{boss_mdf} = $m{mdf} + 500;
					$in{boss_ag} = $m{ag} + 500;
					$in{boss_cha} = $m{cha} + 500;
					open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
					print $bfh "魔女$m{name}<>0<>99999<>99999<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$m{wea}<>$m{skills}<>$m{mes_lose}<>$m{mes_win}<>$default_icon<>$m{wea_name}<>\n";
					close $bfh;
				}
			}

			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}

			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]★$m{pet_c}の力によりｽﾃｰﾀｽがそのまま引き継がれました<br>";
				$mes .= "役目を終えた$pets[$m{pet}][1]★$m{pet_c}は、光の中へと消えていった…<br>";
				&remove_pet;
			}
			else {
				&c_up('boch_c');
				my $down_par = $m{sedai} > 7 ? (rand(0.25)+0.6) : $m{sedai} * 0.05 + 0.35;
				if($m{job} eq '22' || $m{job} eq '23'){
					$down_par = (rand(0.5) + 0.45);
				}
				for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
					unless($m{job} eq '24' && ($k eq 'max_mp' || $k eq 'cha' || $k eq 'cha_org')){
						$m{$k} = int($m{$k} * $down_par);
					}
				}
				if($m{job} eq '24'){
					$m{job} = 0;
				}
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} -= int(rand(2));
				$m{super_rank} = 0;
				$m{rank_name} = '';
			}
		}
		if($m{master} && $m{master_c} && $m{sedai} >= 3){
			&graduate;
		}
		# 以下共通の処理
		$m{rank} = 1 if $m{rank} < 1;

		&use_pet('sedai');

		if ($m{skills}) { # 覚えている技を保存
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# 覚えていないｽｷﾙなら追加
				unless ($line =~ /,\Q$skill\E,/) {
					$is_rewrite = 1;
					$line .= "$skill,";
				}
			}
			if ($is_rewrite) {
				$line  = join ",", sort { $a <=> $b } split /,/, $line;
				$line .= ',';

				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
			}
			close $fh;
		}
		if ($pets[$m{pet}][2] eq 'keep_seed') {
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}の力により種族がそのまま引き継がれました<br>";
			$mes .= "役目を終えた$pets[$m{pet}][1]★$m{pet_c}は、光の中へと消えていった…<br>";
			&remove_pet;
			&seed_change('keep');
		} elsif ($pets[$m{pet}][2] eq 'change_seed') {
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}の力により種族が変わるかもしれません<br>";
			$mes .= "役目を終えた$pets[$m{pet}][1]★$m{pet_c}は、光の中へと消えていった…<br>";
			&remove_pet;
			&seed_change('change');
		} else {
			&seed_change('');
		}
		$m{marriage} = '';
#		&refresh_new_commer;
	}
	# レベルアップ
	else {
		$mes .= "Lvｱｯﾌﾟ♪<br>";

		# HP だけは必ず１以上upする仕様
		my $v = int( rand($jobs[$m{job}][2]) ) + 1;
		$m{max_hp} += $v;
		$mes .= "$e2j{max_hp}+$v ";

		my $count = 3;
		for my $k (qw/max_mp at df mat mdf ag lea cha/) {
			my $v = int( rand($jobs[$m{job}][$count]+1) );
#			$v = &seed_bonus($k, $v);
			$m{$k} += $v;
			if ($k eq 'cha') {
				$m{cha_org} += $v;
			}
			$mes .= "$e2j{$k}+$v ";
			++$count;
		}

		&use_pet('lv_up');
		&run_tutorial_quest('tutorial_lv_20_1') if $m{lv} == 20;
	}
}

#================================================
# 弟子卒業
#================================================
sub graduate {
	&send_item($m{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
	if(rand(7) > 1){
		&send_item($m{master}, 2, int(rand($#eggs)+1), 0, 0, 1);
	}else{
		require './lib/shopping_offertory_box.cgi';
		&send_god_item(5, $m{master});
	}

	&mes_and_world_news("$m{master}の弟子として立派に成長しました", 1);
	&regist_you_data($m{master}, 'master', '');
	$m{master} = '';
	$m{master_c} = '';
}

sub sub_test {
	$debug_mes .= "$_[0]";
	$_[0] + $_[1];
}
#================================================
# クリスマス終了処理(ﾘﾌｫｰﾑ、武器、絵)
#================================================
sub winter_xmas_end{
	if($m{sox_kind} eq '10'){#受胎告知
		$mes .= "持っていた靴下が光だしました！<br>";
		$mes .= "あなたは体に何かが宿るのを感じた！<br>";
		$mes .= "「Merry X'mas！良いお年を！」<br>";
		$m{sox_kind} = 11;#0にする処理はlv_up関数に埋め込み
	}
	if($m{sox_kind} eq '20'){#ﾘﾌｫｰﾑ
		$mes .= "持っていた靴下が光だしました！<br>";
		$mes .= "なんということでしょうｻﾝﾀｸﾛｰｽのﾘﾌｫｰﾑにより<br>あんなに狭かった預り所が少し広くなりました<br>";
		$mes .= "「Merry X'mas！良いお年を！」<br>";
		++$m{depot_bonus};
		$m{sox_kind} = 0;
	}
	if($m{sox_kind} eq '30'){#あの絵が欲しい
		use File::Copy::Recursive qw 'rcopy';
		use File::Path;
		rcopy("$logdir/legend/picture/$m{sox_picture}","$userdir/$id/picture/$m{sox_picture}") or &error("が存在しません");
		$mes .= "持っていた靴下が光だしました！<br>";
		$mes .= "靴下の中からずっと欲しかったあの絵が出てきた！<br>";
		$mes .= "「Merry X'mas！良いお年を！」<br>";
		$m{sox_kind} = 0;
	}
	if($m{sox_kind} eq '40'){#かっこいい武器が欲しい
		#武器　ｸﾛﾑﾊｰﾂ、ﾄﾞﾚｲﾉｸｻﾘ
		#ﾐｻｲﾙ実装後は追加
		#send_item関数アップデート後以下の処理を修正する予定
		&send_item($m{name}, 1, int(31 + rand(2)), 0, 0);
		$mes .= "持っていた靴下が光だしました！<br>";
		$mes .= "サンタクロースの不思議な力により新しい武器を手に入れました！<br>";
		$mes .= "「Merry X'mas！良いお年を！」<br>";
		$m{sox_kind} = 0;
	}
	if($m{sox_kind} eq '50'){#ハズレ 何もなしだとかわいそうかなと思いステぺ贈呈
		@status_up_pets = (78..110);#ステータスupペット
		&send_item($m{name}, 3,$status_up_pets[rand($#status_up_pets)], 0, 0);
		$mes .= "靴下にはささやかな幸せが入っていた。<br>";
		$mes .= "「Merry X'mas！良いお年を！」<br>";
		$m{sox_kind} = 0;
	}

}
1; # 削除不可
