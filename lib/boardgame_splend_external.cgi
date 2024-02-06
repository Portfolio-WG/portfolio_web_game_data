#boardgame_splend_external.cgi

my $data_file_name = "splend_2";


require "$datadir/splend/$data_file_name.cgi";
#====================================
#boardgame_splend.cgi�̊֐�
#�g���p�x����r�I���Ȃ��֐��������Ɋi�[
#�O���[�o���Ȏ����ϐ�$spl{}�ȂǎQ�Ƃ��Ȃ��悤����
#====================================
#�֐��ڐA���̒ǉ�
#�t�@�C�������ext,
#====================================
$this_file = "boradgame_splend.cgi";
my $ext_this_file = "boradgame_splend_external.cgi";
my $ext_user_file = "$userdir/$id/splend.cgi";#���[�U�[�f�[�^
my $ext_data_file = "$datadir/splend/$data_file_name.cgi";#�ÓIdata�t�@�C��
my $ext_log_dir = "$logdir/splend";#excav,field_point�̃t�@�C��
my $ext_icon_dir = "$icondir/splend";#icon



#�J�n����init
#====================================
#�f�[�^����������
#====================================
#����͊댯�Ȃ̂Ŗ{�̂̕��ɒu���H
sub splend_init_player_data{
#  require "$datadir/splend/splend_1.cgi";
  #�t�@�C���f�[�^������
  open my $fh, "> $ext_user_file" or &error("user�f�[�^���J���܂���");
  close $fh;

  #data�f�B���N�g���̂�͕��ʂɃO���[�o���ŎQ�Ƃ�������Ă邯�ǎQ�Ƃ��������܂��������E�E�E
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

  #۰�ގ���
  $spl{last_roadtime} = $time;
  $spl{turn_allroad} = 0;

  #�����s���׸ސ�
  $spl{jewel_flag} = 2;
  $spl{card_flag} = 2;
  $spl{dice_flag} = 2;
  #�����ʒu
  $spl{place} = 1;

  #�����_�A���B����
  $spl{max_range} = 0;
  $spl{win_point} = 0;


  &write_user_data;
  return;
}

