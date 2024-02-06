require 'config.cgi';
require 'config_game.cgi';

#===================================================
#年賀はがき抽選会(1/20,22:00より)メイン処理 created by あおのり
#===================================================
@message_newyear_lot = (
"皆様、お集まり頂きありがとうございます。これよりお年玉付き年賀はがき抽選会を行います",
"この大会は",#lot_system内に続きを埋め込み
"1等は下5桁、2等は下3桁、3等は下2桁、4等は下1桁の一致で当選となります",
"また各賞の景品は、1等200万G、2等100万G、3等30万G、4等5万Gとなっております",
"それではプレイヤーの皆様、& eventを入力し、お手元にあるダイスをお振りくださいませ",
"集計処理中...",
"$m{name}はダイスを振った！$prize_grade等賞の抽選番号は、下5桁",#lot_system内に続きを埋め込み
"$m{name}はダイスを振った！$prize_grade等賞の抽選番号は、下3桁",#lot_system内に続きを埋め込み
"$m{name}はダイスを振った！$prize_grade等賞の抽選番号は、下2桁",#lot_system内に続きを埋め込み
"$m{name}はダイスを振った！$prize_grade等賞の抽選番号は、下1桁",#lot_system内に続きを埋め込み
"全ての番号が出揃いました！当選した方には豪華プレゼントを贈呈いたします！",
"なお、今回惜しくも当選を逃してしまった方々にも景品をご用意しておりますので、ご安心ください",
"これにて当抽選会を終了とさせていただきます。今年も当鯖をご愛顧の程よろしくお願いします。"
);

#各等の賞金額　shopping_greeting_card_lotcheck.cgiにも同様の配列があるので変更するときはそっちも
my @lot_grade_money = (2000000,1000000,300000,50000);

#lot_system連続更新禁止時間
my $bad_time_newyearlot = 15;

#1から4等までの各賞の下n桁(下n桁が一致すると当選判定)
my @lot_last_n_digit = (5,3,2,1);
#my $lot_last_n_digit_num = 4;
#my $lot_first_lastdigit = 6;
#my $lot_second_lastdigit = 4;
#my $lot_third_lastdigit = 3;
#my $lot_fourth_lastdigit = 2;

#1から4等までの番号の数
my $lot_first = 1;
my $lot_second = 2;
my $lot_third = 3;
my $lot_fourth = 2;

#以下message_newyear_lot(イベントメッセージ表示)、数字を動かす場合は位置に注意、1スタートなので注意
my $lotsys_sponsorship = 2;#スポンサーの表示タイミング
my $lotsys_gather = 6;#どのタイミングで集計するか
my $lotsys_reveal_start = 7;#発表開始
my $lotsys_reveal_end = 11;#発表終了

# lot_sponsorshipで使用、
my @files = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名(shop_list_xxxx←の部分)'],
	['商人のお店',	'',			'個'],
	['美の画伯館',	'picture',	'枚'],
	['ﾌﾞｯｸﾏｰｹｯﾄ',	'book',		'冊'],
	['商人の銀行',	'bank',		'回'],
);

sub lot_reveal{#lot_systemで番号を発表する時に使用
  my($prize_grade) = @_;
  my @prize_number = ();
  open my $fh, "< $logdir/greeting_card_summary.cgi" or &error("そのような$userdir/$id/greeting_card_summary.cgiが存在しません");
  my($time, $time_next) = split /<>/, $head_line;
  while(my $line = <$fh>){
    my($no,$yname,$mname,$newyear_lot_num) = split /<>/, $line;
    if($no eq $prize_grade){
      push @prize_number, $newyear_lot_num;
#      next;
    }
  }

  close $fh;
  return \@prize_number;
}

