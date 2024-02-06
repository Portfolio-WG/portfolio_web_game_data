#boardgame_splend.cgi
#====================================
#keyword
#splend,
#jewel,

#====================================
#関連ファイル一覧

#./lib/boardgame_splend_test.cgi(本体)
#./lib/boardgame/splend_external(ゲーム開始終了処理(プレイヤーデータ作成除く)、ランキング更新、実績解除)
#./data/splend/splend_N.cgi(Nは番号、現在1)(ｶｰﾄﾞ全般、宝石、実績など定数全般)
#./html/splend/style_splend_N.css(ランキングのtablesorter,ｽﾃｰﾀｽのUI、画像canvasなど)

#====================================
my $this_file = "boradgame_splend.cgi";
my $user_file = "$userdir/$id/splend.cgi";#ユーザーデータ

$log_dir = "$logdir/splend";#excav,field_pointのファイル

$log_result_dir = "$logdir/splend_result";

$log_time_file = "$logdir/splend/splend_time.cgi";#時間処理管理のファイル,externalで使っているのでグローバル必須

my $data_file_name = "splend_2";

$icon_dir = "$icondir/splend/$data_file_name";#icon

my $data_file = "$datadir/splend/$data_file_name.cgi";#静的dataファイル
my $data_file_2 = "$datadir/splend_achieve/$data_file_name.cgi";#静的dataファイル(achieve類)
my $stylesheet_file = "$htmldir/splend/$data_file_name.css";
#↑ゲームを飽きさせないようステージ変更を加えるかもなので、後に動的参照にする可能性が高い
#logファイル
#ランキング
#log_dir/splend_rank_max_range, log_dir/splend_rank_win_point, log_dir/splend_rank_gold,
#====================================
#dataファイルのデータ
#====================================
#　!は使用中を表すため、位置を変更することはできない
require "$datadir/splend/$data_file_name.cgi";
#========================================================================
#ユーザーデータロード
%spl  = ();
&road_user_data;
#========================================================================
#終了後にハマる人対策
my $splned_game_state = &splend_open_time_file();
if($splned_game_state eq "end" && $m{tp} > 1 && $m{tp} < 1000){
  &begin;
}
#========================================================================
sub begin{

  $mes .= &next_time_display;

  #2023年秋イベ 緊急処理
  #$mes .= '<font size=-1 color="#ff9966">';
  #$mes .= '新ステージのテスト終わりました<br>';
  #$mes .= '11/1の19時から開始予定です<br>';
  #$mes .= 'ゲーム終了は11/30の18:59の予定です<br>';
  #$mes .= 'みんなで楽しもう！<br>';

  #$mes .= '<br>注:15日19時から一週間程度、新ステージのテストします<br>';
  #$mes .= 'ゲーム中に色々変更を加えたりするかもなのでご注意ください<br>';
  #$mes .= '本番の開始時期は10月下旬or11月頭になる予定です<br>';
  #$mes .= '本番の詳細な日時は後日お伝えします<br><br>';
  $mes .= '</font>';

  $mes .= '<font size="-1" color="#ff3333">';
  $mes .= 'バグ対応として、公平性のために一時的にストックが12まで溜め込めるようになりました<br>';
  $mes .= '11/23の10:00ごろに元の5に引き下げます<br>';
  $mes .= 'ご迷惑おかけして誠に申し訳ありませんでした<br>';
  $mes .= '</font>';


  if ($m{tp} > 1) {
    $mes .= '他に何する？<br>';
    $m{tp} = 1;
  }
  else {
    $mes .= '春イベ ボードゲーム<br>';
    $mes .= '何する？<br>';
  }

  &menu('やめる','宝石採集','ﾙｰﾙ説明','ｺﾚｸｼｮﾝﾙｰﾑ');
  return;
}

sub tp_1 {
  if($cmd eq 1){
    #時間取得==================
    #ｹﾞｰﾑ中はstart_timeが0,ｹﾞｰﾑ期間以外はend_timeが0となり、この判定に使用される
    my $splned_game_state = &splend_open_time_file();
    #開始判定処理,終了判定処理==================
    if($splned_game_state eq "start"){#ゲーム開始時
#    if(!-f "$log_dir/playfield_map.cgi"){#ゲーム開始時
      $mes .= "ｹﾞｰﾑﾌｨｰﾙﾄﾞを作成中<br>";
      require "boardgame_splend_external.cgi";
      &splend_init_data;#ｹﾞｰﾑﾌｨｰﾙﾄﾞ作成処理
      $mes .= "ｹﾞｰﾑ開始処理完了<br>";
      #ここ踏む時どうしても後の判定関数を通らなかったので追加
      $mes .= '初期ﾃﾞｰﾀを作成中<br>';
      &splend_init_player_data;#プレイヤーデータ作成処理
    }elsif($splned_game_state eq "end_func"){
      require "boardgame_splend_external.cgi";
      &splend_end_data;
      $mes .= 'ｹﾞｰﾑ終了処理完了<br>';
      $mes .= "ゲームは終了しました<br>";
      &begin;
      return;
    }elsif($splned_game_state eq "end"){
      $mes .= "ゲームは終了しました<br>";
      &begin;
      return;
    }
    #ここまで$spl{}を使用しないこと
    #====================================
    $mes .= "鯖のみんなでボードゲーム<br>";
    $mes .= "読み込み中<br>";
    #ユーザーデータ初期化==================
    if(!-f "$user_file"){#初プレイの時
      $mes .= '初期ﾃﾞｰﾀを作成中<br>';
      require "boardgame_splend_external.cgi";
      &splend_init_player_data;#プレイヤーデータ作成処理
    }
    #==================
    #playfield_excavをopen time_to_dateで更新

    #応急処置
    my @user_fields = split /,/, $spl{field_point};
    my $fields_num = @user_fields;
    if($fields_num < 10){
      my @new_user_fields = ();
      for my $i (0..$#fields){
        push @new_user_fields,0;
      }
      for my $i (0..$#user_fields){
        $new_user_fields[$i] = $user_fields[$i];
      }
      $spl{field_point} = join ",", @new_user_fields;
      $mes .= "領地ｶｰﾄﾞ修正処理完了<br>";
    }

    #==================================
    $mes .= &is_wait_time($spl{last_roadtime});
    &reload_wait;#前回の更新時間を参照し行動可能回数をﾘﾛｰﾄﾞ
    &write_user_data;
    $mes .= "reload_time = $spl{last_roadtime},road_count = $spl{road_count}";
    $m{tp} = $cmd * 100;
    &n_menu;
  }elsif($cmd >= 2){
    $m{tp} = $cmd * 1000;
    &{'tp_'. $m{tp} };
  }else{
    $mes .= "やめました";
    &begin;
  }
  return;
}

sub tp_100 {
  $mes .= "βテスト版<br>";#ここに表示を作成しておくこと
  $mes .= "何をしますか？<br>";
  $mes .= &splend_status_display;

  @menus = ('やめる','更新','宝石を得る','ﾀﾞｲｽを振る','購入する','勢力図確認','ﾗﾝｷﾝｸﾞ');
  &menu(@menus);
  $m{tp} += 10;
}

