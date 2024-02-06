require 'config.cgi';
require 'config_game.cgi';

#===================================================
#�N��͂������I��(1/20,22:00���)���C������ created by �����̂�
#===================================================
@message_newyear_lot = (
"�F�l�A���W�܂蒸�����肪�Ƃ��������܂��B�����肨�N�ʕt���N��͂������I����s���܂�",
"���̑���",#lot_system���ɑ����𖄂ߍ���
"1���͉�5���A2���͉�3���A3���͉�2���A4���͉�1���̈�v�œ��I�ƂȂ�܂�",
"�܂��e�܂̌i�i�́A1��200��G�A2��100��G�A3��30��G�A4��5��G�ƂȂ��Ă���܂�",
"����ł̓v���C���[�̊F�l�A& event����͂��A���茳�ɂ���_�C�X�����U�肭�������܂�",
"�W�v������...",
"$m{name}�̓_�C�X��U�����I$prize_grade���܂̒��I�ԍ��́A��5��",#lot_system���ɑ����𖄂ߍ���
"$m{name}�̓_�C�X��U�����I$prize_grade���܂̒��I�ԍ��́A��3��",#lot_system���ɑ����𖄂ߍ���
"$m{name}�̓_�C�X��U�����I$prize_grade���܂̒��I�ԍ��́A��2��",#lot_system���ɑ����𖄂ߍ���
"$m{name}�̓_�C�X��U�����I$prize_grade���܂̒��I�ԍ��́A��1��",#lot_system���ɑ����𖄂ߍ���
"�S�Ă̔ԍ����o�����܂����I���I�������ɂ͍��؃v���[���g�𑡒悢�����܂��I",
"�Ȃ��A����ɂ��������I�𓦂��Ă��܂������X�ɂ��i�i�����p�ӂ��Ă���܂��̂ŁA�����S��������",
"����ɂē����I����I���Ƃ����Ă��������܂��B���N�����I�������ڂ̒���낵�����肢���܂��B"
);

#�e���̏܋��z�@shopping_greeting_card_lotcheck.cgi�ɂ����l�̔z�񂪂���̂ŕύX����Ƃ��͂�������
my @lot_grade_money = (2000000,1000000,300000,50000);

#lot_system�A���X�V�֎~����
my $bad_time_newyearlot = 15;

#1����4���܂ł̊e�܂̉�n��(��n������v����Ɠ��I����)
my @lot_last_n_digit = (5,3,2,1);
#my $lot_last_n_digit_num = 4;
#my $lot_first_lastdigit = 6;
#my $lot_second_lastdigit = 4;
#my $lot_third_lastdigit = 3;
#my $lot_fourth_lastdigit = 2;

#1����4���܂ł̔ԍ��̐�
my $lot_first = 1;
my $lot_second = 2;
my $lot_third = 3;
my $lot_fourth = 2;

#�ȉ�message_newyear_lot(�C�x���g���b�Z�[�W�\��)�A�����𓮂����ꍇ�͈ʒu�ɒ��ӁA1�X�^�[�g�Ȃ̂Œ���
my $lotsys_sponsorship = 2;#�X�|���T�[�̕\���^�C�~���O
my $lotsys_gather = 6;#�ǂ̃^�C�~���O�ŏW�v���邩
my $lotsys_reveal_start = 7;#���\�J�n
my $lotsys_reveal_end = 11;#���\�I��

# lot_sponsorship�Ŏg�p�A
my @files = (
#	['����',		'۸�̧�ٖ�(shop_list_xxxx���̕���)'],
	['���l�̂��X',	'',			'��'],
	['���̉攌��',	'picture',	'��'],
	['�ޯ�ϰ���',	'book',		'��'],
	['���l�̋�s',	'bank',		'��'],
);

sub lot_reveal{#lot_system�Ŕԍ��𔭕\���鎞�Ɏg�p
  my($prize_grade) = @_;
  my @prize_number = ();
  open my $fh, "< $logdir/greeting_card_summary.cgi" or &error("���̂悤��$userdir/$id/greeting_card_summary.cgi�����݂��܂���");
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

sub lot_show{#�����A���ʁA�Ԃ�ln���̓��I��
  my($prize_grade) = @_;
#@
  my $won_lot = 0;#���I��
#  my $i = 0;
  my @lot_f_show = ();
#  my @lot_s_show = ();
#  my @lot_t_show = ();
#  my @lot_fo_show = ();
  open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("���̂悤��$userdir/$id/greeting_card.cgi�����݂��܂���");
  while(my $line = <$fh>){
    my($mname,$yname,$newyear_lot_num) = split /<>/, $line;
    push @lot_f_show, &lot_calculate($newyear_lot_num,$lot_last_n_digit[$prize_grade - 1]);
#    push @lot_s_show, &lot_calculate($lot_f_show[i],4);
#    push @lot_t_show, &lot_calculate($lot_s_show[i],3);
#    push @lot_fo_show, &lot_calculate($lot_t_show[i],2);
  }
  close $fh;

  open my $fh, "< $logdir/greeting_card_summary.cgi" or &error("���̂悤��$logdir/greeting_card_summary.cgi�����݂��܂���");
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
  #main.cgi�Ȃǂœ��I�m�F������Ƃ��̏����A

}

sub lot_main{#���I�ԍ������肷�鏈��
  my @A = ();#���ƂŃt�@�C���ɓ\��t���钆�g
  my @line_lotnum = ();#�euser�̒��I�ԍ�������
  my @line_id = ();#���I�ҏd���h�~�p��id���X�g
  opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
  while (my $id = readdir $dh) {
    next if $id =~ /\./;
    next if $id =~ /backup/;

    my %m = &get_you_datas($id, 1);

    unless (-f "$userdir/$id/greeting_card.cgi") {
      open my $fh, "> $userdir/$id/greeting_card.cgi";
      close $fh;
    }
    open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("���̂悤��$userdir/$id/greeting_card.cgi�����݂��܂���");
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

  open my $fh, "> $logdir/greeting_card_summary.cgi" or &error("���̂悤��$userdir/$id/greeting_card_summary.cgi�����݂��܂���");
  my $time_next = $time + 3600 * 24 * 364;

  print $fh "$time<>$time_next<>\n";

  for my $i (0..$lot_first-1){
    my $p_n = $lot_fnum;#�d���h�~�p
    $lot_fnum = rand($#line_lotnum);
    if($line_id[$p_n] eq $line_id[$lot_fnum] && i != 0){#�I�o������
      $lot_fnum = rand($#line_lotnum);
    }
    my($mname,$yname,$newyear_lot_num) = split /<>/, $line_lotnum[$lot_fnum];
    $newyear_lot_num = &lot_calculate($newyear_lot_num,$lot_last_n_digit[0]);
    print $fh "1<>$mname<>$yname<>$newyear_lot_num<>\n";
  }

  for my $i (0..$lot_second-1){
    my $p_n = $lot_snum;#�d���h�~�p
    $lot_snum = rand($#line_lotnum);
    if($line_id[$p_n] eq $line_id[$lot_snum] && i != 0){#�I�o������
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

sub lot_system{#�S�̃V�X�e��(���I��̐i�s������֐�)�A���b�Z�[�W��_write_tag.cgi�ɕԂ�
#$lotsys_newyear:0�X�^�[�g�O�A1�X�^�[�g
  my $lotsys_newyear = 0;
  my $time_next = 0;#lot_system�̍X�V�A�Ŗh�~�p�A����̊J�Ó��̎w��⏕
  my $message_lot = "";

  open my $fh, "< $logdir/event_switch.cgi" or &error("���̂悤��$logdir/event_switch.cgi�����݂��܂���");
  while(my $line = <$fh>){
    my($time_next_r,$lotsys_newyear_r) = split /<>/, $line;
    $lotsys_newyear = $lotsys_newyear_r;
    $time_next = $time_next_r;
  }
  close $fh;

  if($time > $time_next && (&on_new_year_end || &on_new_year_end_lot) && $lotsys_newyear eq 0){
    $lotsys_newyear = 1;#�J�n
		&write_world_news("<i>BJ���N�ʕt���N��͂������I��J�Â���܂����I</i>");
  }
	if($time_next > $time && $lotsys_newyear ne 0){
		$message_lot = "���X���҂���������";
		return $message_lot;
	}
  if($lotsys_newyear){
    $message_lot = $message_newyear_lot[$lotsys_newyear - 1];
    if($lotsys_newyear eq $lotsys_sponsorship){#�X�|���T�[(����グ1��)�̕\��
      @sponsors_sys = @{&lot_sponsorship()};
      my $length_lotsys = @sponsors_sys;
      for my $i (1..$length_lotsys){
        $message_lot .= $i == $length_lotsys ? "$sponsors_sys[$i - 1]" : "$sponsors_sys[$i - 1],";
      }
			$message_lot .="�̒񋟂ł����肵�Ă���܂�";
    }
    if($lotsys_newyear eq $lotsys_gather){#�W�v����
      &lot_main;
    }
    if($lotsys_newyear >= $lotsys_reveal_start && $lotsys_newyear < $lotsys_reveal_end){#���I�ԍ���\��
			my $prize_grade_lotsys = $lotsys_newyear - $lotsys_gather;
      my @prize_number_w = @{&lot_reveal($prize_grade_lotsys)};
      my $length_lotsys = @prize_number_w;
			my $message_lotsys_world = "";
      for my $i (1..$length_lotsys){
#        $message_lot .= "$i,";
        $message_lot .= $i == $length_lotsys ? "$prize_number_w[$i - 1]�I" : "$prize_number_w[$i - 1],";
				$message_lotsys_world .= "$prize_number_w[$i - 1],";
      }
			&write_send_news("$prize_grade_lotsys ���̓��I�ԍ�,��$lot_last_n_digit[$prize_grade_lotsys - 1]��$message_lotsys_world");
    }
    $lotsys_newyear++;
		$time_next = $time + 30;
    if($lotsys_newyear > $#message_newyear_lot + 1){#�I������
			$time_next = $time + 3600 * 24 * 364;
      $lotsys_newyear = 0;
    }
  }else{
    $message_lot = "���݃C�x���g�͊J�Â���Ă��܂���";
  }

  open my $fh, "> $logdir/event_switch.cgi" or &error("���̂悤��$logdir/event_switch.cgi�����݂��܂���");
  print $fh "$time_next<>$lotsys_newyear<>\n";
  close $fh;

  return $message_lot;

}

sub lot_calculate{#���ƒ��I�ԍ��������Ƃ��āA��n���݂̂�Ԃ��A
  my($p_num_cal,$digit) = @_;
  $f = int($p_num_cal % (10 ** $digit));
  return $f;
}

sub lot_sponsorship{#����グ1�ʂ̓X���X�|���T�[�Ƃ��ĕ\��
  @sponsors = ();
  for my $i (0..$#files){
    my $type = $files[$i][1] ? "_$files[$i][1]" : '';
    my $this_file = "$logdir/shop_list${type}.cgi";
    open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
    my $line = <$fh>;
    my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
    push @sponsors, $shop_name;
    close $fh;
  }
  return \@sponsors;
}

sub lot_delete{#2/1�ɔN���f�[�^�Ȃǂ����X�폜�Amain.cgi�ɔz�u
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		unlink "$userdir/$id/is_on_greeting_card.cgi" or &error("$userdir/$id/is_on_greeting_card.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$userdir/$id/greeting_card.cgi"){
		unlink "$userdir/$id/greeting_card.cgi" or &error("$userdir/$id/greeting_card.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$userdir/$id/greeting_card_switch.cgi"){
		unlink "$userdir/$id/greeting_card_switch.cgi" or &error("$userdir/$id/greeting_card_switch.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$userdir/$id/is_get_greeting_card.cgi"){
		unlink "$userdir/$id/is_get_greeting_card.cgi" or &error("$userdir/$id/is_get_greeting_card.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$logdir/december_pet_sale.cgi"){
		unlink "$logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$userdir/$id/december_soba.cgi"){
		unlink "$userdir/$id/december_soba.cgi" or &error("$userdir/$id/december_soba.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
}

1;#�폜�s��
