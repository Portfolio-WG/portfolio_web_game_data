#boardgame_splend.cgi
#====================================
#keyword
#splend,
#jewel,

#====================================
#�֘A�t�@�C���ꗗ

#./lib/boardgame_splend_test.cgi(�{��)
#./lib/boardgame/splend_external(�Q�[���J�n�I������(�v���C���[�f�[�^�쐬����)�A�����L���O�X�V�A���щ���)
#./data/splend/splend_N.cgi(N�͔ԍ��A����1)(���ޑS�ʁA��΁A���тȂǒ萔�S��)
#./html/splend/style_splend_N.css(�����L���O��tablesorter,�ð����UI�A�摜canvas�Ȃ�)

#====================================
my $this_file = "boradgame_splend.cgi";
my $user_file = "$userdir/$id/splend.cgi";#���[�U�[�f�[�^

$log_dir = "$logdir/splend";#excav,field_point�̃t�@�C��

$log_result_dir = "$logdir/splend_result";

$log_time_file = "$logdir/splend/splend_time.cgi";#���ԏ����Ǘ��̃t�@�C��,external�Ŏg���Ă���̂ŃO���[�o���K�{

my $data_file_name = "splend_2";

$icon_dir = "$icondir/splend/$data_file_name";#icon

my $data_file = "$datadir/splend/$data_file_name.cgi";#�ÓIdata�t�@�C��
my $data_file_2 = "$datadir/splend_achieve/$data_file_name.cgi";#�ÓIdata�t�@�C��(achieve��)
my $stylesheet_file = "$htmldir/splend/$data_file_name.css";
#���Q�[����O�������Ȃ��悤�X�e�[�W�ύX�������邩���Ȃ̂ŁA��ɓ��I�Q�Ƃɂ���\��������
#log�t�@�C��
#�����L���O
#log_dir/splend_rank_max_range, log_dir/splend_rank_win_point, log_dir/splend_rank_gold,
#====================================
#data�t�@�C���̃f�[�^
#====================================
#�@!�͎g�p����\�����߁A�ʒu��ύX���邱�Ƃ͂ł��Ȃ�
require "$datadir/splend/$data_file_name.cgi";
#========================================================================
#���[�U�[�f�[�^���[�h
%spl  = ();
&road_user_data;
#========================================================================
#�I����Ƀn�}��l�΍�
my $splned_game_state = &splend_open_time_file();
if($splned_game_state eq "end" && $m{tp} > 1 && $m{tp} < 1000){
  &begin;
}
#========================================================================
sub begin{

  $mes .= &next_time_display;

  #2023�N�H�C�x �ً}����
  #$mes .= '<font size=-1 color="#ff9966">';
  #$mes .= '�V�X�e�[�W�̃e�X�g�I���܂���<br>';
  #$mes .= '11/1��19������J�n�\��ł�<br>';
  #$mes .= '�Q�[���I����11/30��18:59�̗\��ł�<br>';
  #$mes .= '�݂�ȂŊy�������I<br>';

  #$mes .= '<br>��:15��19�������T�Ԓ��x�A�V�X�e�[�W�̃e�X�g���܂�<br>';
  #$mes .= '�Q�[�����ɐF�X�ύX���������肷�邩���Ȃ̂ł����ӂ�������<br>';
  #$mes .= '�{�Ԃ̊J�n������10�����{or11�����ɂȂ�\��ł�<br>';
  #$mes .= '�{�Ԃ̏ڍׂȓ����͌�����`�����܂�<br><br>';
  $mes .= '</font>';

  $mes .= '<font size="-1" color="#ff3333">';
  $mes .= '�o�O�Ή��Ƃ��āA�������̂��߂Ɉꎞ�I�ɃX�g�b�N��12�܂ŗ��ߍ��߂�悤�ɂȂ�܂���<br>';
  $mes .= '11/23��10:00����Ɍ���5�Ɉ��������܂�<br>';
  $mes .= '�����f���������Đ��ɐ\���󂠂�܂���ł���<br>';
  $mes .= '</font>';


  if ($m{tp} > 1) {
    $mes .= '���ɉ�����H<br>';
    $m{tp} = 1;
  }
  else {
    $mes .= '�t�C�x �{�[�h�Q�[��<br>';
    $mes .= '������H<br>';
  }

  &menu('��߂�','��΍̏W','ِٰ���','�ڸ���ٰ�');
  return;
}

sub tp_1 {
  if($cmd eq 1){
    #���Ԏ擾==================
    #�ްђ���start_time��0,�ްъ��ԈȊO��end_time��0�ƂȂ�A���̔���Ɏg�p�����
    my $splned_game_state = &splend_open_time_file();
    #�J�n���菈��,�I�����菈��==================
    if($splned_game_state eq "start"){#�Q�[���J�n��
#    if(!-f "$log_dir/playfield_map.cgi"){#�Q�[���J�n��
      $mes .= "�ް�̨���ނ��쐬��<br>";
      require "boardgame_splend_external.cgi";
      &splend_init_data;#�ް�̨���ލ쐬����
      $mes .= "�ްъJ�n��������<br>";
      #�������ގ��ǂ����Ă���̔���֐���ʂ�Ȃ������̂Œǉ�
      $mes .= '�����ް����쐬��<br>';
      &splend_init_player_data;#�v���C���[�f�[�^�쐬����
    }elsif($splned_game_state eq "end_func"){
      require "boardgame_splend_external.cgi";
      &splend_end_data;
      $mes .= '�ްяI����������<br>';
      $mes .= "�Q�[���͏I�����܂���<br>";
      &begin;
      return;
    }elsif($splned_game_state eq "end"){
      $mes .= "�Q�[���͏I�����܂���<br>";
      &begin;
      return;
    }
    #�����܂�$spl{}���g�p���Ȃ�����
    #====================================
    $mes .= "�I�݂̂�ȂŃ{�[�h�Q�[��<br>";
    $mes .= "�ǂݍ��ݒ�<br>";
    #���[�U�[�f�[�^������==================
    if(!-f "$user_file"){#���v���C�̎�
      $mes .= '�����ް����쐬��<br>';
      require "boardgame_splend_external.cgi";
      &splend_init_player_data;#�v���C���[�f�[�^�쐬����
    }
    #==================
    #playfield_excav��open time_to_date�ōX�V

    #���}���u
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
      $mes .= "�̒n���ޏC����������<br>";
    }

    #==================================
    $mes .= &is_wait_time($spl{last_roadtime});
    &reload_wait;#�O��̍X�V���Ԃ��Q�Ƃ��s���\�񐔂��۰��
    &write_user_data;
    $mes .= "reload_time = $spl{last_roadtime},road_count = $spl{road_count}";
    $m{tp} = $cmd * 100;
    &n_menu;
  }elsif($cmd >= 2){
    $m{tp} = $cmd * 1000;
    &{'tp_'. $m{tp} };
  }else{
    $mes .= "��߂܂���";
    &begin;
  }
  return;
}

sub tp_100 {
  $mes .= "���e�X�g��<br>";#�����ɕ\�����쐬���Ă�������
  $mes .= "�������܂����H<br>";
  $mes .= &splend_status_display;

  @menus = ('��߂�','�X�V','��΂𓾂�','�޲���U��','�w������','���͐}�m�F','�ݷݸ�');
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
    $mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;

    $m{tp} = 200;
    return;
#    &n_menu;
  }elsif($cmd eq 3){
    $mes .= "�_�C�X����";
    $m{tp} = 300;
    &n_menu;
  }elsif($cmd eq 4){#��΁��̌@��,�����_
    $mes .= "�ǂ��I�т܂���?";
    &menu('��߂�','�̌@�ƶ���','�̒n����','ػް�޶���');
    $m{tp} = 120;
    return;
  }elsif($cmd eq 5){
    $mes .= "����ڲ԰�̓���<br>";
    $m{tp} = 400;
    &tp_400;
  }elsif($cmd eq 6){
    $mes .= "�����_�����L���O<br>";
    $m{tp} = 600;
    &tp_600;
  }else{
    $mes .= "��߂܂���<br>";
    &begin;
  }
  return;
}
#tp������Ȃ�...(�������̃V�X�e�����g���Â炢..)
sub tp_120 {
  if(!$cmd){
    $mes .= "��߂܂���";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  $layout = 2;
  $mes .= "�ǂ��I�т܂���?<br>";
  $mes .= '��:��ް,��:�̧��,��:������,��:�Ʒ�,��:�޲�����<br>';
  $mes .= '1p = �����_1<br>';
  $mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
  my $count = 0;

  $mes .= &splend_status_jewel;

  if($cmd eq 1){
    $mes .= qq|<table class="table1"><tr><th>��</th><th>�ݸ</th><th>����</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;

    # !no,���A�x,name,����,��������
    open my $fh, "< $log_dir/playfield_excav.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
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

    $mes .= qq|<tr><th>��</th><th>�ݸ</th><th>����</th>| unless $is_mobile;
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

    $mes .= qq|<label><input type="checkbox" id="reserve" name="reserve" value="1">ػް�ނ���</label></form>|;
    $m{tp} = 130;
  }elsif($cmd eq 2){
    $mes .= qq|<table class="table1"><tr><th>��</th><th>����</th>| unless $is_mobile;
    for my $i(0..$#jewels){
      $mes .= qq|<th>$jewels[$i][1]</th>|;
    }
    $mes .= qq|</tr>|;

    # !no,name,����,��������
    open my $fh, "< $log_dir/playfield_field.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
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
    $mes .= qq|���ނ�ػް�ނ��鎞��,�w�����遨�̌@�ƶ��ނƉ�����,<br>�uػް�ނ���v�����������čw���{�^���������Ă�������|;
    $mes .= qq|<table class="table1"><tr><th>��</th><th>�ݸ</th><th>����</th>| unless $is_mobile;
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

    # !no,name,����,��������
    $m{tp} = 150;
  }
  #$m{stock} = $count;
  $mes .= qq|</table>| unless $is_mobile;
  $mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
  $mes .= qq|<p><input type="submit" value="�w������" class="button1"></p></form>|;


  #=========================================
  return;
}
#�J�[�h(excav)�̍w������
sub tp_130 {
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#���ƂŒ���
    $mes .= '��߂܂���<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #�t�@�C������(open,���o���I��,�ւ��ǉ�,close)
  #==========================================
  my $line = ''; # �������A�C�e����񂪓���
  my @lines = (); # ���̑��̏��i������
  my $flag = 0;
  open my $fh, "< $log_dir/playfield_excav.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
  eval { flock $fh, 2; };
  while (my $_line = <$fh>) {
    if (index($_line, "$cmd,") == 0 && !$flag) { $line = $_line; $flag = 1;}
#    else { push @lines, $_line; }
  }
  close $fh;

  #�}�X�ŗL�̃J�[�h�𔃂������̏���
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
        my $sum = $excav_need[$i] - $user_excav_jewels[$i];#�i�v��Ε�����������
        $sum = 0 if $sum < 0;#
        my $sum = $user_jewels[$i] - $sum;#��΂������
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#����Ȃ��ꍇ��gold���g�p
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #excav_jewels�ւ̌���==========================================
      for my $add_no (split /,/, $excavaters[$no][6]){
        $user_excav_jewels[$add_no] += 1;
      }
      $spl{excav_jewel} = join ",", @user_excav_jewels;
      #excav�փf�[�^�ۑ�==========================================
      my @user_excavs = split /,/, $spl{excav};
      $user_excavs[$no]++;
      $spl{excav} = join ",", @user_excavs;
      #==========================================
      $spl{win_point} += $excavaters[$no][7];
      $mes .= "�w�����܂���<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      &n_menu;
      #���я���==========================================
      $spl{max_excav} = &splend_achievement_regist(1,$spl{max_excav});
      $mes .= &splend_achievement_check($spl{max_excav},"max_excav",1);
      #�J�[�h���[==========================================
#      my $rand_no = int(rand($#excavaters) + 1);#�{���̓��A�x��1,2,3�ϓ��ɂȂ�悤�ɂ��������ǂƂ肠���������_����
##      my $rand_no = &splend_excav_add($no);
##      push @lines, "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
##      $mes .= "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
    }else{
      $mes .= "�w���ɕK�v�ȋ��݂ƕ�΂�����܂���<br>";
      $m{tp} = 100;
      &n_menu;
      return;
    }
  }elsif($line && $in{reserve}){#ػް��
    #reserves�փf�[�^�ۑ�==========================================
    my @user_reserves = split /,/, $spl{reserves};
    my $user_reservable = @user_reserves;
    if($user_reservable >= $max_reservable){#�\�񐔏��
      $mes .= "ػް�ސ��̏���𒴂��Ă��܂�";
      $m{tp} = 100;
      &n_menu;
      return;
    }
    push @user_reserves,"$cmd,";
    $spl{reserves} = join ",", @user_reserves;
    $spl{gold}++;#���݈ꖇ���l������
    $mes .= "ػް�ނ��܂���<br>";
    $spl{card_flag} = &use_wait_flag($spl{card_flag});
    &n_menu;
    &write_user_data;#����2�d��������񂩂�
    #�J�[�h���[==========================================
#    my $rand_no = int(rand($#excavaters) + 1);#�{���̓��A�x��1,2,3�ϓ��ɂȂ�悤�ɂ��������ǂƂ肠���������_����
##    my $rand_no = &splend_excav_add($cmd);
##    push @lines, "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
##    $mes .= "$excavaters[$rand_no][0],$excavaters[$rand_no][4],$excavaters[$rand_no][2],$excavaters[$rand_no][3],$excavaters[$rand_no][5]\n";
  }else{
    $mes .= "���̶��ނ͂��łɍw�����ꂽ�悤�ł�";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #���̑I�����͓r����return���Ă���̂ő��v�Ȃ͂�

##  open my $fh, "> $log_dir/playfield_excav.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
##  print $fh @lines;
##  close $fh;
  #==========================================
  &write_user_data;
  $m{tp} = 100;
  return;
}
#�̒n(�����_)�̍w��
sub tp_140 {
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#���ƂŒ���
    $mes .= '��߂܂���<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  if(!$cmd){#���ƂŒ���
    $mes .= '��߂܂���<br>';
    $m{tp} = 100;
    &n_menu;
    return;
  }
  my $line = ''; # �������A�C�e����񂪓���
  my @lines = (); # ���̑��̏��i������
  my $flag = 0;
  #==========================================
  #�t�@�C������(open,���o���I��,�ւ��ǉ�,close)
  open my $fh, "< $log_dir/playfield_field.cgi" or &error('�̒nؽ�̧�ق��ǂݍ��߂܂���');
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
    if($is_changeable){#�����\�Ȏ�
      my @field_need = split /<>/, $fields[$no][4];
      my @user_jewel_sum = ();
      for my $i (0..$#field_need){
        my $sum = $field_need[$i] - $user_excav_jewels[$i];#�i�v��Ε�����������
        $sum = 0 if $sum < 0;
        my $sum = $user_jewels[$i] - $sum;#��΂������
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#����Ȃ��ꍇ��gold���g�p
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #fields�փf�[�^�ۑ�==========================================
      my @user_fields = split /,/, $spl{field_point};
      $user_fields[$no]++;
      $spl{field_point} = join ",", @user_fields;
      #==========================================
      $spl{win_point} += $fields[$no][5];
      $mes .= "�������܂���<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      #���я���==========================================
      $spl{max_field} = &splend_achievement_regist(1,$spl{max_field});
      $mes .= &splend_achievement_check($spl{max_field},"max_field",1);
      #==========================================
      &n_menu;
      $m{tp} = 100;
      my $rand_no = int(rand($#fields) + 1);#�{���̓��A�x��1,2,3�ϓ��ɂȂ�悤�ɂ��������ǂƂ肠���������_����
      # !no,name,����,��������
##      push @lines, "$fields[$rand_no][0],$fields[$rand_no][2],$fields[$rand_no][3],$fields[$rand_no][4]\n";
    }else{
      $mes .= "�w���ɕK�v�ȋ��݂ƕ�΂�����܂���<br>";
      $m{tp} = 100;
      &n_menu;
      return;
    }
##    open my $fh, "> $log_dir/playfield_field.cgi" or &error('�̒nؽ�̧�ق��ǂݍ��߂܂���');
##    print $fh @lines;
##    close $fh;
  }else{
    $mes .= "���̶��ނ͂��łɍw�����ꂽ�悤�ł�";
    $m{tp} = 100;
    &n_menu;
    return;
  }
  #�t�@�C������(open,���o���I��,�ւ��ǉ�,close)
  #==========================================
  &write_user_data;

  return;
}
sub tp_150 {#ػް�޶��ނ��w��
  return if &is_ngflag_spl($spl{card_flag});

  if(!$cmd){#���ƂŒ���
    $mes .= '��߂܂���<br>';
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
        my $sum = $excav_need[$i] - $user_excav_jewels[$i];#�i�v��Ε�����������
        $sum = 0 if $sum < 0;#
        my $sum = $user_jewels[$i] - $sum;#��΂������
        if($sum < 0){
          $spl{gold} += $sum;
          $sum = 0;
        };#����Ȃ��ꍇ��gold���g�p
        push @user_jewel_sum,$sum;
      }
      $spl{jewel} = join ",", @user_jewel_sum;
      #excav_jewels�ւ̌���==========================================
      for my $add_no (split /,/, $excavaters[$no][6]){
        $user_excav_jewels[$add_no] += 1;
      }
      $spl{excav_jewel} = join ",", @user_excav_jewels;
      #excav�փf�[�^�ۑ�==========================================
      my @user_excavs = split /,/, $spl{excav};
      $user_excavs[$no]++;
      $spl{excav} = join ",", @user_excavs;
      #�w������ػް�޶��ނ��폜==========================================
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
      #���я���==========================================
      $spl{max_excav} = &splend_achievement_regist(1,$spl{max_excav});
      $mes .= &splend_achievement_check($spl{max_excav},"max_excav",1);
      #==========================================
      $spl{win_point} += $excavaters[$no][7];
      $mes .= "ػް�޶��� $excavaters[$no][2] ���w�����܂���<br>";
      $spl{card_flag} = &use_wait_flag($spl{card_flag});
      &n_menu;
    }else{
      $mes .= "�����ɕK�v�ȋ��݂ƕ�΂�����܂���<br>";
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
      $mes .= "��߂܂���";
    }else{
      $mes .= "�L���Ȑ�������͂��Ă�������";
    }
    $m{tp} = 100;
    &n_menu;
    return;
  }
  $spl{jewel_flag} = &use_wait_flag($spl{jewel_flag});
  #��΍̌@=========================================
  my @user_jewels = split /,/, $spl{jewel};
  my @result_jewel = @{&excavate($in{jewel1},$in{jewel2})};
  for my $i (0..$#result_jewel){
    $user_jewels[$i] += $result_jewel[$i];
  }
  $spl{jewel} = join ",", @user_jewels;
  #���[�U�[�f�[�^�ɏ�������=============================
  &write_user_data;
  #=========================================
  $mes .= "���:$jewels[$in{jewel1}][1],$jewels[$in{jewel2}][1]���l������!<br>";

  $m{tp} = 100;
  &n_menu;
  $mes .= "�쐬��<br>";
  return;
}
sub tp_210 {
  $mes .= "���s����<br>";
  return;
}