sub tp_110 {
  if($cmd eq 1){
    $m{tp} = 100;
    &tp_100;
    return;
  }elsif($cmd eq 2){
    return if &is_ngflag_spl($spl{jewel_flag});
    &n_menu;
    $mes .= qq|<form method="$method" action="$script">|;
    for my $i (1..$#jewels){
      $mes .= qq|<input type="radio" name="jewel1" value="$i">$jewels[$i][1]|;
    }
    $mes .= qq|<br>|;
    $mes .= qq|<form method="$method" action="$script">|;
    for my $i (1..$#jewels){
      $mes .= qq|<input type="radio" name="jewel2" value="$i">$jewels[$i][1]|;
    }
    $mes .= qq|<br>|;
    $mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
    $mes .= qq|<p><input type="submit" value="交換する" class="button1"></p></form>|;

    $m{tp} = 200;
    return;
#    &n_menu;
  }elsif($cmd eq 3){
    $mes .= "ダイス処理";
    $m{tp} = 300;
    &n_menu;
  }elsif($cmd eq 4){#宝石→採掘家,勝利点
    $mes .= "どれを選びますか?";
    &menu('やめる','採掘家ｶｰﾄﾞ','領地ｶｰﾄﾞ','ﾘｻﾞｰﾌﾞｶｰﾄﾞ');
    $m{tp} = 120;
    return;
  }elsif($cmd eq 5){
    $mes .= "他ﾌﾟﾚｲﾔｰの動向<br>";
    $m{tp} = 400;
    &tp_400;
  }elsif($cmd eq 6){
    $mes .= "勝利点ランキング<br>";
    $m{tp} = 600;
    &tp_600;
  }else{
    $mes .= "やめました<br>";
    &begin;
  }
  return;
}
#tpが足りない...(正直元のシステムが使いづらい..)
sub tp_120 {
  if(!$cmd){
    $mes .= "やめました";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  $layout = 2;
  $mes .= "どれを選びますか?<br>";
  $mes .= '赤:ﾙﾋﾞｰ,青:ｻﾌｧｲｱ,緑:ｴﾒﾗﾙﾄﾞ,黒:ｵﾆｷｽ,白:ﾀﾞｲﾔﾓﾝﾄﾞ<br>';
  $mes .= '1p = 勝利点1<br>';
  $mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
  my $count = 0;

  $mes .= &splend_status_jewel;

  if($cmd eq 1){
    $mes .= qq|<table class="table1"><tr><th>名</th><th>ﾗﾝｸ</th><th>効果</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;

    # !no,レア度,name,効果,交換条件
    open my $fh, "< $log_dir/playfield_excav.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
    while (my $line = <$fh>) {
      my($no,$rare,$name,$excav_effect,$excav_condition) = split /,/, $line;
      my @excav_jewel_condition = split /<>/, $excav_condition;
      $mes .= qq|<tr><td><label><input type="radio" name="cmd" value="$no"><font color="$gc">$name</font></label></td><td>$rare</td><td>$excav_effect</td>|;
      for my $jewel_needs (@excav_jewel_condition){
        $mes .= qq|<td>$jewel_needs</td>|;
      }
      $mes .= qq|</tr>|;
      $count++;
    }
    close $fh;
    #=======================
    #buyable_card_kind

    $mes .= qq|<tr><th>名</th><th>ﾗﾝｸ</th><th>効果</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;

    my @buyable_cards = split /,/, $spl{buyable_card_kind};
    $mes .= qq|@buyable_cards|;
    for my $buyable_card_(@buyable_cards){

      my @reserve_jewel_condition = split /<>/, $excavaters[$buyable_card_][5];
      $mes .= qq|<tr><td><label><input type="hidden" name="buyable_flag" value="1"><input type="radio" name="cmd" value="$excavaters[$buyable_card_][0]"><font color="$gc">$excavaters[$buyable_card_][2]</font></label></td><td>$excavaters[$buyable_card_][4]</td><td>$excavaters[$buyable_card_][3]</td>|;
      for my $jewel_needs (@reserve_jewel_condition){
        $mes .= qq|<td>$jewel_needs</td>|;
      }
      $mes .= qq|</tr>|;
    }

    $mes .= qq|<label><input type="checkbox" id="reserve" name="reserve" value="1">ﾘｻﾞｰﾌﾞする</label></form>|;
    $m{tp} = 130;
  }elsif($cmd eq 2){
    $mes .= qq|<table class="table1"><tr><th>名</th><th>効果</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;

    # !no,name,効果,交換条件
    open my $fh, "< $log_dir/playfield_field.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
    while (my $line = <$fh>) {
      my($no,$name,$excav_effect,$field_condition) = split /,/, $line;
      my @field_jewel_condition = split /<>/, $field_condition;
      $mes .= qq|<tr><td><label><input type="radio" name="cmd" value="$no"><font color="$gc">$name</font></label></td><td>$excav_effect</td>|;
      for my $jewel_needs (@field_jewel_condition){
        $mes .= qq|<td>$jewel_needs</td>|;
      }
      $mes .= qq|</tr>|;
      $count++;
    }
    close $fh;
    $m{tp} = 140;
  }elsif($cmd eq 3){
    $mes .= qq|ｶｰﾄﾞをﾘｻﾞｰﾌﾞする時は,購入する→採掘家ｶｰﾄﾞと押して,<br>「ﾘｻﾞｰﾌﾞする」にﾁｪｯｸを入れて購入ボタンを押してください|;
    $mes .= qq|<table class="table1"><tr><th>名</th><th>ﾗﾝｸ</th><th>効果</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;


    for my $user_reserves (split /,/, $spl{reserves}){
      my @reserve_jewel_condition = split /<>/, $excavaters[$user_reserves][5];

      $mes .= qq|<tr><td><label><input type="radio" name="cmd" value="$excavaters[$user_reserves][0]"><font color="$gc">$excavaters[$user_reserves][2]</font></label></td><td>$excavaters[$user_reserves][4]</td><td>$excavaters[$user_reserves][3]</td>|;
      for my $jewel_needs (@reserve_jewel_condition){
        $mes .= qq|<td>$jewel_needs</td>|;
      }
      $mes .= qq|</tr>|;
    }

    # !no,name,効果,交換条件
    $m{tp} = 150;
  }
  #$m{stock} = $count;
  $mes .= qq|</table>| unless $is_mobile;
  $mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
  $mes .= qq|<p><input type="submit" value="購入する" class="button1"></p></form>|;


  #=========================================
  return;
}
#カード(excav)の購入処理
sub tp_130 {
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#あとで直す
    $mes .= 'やめました<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #ファイル操作(open,取り出し選択,替え追加,close)
  #==========================================
  my $line = ''; # 買ったアイテム情報が入る
  my @lines = (); # その他の商品が入る
  my $flag = 0;
  open my $fh, "< $log_dir/playfield_excav.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
  eval { flock $fh, 2; };
  while (my $_line = <$fh>) {
    if (index($_line, "$cmd,") == 0 && !$flag) { $line = $_line; $flag = 1;}
#    else { push @lines, $_line; }
  }
  close $fh;

  #マス固有のカードを買った時の処理
  if($in{buyable_flag}){
    $line = "$cmd,$excavaters[$no][4],$excavaters[$no][2],$excavaters[$no][3],$excavaters[$no][5]";
  }

  if ($line && !$in{reserve}) {
    my($no,$rare,$name,$excav_effect,$excav_condition) = split /,/, $line;
    my @user_jewels = split /,/, $spl{jewel};
    my @user_excav_jewels = split /,/, $spl{excav_jewel};
    my $is_changeable = &is_change_excav(\@user_jewels,$spl{gold},\@user_excav_jewels,$no,1);
    if($is_changeable){
      my @excav_need = split /<>/, $excavaters[$no][5];
      my @user_jewel_sum = ();
      for my $i (0..$#excav_need){
        my $sum = $excav_need[$i] - $user_excav_jewels[$i];#永久宝石分を差し引き
        $sum = 0 if $sum < 0;#
        my $sum = $user_jewels[$i] - $sum;#宝石から引く
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#足りない場合はgoldを使用
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #excav_jewelsへの効果==========================================
      for my $add_no (split /,/, $excavaters[$no][6]){
        $user_excav_jewels[$add_no] += 1;
      }
      $spl{excav_jewel} = join ",", @user_excav_jewels;
      #excavへデータ保存==========================================
      my @user_excavs = split /,/, $spl{excav};
      $user_excavs[$no]++;
      $spl{excav} = join ",", @user_excavs;
      #==========================================
      $spl{win_point} += $excavaters[$no][7];
      $mes .= "購入しました<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      &n_menu;
      #実績処理==========================================
      $spl{max_excav} = &splend_achievement_regist(1,$spl{max_excav});
      $mes .= &splend_achievement_check($spl{max_excav},"max_excav",1);
      #カードを補充==========================================
#      my $rand_no = int(rand($#excavaters) + 1);#本当はレア度が1,2,3均等になるようにしたいけどとりあえずランダムで
##      my $rand_no = &splend_excav_add($no);
##      push @lines, "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
##      $mes .= "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
    }else{
      $mes .= "購入に必要な金貨と宝石が足りません<br>";
      $m{tp} = 100;
      &n_menu;
      return;
    }
  }elsif($line && $in{reserve}){#ﾘｻﾞｰﾌﾞ
    #reservesへデータ保存==========================================
    my @user_reserves = split /,/, $spl{reserves};
    my $user_reservable = @user_reserves;
    if($user_reservable >= $max_reservable){#予約数上限
      $mes .= "ﾘｻﾞｰﾌﾞ数の上限を超えています";
      $m{tp} = 100;
      &n_menu;
      return;
    }
    push @user_reserves,"$cmd,";
    $spl{reserves} = join ",", @user_reserves;
    $spl{gold}++;#金貨一枚を獲得する
    $mes .= "ﾘｻﾞｰﾌﾞしました<br>";
    $spl{card_flag} = &use_wait_flag($spl{card_flag});
    &n_menu;
    &write_user_data;#これ2重だしいらんかも
    #カードを補充==========================================
#    my $rand_no = int(rand($#excavaters) + 1);#本当はレア度が1,2,3均等になるようにしたいけどとりあえずランダムで
##    my $rand_no = &splend_excav_add($cmd);
##    push @lines, "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
##    $mes .= "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
  }else{
    $mes .= "そのｶｰﾄﾞはすでに購入されたようです";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #他の選択肢は途中でreturnしているので大丈夫なはず

##  open my $fh, "> $log_dir/playfield_excav.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
##  print $fh @lines;
##  close $fh;
  #==========================================
  &write_user_data;
  $m{tp} = 100;
  return;
}
#領地(勝利点)の購入
sub tp_140 {
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#あとで直す
    $mes .= 'やめました<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  if(!$cmd){#あとで直す
    $mes .= 'やめました<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  my $line = ''; # 買ったアイテム情報が入る
  my @lines = (); # その他の商品が入る
  my $flag = 0;
  #==========================================
  #ファイル操作(open,取り出し選択,替え追加,close)
  open my $fh, "< $log_dir/playfield_field.cgi" or &error('領地ﾘｽﾄﾌｧｲﾙが読み込めません');
  eval { flock $fh, 2; };
  while (my $_line = <$fh>) {
    if (index($_line, "$cmd,") == 0 && !$flag) { $line = $_line; $flag = 1;}
##    else { push @lines, $_line; }
  }
  close $fh;

  my $no = $cmd;

  if ($line) {
##    my($no,$name,$excav_effect,$excav_condition) = split /,/, $line;
    my @user_jewels = split /,/, $spl{jewel};
    my @user_excav_jewels = split /,/, $spl{excav_jewel};
    my $is_changeable = &is_change_excav(\@user_jewels,$spl{gold},\@user_excav_jewels,$no,2);
    if($is_changeable){#交換可能な時
      my @field_need = split /<>/, $fields[$no][4];
      my @user_jewel_sum = ();
      for my $i (0..$#field_need){
        my $sum = $field_need[$i] - $user_excav_jewels[$i];#永久宝石分を差し引き
        $sum = 0 if $sum < 0;
        my $sum = $user_jewels[$i] - $sum;#宝石から引く
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#足りない場合はgoldを使用
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #fieldsへデータ保存==========================================
      my @user_fields = split /,/, $spl{field_point};
      $user_fields[$no]++;
      $spl{field_point} = join ",", @user_fields;
      #==========================================
      $spl{win_point} += $fields[$no][5];
      $mes .= "交換しました<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      #実績処理==========================================
      $spl{max_field} = &splend_achievement_regist(1,$spl{max_field});
      $mes .= &splend_achievement_check($spl{max_field},"max_field",1);
      #==========================================
      &n_menu;
      $m{tp} = 100;
      my $rand_no = int(rand($#fields) + 1);#本当はレア度が1,2,3均等になるようにしたいけどとりあえずランダムで
      # !no,name,効果,交換条件
##      push @lines, "$fields[$rand_no][0],$fields[$rand_no][2],$fields[$rand_no][3],$fields[$rand_no][4]\n";
    }else{
      $mes .= "購入に必要な金貨と宝石が足りません<br>";
      $m{tp} = 100;
      &n_menu;
      return;
    }
##    open my $fh, "> $log_dir/playfield_field.cgi" or &error('領地ﾘｽﾄﾌｧｲﾙが読み込めません');
##    print $fh @lines;
##    close $fh;
  }else{
    $mes .= "そのｶｰﾄﾞはすでに購入されたようです";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #ファイル操作(open,取り出し選択,替え追加,close)
  #==========================================
  &write_user_data;

  return;
}
sub tp_150 {#ﾘｻﾞｰﾌﾞｶｰﾄﾞを購入
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#あとで直す
    $mes .= 'やめました<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  if($cmd){
    my @user_reserves = split /,/, $spl{reserves};
    my @user_jewels = split /,/, $spl{jewel};
    my @user_excav_jewels = split /,/, $spl{excav_jewel};
    my $is_changeable = &is_change_excav(\@user_jewels,$spl{gold},\@user_excav_jewels,$cmd,1);
    if($is_changeable){
      my $no = $cmd;
      my @excav_need = split /<>/, $excavaters[$no][5];
      my @user_jewel_sum = ();
      for my $i (0..$#excav_need){
        my $sum = $excav_need[$i] - $user_excav_jewels[$i];#永久宝石分を差し引き
        $sum = 0 if $sum < 0;#
        my $sum = $user_jewels[$i] - $sum;#宝石から引く
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#足りない場合はgoldを使用
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #excav_jewelsへの効果==========================================
      for my $add_no (split /,/, $excavaters[$no][6]){
        $user_excav_jewels[$add_no] += 1;
      }
      $spl{excav_jewel} = join ",", @user_excav_jewels;
      #excavへデータ保存==========================================
      my @user_excavs = split /,/, $spl{excav};
      $user_excavs[$no]++;
      $spl{excav} = join ",", @user_excavs;
      #購入したﾘｻﾞｰﾌﾞｶｰﾄﾞを削除==========================================
      my @new_reserves = ();
      my $reserve_bought_flag = 0;
      for my $user_reserves (split /,/, $spl{reserves}){
        if($user_reserves eq $cmd && !$reserve_bought_flag){
          $reserve_bought_flag = 1;
          next;
        }
        push @new_reserves,$user_reserves;
      }
      $spl{reserves} = join ",", @new_reserves;
      #実績処理==========================================
      $spl{max_excav} = &splend_achievement_regist(1,$spl{max_excav});
      $mes .= &splend_achievement_check($spl{max_excav},"max_excav",1);
      #==========================================
      $spl{win_point} += $excavaters[$no][7];
      $mes .= "ﾘｻﾞｰﾌﾞｶｰﾄﾞ $excavaters[$no][2] を購入しました<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      &n_menu;
    }else{
      $mes .= "交換に必要な金貨と宝石が足りません<br>";
      $m{tp} = 100;
      &n_menu;
      return;
    }

  }
  #==========================================
  &write_user_data;
  $m{tp} = 100;
  return;

##  $m{tp} = 100;
##  &n_menu;
##  return;
}

sub tp_200 {
  if($in{jewel1} <= 0 || $in{jewel2} <= 0 || $in{jewel1} > $#jewels || $in{jewel2} > $#jewels){
    if($in{jewel1} <= 0 && $in{jewel2} <= 0){
      $mes .= "やめました";
    }else{
      $mes .= "有効な数字を入力してください";
    }
    $m{tp} = 100;
    &n_menu;
    return;
  }
  $spl{jewel_flag} = &use_wait_flag($spl{jewel_flag});
  #宝石採掘=========================================
  my @user_jewels = split /,/, $spl{jewel};
  my @result_jewel = @{&excavate($in{jewel1},$in{jewel2})};
  for my $i (0..$#result_jewel){
    $user_jewels[$i] += $result_jewel[$i];
  }
  $spl{jewel} = join ",", @user_jewels;
  #ユーザーデータに書き込み=============================
  &write_user_data;
  #=========================================
  $mes .= "宝石:$jewels[$in{jewel1}][1],$jewels[$in{jewel2}][1]を獲得した!<br>";

  $m{tp} = 100;
  &n_menu;
  $mes .= "作成中<br>";
  return;
}
sub tp_210 {
  $mes .= "実行完了<br>";
  return;
}

sub tp_300 {
  return if &is_ngflag_spl($spl{dice_flag});
  #unless(&is_sabakan){
  #  return if &is_ngflag_spl($spl{dice_flag});
  #}
  #ダイス処理==========================================
  my $dice = int(rand(6) + 1);
  $mes .= "出目は$dice!<br>";
  #if(&is_sabakan){
  #  $dice = 1;
  #}
  #userデータ処理==========================================
  my $place_past = $spl{place};#移動前の位置,データﾌｧｲﾙ操作で使用
  $spl{place} += $dice;
  if($spl{place} > $#places){#一周
    $spl{place} -= $#places;
  }
  $spl{max_range} += $dice;
  $mes .= "現在地:$places[$spl{place}][1]<br>";
  #移動先のjewel獲得========================================
  my @user_jewels = split /,/, $spl{jewel};
  $user_jewels[$places[$spl{place}][3]]++;
  $spl{jewel} = join ",", @user_jewels;
  my $place_jewel = $places[$spl{place}][3];
  $mes .= "宝石:$jewels[$place_jewel][1] を獲得した<br>";
  $spl{dice_flag} = &use_wait_flag($spl{dice_flag});
  #データﾌｧｲﾙ操作==========================================
  require "boardgame_splend_external.cgi";
  $mes .= &splend_init_excav_field_map;
  #playfield_mapは,他プレイヤーの位置確認,
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀが読み込めません');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  my @lines = ();
  #到達map種類カウント,実績処理==========================================
  $mes .= &splend_achievement_check($spl{max_range},'max_range_map',2);
  $spl{map_kind} = &splend_array_add($spl{place},$spl{map_kind});#マップ種類
  $mes .= &splend_achievement_array($spl{map_kind},'max_kind_map',1);
  #災害直撃処理,天候(災害場所)の変化(head_line)===============
=pod
  if($spl{place} eq $weather_map_no){
    $mes .= "突如、轟々と吹き荒れる砂嵐があなたを襲った!<br>";
    $mes .= &weather_damages;
    #ダメージ処理作成中(宝石or永久宝石excav_jewelgが減少)
  }

  if($time > $next_weather_time){
    $next_weather_time = $time + $weather_reload_time;
    $weather_map_no = int(rand($#places));
  }
=cut
  my $new_head_line = "$next_weather_time<>$weather_map_no<>\n";
  push @lines,$new_head_line;
  #head_line中身 next_weather_time,dummy
  #移動処理=====================================
  my $count = 1;
  my $new_line = "";
  while (my $line = <$fh>) {
    my ($no,$people,$weather,$dummy2) = split /<>/, $line;
    if(index($place_past,$count) eq 0){#移動する前のマス
      my @peoples = split /,/, $people;
      my @new_peoples = ();
      for my $p (@peoples){
        next if $p eq $m{name};
        push @new_peoples,$p;
      }
      my $new_people .= join ",", @new_peoples;
      $new_line = "$no<>$new_people<>$weather<>\n";
    }elsif($count eq $spl{place}){#移動後のマス
      $new_line = "$no<>$m{name},$people<>$weather<>\n";
      $spl{buyable_card_kind} = $weather;#そのマスにおける購入可能カードを保存
    }else{#そのほかのマス
      $new_line = $line;
    }
    push @lines,$new_line;
    $count++;
  }
  close $fh;

  open my $fh, "> $log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀに書き込めません');
  print $fh @lines;
  close $fh;

  $m{tp} = 100;
  &n_menu;
  #==========================================
  &write_user_data;
  return;
}

sub tp_400 {
  $layout = 2;
  $mes .= &splend_others_display;
  &n_menu;
  $m{tp} = 100;
  return;
}

sub tp_500 {
  #ランキング表示はexternal関数ファイルに切り離す予定なので注意
  $layout = 2;
  require "boardgame_splend_external.cgi";
  &splend_rank_reload;
  &n_menu;
  $m{tp} = 100;
  return;
}

sub tp_600 {
  #ランキングをjsでソートできるようにしたい
  $layout = 2;

  #ランキング更新判定,ついでにplayfieldのexcavとfieldを更新=====================================
  open my $tfh, "< $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新データが開けません");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  if(&time_to_date($time) ne &time_to_date($splend_last_time)){
    require "boardgame_splend_external.cgi";
    &splend_rank_reload;
    $splend_last_time = $time;
    open my $tfh, "> $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新データが開けません");
    print $tfh "$splend_last_time<>$splend_start_time<>$splend_end_time<>\n";
    close $tfh;
    #playfieldのexcavとfieldを更新=====================================
    &splend_excav_field_reload;
  }
  #=====================================
  $mes .= &splend_ranking_display;


  &n_menu;
  $m{tp} = 100;

  return;
}

sub tp_2000 {#ルール説明
  $mes .= qq|<form method="$method" action="./log/library/book/837b815b83688351815b83802020838b815b838b90e096be76657220312d31208dec3a82a082a882cc82e8.html">|;
  $mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
  $mes .= qq|<input type="submit" value="ﾙｰﾙ説明" class="button1"></form>|;
  &n_menu;
  $m{tp} = 1;
  return;
}

sub tp_3000 {#コレクションルーム、
  $layout = 2;
  #読み込むファイルをresultに変更============================
  my $splend_game_state = &splend_open_time_file();
  if($splend_game_state eq "end"){#ゲーム終了後はファイルが変更されるため
    $user_file = "$userdir/$id/splend_result.cgi";
    if(!$spl{is_achieve_end}){#実績報酬処理
      require "boardgame_splend_external.cgi";
      &splend_achievement_end();
      $spl{is_achieve_end} = 1;#報酬獲得済みフラグ
    }
  }
  &road_user_data;#user_fileを再定義してから$splのデータ読み込み
  #自分の順位を取得,保存=====================================
  if(!-f "$log_result_dir/splend_rank_win_point.cgi"){
    $mes .= "まだ結果データがありません<br>";
    &begin;
    $layout = 0;
    return;
  }
  open my $fh, "< $log_result_dir/splend_rank_win_point.cgi" or &error("ﾎﾞﾄﾞｹﾞﾗﾝｷﾝｸﾞ結果データが開けません");
  my $head_line = <$fh>;
  my ($last_rank_time,$end_rank_time) = split /<>/, $head_line;
  my $rank_count = 1;
  while (my $line = <$fh>) {
    my ($pname,$pwin_point) = split /<>/, $line;
    if($pname eq $m{name}){$spl{rank} = $rank_count;}
    $rank_count++;
  }
  close $fh;
  #=================================
  &write_user_data;
  #結果表示==========================
  #勝利点,順位
  $mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $mes .= qq|<th>ﾗﾝｸ</th><td align="right">$spl{rank}</td>|;
  $mes .= qq|<th>勝利点</th><td align="right">$spl{win_point}</td>|;
  $mes .= qq|<tr></table>|;
  #宝石
  $mes .= qq|【ｽﾃｰﾀｽ】宝石<br>|;
  $mes .= &splend_status_jewel;


  $mes .= qq|<table width="50%"><tr><td>|;

  $mes .= qq|【ｶｰﾄﾞ】採掘家<br>|;
  $mes .= qq|<table class="table1" cellpadding="3">|;
  $mes .= qq|<tr><th>ｶｰﾄﾞNo.</th><th>名前</th><th>枚数</th></tr>|;
  my @user_excav_jewels = split /,/, $spl{excav};
  for my $i(0..$#user_excav_jewels){
    $mes .= qq|<tr><td>$i</td><td>$excavaters[$i][2]</td><td>$user_excav_jewels[$i]</td></tr>|;
  }
  $mes .= qq|</table>|;
  $mes .= qq|</td><td>|;
  $mes .= qq|【ｶｰﾄﾞ】領地<br>|;
  $mes .= qq|<table class="table1" cellpadding="3">|;
  $mes .= qq|<tr><th>ｶｰﾄﾞNo.</th><th>名前</th><th>枚数</th></tr>|;
  my @user_fields = split /,/, $spl{field_point};
  for my $i(0..$#user_fields){
    $mes .= qq|<tr><td>$i</td><td>$fields[$i][2]</td><td>$user_fields[$i]</td></tr>|;
  }
  $mes .= qq|</table>|;

  $mes .= qq|</td></tr></table>|;

  $mes .= &splend_ranking_display;
  #永久宝石,採掘カード(excav),領地カード(field)を種類ごとに表示
  #実績判定(購入の所に埋め込む可能性が高い)
  #獲得実績
#  $mes .= "テスト";
  &n_menu;
  $m{tp} = 1;
  return;
}
#========================================================================
sub splend_ranking_display {
  my $tmp_mes .= "";
  $tmp_mes .= qq|<link rel="stylesheet" type="text/css" href="$stylesheet_file">|;
  $tmp_mes .= qq|<script type="text/javascript" src="./html/jquery-latest.js"></script><script type="text/javascript" src="./html/jquery.tablesorter.js"></script>|;
  $tmp_mes .= qq|<script type="text/javascript">|;
  #ドルマークが変数だと認識されてしまうので力技 いい方法あればぜひ改変お願いします
  $tmp_mes .= '$(document).ready(function() {$(".tablesorter").tablesorter({widgets: ["zebra"]});	});</script>';

  my @rows = (qw/ﾗﾝｸ 名前 勝利点/);
  my $tmp_html = '';
  $tmp_html .= qq|<table class="tablesorter"><thead><tr>|;
  $tmp_html .= qq|<th>$_</th>| for (@rows);
  $tmp_html .= qq|</tr></thead><tbody>|;

  my $splned_game_state = &splend_open_time_file();
  my $tmp_file_name = "";
  if($splned_game_state eq "end"){
    $tmp_file_name = "$log_result_dir/splend_rank_win_point.cgi";
  }else{
    $tmp_file_name = "$log_dir/splend_rank_win_point.cgi";
  }

  open my $fh, "< $tmp_file_name" or &error("ﾎﾞﾄﾞｹﾞﾗﾝｷﾝｸﾞデータが開けません");
  my $head_line = <$fh>;
  my ($last_rank_time,$end_rank_time) = split /<>/, $head_line;
  my $rank_count = 1;
  my $rank = 1;
  my $past_win_p = -10000;
  while (my $line = <$fh>) {
    my ($pname,$pwin_point) = split /<>/, $line;
    if($past_win_p ne $pwin_point){
      $rank = $rank_count;
      $past_win_p = $pwin_point;
    }
    #自分の順位を取得,保存=====================================
    if($pname eq $m{name}){
      $spl{rank} = $rank;
    }#ゲーム終了後のtp_3000でも順位の取得更新をできるようにする
    #=====================================
    $tmp_html .= qq|<tr>|;
    $tmp_html .= qq|<td>$rank</td>|;
    $tmp_html .= qq|<td>$pname</td>|;
    $tmp_html .= qq|<td>$pwin_point</td>|;
    $tmp_html .= qq|</tr>\n|;
    $rank_count++;
  }
  close $fh;
  $tmp_html .= qq|</tbody></table>|;
  #=====================================
  #テスト
  $tmp_html .= &splend_achievement_check($spl{max_field},"max_field",1);
  &write_user_data;

  $tmp_mes .= $tmp_html;
  return $tmp_mes;
}

#グローバル変数参照
#これはexternalにおいてもいいかもしれない
sub splend_others_display {
  my $tmp_mes = "";
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀが読み込めません');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;


  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>場所</th><th>獲得宝石</th><th>滞在中のﾌﾟﾚｲﾔｰ</th></tr>|;
  while (my $line = <$fh>) {
    my ($no,$people,$weather,$dummy) = split /<>/, $line;
    my $place_jewel = $places[$no][3];
    $tmp_mes .= qq|<tr><td>$places[$no][1]</td><td>$jewels[$place_jewel][1]</td><td>$people</td></tr>|;
  }
  $tmp_mes .= qq|</table>|;
  close $fh;

  return $tmp_mes;
}

sub splend_status_jewel {
  $tmp_mes .= "";
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr><th>金貨</th><td align="right">$spl{gold}</td></tr></table>|;
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>宝石一覧</th>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<th>$jewels[$i][1]</th>|;
  }
  $tmp_mes .= qq|</tr><tr>|;

  my @user_jewels = split /,/, $spl{jewel};
  $tmp_mes .= qq|<td>宝石</td>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<td>$user_jewels[$i]</td>|;
  }
  $tmp_mes .= qq|</tr><tr>|;
  my @user_excav_jewels = split /,/, $spl{excav_jewel};
  $tmp_mes .= qq|<td>永久宝石</td>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<td>$user_excav_jewels[$i]</td>|;
  }
  $tmp_mes .= qq|</tr></table>|;
  return $tmp_mes;
}

#他プレイヤーのも見れるようにするときは引数にuserデータ指定してroad_user_dataと同様の処理をする
sub splend_status_display {
  my $tmp_mes = "";
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀが読み込めません');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  close $fh;

  $tmp_mes .= qq|<table width="100%" border="0"><tr>|;
  $tmp_mes .= qq|<td width="50%">|;

  $tmp_mes .= "現在地:$places[$spl{place}][1]  ";#場所の名前
  $tmp_mes .= qq|天候:なし<br>|;

  $tmp_mes .= qq|<font color="$places[$spl{place}][2]">$places[$spl{place}][6]</font>|;
  $tmp_mes .= qq|</td><td>|;
  $tmp_mes .= qq|<img src="$icon_dir/$spl{place}$picture_extension" width="100%">|;
  $tmp_mes .= qq|$places[$spl{place}][4]<br>|;
  $tmp_mes .= qq|<td></tr></table>|;
  $tmp_mes .= qq|<iframe src="$splend_google_map[$spl{place}][2]" width="100%" height="200" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>|;


  $tmp_mes .= qq|<hr size="1">|;
  $tmp_mes .= qq|現在ﾀｰﾝ数: $spl{turn_allroad}<br>|;
  $tmp_mes .= qq|次の街|;
  if($spl{place} > $#places){#一周
    $spl{place} -= $#places;
  }
  for my $i(0..4){
    my $p_count = $i + $spl{place};
    if($p_count > $#places){#一周
      $p_count -= $#places;
    }
    my $p_jewel = $places[$p_count][3];
    $tmp_mes .= qq|→<font color=$jewels[$p_jewel][4]>$places[$p_count][1]</font>|;
  }
  $tmp_mes .= qq|<br>|;
##  $tmp_mes .= qq|news : <font color="#AAFFAA">現在$places[$weather_map_no][1]において大嵐が発生中！付近を通行する商人は宝石にご注意ください。</font>|;
  $tmp_mes .= qq|<hr size="1">|;

  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>ﾗﾝｸ</th><td align="right">$spl{rank}</td>|;
  $tmp_mes .= qq|<th>勝利点</th><td align="right">$spl{win_point}</td>|;
  $tmp_mes .= qq|<th>踏破距離</th><td align="right">$spl{max_range}</td>|;
  $tmp_mes .= qq|</tr></table>|;

  $tmp_mes .= qq|【ｽﾄｯｸ】<br>|;
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>採掘</th><td align="right"><font color="#ff9966">$spl{jewel_flag}</font> <font size="1">/$reloadmax_jewel_flag</font></td>|;
  $tmp_mes .= qq|<th>ﾀﾞｲｽ</th><td align="right"><font color="#ff9966">$spl{dice_flag}</font> <font size="1">/$reloadmax_dice_flag</font></td>|;
  $tmp_mes .= qq|<th>購入</th><td align="right"><font color="#ff9966">$spl{card_flag}</font> <font size="1">/$reloadmax_card_flag</font></td>|;
  $tmp_mes .= qq|</tr></table>|;
  $tmp_mes .= qq|<font color="#ff9966">↑ 11/23の10:00ごろに12→5に引き下げるので注意</font><br>|;

  $tmp_mes .= qq|【ｽﾃｰﾀｽ】宝石<br>|;
  $tmp_mes .= &splend_status_jewel;

  $tmp_mes .= qq|<hr size="1">|;
  $tmp_mes .= qq|ﾘｻﾞｰﾌﾞ中カード<br>|;
  for my $user_reserves (split /,/, $spl{reserves}){
    $tmp_mes .= "$excavaters[$user_reserves][2],";
  }
  $tmp_mes .= qq|<br>|;


  return $tmp_mes;
}

sub next_time_display{
  open my $tfh, "< $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新データが開けません");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  my $splend_game_time_mes = "";
#  my $splend_game_state = "";
  if($splend_start_time && $time < $splend_start_time){#ゲーム開始前

    my($min,$hour,$day,$month) = (localtime($splend_start_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "次のｹﾞｰﾑの開始時刻は$month月$day日$hour時$min分です<br>";

  }elsif($splend_end_time && $time < $splend_end_time){#ゲーム終了前

    my($min,$hour,$day,$month) = (localtime($splend_end_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "ｹﾞｰﾑの終了時刻は$month月$day日$hour時$min分です<br>";
    open my $fh, "< $log_dir/playfield_map.cgi" or &error("ﾎﾞﾄﾞｹﾞﾏｯﾌﾟデータが開けません");
    my $head_line = <$fh>;
    #マップカード更新時刻=====================#
    my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
    close $fh;
    my($min,$hour,$day,$month) = (localtime($next_weather_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "次のﾏｯﾌﾟ限定の採掘家カードの更新時刻は$month月$day日$hour時$min分です<br>";
    #=============================#
  }elsif(!$splend_end_time){#
    $splend_game_time_mes .= "<br>";
  }
  return $splend_game_time_mes;
}

sub weather_damages{#後でweather以外で使うかもしれないので分離

  my $weather_rand = int(rand(3));
  my $temp_mes = "";
  if($weather_rand eq 0){
    my @weather_jewels = split /<>/, $spl{jewel};
    for my $i(0..$#weather_jewels){
      $weather_jewels[$i] = int($weather_jewels[$i] * 0.5);
    }
    $spl{jewel} = join ",", @weather_jewels;
    $temp_mes .= "宝石が被害を受けました<br>";
  }elsif($wether_rand eq 1){
    my @weather_excav_jewels = split /<>/, $spl{excav_jewel};
    for my $i(0..$#weather_excav_jewels){
      $weather_excav_jewels[$i] = int($weather_excav_jewels[$i] * 0.75);
    }
    $spl{excav_jewel} = join ",", @weather_excav_jewels;
    $temp_mes .= "永久宝石が被害を受けました<br>";
  }else{
    $spl{win_point} = int($spl{win_point} - 2);
    $temp_mes .= "勝利点が被害を受けました<br>";
  }
  #宝石減少,永久宝石(excav_jewel)減少、勝利点減少のいずれか
  #3以下は無傷,4,5は-1,それ以上は-2(進んでいる人ほどダメージ)
  #でももう少しゲーム性が欲しい,,,
  return $temp_mes;

}

#========================================================================
#リファレンス使ってるcgi domesticとか?を確認
#リファレンスを全力でテスト

sub use_wait_flag {
  my $flag = shift;
  $flag -= 1;
  if($flag < 0){
    $flag = 0;
  }
  return $flag;
}
#====================================
#宝石の色番号を入力し、色付きの宝石名を取得
sub splend_jewel_color {
  my $jewel_no .= shift;
  my $tmp_mes .= qq|<font color=$jewel_no>$jewels[$jewel_no][1]</font>|;
  return $tmp_mes;
}
#入力 excavatersの番号 出力 入力の番号と同じレア度?のカードの番号(ランダム)
sub splend_excav_add {
  my $excav_no = shift;
  if($excavaters[$excav_no][4] eq 1){
    $excav_no = int(rand($num_playfield_excav_1) + 1);
  }elsif($excavaters[$excav_no][4] eq 2){
    $excav_no = int(rand($num_playfield_excav_2) + $num_playfield_excav_1 + 1);
  }elsif($excavaters[$excav_no][4] eq 3){
    $excav_no = int(rand($num_playfield_excav_3) + $num_playfield_excav_2 + $num_playfield_excav_1 + 1);
  }
  return $excav_no;
}
#====================================
#採掘(必要な燃料と採掘機を引いて、取れた宝石と燃料の値を返す)
#====================================
#引数　欲しい宝石を2つ(no)(配列) (移動(dice)で宝石ランダムに1つ)
sub excavate {
  my ($jewel1,$jewel2) = @_;
  my @e_jewels = ();#returnする宝石の配列
  for my $jewels (@jewels){#配列初期化
    push @e_jewels,0;
  }
  #基本効果================================
  $e_jewels[$jewel1] += 1;#種類確定1つ
  $e_jewels[$jewel2] += 1;#種類確定1つ
  return \@e_jewels;
}

#====================================
#個々の判定関数,宝石→採掘機(reserve_excavなどで使用)
#====================================
#引数　jewel,,gold,excav(no)(not配列),
#戻り値　1か0
sub is_change_excav{
  my ($ice_ref_jewel,$ref_ice_gold,$ice_ref_e_jewel,$ref_ice_excav_no,$excav_field_flag) = @_;
  my $ice_gold = $ref_ice_gold;
  my $ice_no = $ref_ice_excav_no;
  my @ice_jewel_sum = ();
  my @ice_jewel = @{$ice_ref_jewel};
  my @ice_e_jewel = @{$ice_ref_e_jewel};
  my $is_changeable = 1;
  my $jewels_count = @jewels;
  $jewels_count++;
  for my $i (0 .. $jewels_count){
    my $ice_sum_count = $ice_e_jewel[$i] + $ice_jewel[$i];
    push @ice_jewel_sum , $ice_sum_count;
  }
  #判定
  my @ice_need = ();
  if($excav_field_flag eq 1){
    @ice_need = split /<>/, $excavaters[$ice_no][5];
  }elsif($excav_field_flag eq 2){
    @ice_need = split /<>/, $fields[$ice_no][4];
  }
  for my $i (0 .. $#ice_need){
    my $ice_sum_count = $ice_jewel_sum[$i] - $ice_need[$i];
    if($ice_sum_count < 0){
      $ice_gold += $ice_sum_count;
      if($ice_gold < 0){
        $is_changeable = 0;
        last;
      }
    }
  }
  return $is_changeable;
}
#====================================
#個々の判定関数,宝石→勝利点 is_change_excavと合体してもいいかもしれない
#====================================
#引数
#戻り値
sub is_change_field {
  my ($icf_ref_jewel,$ref_icf_gold,$icf_ref_e_jewel,$ref_icf_field_no) = @_;
  my $icf_gold = $$ref_icf_gold;
  my $icf_field_no = $$ref_icf_field_no;
  my @icf_jewel_sum = ();
  my @icf_jewel = @{$icf_ref_jewel};
  my @icf_e_jewel = @{$icf_ref_e_jewel};
  my $is_changeable = 1;
  my $jewels_count = @jewels;
  for my $i (0 .. $jewels_count){
    my $icf_sum_count = $icf_e_jewel[$i] + $icf_jewel[$i];
    push @icf_jewel_sum , $icf_sum_count;
  }
  #判定
  my @icf_need = split /<>/, $fields[$icf_field_no][4];
  for my $i (0 .. $#icf_need){
    my $icf_sum_count = $icf_jewel_sum[$i] - $icf_need[$i];
    if($icf_sum_count < 0){
      $icf_gold += $icf_sum_count;
      if($icf_gold < 0){
        $is_changeable = 0;
        last;
      }
    }
  }
  return $is_changeable;
}


#========================================================================
#ダイス処理
#========================================================================
#wait処理 データロード時に使用
#グローバル変数,グローバル関数参照
sub reload_wait {
  my ($rw_sec,$rw_min,$rw_hour,$rw_mday,$rw_month,$rw_year,$rw_wday,$rw_stime) = localtime($spl{last_roadtime});
  my $road_count = &is_wait_time($spl{last_roadtime});
  $spl{last_roadtime} = $time;
  $spl{road_count} = "$road_count";
  $spl{turn_allroad} += $road_count;#更新ﾀｰﾝ数追加

  my @reload_counts = ('jewel_flag','card_flag','dice_flag');
  for my $count(@reload_counts){
    $spl{$count} += $road_count;
    if($spl{$count} > $reloadmax_jewel_flag){$spl{$count} = $reloadmax_jewel_flag;}
  }
  return;
}
#グローバル変数参照関数
sub is_ngflag_spl {
  $is_flag = shift;
  if(!$is_flag){
    $mes .= "次のﾘﾛｰﾄﾞ時間までお待ちください<br>";
    &n_menu;
    $m{tp} = 100;
    return 1;
  }
  return 0;
}

#一日2回　7時更新
#
#戻り値　未更新回数
#月や年のまたぎは考慮されていないが、ゲームを拡張させる上で月のまたぎ程度は作った方がいい

sub is_wait_time {
  my $ftime = shift;
  #time,ftimeの変換,$reload_hourで修正
  my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time - $reload_hour * 3600);
  my ($f_sec,$f_min,$f_hour,$f_mday,$f_month,$f_year,$f_wday,$f_stime) = localtime($ftime - $reload_hour * 3600);

  #午前か午後か判定(7時間(reload_hour)で補正してあることに注意)
  my $f_is_hour = 0;
  my $is_hour = 0;
  if($f_hour >= 12){$f_is_hour = 1;}
  if($hour >= 12){$is_hour = 1;}
  #その日の0時00分のtimeを取得
  my $tmp_times .= &time_to_date($time - $reload_hour * 3600);
  $tmp_times = &date_to_time($tmp_times);

  my $tmp_f_times .= &time_to_date($ftime - $reload_hour * 3600);
  $tmp_f_times = &date_to_time($tmp_f_times);
  #0時00分同士で計算,12時間で割ることで更新回数を算出
  #さらに午前(7amから7pm)or午後(7pmから7am)を計算に入れる
  my $m_cal = int(($tmp_times - $tmp_f_times) / (3600 * 12)) + $is_hour - $f_is_hour;

  return $m_cal;
}


#入力 値,spl_keys
#keysに対応した配列をチェックして称号を獲得
#出力 ($spl{achieves}を変更)
sub splend_achievement_check {
  #akeyはdataのachieveファイルのarrayと名前が同期
  my ($anum,$akey,$atype) = @_;
  my ($anum_n,$anum_a) = split /,/, $anum;
  if($atype eq 2){#max_rangeなど
    $anum_n = $anum;
    $anum_a = $spl{$akey};
  }
  require "$data_file_2";
  my $achieve_count = $#{ 'achieve_'.$akey };
  my $tmp_mes = "";
  $anum_a++;
  for my $i($anum_a..$achieve_count){
    if($anum_n >= ${ 'achieve_'.$akey }[$i][2]){
      $tmp_mes .= qq|<font color=#ffd700>実績「|;
      $tmp_mes .= qq|${ 'achieve_'.$akey }[$i][3]|;
      $tmp_mes .= qq|」が解除されました!</font><br>|;
      $anum_a = $i;
    }
  }
  $spl{$akey} = join ",", ($anum_n,$anum_a);
  return $tmp_mes;
}
sub splend_achievement_array {
  #arrayではakeyはsplを取得する用としても使用(もちろんdataのachieveファイルのarrayと名前が同期)
  #$atypeは1で(配列数=獲得数),2で(配列数=種類で、0でない値の数=獲得数)とする
  my ($anum,$akey,$atype) = @_;
  my $anum_a = $spl{$akey};
  my $tmp_mes .= "";
  my @anum_array = split /,/, $anum;
  my $anum_n = 0;
  if($atype eq 1){
    $anum_n = @anum_array;
  }elsif($atype eq 2){
    $anum_n = 0;
    for my $i(0..$#anum_array){
      if($anum_array[$i]){
        $anum_n++;
      }
    }
  }else{
    return;
  }
  require "$data_file_2";
  my $achieve_count = $#{ 'achieve_'.$akey };
  $anum_a++;
  for my $i($anum_a..$achieve_count){
    if($anum_n >= ${ 'achieve_'.$akey }[$i][2]){
      $tmp_mes .= qq|<font color=#ffd700>実績「|;
      $tmp_mes .= qq|${ 'achieve_'.$akey }[$i][3]|;
      $tmp_mes .= qq|」が解除されました!</font><br>|;
      $spl{$akey} = $i;
    }
  }
  return $tmp_mes;
}

#引き値 加算値,加算する対象
#splend_achievement_checkと使う対象が同期
sub splend_achievement_regist {
  my ($aaddnum,$anum) = @_;
  my ($anum_n,$anum_a) = split /,/, $anum;
  $anum_n += $aaddnum;
  $anum = join ",", ($anum_n,$anum_a);
  return $anum;
}
#引き値 加算する種類,加算する対象(配列)
#配列に追加(append)するほう
#map_kindなど実績登録に使用
sub splend_array_add {
  my ($aaddkind,$anum) = @_;
  my @anum_array = split /,/, $anum;
  my $count_flag = 0;
  for my $i(0..$#anum_array){
    if($anum_array[$i] eq $aaddkind){$count_flag = 1;}
  }
  if(!$count_flag){push @anum_array, "$aaddkind";}#新規の種類だった時配列に追加 配列長=getした数
  $anum = join ",", @anum_array;
  return $anum;
}
#====================================
sub splend_open_time_file {#現在の時間を取得し,ゲームの状況を出力
  open my $tfh, "< $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新データが開けません");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  my $splend_game_state = "";
  if($splend_start_time && $time > $splend_start_time){#ゲーム開始時
    $splend_game_state = "start";
  }elsif($splend_end_time && $time > $splend_end_time){#ゲーム終了時
    $splend_game_state = "end_func";
  }elsif(!$splend_end_time){#ゲーム終了後
    $splend_game_state = "end";
  }
  return $splend_game_state;
}
#====================================
#userデータ
#====================================
#自プレイヤーデータロード
sub road_user_data{
#	if(!-f "$user_file"){#あとでinit_player_dataに埋め込み
#		open my $fh, "> $user_file" or &error("userデータが開けません");
#		close $fh;
#	}
	if(!-f "$user_file"){#ゲーム終了後のための処理,ファイル作成処理はinit_player_dataに埋め込み済み
    return;
	}
	open my $fh, "< $user_file" or &error("userデータが開けません");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$spl{$k} = $v; # $s
	}
	return;
}
#自プレイヤーデータ保存
sub write_user_data{
	my @spl_keys = (qw/
		fuel gold field_point win_point jewel excav_jewel excav achieves jewel_flag card_flag dice_flag disturb_flag reserves place max_range last_roadtime road_count turn_allroad buyable_card_kind
    max_excav max_field map_kind max_weather_damage rank max_kind_map is_achieve_end max_range_map
	/);
	my $line_spl = "";
	for my $k_spl (@spl_keys) {
		$line_spl .= "$k_spl;$spl{$k_spl}<>";
	}
	open my $fh, "> $user_file" or &error("userデータが開けません");
	print $fh "$line_spl\n";
	close $fh;
}
1#削除不可
