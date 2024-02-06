require "./lib/greeting_card_lot.cgi";
#================================================
#年賀状抽選確認所
#================================================
#greeting_card_lot.cgiでも配置したけど動かなかったのでこっちにも置く
my @lot_grade_money = (2000000,1000000,300000,50000);

#1から4等までの各賞の下n桁(下n桁が一致すると当選判定)
my @lot_last_n_digit = (5,3,2,1);

#福袋 ランダム選択のペットが出現する確率 1/$per_rand_pet
my $per_rand_pet = 10;
#福袋 入れるペットの数
my $sale_pet_num = 3;

#================================================
sub begin {
	if ($m{tp} > 1) {
#		$mes .= '<br>';
		$m{tp} = 1;
		$mes .= '年賀はがきの当選確認<br>';
	}
	else {
		$mes .= '年賀はがきの当選確認<br>';
		$mes .= '当たってるといいね<br>';
	}
	@menus = ('やめる','福袋販売');
	if(&on_new_year_end){#年賀状くじ
		push @menus, '当選確認をする';
		push @menus, '換金する';
	}
	&menu(@menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		$mes .= "既に景品をもらっています<br>";
		&begin;
		return;
	}
	if($cmd eq 1) {
		$mes .= "新春福袋市!<br>一つ12万Gで3つ入りのペットを買えるよ";
		&menu('やめる', '購入する');
		return;
	}elsif ($cmd eq 2) {
		open my $fh, "> $userdir/$id/greeting_card_switch.cgi" or &error("そのような$userdir/$id/greeting_card_switch.cgiが開けません");
#		my $ii = @lot_last_n_digit;
		for my $i (1..($#lot_last_n_digit + 1)){
			my $won_sum_newyear = 0;
			$won_sum_newyear = &lot_show($i);
#			$mes .= "$i<br>";
			$mes .= "$i等に$won_sum_newyear回当選しました！<br>";
			my $time_next = $time + 3600 * 24 * 364;
			print $fh "$i<>$won_sum_newyear<>\n";
		}
		close $fh;

		open my $fh, ">> $userdir/$id/is_get_greeting_card.cgi"or &error("$userdir/$id/is_get_greeting_card.cgiが開けません");
		close $fh;#当選確認を押したかどうか判定するファイル作成

		&begin;
	}elsif($cmd eq 3){
		$mes .= '手持ち資金が溢れないよう注意しましょう<br>';
		$mes .= "はがきを換金しますか？<br>";
		$mes .= '1等:300万G<br>2等:100万G<br>3等:30万G<br>4等:5万G<br>';
		&menu('やめる', '換金');
	}else{
		&begin;
	}
}
#================================================
#福袋販売(pet_sale)
#================================================
#ファイル名
#userdir/$id/is_pet_sale.cgi,logdir/december_pet_sale.cgi
sub tp_100 {
	return if &is_ng_cmd(1);
	if(!-f "$logdir/december_pet_sale.cgi"){
		$mes .= "完売しました<br>";
		$mes .= "今年もよろしくお願いいたします<br>";
		&begin;
		return;
	}
	if(!-f "$userdir/$id/is_pet_sale.cgi"){#ファイルが存在しない場合
		open my $fh, "> $userdir/$id/is_pet_sale.cgi" or &error("$userdir/$id/is_pet_sale.cgiが作成できません");
		print $fh 0;
		close $fh;
	}
	open my $fh, "< $userdir/$id/is_pet_sale.cgi" or &error("そのような$userdir/$id/is_pet_sale.cgiが存在しません");
	my $head_line = <$fh>;
	my ($last_time) = split /<>/, $head_line;
	close $fh;

	if (&time_to_date($time) ne &time_to_date($last_time)) {#日を跨いでいた時
		my $rand_pet = int(rand($per_rand_pet));#ランダムペット出現判定
		my @sale_pets = ();#福袋のペット(ペットNo)
		#===========================================
		my $pets_count = 0;#処理中の福袋内のペット数 $#sale_petsの挙動が怖いので分離
		if($rand_pet eq 0){#ランダムペットが出現する時
			my $i = int(rand($#pets));
			push @sale_pets,$i;#send_item用にpush
			$pets_count++;
		}
		#===========================================
		my $count = 0;
		my @new_line = ();
		open my $fh, "< $logdir/december_pet_sale.cgi" or &error("そのような$logdir/december_pet_sale.cgiが存在しません");
		while(my $line = <$fh>){
			push @new_line,$line;
			$count++;
		}
		close $fh;
		#===========================================
		my $new_sale_pet_num = $sale_pet_num - $pets_count;#ランダムで追加したペット数を差し引き
		for my $i(1..$new_sale_pet_num){#既存のdecember_pet_saleから取り出し
			my $s_pet_no = int(rand($count));#line取り出し
			my ($name, $kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line[$s_pet_no];#ペットno取得
			push @sale_pets,$item_no;#send_item用に$item_noをpush
			splice(@new_line,$s_pet_no,1);#new_lineから取り出したlineを削除
			$count--;
		}
		#december_pet_sale.cgi更新=====================
		open my $fh, "> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgiを作成できません");
		print $fh @new_line;
		close $fh;
		if($#new_line < 2){#ペットがなくなった時(2個以下の時)
			unlink "$logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgiを削除することができません");
		}
		#send_item===================================
		for my $s_pet(@sale_pets){
			#my($send_name, $kind, $item_no, $item_c, $item_lv) = @_;
			&send_item($m{name}, 3, $s_pet, 0, 0, 1);
		}

		$m{money} -= 120000;
		$mes .= "福袋を購入しました!<br>";
		$mes .= "購入したペットは預かり所に送られました<br>";
		#is_pet_sale.cgi(userデータ)にlast_timeの書き込み===============
		open my $fh, "> $userdir/$id/is_pet_sale.cgi" or &error("$userdir/$id/is_pet_sale.cgiを作成できません");
		print $fh "$time<>\n";
		close $fh;
	}else{
		$mes .= "1日1個まで購入できます<br>";
		&begin;
		return;
	}
	#time_to_dateを利用して判定
	#randでペットを入れるどうか選択　以下入れない処理
	#ランダムに選択
	#選択したものをsend用にpush、それ以外を書き込み用にpush,(一応akindo処理をチェックして最適化)
	#send_item3回
	#is_pet_sale.cgiを作成
	&begin;
	return;
}
#================================================
#年賀状景品受け取り
#================================================
sub tp_300 {
	return if &is_ng_cmd(1);
	unless(-f "$userdir/$id/is_get_greeting_card.cgi"){
		$mes .= "まず当選確認する必要があります<br>";
		&begin;
		return;
	}
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		$mes .= "既に景品をもらっています<br>";
		&begin;
		return;
	}#一応ここにも配置
	my $count_no_lot = 0;#当選しなかった回数をカウント
	open my $fh, "< $userdir/$id/greeting_card_switch.cgi" or &error("そのような$userdir/$id/greeting_card_switch.cgiが存在しません");
	while(my $line = <$fh>){
		my($prize_grade,$won_sum_newyear) = split /<>/, $line;
		my $money = $lot_grade_money[$prize_grade - 1] * $won_sum_newyear;
		$m{money} += $money;
		$mes .= "$prize_grade等の$money Gを受け取りました<br>";
		$count_no_lot++ if $money eq 0;
#		push @line_lotnum, "$yname<>$mname<>$newyear_lot_num<>\n";
#      push @line_lotnum, ($yname,$mname,$newyear_lot_num);
#		push @line_id, $yname;
	}
	close $fh;
	if($count_no_lot - 1 == $#lot_last_n_digit){#1回も当選しなかった人にﾈｵﾊｽﾞﾚかﾊｽﾞﾚ
		if(rand(2) == 0){
			&send_item($m{name}, 2, 53, 0, 0, 1);
		}else{
			&send_item($m{name}, 2, 53, 0, 0, 1);
		}
		$mes .= "参加賞を受け取りました<br>";
	}
	#ファイルを作り2回以上景品を貰わないようにする
	open my $fh, ">> $userdir/$id/is_on_greeting_card.cgi"or &error("$userdir/$id/is_on_greeting_card.cgiが開けません");
	close $fh;

	unlink "$userdir/$id/is_get_greeting_card.cgi" or &error("$userdir/$id/is_get_greeting_card.cgiﾌｧｲﾙを削除することができません");
	&begin;
}

1;#削除不可