sub tp_300 {
  return if &is_ngflag_spl($spl{dice_flag});
  #unless(&is_sabakan){
  #  return if &is_ngflag_spl($spl{dice_flag});
  #}
  #�_�C�X����==========================================
  my $dice = int(rand(6) + 1);
  $mes .= "�o�ڂ�$dice!<br>";
  #if(&is_sabakan){
  #  $dice = 1;
  #}
  #user�f�[�^����==========================================
  my $place_past = $spl{place};#�ړ��O�̈ʒu,�f�[�^̧�ّ���Ŏg�p
  $spl{place} += $dice;
  if($spl{place} > $#places){#���
    $spl{place} -= $#places;
  }
  $spl{max_range} += $dice;
  $mes .= "���ݒn:$places[$spl{place}][1]<br>";
  #�ړ����jewel�l��========================================
  my @user_jewels = split /,/, $spl{jewel};
  $user_jewels[$places[$spl{place}][3]]++;
  $spl{jewel} = join ",", @user_jewels;
  my $place_jewel = $places[$spl{place}][3];
  $mes .= "���:$jewels[$place_jewel][1] ���l������<br>";
  $spl{dice_flag} = &use_wait_flag($spl{dice_flag});
  #�f�[�^̧�ّ���==========================================
  require "boardgame_splend_external.cgi";
  $mes .= &splend_init_excav_field_map;
  #playfield_map��,���v���C���[�̈ʒu�m�F,
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ϯ���ް����ǂݍ��߂܂���');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  my @lines = ();
  #���Bmap��ރJ�E���g,���я���==========================================
  $mes .= &splend_achievement_check($spl{max_range},'max_range_map',2);
  $spl{map_kind} = &splend_array_add($spl{place},$spl{map_kind});#�}�b�v���
  $mes .= &splend_achievement_array($spl{map_kind},'max_kind_map',1);
  #�ЊQ��������,�V��(�ЊQ�ꏊ)�̕ω�(head_line)===============
=pod
  if($spl{place} eq $weather_map_no){
    $mes .= "�˔@�A���X�Ɛ����r��鍻�������Ȃ����P����!<br>";
    $mes .= &weather_damages;
    #�_���[�W�����쐬��(���or�i�v���excav_jewelg������)
  }

  if($time > $next_weather_time){
    $next_weather_time = $time + $weather_reload_time;
    $weather_map_no = int(rand($#places));
  }
=cut
  my $new_head_line = "$next_weather_time<>$weather_map_no<>\n";
  push @lines,$new_head_line;
  #head_line���g next_weather_time,dummy
  #�ړ�����=====================================
  my $count = 1;
  my $new_line = "";
  while (my $line = <$fh>) {
    my ($no,$people,$weather,$dummy2) = split /<>/, $line;
    if(index($place_past,$count) eq 0){#�ړ�����O�̃}�X
      my @peoples = split /,/, $people;
      my @new_peoples = ();
      for my $p (@peoples){
        next if $p eq $m{name};
        push @new_peoples,$p;
      }
      my $new_people .= join ",", @new_peoples;
      $new_line = "$no<>$new_people<>$weather<>\n";
    }elsif($count eq $spl{place}){#�ړ���̃}�X
      $new_line = "$no<>$m{name},$people<>$weather<>\n";
      $spl{buyable_card_kind} = $weather;#���̃}�X�ɂ�����w���\�J�[�h��ۑ�
    }else{#���̂ق��̃}�X
      $new_line = $line;
    }
    push @lines,$new_line;
    $count++;
  }
  close $fh;

  open my $fh, "> $log_dir/playfield_map.cgi" or &error('ϯ���ް��ɏ������߂܂���');
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
  #�����L���O�\����external�֐��t�@�C���ɐ؂藣���\��Ȃ̂Œ���
  $layout = 2;
  require "boardgame_splend_external.cgi";
  &splend_rank_reload;
  &n_menu;
  $m{tp} = 100;
  return;
}

sub tp_600 {
  #�����L���O��js�Ń\�[�g�ł���悤�ɂ�����
  $layout = 2;

  #�����L���O�X�V����,���ł�playfield��excav��field���X�V=====================================
  open my $tfh, "< $log_time_file" or &error("���޹ގ��ԍX�V�f�[�^���J���܂���");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  if(&time_to_date($time) ne &time_to_date($splend_last_time)){
    require "boardgame_splend_external.cgi";
    &splend_rank_reload;
    $splend_last_time = $time;
    open my $tfh, "> $log_time_file" or &error("���޹ގ��ԍX�V�f�[�^���J���܂���");
    print $tfh "$splend_last_time<>$splend_start_time<>$splend_end_time<>\n";
    close $tfh;
    #playfield��excav��field���X�V=====================================
    &splend_excav_field_reload;
  }
  #=====================================
  $mes .= &splend_ranking_display;


  &n_menu;
  $m{tp} = 100;

  return;
}

sub tp_2000 {#���[������
  $mes .= qq|<form method="$method" action="./log/library/book/837b815b83688351815b83802020838b815b838b90e096be76657220312d31208dec3a82a082a882cc82e8.html">|;
  $mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
  $mes .= qq|<input type="submit" value="ِٰ���" class="button1"></form>|;
  &n_menu;
  $m{tp} = 1;
  return;
}

sub tp_3000 {#�R���N�V�������[���A
  $layout = 2;
  #�ǂݍ��ރt�@�C����result�ɕύX============================
  my $splend_game_state = &splend_open_time_file();
  if($splend_game_state eq "end"){#�Q�[���I����̓t�@�C�����ύX����邽��
    $user_file = "$userdir/$id/splend_result.cgi";
    if(!$spl{is_achieve_end}){#���ѕ�V����
      require "boardgame_splend_external.cgi";
      &splend_achievement_end();
      $spl{is_achieve_end} = 1;#��V�l���ς݃t���O
    }
  }
  &road_user_data;#user_file���Ē�`���Ă���$spl�̃f�[�^�ǂݍ���
  #�����̏��ʂ��擾,�ۑ�=====================================
  if(!-f "$log_result_dir/splend_rank_win_point.cgi"){
    $mes .= "�܂����ʃf�[�^������܂���<br>";
    &begin;
    $layout = 0;
    return;
  }
  open my $fh, "< $log_result_dir/splend_rank_win_point.cgi" or &error("���޹��ݷݸތ��ʃf�[�^���J���܂���");
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
  #���ʕ\��==========================
  #�����_,����
  $mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $mes .= qq|<th>�ݸ</th><td align="right">$spl{rank}</td>|;
  $mes .= qq|<th>�����_</th><td align="right">$spl{win_point}</td>|;
  $mes .= qq|<tr></table>|;
  #���
  $mes .= qq|�y�ð���z���<br>|;
  $mes .= &splend_status_jewel;


  $mes .= qq|<table width="50%"><tr><td>|;

  $mes .= qq|�y���ށz�̌@��<br>|;
  $mes .= qq|<table class="table1" cellpadding="3">|;
  $mes .= qq|<tr><th>����No.</th><th>���O</th><th>����</th></tr>|;
  my @user_excav_jewels = split /,/, $spl{excav};
  for my $i(0..$#user_excav_jewels){
    $mes .= qq|<tr><td>$i</td><td>$excavaters[$i][2]</td><td>$user_excav_jewels[$i]</td></tr>|;
  }
  $mes .= qq|</table>|;
  $mes .= qq|</td><td>|;
  $mes .= qq|�y���ށz�̒n<br>|;
  $mes .= qq|<table class="table1" cellpadding="3">|;
  $mes .= qq|<tr><th>����No.</th><th>���O</th><th>����</th></tr>|;
  my @user_fields = split /,/, $spl{field_point};
  for my $i(0..$#user_fields){
    $mes .= qq|<tr><td>$i</td><td>$fields[$i][2]</td><td>$user_fields[$i]</td></tr>|;
  }
  $mes .= qq|</table>|;

  $mes .= qq|</td></tr></table>|;

  $mes .= &splend_ranking_display;
  #�i�v���,�̌@�J�[�h(excav),�̒n�J�[�h(field)����ނ��Ƃɕ\��
  #���є���(�w���̏��ɖ��ߍ��މ\��������)
  #�l������
#  $mes .= "�e�X�g";
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
  #�h���}�[�N���ϐ����ƔF������Ă��܂��̂ŗ͋Z �������@����΂��Љ��ς��肢���܂�
  $tmp_mes .= '$(document).ready(function() {$(".tablesorter").tablesorter({widgets: ["zebra"]});	});</script>';

  my @rows = (qw/�ݸ ���O �����_/);
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

  open my $fh, "< $tmp_file_name" or &error("���޹��ݷݸރf�[�^���J���܂���");
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
    #�����̏��ʂ��擾,�ۑ�=====================================
    if($pname eq $m{name}){
      $spl{rank} = $rank;
    }#�Q�[���I�����tp_3000�ł����ʂ̎擾�X�V���ł���悤�ɂ���
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
  #�e�X�g
  $tmp_html .= &splend_achievement_check($spl{max_field},"max_field",1);
  &write_user_data;

  $tmp_mes .= $tmp_html;
  return $tmp_mes;
}

#�O���[�o���ϐ��Q��
#�����external�ɂ����Ă�������������Ȃ�
sub splend_others_display {
  my $tmp_mes = "";
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ϯ���ް����ǂݍ��߂܂���');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;


  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>�ꏊ</th><th>�l�����</th><th>�؍ݒ�����ڲ԰</th></tr>|;
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
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr><th>����</th><td align="right">$spl{gold}</td></tr></table>|;
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>��Έꗗ</th>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<th>$jewels[$i][1]</th>|;
  }
  $tmp_mes .= qq|</tr><tr>|;

  my @user_jewels = split /,/, $spl{jewel};
  $tmp_mes .= qq|<td>���</td>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<td>$user_jewels[$i]</td>|;
  }
  $tmp_mes .= qq|</tr><tr>|;
  my @user_excav_jewels = split /,/, $spl{excav_jewel};
  $tmp_mes .= qq|<td>�i�v���</td>|;
  for my $i(1..$#jewels){
    $tmp_mes .= qq|<td>$user_excav_jewels[$i]</td>|;
  }
  $tmp_mes .= qq|</tr></table>|;
  return $tmp_mes;
}

