$mes .= qq|��ށy$m{lot}�z<br>| if $is_mobile && $m{lot};
#================================================
# �󂭂� Created by Merino
#================================================

# �󂭂��̒l�i
my $need_money = 1000;

# ���������ɓ��I���\���邩(��)
my $lot_cycle_day = 7;

# ����܂̏ܕi
my @wea_nos = (5,10,15,20,25,31,32);

# �Ϻޏ܂̏ܕi
my @egg_nos = (35..41);


#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($w{player} < 30) { # ��ڲ԰��30�l����
		$mes .= '����������<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	open my $fh, "+< $logdir/lot.cgi" or &error('�󂭂�̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my($lot_next_time, $round, $atari1,$no1, $atari2,$no2, $atari3,$no3) = split /<>/, $line;
	$round++;
	$round  = $round > 9 ? 1 : $round;
	
	# ���I���\����
	if ($time > $lot_next_time) {
		# �󂭂��̌i�i�ݒ�
		$no1 = $wea_nos[int(rand(@wea_nos))];
		$no2 = $egg_nos[int(rand(@egg_nos))];
		$no3 = int(rand(21)+20) * 10000;
		
		$lot_next_time = int($time + 24 * 3600 * $lot_cycle_day);
		$atari1 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari2 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari3 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari2 += 1 if $atari1 eq $atari2;
		$atari3 += 3 if $atari3 eq $atari1 || $atari3 eq $atari2;
		
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh "$lot_next_time<>$round<>$atari1<>$no1<>$atari2<>$no2<>$atari3<>$no3<>";
		close $fh;
		
		&write_send_news(qq|<font color="#FFCC00">�y�󂭂����I���\\�z<br>����܁y$atari1�z$weas[$no1][1]<br>�Ϻޏ܁y$atari2�z$eggs[$no2][1]<br>���ݏ܁y$atari3�z$no3 G</font>|);
	}
	close $fh;
	
	# ���I�҂�������ܕi�𑗂��
	if ($atari1 eq $m{lot}) {
		$mes .= "����!���I���߂ł�!�ܕi�� $weas[$no1][1] �͗a���菊�ɑ����Ă�������<br>";
		&send_item($m{name}, 1, $no1, $weas[$no1][4], 10);
		$m{lot} = '';
	}
	elsif ($atari2 eq $m{lot}) {
		$mes .= "����!���I���߂ł�!�ܕi�� $eggs[$no2][1] �͗a���菊�ɑ����Ă�������<br>";
		&send_item($m{name}, 2, $no2);
		$m{lot} = '';
	}
	elsif ($atari3 eq $m{lot}) {
		$mes .= "����!���I���߂ł�!�ܕi�� $no3 G�͑������Ă�������<br>";
		&send_money($m{name}, '�󂭂���', $no3);
		$m{lot} = '';
	}
	
	my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
	++$lmonth;
	
	my $round_old = $round == 1 ? 9 : $round -1;
	$mes .= qq|<font color="#FFCC00">�y��$round_old��̓��I�ԍ��z<br>����܁y$atari1�F$weas[$no1][1]�z<br>�Ϻޏ܁y$atari2�F$eggs[$no2][1]�z<br>���ݏ܁y$atari3�F$no3 G�z<br></font>|;
	$mes .= "�󂭂��͂P�� $need_money G����<br>";
	$mes .= "��$round��̓��I���\\�� $lmonth��$lday��$lhour��$lmin��������<br>";
	$mes .= '�V�����̂𔃂��ꍇ�́A�������Ă��邭������������<br>' if $m{lot};
	
	&menu('��߂�', '����');
}

sub tp_1 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $need_money) {
		open my $fh, "< $logdir/lot.cgi" or &error('�󂭂�̧�ق��ǂݍ��߂܂���');
		my $line = <$fh>;
		close $fh;
		my($lot_next_time, $round) = (split /<>/, $line)[0..1];
		++$round;
		$round  = $round > 9 ? 1 : $round;
		
		my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
		++$lmonth;
		
		$m{lot} = $round . sprintf("%03d", int(rand($w{player})) );
		$m{money} -= $need_money;
		
		$mes .= "�܂���!<br>���I���\\�� $lmonth��$lday��$lhour��$lmin��������<br>";
	}
	else {
		$mes .= "�������Ȃ���Ζ��������₵�Ȃ���<br>";
	}
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}


1; # �폜�s��
