#================================================
# 年末イベント
#=================================================

# 年末売出
@shop_list = (
#    cmd, 商品, 金額
	[1, '年越しそば', 10000],
);

# 靴下、年賀状を買う値段
my $buy_price  = 500;

# 年末売出 ペット売却額
my $sell_pet_price = 30000;

#同じ人から同じ人あての年賀状の枚数上限
my $no_duplicate_num = 5;

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= 'メリー天皇誕生日<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'よい年越しを<br>';
	}

	&menu('やめる','靴下を買う','年賀状を送る','年末市');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;

	if ($cmd eq '1') {
		if(&on_december_end) {
			$mes .= 'クリスマスはまた来年<br>';
			&begin;
			return;
		}
		$mes .= "靴下買うか?<br>片方しかないから $buy_price Gでやる<br>";
		&menu('やめる','買う');
	}elsif ($cmd eq '2') {
		$mes .= "おどしたまつき $buy_price Gで送る<br>";
		&menu('やめる', '送る');
	}elsif ($cmd eq '3') {
		$mes .= "年末限定!<br>";
		if(&on_december_end) {
			&menu('やめる', '売る', '買う');
		}else{
			&menu('やめる', '売る');
		}
	#		if(!&on_december_end) {
	#			$mes .= 'ｸﾘｽﾏｽ後まで準備中みたい・・・<br>';
	#			&begin;
	#			return;
	#		}
	}else{
		&begin;
	}
}

#=================================================
# 靴下
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);

	if ($m{money} < $buy_price) {
		$mes .= 'お前貧乏。かわいそうだからやる。片方しかないけどな。<br>';
	}
	else {
		$m{money} -= $buy_price;
	}
	if ($m{sox_kind}) {
		$mes .= 'もう靴下は用意してあるけど別のと取り替えよう<br>';
	}
	$mes .= '靴下にどんな願い入れようか';

	$m{tp} += 10;
	&menu('受胎告知', 'ﾘﾌｫｰﾑ', 'あの絵が欲しい', 'かっこいい武器が欲しい');
}

sub tp_110 {
	if ($cmd eq '0') {#受胎告知
		$m{sox_kind} = 10;
		$m{sox_no} = 183;
		&begin;
	} elsif ($cmd eq '1') {#ﾘﾌｫｰﾑ
		if (rand(10) < 1) {
			$m{sox_kind} = 20;
			$m{sox_no} = 168;
		} else {
			$m{sox_kind} = 50;
			$m{sox_no} = 191;
		}
		&begin;
	} elsif ($cmd eq '2') {#あの絵が欲しい
		$mes .= 'どの絵が欲しい？';
		$m{tp} += 10;
		&menu('ｺﾝﾃｽﾄ', '他の人の顔絵');
	} else {#かっこいい武器が欲しい
		if (rand(10) < 1) {
			$m{sox_kind} = 40;
			$m{sox_no} = 21;
			&begin;
		} else {
			$m{sox_kind} = 50;
			$m{sox_no} = 191;
			&begin;
		}
	}
}
sub tp_120{
	if ($cmd eq '0') {
		&seek_from_contest;
		$m{tp} += 10;
	}	elsif ($cmd eq '1') {
		&begin;
	}else{
		&begin;
	}
}
sub tp_130{
	$m{sox_kind} = 30;
	$m{sox_no} = 191;
	$m{sox_picture} = $in{file_name};#ファイル名を靴下の中身にする
	$mes .= "サンタさんにお願いしました！<br>";
	&begin;
}
#=================================================
# 年賀状
#=================================================
sub tp_200 {
	return if &is_ng_cmd(1);
	$mes .= "誰に年賀状を送りますか?<br>";
	$mes .= "裏面は印刷済みなので書く必要はないよ?<br>";

	$mes .= qq|<form method="$method" action="$script"><p>宛名：<input type="text" name="to_name" class="text_box1"></p>|;
	$mes .= qq|<p>送り主：<input type="text" name="from_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">送る<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="送る" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_210 {
	return if &is_ng_cmd(1);

	if ($m{money} < $buy_price) {
		$mes .= 'はがき代足りない。帰れ。<br>';
	}
	elsif($in{to_name} eq $m{name}){
		$mes .= '自分に送ることはできません<br>';
	}
	else {
		my $to_id = unpack 'H*', $in{to_name};
		unless(-f "$userdir/$to_id/greeting_card.cgi"){
			open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("ポストが開けません");
			close $fh;
		}
		my $count_for_duplicate = 0;#同じ人からの手紙は5通まで
		open my $fh2, "< $userdir/$to_id/greeting_card.cgi" or &error("ポストが開けません");
		while(my $lines = <$fh2>){
			my($from_name_g,$id_g,$number_g) = split /<>/, $lines;
			$count_for_duplicate++ if $id_g eq $id;
		}
		close $fh;
		if ($no_duplicate_num < $count_for_duplicate) {
			$mes .= "同じ人に$no_duplicate_num枚より多く年賀状は送れません<br>";
			&begin;
			return;
		}
		$m{money} -= $buy_price;
		my $number = int(rand(1000000000));
		open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("ポストが開けません");
		print $fh "$in{from_name}<>$id<>$number<>\n";
		close $fh;
	}
	&begin;
}
sub seek_from_contest{
	#無駄な処理が入っていると思うのでおいおい修正したいby青海苔
	my $this_file      = "$userdir/$id/shop_$goods_dir.cgi";
	my $this_path_dir  = "$userdir/$id/$goods_dir";
	my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
	$layout = 2;
	my $count = 0;
	my $sub_mes .= qq|<form method="$method" action="$script"><hr><input type="radio" name="file_name" value="0" checked>やめる|;
	require "$datadir/contest.cgi";
	open my $fh, "< $logdir/legend/picture.cgi" or &error("$logdir/legend/picture.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($round, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
		$sub_mes .= qq|<hr><img src="$logdir/legend/picture/$file_name" style="vertical-align:middle;"> 第$round回$contests[$in{no}][0]優秀作品『$file_title』作: $name|;
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">|;
	}
	close $fh;
	$mes .= qq|究極の美<br>|;
	$mes .= qq|$sub_mes<hr>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ｻﾝﾀさんにお願い" class="button1"></p></form>|;

}


#=================================================
# 年末売出
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..2);

	if($cmd eq 1){
		$mes .= "持っているﾍﾟｯﾄを $sell_pet_price Gで売ることができるよ<br>";
		$mes .= 'どうする?';
		$m{tp} += 20;
		&menu('やめる', '売る');
	}elsif($cmd eq 2){
		$layout = 1;
		$mes .= '何買おっか？<br>';

		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= $is_mobile ? qq|<hr>商品/金額<br>|
			: qq|<table class="table1" cellpadding="3"><tr><th>商品</th><th>金額<br></th>|;

		for my $shop_ref (@shop_list) {
			my @shop = @$shop_ref;
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$shop[0]">$shop[1]/$shop[2] G<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$shop[0]">$shop[1]</td><td align="right">$shop[2] G<br></td></tr>|;
		}

		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="買う" class="button1"></p></form>|;

		$m{tp} += 10;
	}
}

sub tp_310{

	if($cmd eq 1){
		if ($m{money} >= $money && !-f "$userdir/$id/december_soba.cgi") {
			$m{money} -= $money;
			$m{hp} = $m{max_hp};
			$m{mp} = $m{max_mp};
			$m{act} -= 15;

			#ファイル作成
			open my $fh, "> $userdir/$id/december_soba.cgi" or &error("$userdir/$id/december_soba.cgiﾌｧｲﾙが読み込めません");
			close $fh;
			$mes .= 'hpとmpが全回復しました<br>';
			$mes .= '疲労度が少し回復しました<br>';
			$mes .= '毎度あり！来年もよろしくな！<br>';
		}elsif(-f "$userdir/$id/december_soba.cgi"){
			$mes .= '年越しは1回で十分だぜ！！<br>';
		}else{
			$mes .= 'よく見てみろ！　ゼニが足りねぇぜ！！<br>';
		}
	}else{
		$mes .= 'やめました<br>';
	}
	&begin;
	return;
}

sub tp_320{
	return if &is_ng_cmd(1);

	if($cmd eq 1){
		if($m{pet} > 0){
			$m{money} += $sell_pet_price;

			$mes .= "$pets[$m{pet}][1]★$m{pet_c}を売りました<br>";
			#ファイル作成処理、削除処理はgreeting_card_lot.cgiのlot_delete関数に埋め込みする===============================
			if(!-f "$logdir/december_pet_sale.cgi"){
				open my $fh, "> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgiが開けません");
				close $fh;
			}
			#=================
			open my $fh, ">> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgiが開けません");
			print $fh "$m{name}<>3<>$m{pet}<>$m{pet_c}<>0<>\n";#3というのは道具の種類(petは3)を表すもの　0はitem_lv 今後武器や卵を売ることを想定
			close $fh;
			$m{pet} = 0;
			$m{pet_c} = 0;

			#=================
		}else{
			$mes .= "ﾍﾟｯﾄを持っていません<br>";
		}
	}else{
		$mes .= 'やめました<br>';
	}
	&begin;
	return;
}
1; # 削除不可