#���v���C���[�̂������悤�ɂ���Ƃ��͈�����user�f�[�^�w�肵��road_user_data�Ɠ��l�̏���������
sub splend_status_display {
  my $tmp_mes = "";
  open my $fh, "< $log_dir/playfield_map.cgi" or &error('ϯ���ް����ǂݍ��߂܂���');
  my $head_line = <$fh>;
  my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
  close $fh;

  $tmp_mes .= qq|<table width="100%" border="0"><tr>|;
  $tmp_mes .= qq|<td width="50%">|;

  $tmp_mes .= "���ݒn:$places[$spl{place}][1]  ";#�ꏊ�̖��O
  $tmp_mes .= qq|�V��:�Ȃ�<br>|;

  $tmp_mes .= qq|<font color="$places[$spl{place}][2]">$places[$spl{place}][6]</font>|;
  $tmp_mes .= qq|</td><td>|;
  $tmp_mes .= qq|<img src="$icon_dir/$spl{place}$picture_extension" width="100%">|;
  $tmp_mes .= qq|$places[$spl{place}][4]<br>|;
  $tmp_mes .= qq|<td></tr></table>|;
  $tmp_mes .= qq|<iframe src="$splend_google_map[$spl{place}][2]" width="100%" height="200" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>|;


  $tmp_mes .= qq|<hr size="1">|;
  $tmp_mes .= qq|������ݐ�: $spl{turn_allroad}<br>|;
  $tmp_mes .= qq|���̊X|;
  if($spl{place} > $#places){#���
    $spl{place} -= $#places;
  }
  for my $i(0..4){
    my $p_count = $i + $spl{place};
    if($p_count > $#places){#���
      $p_count -= $#places;
    }
    my $p_jewel = $places[$p_count][3];
    $tmp_mes .= qq|��<font color=$jewels[$p_jewel][4]>$places[$p_count][1]</font>|;
  }
  $tmp_mes .= qq|<br>|;
##  $tmp_mes .= qq|news : <font color="#AAFFAA">����$places[$weather_map_no][1]�ɂ����đ嗒���������I�t�߂�ʍs���鏤�l�͕�΂ɂ����ӂ��������B</font>|;
  $tmp_mes .= qq|<hr size="1">|;

  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>�ݸ</th><td align="right">$spl{rank}</td>|;
  $tmp_mes .= qq|<th>�����_</th><td align="right">$spl{win_point}</td>|;
  $tmp_mes .= qq|<th>���j����</th><td align="right">$spl{max_range}</td>|;
  $tmp_mes .= qq|</tr></table>|;

  $tmp_mes .= qq|�y�į��z<br>|;
  $tmp_mes .= qq|<table class="table1" cellpadding="3"><tr>|;
  $tmp_mes .= qq|<th>�̌@</th><td align="right"><font color="#ff9966">$spl{jewel_flag}</font> <font size="1">/$reloadmax_jewel_flag</font></td>|;
  $tmp_mes .= qq|<th>�޲�</th><td align="right"><font color="#ff9966">$spl{dice_flag}</font> <font size="1">/$reloadmax_dice_flag</font></td>|;
  $tmp_mes .= qq|<th>�w��</th><td align="right"><font color="#ff9966">$spl{card_flag}</font> <font size="1">/$reloadmax_card_flag</font></td>|;
  $tmp_mes .= qq|</tr></table>|;
  $tmp_mes .= qq|<font color="#ff9966">�� 11/23��10:00�����12��5�Ɉ���������̂Œ���</font><br>|;

  $tmp_mes .= qq|�y�ð���z���<br>|;
  $tmp_mes .= &splend_status_jewel;

  $tmp_mes .= qq|<hr size="1">|;
  $tmp_mes .= qq|ػް�ޒ��J�[�h<br>|;
  for my $user_reserves (split /,/, $spl{reserves}){
    $tmp_mes .= "$excavaters[$user_reserves][2],";
  }
  $tmp_mes .= qq|<br>|;


  return $tmp_mes;
}

sub next_time_display{
  open my $tfh, "< $log_time_file" or &error("���޹ގ��ԍX�V�f�[�^���J���܂���");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  my $splend_game_time_mes = "";
#  my $splend_game_state = "";
  if($splend_start_time && $time < $splend_start_time){#�Q�[���J�n�O

    my($min,$hour,$day,$month) = (localtime($splend_start_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "���̹ްт̊J�n������$month��$day��$hour��$min���ł�<br>";

  }elsif($splend_end_time && $time < $splend_end_time){#�Q�[���I���O

    my($min,$hour,$day,$month) = (localtime($splend_end_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "�ްт̏I��������$month��$day��$hour��$min���ł�<br>";
    open my $fh, "< $log_dir/playfield_map.cgi" or &error("���޹�ϯ�߃f�[�^���J���܂���");
    my $head_line = <$fh>;
    #�}�b�v�J�[�h�X�V����=====================#
    my ($next_weather_time,$weather_map_no,$dummy) = split /<>/, $head_line;
    close $fh;
    my($min,$hour,$day,$month) = (localtime($next_weather_time))[1..4];
    ++$month;
    $splend_game_time_mes .= "����ϯ�ߌ���̍̌@�ƃJ�[�h�̍X�V������$month��$day��$hour��$min���ł�<br>";
    #=============================#
  }elsif(!$splend_end_time){#
    $splend_game_time_mes .= "<br>";
  }
  return $splend_game_time_mes;
}

sub weather_damages{#���weather�ȊO�Ŏg����������Ȃ��̂ŕ���

  my $weather_rand = int(rand(3));
  my $temp_mes = "";
  if($weather_rand eq 0){
    my @weather_jewels = split /<>/, $spl{jewel};
    for my $i(0..$#weather_jewels){
      $weather_jewels[$i] = int($weather_jewels[$i] * 0.5);
    }
    $spl{jewel} = join ",", @weather_jewels;
    $temp_mes .= "��΂���Q���󂯂܂���<br>";
  }elsif($wether_rand eq 1){
    my @weather_excav_jewels = split /<>/, $spl{excav_jewel};
    for my $i(0..$#weather_excav_jewels){
      $weather_excav_jewels[$i] = int($weather_excav_jewels[$i] * 0.75);
    }
    $spl{excav_jewel} = join ",", @weather_excav_jewels;
    $temp_mes .= "�i�v��΂���Q���󂯂܂���<br>";
  }else{
    $spl{win_point} = int($spl{win_point} - 2);
    $temp_mes .= "�����_����Q���󂯂܂���<br>";
  }
  #��Ό���,�i�v���(excav_jewel)�����A�����_�����̂����ꂩ
  #3�ȉ��͖���,4,5��-1,����ȏ��-2(�i��ł���l�قǃ_���[�W)
  #�ł����������Q�[�������~����,,,
  return $temp_mes;

}

#========================================================================
#���t�@�����X�g���Ă�cgi domestic�Ƃ�?���m�F
#���t�@�����X��S�͂Ńe�X�g

sub use_wait_flag {
  my $flag = shift;
  $flag -= 1;
  if($flag < 0){
    $flag = 0;
  }
  return $flag;
}
#====================================
#��΂̐F�ԍ�����͂��A�F�t���̕�Ζ����擾
sub splend_jewel_color {
  my $jewel_no .= shift;
  my $tmp_mes .= qq|<font color=$jewel_no>$jewels[$jewel_no][1]</font>|;
  return $tmp_mes;
}
#���� excavaters�̔ԍ� �o�� ���͂̔ԍ��Ɠ������A�x?�̃J�[�h�̔ԍ�(�����_��)
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
#�̌@(�K�v�ȔR���ƍ̌@�@�������āA��ꂽ��΂ƔR���̒l��Ԃ�)
#====================================
#�����@�~������΂�2��(no)(�z��) (�ړ�(dice)�ŕ�΃����_����1��)
sub excavate {
  my ($jewel1,$jewel2) = @_;
  my @e_jewels = ();#return�����΂̔z��
  for my $jewels (@jewels){#�z�񏉊���
    push @e_jewels,0;
  }
  #��{����================================
  $e_jewels[$jewel1] += 1;#��ފm��1��
  $e_jewels[$jewel2] += 1;#��ފm��1��
  return \@e_jewels;
}

#====================================
#�X�̔���֐�,��΁��̌@�@(reserve_excav�ȂǂŎg�p)
#====================================
#�����@jewel,,gold,excav(no)(not�z��),
#�߂�l�@1��0
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
  #����
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
#�X�̔���֐�,��΁������_ is_change_excav�ƍ��̂��Ă�������������Ȃ�
#====================================
#����
#�߂�l
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
  #����
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
#�_�C�X����
#========================================================================
#wait���� �f�[�^���[�h���Ɏg�p
#�O���[�o���ϐ�,�O���[�o���֐��Q��
sub reload_wait {
  my ($rw_sec,$rw_min,$rw_hour,$rw_mday,$rw_month,$rw_year,$rw_wday,$rw_stime) = localtime($spl{last_roadtime});
  my $road_count = &is_wait_time($spl{last_roadtime});
  $spl{last_roadtime} = $time;
  $spl{road_count} = "$road_count";
  $spl{turn_allroad} += $road_count;#�X�V��ݐ��ǉ�

  my @reload_counts = ('jewel_flag','card_flag','dice_flag');
  for my $count(@reload_counts){
    $spl{$count} += $road_count;
    if($spl{$count} > $reloadmax_jewel_flag){$spl{$count} = $reloadmax_jewel_flag;}
  }
  return;
}
#�O���[�o���ϐ��Q�Ɗ֐�
sub is_ngflag_spl {
  $is_flag = shift;
  if(!$is_flag){
    $mes .= "�����۰�ގ��Ԃ܂ł��҂���������<br>";
    &n_menu;
    $m{tp} = 100;
    return 1;
  }
  return 0;
}

#���2��@7���X�V
#
#�߂�l�@���X�V��
#����N�̂܂����͍l������Ă��Ȃ����A�Q�[�����g���������Ō��̂܂������x�͍������������

sub is_wait_time {
  my $ftime = shift;
  #time,ftime�̕ϊ�,$reload_hour�ŏC��
  my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time - $reload_hour * 3600);
  my ($f_sec,$f_min,$f_hour,$f_mday,$f_month,$f_year,$f_wday,$f_stime) = localtime($ftime - $reload_hour * 3600);

  #�ߑO���ߌォ����(7����(reload_hour)�ŕ␳���Ă��邱�Ƃɒ���)
  my $f_is_hour = 0;
  my $is_hour = 0;
  if($f_hour >= 12){$f_is_hour = 1;}
  if($hour >= 12){$is_hour = 1;}
  #���̓���0��00����time���擾
  my $tmp_times .= &time_to_date($time - $reload_hour * 3600);
  $tmp_times = &date_to_time($tmp_times);

  my $tmp_f_times .= &time_to_date($ftime - $reload_hour * 3600);
  $tmp_f_times = &date_to_time($tmp_f_times);
  #0��00�����m�Ōv�Z,12���ԂŊ��邱�ƂōX�V�񐔂��Z�o
  #����ɌߑO(7am����7pm)or�ߌ�(7pm����7am)���v�Z�ɓ����
  my $m_cal = int(($tmp_times - $tmp_f_times) / (3600 * 12)) + $is_hour - $f_is_hour;

  return $m_cal;
}


#���� �l,spl_keys
#keys�ɑΉ������z����`�F�b�N���ď̍����l��
#�o�� ($spl{achieves}��ύX)
sub splend_achievement_check {
  #akey��data��achieve�t�@�C����array�Ɩ��O������
  my ($anum,$akey,$atype) = @_;
  my ($anum_n,$anum_a) = split /,/, $anum;
  if($atype eq 2){#max_range�Ȃ�
    $anum_n = $anum;
    $anum_a = $spl{$akey};
  }
  require "$data_file_2";
  my $achieve_count = $#{ 'achieve_'.$akey };
  my $tmp_mes = "";
  $anum_a++;
  for my $i($anum_a..$achieve_count){
    if($anum_n >= ${ 'achieve_'.$akey }[$i][2]){
      $tmp_mes .= qq|<font color=#ffd700>���сu|;
      $tmp_mes .= qq|${ 'achieve_'.$akey }[$i][3]|;
      $tmp_mes .= qq|�v����������܂���!</font><br>|;
      $anum_a = $i;
    }
  }
  $spl{$akey} = join ",", ($anum_n,$anum_a);
  return $tmp_mes;
}
sub splend_achievement_array {
  #array�ł�akey��spl���擾����p�Ƃ��Ă��g�p(�������data��achieve�t�@�C����array�Ɩ��O������)
  #$atype��1��(�z��=�l����),2��(�z��=��ނŁA0�łȂ��l�̐�=�l����)�Ƃ���
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
      $tmp_mes .= qq|<font color=#ffd700>���сu|;
      $tmp_mes .= qq|${ 'achieve_'.$akey }[$i][3]|;
      $tmp_mes .= qq|�v����������܂���!</font><br>|;
      $spl{$akey} = $i;
    }
  }
  return $tmp_mes;
}

#�����l ���Z�l,���Z����Ώ�
#splend_achievement_check�Ǝg���Ώۂ�����
sub splend_achievement_regist {
  my ($aaddnum,$anum) = @_;
  my ($anum_n,$anum_a) = split /,/, $anum;
  $anum_n += $aaddnum;
  $anum = join ",", ($anum_n,$anum_a);
  return $anum;
}
#�����l ���Z������,���Z����Ώ�(�z��)
#�z��ɒǉ�(append)����ق�
#map_kind�Ȃǎ��ѓo�^�Ɏg�p
sub splend_array_add {
  my ($aaddkind,$anum) = @_;
  my @anum_array = split /,/, $anum;
  my $count_flag = 0;
  for my $i(0..$#anum_array){
    if($anum_array[$i] eq $aaddkind){$count_flag = 1;}
  }
  if(!$count_flag){push @anum_array, "$aaddkind";}#�V�K�̎�ނ��������z��ɒǉ� �z��=get������
  $anum = join ",", @anum_array;
  return $anum;
}
#====================================
sub splend_open_time_file {#���݂̎��Ԃ��擾��,�Q�[���̏󋵂��o��
  open my $tfh, "< $log_time_file" or &error("���޹ގ��ԍX�V�f�[�^���J���܂���");
  my $head_line = <$tfh>;
  my ($splend_last_time,$splend_start_time,$splend_end_time) = split /<>/, $head_line;
  close $tfh;
  my $splend_game_state = "";
  if($splend_start_time && $time > $splend_start_time){#�Q�[���J�n��
    $splend_game_state = "start";
  }elsif($splend_end_time && $time > $splend_end_time){#�Q�[���I����
    $splend_game_state = "end_func";
  }elsif(!$splend_end_time){#�Q�[���I����
    $splend_game_state = "end";
  }
  return $splend_game_state;
}
#====================================
#user�f�[�^
#====================================
#���v���C���[�f�[�^���[�h
sub road_user_data{
#	if(!-f "$user_file"){#���Ƃ�init_player_data�ɖ��ߍ���
#		open my $fh, "> $user_file" or &error("user�f�[�^���J���܂���");
#		close $fh;
#	}
	if(!-f "$user_file"){#�Q�[���I����̂��߂̏���,�t�@�C���쐬������init_player_data�ɖ��ߍ��ݍς�
    return;
	}
	open my $fh, "< $user_file" or &error("user�f�[�^���J���܂���");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$spl{$k} = $v; # $s
	}
	return;
}
#���v���C���[�f�[�^�ۑ�
sub write_user_data{
	my @spl_keys = (qw/
		fuel gold field_point win_point jewel excav_jewel excav achieves jewel_flag card_flag dice_flag disturb_flag reserves place max_range last_roadtime road_count turn_allroad buyable_card_kind
    max_excav max_field map_kind max_weather_damage rank max_kind_map is_achieve_end max_range_map
	/);
	my $line_spl = "";
	for my $k_spl (@spl_keys) {
		$line_spl .= "$k_spl;$spl{$k_spl}<>";
	}
	open my $fh, "> $user_file" or &error("user�f�[�^���J���܂���");
	print $fh "$line_spl\n";
	close $fh;
}
1#�폜�s��
