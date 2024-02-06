#boardgame_splend_external.cgi

my $data_file_name = "splend_2";


require "$datadir/splend/$data_file_name.cgi";
#====================================
#boardgame_splend.cgiの関数
#使う頻度が比較的少ない関数をここに格納
#グローバルな辞書変数$spl{}など参照しないよう注意
#====================================
#関数移植時の追加
#ファイル操作のext,
#====================================
$this_file = "boradgame_splend.cgi";
my $ext_this_file = "boradgame_splend_external.cgi";
my $ext_user_file = "$userdir/$id/splend.cgi";#ユーザーデータ
my $ext_data_file = "$datadir/splend/$data_file_name.cgi";#静的dataファイル
my $ext_log_dir = "$logdir/splend";#excav,field_pointのファイル
my $ext_icon_dir = "$icondir/splend";#icon



#開始処理init
#====================================
#データ初期化処理
#====================================
#これは危険なので本体の方に置く？
sub splend_init_player_data{
#  require "$datadir/splend/splend_1.cgi";
  #ファイルデータ初期化
  open my $fh, "> $ext_user_file" or &error("userデータが開けません");
  close $fh;

  #dataディレクトリのやつは普通にグローバルで参照しちゃってるけど参照だけだしまあいいか・・・
  my @sid_init_jewel = ();
  my @sid_init_e_jewel = ();
  my @sid_init_excav = ();
  my @sid_init_field = ();
  for my $init_jewel(@jewels){
    push @sid_init_jewel, 0;
    push @sid_init_e_jewel, 0;
  }
  for my $init_excav(@excavaters){
    push @sid_init_excav, 0;
  }
  for my $init_field(@fields){
    push @sid_init_field, 0;
  }
  my $fuel_jewels_line = join ",", @e_jewels;
  $spl{gold} = 0;
  $spl{jewel} = join ",", @sid_init_jewel;
  $spl{excav_jewel} = join ",", @sid_init_e_jewel;
  $spl{excav} = join ",", @sid_init_excav;
  $spl{field_point} = join ",", @sid_init_field;

  #ﾛｰﾄﾞ時間
  $spl{last_roadtime} = $time;
  $spl{turn_allroad} = 0;

  #初期行動ﾌﾗｸﾞ数
  $spl{jewel_flag} = 2;
  $spl{card_flag} = 2;
  $spl{dice_flag} = 2;
  #初期位置
  $spl{place} = 1;

  #勝利点、到達距離
  $spl{max_range} = 0;
  $spl{win_point} = 0;


  &write_user_data;
  return;
}

sub splend_init_data {
#  require "$datadir/splend/splend_1.cgi";
  #excavとfield_pointのフィールドデータ初期化====================================
  &splend_excav_field_reload;
  #mapのデータ初期化===============================
  my @init_playfield_map = ();
  push @init_playfield_map, "0<>0<>0<>\n";#head_line
  for my $i(1..$#places){
    push @init_playfield_map, "$i<><><>\n";#no,people,weather,dummy
  }
  open my $fh, "> $ext_log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀに書き込めません');
  print $fh @init_playfield_map;
  close $fh;

  &splend_init_excav_field_map;

  #日付判定データ初期化==========================
  #時間管理用ファイルあとで関数にまとめた方がいいかもしれない
  open my $fh, "> $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新ﾌｧｲﾙが作成できません");
  my $splend_time_ = &time_to_date($time);
  $splend_time_ = &date_to_time($splend_time_);
  if($reload_hour > 12){
    $splend_time_ += $reload_hour * 3600;
  }else{
    $splend_time_ += ($reload_hour + 12) * 3600;
  }