sub splend_init_data {
#  require "$datadir/splend/splend_1.cgi";
  #excav��field_point�̃t�B�[���h�f�[�^������====================================
  &splend_excav_field_reload;
  #map�̃f�[�^������===============================
  my @init_playfield_map = ();
  push @init_playfield_map, "0<>0<>0<>\n";#head_line
  for my $i(1..$#places){
    push @init_playfield_map, "$i<><><>\n";#no,people,weather,dummy
  }
  open my $fh, "> $ext_log_dir/playfield_map.cgi" or &error('ϯ���ް��ɏ������߂܂���');
  print $fh @init_playfield_map;
  close $fh;

  &splend_init_excav_field_map;

  #���t����f�[�^������==========================
  #���ԊǗ��p�t�@�C�����ƂŊ֐��ɂ܂Ƃ߂�����������������Ȃ�
  open my $fh, "> $log_time_file" or &error("���޹ގ��ԍX�V̧�ق��쐬�ł��܂���");
  my $splend_time_ = &time_to_date($time);
  $splend_time_ = &date_to_time($splend_time_);
  if($reload_hour > 12){
    $splend_time_ += $reload_hour * 3600;
  }else{
    $splend_time_ += ($reload_hour + 12) * 3600;
  }
#  my $splend_start_time = $time - 1;
  my $splend_end_time = $splend_game_days * 24 * 3600 + $splend_time_;
  print $fh "$time<>0<>$splend_end_time<>\n";#����(�ݷݸލX�V�p),�Q�[���J�n����,�Q�[���I������
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
  # !no,���A�x,name,����,��������

  #excavaters[$ipd_rand][5]��<>����,�ɕϊ����Ȃ��ƍs���Ȃ�����
  #�Ƃ�����excav�̕���,�ɂ���ׂ��ł́H
  #�S�̒������K�v����
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
#�I������
#====================================
#�ǂݍ��ݒ��̎��ɏI�������
#�܂��͊O���ɏI���{�^���쐬
sub splend_end_data {
  #�����L���O�X�V����========================
  &splend_rank_reload;
  #�i�i�̑���========================
  #���̃t�@�C���Q��data�Ɉڂ�������������������Ȃ�
#  my @files_name = ("rank_max_range","rank_win_point","rank_gold");
#  my @files_news_name = ("���B����","�����_","����");
#  my @files_shogo_name = ("�e�X�g1","�e�X�g2","�e�X�g3");
  my @files_name = ("rank_win_point");
  my @files_news_name = ("�����_");
  my @files_shogo_name = ("���ް�޹ްϰ��");
  for my $i (0..$#files_name){
    open my $fh, "< $log_dir/splend_$files_name[$i].cgi" or &error('ϯ���ް����ǂݍ��߂܂���');
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
    my $past_win_p = -10000;#��΂ɓ��Ă͂܂�Ȃ����������
    for my $line (@lines) {
      my ($name, $win_p) = split /<>/, $line;
      #���_���ǂ�������
      if($past_win_p ne $win_p){
        $past_win_p = $win_p;
        $rank = $rank_count;
      }
      if ($rank > 10) {
        last;
      }
      if ($rank == 1) {
        &write_world_news("$files_news_name[$i]��1�ʂ�$name���񂪋P���܂���!");
        #&write_world_big_news(qq|$files_news_name[$i]��1�ʂ�$name���񂪋P���܂���|);
        #&regist_you_data($name, "shogo", "$files_shogo_name[$i]");
      }
      my $v = 11 - $rank;
#      my $vv = $rank > 7 ? $rank - 7 : 1;
      &send_money($name, "$files_news_name[$i]�� $rank ��", 1 * $v);
#      &send_god_item($v, $name) for (1..$vv);
      $rank_count++;
    }
    #while
    #send_money,(win_point�Ƒ��̂��̂͋�ʂ���������������)
  }
  #�t�@�C���폜(�t�B�[���h�f�[�^�̂݁@�����L���O�͐l�C���[�̂悤�ɂ��΂炭�c��?����)========================

  #splend_result�͂��ƂŐ擪�Œ�`
  #�O��̃t�B�[���h�f�[�^���폜
  if(-d "$logdir/splend_result"){
    rmtree "$logdir/splend_result" or &error('splend_result�ިڸ�؂������ł��܂���');
  }
  mkdir "$logdir/splend_result" or &error("splend_result�ިڸ�؂����܂���");

  my @files_name2 = ("playfield_excav.cgi","playfield_field.cgi","playfield_map.cgi","splend_rank_gold.cgi","splend_rank_max_range.cgi","splend_rank_win_point.cgi","splend_time.cgi");
  for my $file_name(@files_name2){
    if(-f "$log_dir/$file_name"){
      rename "$log_dir/$file_name", "$logdir/splend_result/$file_name" or &error("Cannot rename $log_dir/$file_name to $logdir/splend_result/$file_name");
    }
  }
  #���[�U�[�f�[�^�폜(result�Ƃ��ĕۑ�)
  opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;

    if(-f "$userdir/$id/splend.cgi"){
      rename "$userdir/$id/splend.cgi", "$userdir/$id/splend_result.cgi" or &error("Cannot rename $userdir/$id/splend.cgi to $userdir/$id/splend_result.cgi");
    }
  }

  #opendir while
  #unlink
  #����̊J�n�������w��
  my $splend_next_time = $time - $splend_game_days * 3600 * 24;
  $splend_next_time += 24 * 3600 * 365;
  my $splend_next_time = &time_to_date($splend_next_time);
  $splend_next_time = &date_to_time($splend_next_time);
  if($reload_hour > 12){#�ł���΃��O�C���������ߌ�ɊJ�n�I��������������
    $splend_next_time += $reload_hour * 3600;
  }else{
    $splend_next_time += ($reload_hour + 12) * 3600;
  }
  #��������
  open my $tfh, "> $log_time_file" or &error("���޹ގ��ԍX�V�f�[�^���J���܂���");
  print $tfh "$time<>$splend_next_time<>0<>";
#  my $head_line = <$tfh>;
#  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  #splend_result�t�H���_�쐬
  #ranking�t�@�C���ړ�
  #�c���splend�t�H���_�̃t�@�C���폜

  #========================
  return;
}
#====================================
#�����L���O�X�V
#====================================
sub splend_rank_reload {
  my @files_splend = ("max_range","win_point","gold");
  my @files_name = ("rank_max_range","rank_win_point","rank_gold");
  my @rank_win_point = ();
  my @rank_max_range = ();
  my @rank_gold = ();
  #==========================
  opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;
    next if !-f "$userdir/$id/splend.cgi";

    open my $fh, "< $userdir/$id/splend.cgi" or &error("���޹��ݷݸލX�Vuser�f�[�^���J���܂���");
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
    #�쐬��
  }
  closedir $dh;
  for my $i (0..$#files_splend){
    @{$files_name[$i]} = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @{$files_name[$i]};
    open my $fh, "> $ext_log_dir/splend_rank_$files_splend[$i].cgi" or &error("���޹��ݷݸލX�V$files_splend[$i]�f�[�^���J���܂���");
    seek  $fh, 0, 0;
    truncate $fh, 0;
    print $fh "$time<>\n";
    print $fh @{$files_name[$i]};
    close $fh;
  }
  return;
}
#====================================
#�J�[�h���΂�Ȃ��悤�X�V����֐�
sub splend_excav_field_reload {
  open my $fh, "> $ext_log_dir/playfield_excav.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
  my $init_playfield_excav = &init_playfield_excav;
  print $fh $init_playfield_excav;
  close $fh;
  open my $fh, "> $ext_log_dir/playfield_field.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
  my $init_playfield_field = &init_playfield_field;
  print $fh $init_playfield_field;
  close $fh;
  return;
}
#====================================
#map�ōw���\�ȃJ�[�h������������֐�
#��{�I��init_playfield_excav�̎��s��ɔz�u,���Ԍo��(����)�ōX�V

sub splend_init_excav_field_map {
  my @t_lines = ();
  my $tmp_mes = "";

  open my $fh2, "< $ext_log_dir/playfield_map.cgi" or &error('ϯ��̧�ق��ǂݍ��߂܂���');
  my $head_line = <$fh2>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  if($time <= $next_weather_time){#�܂��X�V���ԂłȂ��Ƃ�
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
    #�Œ�J�[�h���o($places[$i][5]�g�p)----------------
    my @buyable_cards_no = split /,/, $places[$count][5];
    my $count2 = 0;
    for my $card_no(@buyable_cards_no){
      $buyable_card .= $card_no;
      $buyable_card .= ",";
      $count2++;
    }
    #�����_���J�[�h���o----------------
    my $res_buyable = $max_map_buyable_card - $count2;
    $res_buyable = 0 if $res_buyable < 0;#for�o�O�h�~ ����Ȃ�?
    for my $i(0..$res_buyable){
      $buyable_card .= int(rand($#excavaters) + 1);
      unless($i eq $res_buyable){
        $buyable_card .= ",";
      }
    }
    #join���Č��̔z��ɖ߂�----------------
    my $new_line = join "<>", ($no,$people,$buyable_card,$dummy2);
    push @t_lines,$new_line;
    $count++;
  }
  close $fh2;

  open my $fh2, "> $ext_log_dir/playfield_map.cgi" or &error('ϯ��̧�ق��ǂݍ��߂܂���');
  print $fh2 @t_lines;
  close $fh2;

  $tmp_mes .= '�}�b�v�̍w���\�J�[�h���X�V����܂���<br>';

  return $tmp_mes;
}
#====================================
#���щ�������
sub splend_achievement_all_checker {
  return;
}
#====================================
#���ѕ�V����
#���я����֘A�̓R�[�h���������ɃN�\�ėp���̒Ⴂ�R�[�f�B���O�Ȃ̂ł��Ƃō��{�I�ɕς��邩��
sub splend_achievement_end {
  #�{�̂�is_achieve_end��ǉ�
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
  if($all_achieve_points >= 16){#�o�O�h�~�p�A���Ƃō폜
    $all_achieve_points = 16;
  }
  if($all_achieve_points){
    &send_money($name, "���щ�����V $all_achieve_points �߲��", 30000 * $all_achieve_points);
    $tmp_mes .= "���ѕ�V�����I��<br>";
  }
  $spl{is_achieve_end} = 1;
  return;
}
#====================================
#���ʕ\������
sub splend_result_display {
  #�ŏI����
  #��΂̐�
  #�i�v��΂̐�
  #�w���J�[�h���
  #����
  #(�����L���O)
  return;
}

1;#�폜�s��
