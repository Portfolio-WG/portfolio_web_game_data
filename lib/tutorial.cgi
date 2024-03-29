#================================================
# ﾁｭｰﾄﾘｱﾙ
#================================================

# ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞの開始
sub start_tutorial {
	$m{tutorial_switch} = 1;
	&read_tutorial;
}

# ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞの終了
sub stop_tutorial {
	$m{tutorial_switch} = 0;
}

# ﾒｲﾝ画面に表示されるﾒｯｾｰｼﾞ
sub show_tutorial_message {
	my $message = shift;
	$mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ｸｴｽﾄ達成時に表示されるﾒｯｾｰｼﾞ
sub success_quest_mes {
	my $message = shift;
	$tutorial_mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ｸｴｽﾄ達成処理
sub success_quest_result {
	my $k = shift;
	unless ( ($tutorial_quests{$k}[3] eq 'egg_c' && $m{egg} eq '0') || ($tutorial_quests{$k}[3] eq 'wea_lv' && (!$m{wea} || $m{wea_lv} >= 30)) ) {
		$m{$tutorial_quests{$k}[3]} += $tutorial_quests{$k}[2];
	}

	if ($tutorial_quests{$k}[3] eq 'egg_c') {
		return " $tutorial_quests{$k}[2] の孵化値を貰いました";
	}
	elsif ($tutorial_quests{$k}[3] eq 'wea_lv') {
		return "武器を鍛えてもらいました";
	}
	elsif ($tutorial_quests{$k}[3] eq 'money') {
		return " $tutorial_quests{$k}[2] Gが届きました";
	}
	elsif ($tutorial_quests{$k}[3] eq 'coin') {
		return " $tutorial_quests{$k}[2] ｺｲﾝ貰いました";
	}
	elsif ($tutorial_quests{$k}[3] eq 'rank_exp') {
		return " $tutorial_quests{$k}[2] の貢献値を貰いました";
	}
	elsif ($tutorial_quests{$k}[3] eq 'medal') {
		return " $tutorial_quests{$k}[2] の勲章が送られました";
	}
}

# ｸｴｽﾄﾃﾞｰﾀ
%tutorial_quests = (
	#key								=>	[[0]No,	[1]回数,	[2]報酬処理,																					[3]ｸｴｽﾄ文,									[4]報酬,			[5]説明文
#	tutorial_to_country_1		=>	[0,		1,			sub{ my $i = 25; $m{egg_c} += $i if $m{egg}; return " $i の孵化値を貰いました"; },		'ﾈﾊﾞｰﾗﾝﾄﾞから国へ仕官してみよう',	'孵化値+25',	'国に所属することで給料が貰えたり統一戦に参加したりできます'],
	tutorial_bbsc_write_1		=>	[0,		1,			25 ,		'egg_c',		'ﾈﾊﾞﾗﾝ以外の作戦会議室で挨拶してみよう',	'孵化値+25',		'作戦を練ったり雑談したり質問できます'],
	tutorial_junk_shop_wea_1	=>	[1,		1,			3000,		'money',		'ｼﾞｬﾝｸｼｮｯﾌﾟで武器を買ってみよう',			'資金+3000',		'装備すると戦闘・戦争時の攻撃力が上がります'],
	tutorial_junk_shop_gua_1	=>	[2,		1,			3000,		'money',		'ｼﾞｬﾝｸｼｮｯﾌﾟで防具を買ってみよう',			'資金+3000',		'装備すると戦闘時の防御力が上がり、特殊効果が付きます'],
	tutorial_junk_shop_sell_1	=>	[3,		1,			3000,		'money',		'ｼﾞｬﾝｸｼｮｯﾌﾟに何かを売ってみよう',			'資金+3000',		'売ったものはｼﾞｬﾝｸｼｮｯﾌﾟに並び、誰かが買ってくれます'],
	tutorial_5000_gacha_1		=>	[4,		1,			5,			'rank_exp',	'5000ｶﾞﾁｬを回してみよう',						'貢献値+5',			'24時間に1回回せるので毎日回しましょう'],
	tutorial_bank_1				=>	[5,		1,			10,		'coin',		'銀行にお金を預けてみよう',					'ｺｲﾝ+10',			'毎年利子が貰えたり、討伐で負けても安心です'],
	tutorial_hunting_1			=>	[6,		1,			10,		'coin',		'討伐をしてみよう',				'ｺｲﾝ+10',			'討伐ではお金が貰え、卵を拾ったりすることもあります'],
	tutorial_highlow_1			=>	[7,		1,			1,			'wea_lv',	'ｶｼﾞﾉでﾊｲﾛｳをしてみよう',						'武器ﾚﾍﾞﾙ+1',		'貯めたｺｲﾝは役立つｱｲﾃﾑと交換できます'],
	tutorial_training_1			=>	[8,		1,			5000,		'money',		'修行をしてみよう',								'資金+5000',		'赤い相手と戦うと技を閃きやすいです'],
	tutorial_hospital_1			=>	[9,		1,			10000,	'money',		'黒十字病院で治癒して貰おう',					'所持金+10000',	'HP・MPの自動回復を待てない場合は病院で回復できます'],
	tutorial_breeder_1			=>	[10,		1,			20,		'coin',		'育て屋に卵を預けてみよう',					'ｺｲﾝ+20',			'預けた卵は10分毎に孵化値が +1 されます'],
	tutorial_full_act_1			=>	[11,		1,			25,		'egg_c',		'疲労度を 100 %以上にしてみよう',			'孵化値+25',		'疲労が 100 %を超えると内政以外の行動が制限されます'],
	tutorial_dom_1					=>	[12,		1,			10000,	'money',		'内政をしてみよう',								'所持金+10000',	'溜まった疲労を回復しつつ物資を増やすことができます'],
	tutorial_mil_1					=>	[13,		1,			5,			'rank_exp',	'奪軍事をしてみよう',							'貢献値+5',			'物資を奪うことで敵国を妨害しながら物資を増やせます'],
	tutorial_gikei_1				=>	[14,		1,			10,		'coin',		'偽計をしてみよう',								'ｺｲﾝ+10',			'敵国の同盟を無効にしたり、交戦させやすくなります'],
	tutorial_promise1_1			=>	[15,		1,			10000,	'money',		'友好条約を結んでみよう',						'所持金+10000',	'同盟を維持したり、交戦を防ぐことができます'],
	tutorial_mil_ambush_1		=>	[16,		1,			10,		'coin',		'軍事待ち伏せをしてみよう',					'ｺｲﾝ+10',			'効果が長く続くので寝る前などに仕掛けておきましょう'],
	tutorial_promise2_1			=>	[17,		1,			30000,	'money',		'停戦条約を結んでみよう',						'所持金+30000',	'交戦状態を解除することで一方的に攻められるという状況を防げます'],
	tutorial_ceo_1					=>	[18,		1,			1,			'medal',		'君主に立候補してみよう',						'勲章+1',			'君主になると専用ｺﾏﾝﾄﾞが解放されたり、各種行動に補正が付きます'],
	tutorial_job_change_1		=>	[19,		1,			20000,	'money',		'<a href="http://www43.atwiki.jp/bjkurobutasaba/pages/695.html">職業</a>を変えてみよう',			'所持金+20000',		'軍師や踊り子が一般的なようです'],
	tutorial_lv_20_1				=>	[20,		1,			30000,	'money',		'ﾚﾍﾞﾙを 20 にしよう',							'所持金+30000',	'Lv.20になると結婚できるようになります'],
	tutorial_mariage_1			=>	[21,		1,			30,		'coin',		'結婚相談所に登録してみよう',					'貢献値+30',		'結婚すると転生時のステ減少を抑えたり、相手の技を習得できます'],
);

# ｽﾀﾝﾌﾟ数
# ｸｴｽﾄﾃﾞｰﾀに含めるとｸｴｽﾄ数が変動した時に書き換えないとだから分けて自動化
$tutorial_quest_stamps = keys(%tutorial_quests);

# ｽﾀﾝﾌﾟﾃﾞｰﾀ
@tutorial_stamps = (
	#[0]No,	[1]数,	[2]報酬処理,																							[3]報酬
	[0,		3,			sub{ &send_item($m{name}, 2, 51, 0, 0, 1); return "ﾋﾞｷﾞﾅｰｴｯｸﾞを貰いました"; },	'ﾋﾞｷﾞﾅｰｴｯｸﾞ'],
	[1,		6,			sub{ my $i = 5000; $m{money} += $i; return " $i Gが届きました"; },					'資金+5000'],
	[2,		9,			sub{ &send_item($m{name}, 2, 25, 0, 0, 1); return "ｸﾘｽﾀﾙｴｯｸﾞを貰いました"; },		'ｸﾘｽﾀﾙｴｯｸﾞ'],
	[3,		12,		sub{ &send_item($m{name}, 2, 1, 0, 0, 1); return "ﾗﾝﾀﾞﾑｴｯｸﾞを貰いました"; },		'ﾗﾝﾀﾞﾑｴｯｸﾞ'],
	[4,		16,		sub{ my $i = 10000; $m{coin} += $i; return " $i ｺｲﾝ貰いました"; },					'ｺｲﾝ+10000'],
	[5,		19,		sub{ &send_item($m{name}, 2, 19, 0, 0, 1); return "ｽｰﾊﾟｰｴｯｸﾞを貰いました"; },		'ｽｰﾊﾟｰｴｯｸﾞ'],
	[6,		22,		sub{ &send_item($m{name}, 2, 33, 0, 0, 1); return "ｳｪﾎﾟﾝｴｯｸﾞを貰いました"; },		'ｳｪﾎﾟﾝｴｯｸﾞ'],
);

=pod
# ｸｴｽﾄ達成に関する行動の成功時に呼び出すと判定や達成処理などをやってくれる
# 引数にはｸｴｽﾄｷｰを配列で渡す
sub run_tutorial_quest {
	my @ks = @_;

	for my $k (@ks) {
		++$m{$k};
		if ($m{$k} eq $tutorial_quests{$k}[1]) {
			my $str = "報酬として" . &{$tutorial_quests{$k}[2]};
			&success_quest_mes("ｸｴｽﾄ「$tutorial_quests{$k}[3]」を達成しました！<br>$str<br><br>$tutorial_quests{$k}[5]");
			++$m{tutorial_quest_stamp_c};
		}
	}

	# ｽﾀﾝﾌﾟｺﾝﾌﾟﾘｰﾄ
	if ($m{tutorial_quest_stamp_c} eq $tutorial_quest_stamps) {
		&success_quest_mes("すべてのｽﾀﾝﾌﾟを集めました！");
	}
}
=cut

# ﾕｰｻﾞｰのﾁｭｰﾄﾘｱﾙﾃﾞｰﾀの読み込み
sub read_tutorial {
#	&write_tutorial unless -f "$userdir/$id/tutorial.cgi"; # 初期化

	open my $fh, "< $userdir/$id/tutorial.cgi" or &error("ﾁｭｰﾄﾘｱﾙﾌｧｲﾙが存在しません");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$m{$k} = $v; # $s
	}
}

# ﾕｰｻﾞｰのﾁｭｰﾄﾘｱﾙﾃﾞｰﾀの書き込み
sub write_tutorial {
	my $line = "tutorial_quest_stamp_c;$m{tutorial_quest_stamp_c}<>"; # ｽﾀﾝﾌﾟはｸｴｽﾄﾃﾞｰﾀに内包されてないので予め定義

	foreach my $k (keys(%tutorial_quests)) {
		$line .= "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/tutorial.cgi";
	print $fh "$line\n";
	close $fh;
}

# ｸｴｽﾄの達成状態の表示
sub show_stamps {
	&read_tutorial unless $m{tutorial_switch}; # ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞ切っててもｽﾀﾝﾌﾟ帳は見れるように

	$layout = 2;
	my $comp_par = int($m{tutorial_quest_stamp_c} / $tutorial_quest_stamps * 100);
	$mes .= "ｽﾀﾝﾌﾟ帳 《ｺﾝﾌﾟ率 $comp_par%》<br>";

 	$mes .= $is_mobile ? '<hr>番号 / 達成 / ｸｴｽﾄ / 報酬'
 		:qq|<table class="table1" cellpadding="3"><tr><th>番号</th><th>達成</th><th>ｸｴｽﾄ</th><th>報酬</th></tr>|;

	my @list = (); # ｸｴｽﾄﾃﾞｰﾀがﾊｯｼｭで順不同なため、表示用にｿｰﾄする
	$#list = $tutorial_quest_stamps - 1;
	foreach my $k (keys(%tutorial_quests)) {
		my ($no, $result, $quest, $str, $sub_str) = ($tutorial_quests{$k}[0]+1, '', '', '', '');
		if ($m{$k} >= $tutorial_quests{$k}[1]) {
			$result = '○';
			$quest = "<s>$tutorial_quests{$k}[4]</s>";
			$sub_str = $is_mobile ? "<br>$tutorial_quests{$k}[6]"
				: qq|<tr><td colspan="4">$tutorial_quests{$k}[6]</td></tr>|;
		}
		else {
			$result = '×';
			$quest = "$tutorial_quests{$k}[4]";
		}
	 	$str = $is_mobile ? qq|<hr>$no / $result / $quest / $tutorial_quests{$k}[5]|
	 		: qq|<tr><td align="right">$no</td><td align="center">$result</td><td>$quest</td><td>$tutorial_quests{$k}[5]</td></tr>|;
		splice(@list, $tutorial_quests{$k}[0], 1, $str.$sub_str);
	}

	for my $i (0 .. $#list) {
		$mes .= "$list[$i]";
	}

 	$mes .= qq|</table>| unless $is_mobile;

	$mes .= "<p>ｽﾀﾝﾌﾟ報酬</p>";
 	$mes .= $is_mobile ? '<hr>番号 / 達成 / ｽﾀﾝﾌﾟ数 / 報酬'
 		:qq|<table class="table1" cellpadding="3"><tr><th>番号</th><th>達成</th><th>ｽﾀﾝﾌﾟ数</th><th>報酬</th></tr>|;

	my $no = 0;
	if ($is_mobile) {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '○' : '×';
		 	$mes .= "<hr>$result / $tutorial_stamps[$i][1] / $tutorial_stamps[$i][3]";
		}
	}
	else {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '○' : '×';
		 	$mes .= qq|<tr><td align="right">$no</td><td align="center">$result</td><td align="right">$tutorial_stamps[$i][1]</td><td>$tutorial_stamps[$i][3]</td></tr>|;
		}
	}

 	$mes .= qq|</table>| unless $is_mobile;
}

# 未達成な序盤のｸｴｽﾄを表示
sub show_quest {
	my $str = '';
	my $min = $tutorial_quest_stamps;
	foreach my $k (keys(%tutorial_quests)) {
		if ($m{$k} < $tutorial_quests{$k}[1] && $tutorial_quests{$k}[0] < $min) {
			$min = $tutorial_quests{$k}[0];
			$str = $tutorial_quests{$k}[4];
		}
	}

	return $str;
}

1; # 削除不可