sub lot_show{#引数、順位、返り値n等の当選回数
  my($prize_grade) = @_;
#@
  my $won_lot = 0;#当選回数
#  my $i = 0;
  my @lot_f_show = ();
#  my @lot_s_show = ();
#  my @lot_t_show = ();
#  my @lot_fo_show = ();
  open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("そのような$userdir/$id/greeting_card.cgiが存在しません");
  while(my $line = <$fh>){
    my($mname,$yname,$newyear_lot_num) = split /<>/, $line;
    push @lot_f_show, &lot_calculate($newyear_lot_num,$lot_last_n_digit[$prize_grade - 1]);
#    push @lot_s_show, &lot_calculate($lot_f_show[i],4);
#    push @lot_t_show, &lot_calculate($lot_s_show[i],3);
#    push @lot_fo_show, &lot_calculate($lot_t_show[i],2);
  }
  close $fh;

  open my $fh, "< $logdir/greeting_card_summary.cgi" or &error("そのような$logdir/greeting_card_summary.cgiが存在しません");
  my($time, $time_next) = split /<>/, $head_line;
  while(my $line = <$fh>){
    my($no,$yname,$mname,$newyear_lot_num) = split /<>/, $line;
    for my $i (0..$#lot_f_show){
      if($no eq $prize_grade && $lot_f_show[$i] eq $newyear_lot_num){
        $won_lot++;
      }
    }
  }
  close $fh;
  return $won_lot;
  #main.cgiなどで当選確認をするときの処理、

}

sub lot_main{#当選番号を決定する処理
  my @A = ();#あとでファイルに貼り付ける中身
  my @line_lotnum = ();#各userの抽選番号を入れる
  my @line_id = ();#当選者重複防止用のidリスト
  opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;

    my %m = &get_you_datas($id, 1);

    unless (-f "$userdir/$id/greeting_card.cgi") {
      open my $fh, "> $userdir/$id/greeting_card.cgi";
      close $fh;
    }
    open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("そのような$userdir/$id/greeting_card.cgiが存在しません");
    while(my $line = <$fh>){
      my($mname,$yname,$newyear_lot_num) = split /<>/, $line;
      push @line_lotnum, "$yname<>$mname<>$newyear_lot_num<>\n";
      push @line_id, $yname;
    }
    close $fh;
    close $dh;

  }
  my $lot_fnum = 0;
  my $lot_snum = 0;
  my $lot_tnum = 0;
  my $lot_fonum = 0;

  open my $fh, "> $logdir/greeting_card_summary.cgi" or &error("そのような$userdir/$id/greeting_card_summary.cgiが存在しません");
  my $time_next = $time + 3600 * 24 * 364;

  print $fh "$time<>$time_next<>\n";

  for my $i (0..$lot_first-1){
    my $p_n = $lot_fnum;#重複防止用
    $lot_fnum = rand($#line_lotnum);
    if($line_id[$p_n] eq $line_id[$lot_fnum] && i != 0){#選出し直し
      $lot_fnum = rand($#line_lotnum);
    }
    my($mname,$yname,$newyear_lot_num) = split /<>/, $line_lotnum[$lot_fnum];
    $newyear_lot_num = &lot_calculate($newyear_lot_num,$lot_last_n_digit[0]);
    print $fh "1<>$mname<>$yname<>$newyear_lot_num<>\n";
  }

  for my $i (0..$lot_second-1){
    my $p_n = $lot_snum;#重複防止用
    $lot_snum = rand($#line_lotnum);
    if($line_id[$p_n] eq $line_id[$lot_snum] && i != 0){#選出し直し
      $lot_snum = rand($#line_lotnum);
    }
    my($mname,$yname,$newyear_lot_num) = split /<>/, $line_lotnum[$lot_snum];
    $newyear_lot_num = &lot_calculate($newyear_lot_num,$lot_last_n_digit[1]);
    print $fh "2<>$mname<>$yname<>$newyear_lot_num<>\n";
  }

  $lot_snum = int(rand(10 ** $lot_last_n_digit[1]));
  print $fh "2<>random_parameter<>0<>$lot_snum<>\n";

  for my $i (0..$lot_third-1){
    $lot_tnum = int(rand(10 ** $lot_last_n_digit[2]));
    print $fh "3<>random_parameter<>0<>$lot_tnum<>\n";
  }
  for my $i (0..$lot_fourth-1){
    $lot_fonum = int(rand(10 ** $lot_last_n_digit[3]));
    print $fh "4<>random_parameter<>0<>$lot_fonum<>\n";
  }

  close $fh;
}

sub lot_system{#全体システム(抽選会の進行をする関数)、メッセージを_write_tag.cgiに返す
#$lotsys_newyear:0スタート前、1スタート
  my $lotsys_newyear = 0;
  my $time_next = 0;#lot_systemの更新連打防止用、次回の開催日の指定補助
  my $message_lot = "";

  open my $fh, "< $logdir/event_switch.cgi" or &error("そのような$logdir/event_switch.cgiが存在しません");
  while(my $line = <$fh>){
    my($time_next_r,$lotsys_newyear_r) = split /<>/, $line;
    $lotsys_newyear = $lotsys_newyear_r;
    $time_next = $time_next_r;
  }
  close $fh;

  if($time > $time_next && (&on_new_year_end || &on_new_year_end_lot) && $lotsys_newyear eq 0){
    $lotsys_newyear = 1;#開始
		&write_world_news("<i>BJお年玉付き年賀はがき抽選会が開催されました！</i>");
  }
	if($time_next > $time && $lotsys_newyear ne 0){
		$message_lot = "少々お待ちください";
		return $message_lot;
	}
  if($lotsys_newyear){
    $message_lot = $message_newyear_lot[$lotsys_newyear - 1];
    if($lotsys_newyear eq $lotsys_sponsorship){#スポンサー(売り上げ1位)の表示
      @sponsors_sys = @{&lot_sponsorship()};
      my $length_lotsys = @sponsors_sys;
      for my $i (1..$length_lotsys){
        $message_lot .= $i == $length_lotsys ? "$sponsors_sys[$i - 1]" : "$sponsors_sys[$i - 1],";
      }
			$message_lot .="の提供でお送りしております";
    }
    if($lotsys_newyear eq $lotsys_gather){#集計処理
      &lot_main;
    }
    if($lotsys_newyear >= $lotsys_reveal_start && $lotsys_newyear < $lotsys_reveal_end){#当選番号を表示
			my $prize_grade_lotsys = $lotsys_newyear - $lotsys_gather;
      my @prize_number_w = @{&lot_reveal($prize_grade_lotsys)};
      my $length_lotsys = @prize_number_w;
			my $message_lotsys_world = "";
      for my $i (1..$length_lotsys){
#        $message_lot .= "$i,";
        $message_lot .= $i == $length_lotsys ? "$prize_number_w[$i - 1]！" : "$prize_number_w[$i - 1],";
				$message_lotsys_world .= "$prize_number_w[$i - 1],";
      }
			&write_send_news("$prize_grade_lotsys 等の当選番号,下$lot_last_n_digit[$prize_grade_lotsys - 1]桁$message_lotsys_world");
    }
    $lotsys_newyear++;
		$time_next = $time + 30;
    if($lotsys_newyear > $#message_newyear_lot + 1){#終了処理
			$time_next = $time + 3600 * 24 * 364;
      $lotsys_newyear = 0;
    }
  }else{
    $message_lot = "現在イベントは開催されていません";
  }

  open my $fh, "> $logdir/event_switch.cgi" or &error("そのような$logdir/event_switch.cgiが存在しません");
  print $fh "$time_next<>$lotsys_newyear<>\n";
  close $fh;

  return $message_lot;

}

sub lot_calculate{#桁と抽選番号を引数として、下n桁のみを返す、
  my($p_num_cal,$digit) = @_;
  $f = int($p_num_cal % (10 ** $digit));
  return $f;
}

sub lot_sponsorship{#売り上げ1位の店をスポンサーとして表示
  @sponsors = ();
  for my $i (0..$#files){
    my $type = $files[$i][1] ? "_$files[$i][1]" : '';
    my $this_file = "$logdir/shop_list${type}.cgi";
    open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
    my $line = <$fh>;
    my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
    push @sponsors, $shop_name;
    close $fh;
  }
  return \@sponsors;
}

sub lot_delete{#2/1に年賀状データなどを諸々削除、main.cgiに配置
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		unlink "$userdir/$id/is_on_greeting_card.cgi" or &error("$userdir/$id/is_on_greeting_card.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$userdir/$id/greeting_card.cgi"){
		unlink "$userdir/$id/greeting_card.cgi" or &error("$userdir/$id/greeting_card.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$userdir/$id/greeting_card_switch.cgi"){
		unlink "$userdir/$id/greeting_card_switch.cgi" or &error("$userdir/$id/greeting_card_switch.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$userdir/$id/is_get_greeting_card.cgi"){
		unlink "$userdir/$id/is_get_greeting_card.cgi" or &error("$userdir/$id/is_get_greeting_card.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$logdir/december_pet_sale.cgi"){
		unlink "$logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgiﾌｧｲﾙを削除することができません");
	}
	if(-f "$userdir/$id/december_soba.cgi"){
		unlink "$userdir/$id/december_soba.cgi" or &error("$userdir/$id/december_soba.cgiﾌｧｲﾙを削除することができません");
	}
}

1;#削除不可