#  my $splend_start_time = $time - 1;
  my $splend_end_time = $splend_game_days * 24 * 3600 + $splend_time_;
  print $fh "$time<>0<>$splend_end_time<>\n";#時間(ﾗﾝｷﾝｸﾞ更新用),ゲーム開始時間,ゲーム終了時間
  close $fh;

  &write_user_data;
  return;
}
sub init_playfield_field {
  my $ret_mes = "";
  for my $i(1..$num_playfield_field){
    my $ipf_rand = int(rand($#fields) + 1);
    $ret_mes .= "$fields[$ipf_rand][0],$fields[$ipf_rand][2],$fields[$ipf_rand][3],$fields[$ipf_rand][4]\n";
  }
  return $ret_mes;
}

sub init_playfield_excav {
  my $ret_mes = "";
  # !no,レア度,name,効果,交換条件

  #excavaters[$ipd_rand][5]は<>から,に変換しないと行けないかも
  #というかexcavの方を,にするべきでは？
  #全体調整が必要かも
  for my $i(1..$playfield_excav_cardnum){
    my $ipd_rand = int(rand($num_playfield_excav_1) + 1);
    $ret_mes .= "$excavaters[$ipd_rand][0],$excavaters[$ipd_rand][4],$excavaters[$ipd_rand][2],$excavaters[$ipd_rand][3],$excavaters[$ipd_rand][5]\n";
  }
  for my $i(1..$playfield_excav_cardnum){
    my $ipd_rand = int(rand($num_playfield_excav_2) + $num_playfield_excav_1 + 1);
    $ret_mes .= "$excavaters[$ipd_rand][0],$excavaters[$ipd_rand][4],$excavaters[$ipd_rand][2],$excavaters[$ipd_rand][3],$excavaters[$ipd_rand][5]\n";
  }
  for my $i(1..$playfield_excav_cardnum){
    my $ipd_rand = int(rand($num_playfield_excav_3) + $num_playfield_excav_2 + $num_playfield_excav_1 + 1);
    $ret_mes .= "$excavaters[$ipd_rand][0],$excavaters[$ipd_rand][4],$excavaters[$ipd_rand][2],$excavaters[$ipd_rand][3],$excavaters[$ipd_rand][5]\n";
  }
  return $ret_mes;
}
#====================================
#終了処理
#====================================
#読み込み中の時に終了判定回す
#または外部に終了ボタン作成
sub splend_end_data {
  #ランキング更新処理========================
  &splend_rank_reload;
  #景品の贈呈========================
  #このファイル群はdataに移した方がいいかもしれない
#  my @files_name = ("rank_max_range","rank_win_point","rank_gold");
#  my @files_news_name = ("到達距離","勝利点","金貨");
#  my @files_shogo_name = ("テスト1","テスト2","テスト3");
  my @files_name = ("rank_win_point");
  my @files_news_name = ("勝利点");
  my @files_shogo_name = ("★ﾎﾞｰﾄﾞｹﾞｰﾏｰ★");
  for my $i (0..$#files_name){
    open my $fh, "< $log_dir/splend_$files_name[$i].cgi" or &error('ﾏｯﾌﾟﾃﾞｰﾀが読み込めません');
    my $head_line = <$fh>;
    my ($next_time,$test) = split /<>/, $head_line;
    my @lines = ();
    while (my $line = <$fh>) {
      push @lines, $line;
#      my ($name,$win_p) = split /<>/, $line;
    }
    close $fh;
    my $rank_count = 1;
    my $rank = 1;
    my $past_win_p = -10000;#絶対に当てはまらない数字を入力
    for my $line (@lines) {
      my ($name, $win_p) = split /<>/, $line;
      #同点かどうか判定
      if($past_win_p ne $win_p){
        $past_win_p = $win_p;
        $rank = $rank_count;
      }
      if ($rank > 10) {
        last;
      }
      if ($rank == 1) {
        &write_world_news("$files_news_name[$i]第1位に$nameさんが輝きました!");
        #&write_world_big_news(qq|$files_news_name[$i]第1位に$nameさんが輝きました|);
        #&regist_you_data($name, "shogo", "$files_shogo_name[$i]");
      }
      my $v = 11 - $rank;
#      my $vv = $rank > 7 ? $rank - 7 : 1;
      &send_money($name, "$files_news_name[$i]第 $rank 位", 1 * $v);
#      &send_god_item($v, $name) for (1..$vv);
      $rank_count++;
    }
    #while
    #send_money,(win_pointと他のものは区別した方がいいかも)
  }
  #ファイル削除(フィールドデータのみ　ランキングは人気投票のようにしばらく残す?かも)========================

  #splend_resultはあとで先頭で定義
  #前回のフィールドデータを削除
  if(-d "$logdir/splend_result"){
    rmtree "$logdir/splend_result" or &error('splend_resultﾃﾞｨﾚｸﾄﾘを消去できません');
  }
  mkdir "$logdir/splend_result" or &error("splend_resultﾃﾞｨﾚｸﾄﾘが作れません");

  my @files_name2 = ("playfield_excav.cgi","playfield_field.cgi","playfield_map.cgi","splend_rank_gold.cgi","splend_rank_max_range.cgi","splend_rank_win_point.cgi","splend_time.cgi");
  for my $file_name(@files_name2){
    if(-f "$log_dir/$file_name"){
      rename "$log_dir/$file_name", "$logdir/splend_result/$file_name" or &error("Cannot rename $log_dir/$file_name to $logdir/splend_result/$file_name");
    }
  }
  #ユーザーデータ削除(resultとして保存)
  opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;

    if(-f "$userdir/$id/splend.cgi"){
      rename "$userdir/$id/splend.cgi", "$userdir/$id/splend_result.cgi" or &error("Cannot rename $userdir/$id/splend.cgi to $userdir/$id/splend_result.cgi");
    }
  }

  #opendir while
  #unlink
  #次回の開始時刻を指定
  my $splend_next_time = $time - $splend_game_days * 3600 * 24;
  $splend_next_time += 24 * 3600 * 365;
  my $splend_next_time = &time_to_date($splend_next_time);
  $splend_next_time = &date_to_time($splend_next_time);
  if($reload_hour > 12){#できればログインが多い午後に開始終了させたいから
    $splend_next_time += $reload_hour * 3600;
  }else{
    $splend_next_time += ($reload_hour + 12) * 3600;
  }
  #書き込み
  open my $tfh, "> $log_time_file" or &error("ﾎﾞﾄﾞｹﾞ時間更新データが開けません");
  print $tfh "$time<>$splend_next_time<>0<>";
#  my $head_line = <$tfh>;
#  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  #splend_resultフォルダ作成
  #rankingファイル移動
  #残りのsplendフォルダのファイル削除

  #========================
  return;
}
#====================================
#ランキング更新
#====================================
sub splend_rank_reload {
  my @files_splend = ("max_range","win_point","gold");
  my @files_name = ("rank_max_range","rank_win_point","rank_gold");
  my @rank_win_point = ();
  my @rank_max_range = ();
  my @rank_gold = ();
  #==========================
  opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;
    next if !-f "$userdir/$id/splend.cgi";

    open my $fh, "< $userdir/$id/splend.cgi" or &error("ﾎﾞﾄﾞｹﾞﾗﾝｷﾝｸﾞ更新userデータが開けません");
    my $line = <$fh>;
    close $fh;

    %tmp_spl  = ();
    for my $hash (split /<>/, $line) {
      my($k, $v) = split /;/, $hash;
      $tmp_spl{$k} = $v; # $s
    }
    my $tmp_name = pack 'H*', $id;

    for my $i (0..$#files_splend){
      my $idata = $files_splend[$i];
      push @{$files_name[$i]}, "$tmp_name<>$tmp_spl{$idata}<>\n";
    }
#log_dir/splend_rank_max_range, log_dir/splend_rank_win_point, log_dir/splend_rank_gold,
#    my @files_splend = ("max_range","win_point","gold");
    #作成中
  }
  closedir $dh;
  for my $i (0..$#files_splend){
    @{$files_name[$i]} = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @{$files_name[$i]};
    open my $fh, "> $ext_log_dir/splend_rank_$files_splend[$i].cgi" or &error("ﾎﾞﾄﾞｹﾞﾗﾝｷﾝｸﾞ更新$files_splend[$i]データが開けません");
    seek  $fh, 0, 0;
    truncate $fh, 0;
    print $fh "$time<>\n";
    print $fh @{$files_name[$i]};
    close $fh;
  }
  return;
}
#====================================
#カードが偏らないよう更新する関数
sub splend_excav_field_reload {
  open my $fh, "> $ext_log_dir/playfield_excav.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
  my $init_playfield_excav = &init_playfield_excav;
  print $fh $init_playfield_excav;
  close $fh;
  open my $fh, "> $ext_log_dir/playfield_field.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
  my $init_playfield_field = &init_playfield_field;
  print $fh $init_playfield_field;
  close $fh;
  return;
}
#====================================
#mapで購入可能なカードを初期化する関数
#基本的にinit_playfield_excavの実行後に配置,時間経過(数日)で更新

sub splend_init_excav_field_map {
  my @t_lines = ();
  my $tmp_mes = "";

  open my $fh2, "< $ext_log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾌｧｲﾙが読み込めません');
  my $head_line = <$fh2>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  if($time <= $next_weather_time){#まだ更新時間でないとき
    close $fh2;
    return;
  }
  $next_weather_time = $time + $map_buyable_card_reload_time;
  my $new_head_line = "$next_weather_time<>$weather_map_no<>\n";
  push @t_lines,$new_head_line;

  my $count = 0;
  while (my $line = <$fh2>) {
    my ($no,$people,$buyable_card,$dummy2) = split /<>/, $line;
    $buyable_card = "";
    #固定カード抽出($places[$i][5]使用)----------------
    my @buyable_cards_no = split /,/, $places[$count][5];
    my $count2 = 0;
    for my $card_no(@buyable_cards_no){
      $buyable_card .= $card_no;
      $buyable_card .= ",";
      $count2++;
    }
    #ランダムカード抽出----------------
    my $res_buyable = $max_map_buyable_card - $count2;
    $res_buyable = 0 if $res_buyable < 0;#forバグ防止 いらない?
    for my $i(0..$res_buyable){
      $buyable_card .= int(rand($#excavaters) + 1);
      unless($i eq $res_buyable){
        $buyable_card .= ",";
      }
    }
    #joinして元の配列に戻す----------------
    my $new_line = join "<>", ($no,$people,$buyable_card,$dummy2);
    push @t_lines,$new_line;
    $count++;
  }
  close $fh2;

  open my $fh2, "> $ext_log_dir/playfield_map.cgi" or &error('ﾏｯﾌﾟﾌｧｲﾙが読み込めません');
  print $fh2 @t_lines;
  close $fh2;

  $tmp_mes .= 'マップの購入可能カードが更新されました<br>';

  return $tmp_mes;
}
#====================================
#実績解除処理
sub splend_achievement_all_checker {
  return;
}
#====================================
#実績報酬処理
#実績処理関連はコードが長い割にクソ汎用性の低いコーディングなのであとで根本的に変えるかも
sub splend_achievement_end {
  #本体にis_achieve_endを追加
  my @keys1 = (qw/
    max_evcav max_field
  /);
  my @keys2 = (qw/
    max_kind_map max_range
  /);
  my $all_achieve_points = 0;
  my $tmp_mes .= "";
  for my $key1(@keys1){
    my ($anum_n,$anum_a) = split /,/, $spl{$key1};
    $all_achieve_points += $anum_a;
  }
  for my $key2(@keys2){
    $all_achieve_points += $spl{$key2};
  }
  if($all_achieve_points >= 16){#バグ防止用、あとで削除
    $all_achieve_points = 16;
  }
  if($all_achieve_points){
    &send_money($name, "実績解除報酬 $all_achieve_points ﾎﾟｲﾝﾄ", 30000 * $all_achieve_points);
    $tmp_mes .= "実績報酬処理終了<br>";
  }
  $spl{is_achieve_end} = 1;
  return;
}
#====================================
#結果表示処理
sub splend_result_display {
  #最終順位
  #宝石の数
  #永久宝石の数
  #購入カード種類
  #実績
  #(ランキング)
  return;
}

1;#削除不可
