require "./lib/greeting_card_lot.cgi";
#================================================
#�N��󒊑I�m�F��
#================================================
#greeting_card_lot.cgi�ł��z�u�������Ǔ����Ȃ������̂ł������ɂ��u��
my @lot_grade_money = (2000000,1000000,300000,50000);

#1����4���܂ł̊e�܂̉�n��(��n������v����Ɠ��I����)
my @lot_last_n_digit = (5,3,2,1);

#���� �����_���I���̃y�b�g���o������m�� 1/$per_rand_pet
my $per_rand_pet = 10;
#���� �����y�b�g�̐�
my $sale_pet_num = 3;

#================================================
sub begin {
	if ($m{tp} > 1) {
#		$mes .= '<br>';
		$m{tp} = 1;
		$mes .= '�N��͂����̓��I�m�F<br>';
	}
	else {
		$mes .= '�N��͂����̓��I�m�F<br>';
		$mes .= '�������Ă�Ƃ�����<br>';
	}
	@menus = ('��߂�','���ܔ̔�');
	if(&on_new_year_end){#�N��󂭂�
		push @menus, '���I�m�F������';
		push @menus, '��������';
	}
	&menu(@menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		$mes .= "���Ɍi�i��������Ă��܂�<br>";
		&begin;
		return;
	}
	if($cmd eq 1) {
		$mes .= "�V�t���܎s!<br>���12��G��3����̃y�b�g�𔃂����";
		&menu('��߂�', '�w������');
		return;
	}elsif ($cmd eq 2) {
		open my $fh, "> $userdir/$id/greeting_card_switch.cgi" or &error("���̂悤��$userdir/$id/greeting_card_switch.cgi���J���܂���");
#		my $ii = @lot_last_n_digit;
		for my $i (1..($#lot_last_n_digit + 1)){
			my $won_sum_newyear = 0;
			$won_sum_newyear = &lot_show($i);
#			$mes .= "$i<br>";
			$mes .= "$i����$won_sum_newyear�񓖑I���܂����I<br>";
			my $time_next = $time + 3600 * 24 * 364;
			print $fh "$i<>$won_sum_newyear<>\n";
		}
		close $fh;

		open my $fh, ">> $userdir/$id/is_get_greeting_card.cgi"or &error("$userdir/$id/is_get_greeting_card.cgi���J���܂���");
		close $fh;#���I�m�F�����������ǂ������肷��t�@�C���쐬

		&begin;
	}elsif($cmd eq 3){
		$mes .= '�莝�����������Ȃ��悤���ӂ��܂��傤<br>';
		$mes .= "�͂������������܂����H<br>";
		$mes .= '1��:300��G<br>2��:100��G<br>3��:30��G<br>4��:5��G<br>';
		&menu('��߂�', '����');
	}else{
		&begin;
	}
}
#================================================
#���ܔ̔�(pet_sale)
#================================================
#�t�@�C����
#userdir/$id/is_pet_sale.cgi,logdir/december_pet_sale.cgi
sub tp_100 {
	return if &is_ng_cmd(1);
	if(!-f "$logdir/december_pet_sale.cgi"){
		$mes .= "�������܂���<br>";
		$mes .= "���N����낵�����肢�������܂�<br>";
		&begin;
		return;
	}
	if(!-f "$userdir/$id/is_pet_sale.cgi"){#�t�@�C�������݂��Ȃ��ꍇ
		open my $fh, "> $userdir/$id/is_pet_sale.cgi" or &error("$userdir/$id/is_pet_sale.cgi���쐬�ł��܂���");
		print $fh 0;
		close $fh;
	}
	open my $fh, "< $userdir/$id/is_pet_sale.cgi" or &error("���̂悤��$userdir/$id/is_pet_sale.cgi�����݂��܂���");
	my $head_line = <$fh>;
	my ($last_time) = split /<>/, $head_line;
	close $fh;

	if (&time_to_date($time) ne &time_to_date($last_time)) {#�����ׂ��ł�����
		my $rand_pet = int(rand($per_rand_pet));#�����_���y�b�g�o������
		my @sale_pets = ();#���܂̃y�b�g(�y�b�gNo)
		#===========================================
		my $pets_count = 0;#�������̕��ܓ��̃y�b�g�� $#sale_pets�̋������|���̂ŕ���
		if($rand_pet eq 0){#�����_���y�b�g���o�����鎞
			my $i = int(rand($#pets));
			push @sale_pets,$i;#send_item�p��push
			$pets_count++;
		}
		#===========================================
		my $count = 0;
		my @new_line = ();
		open my $fh, "< $logdir/december_pet_sale.cgi" or &error("���̂悤��$logdir/december_pet_sale.cgi�����݂��܂���");
		while(my $line = <$fh>){
			push @new_line,$line;
			$count++;
		}
		close $fh;
		#===========================================
		my $new_sale_pet_num = $sale_pet_num - $pets_count;#�����_���Œǉ������y�b�g������������
		for my $i(1..$new_sale_pet_num){#������december_pet_sale������o��
			my $s_pet_no = int(rand($count));#line���o��
			my ($name, $kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line[$s_pet_no];#�y�b�gno�擾
			push @sale_pets,$item_no;#send_item�p��$item_no��push
			splice(@new_line,$s_pet_no,1);#new_line������o����line���폜
			$count--;
		}
		#december_pet_sale.cgi�X�V=====================
		open my $fh, "> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgi���쐬�ł��܂���");
		print $fh @new_line;
		close $fh;
		if($#new_line < 2){#�y�b�g���Ȃ��Ȃ�����(2�ȉ��̎�)
			unlink "$logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgi���폜���邱�Ƃ��ł��܂���");
		}
		#send_item===================================
		for my $s_pet(@sale_pets){
			#my($send_name, $kind, $item_no, $item_c, $item_lv) = @_;
			&send_item($m{name}, 3, $s_pet, 0, 0, 1);
		}

		$m{money} -= 120000;
		$mes .= "���܂��w�����܂���!<br>";
		$mes .= "�w�������y�b�g�͗a���菊�ɑ����܂���<br>";
		#is_pet_sale.cgi(user�f�[�^)��last_time�̏�������===============
		open my $fh, "> $userdir/$id/is_pet_sale.cgi" or &error("$userdir/$id/is_pet_sale.cgi���쐬�ł��܂���");
		print $fh "$time<>\n";
		close $fh;
	}else{
		$mes .= "1��1�܂ōw���ł��܂�<br>";
		&begin;
		return;
	}
	#time_to_date�𗘗p���Ĕ���
	#rand�Ńy�b�g������ǂ����I���@�ȉ�����Ȃ�����
	#�����_���ɑI��
	#�I���������̂�send�p��push�A����ȊO���������ݗp��push,(�ꉞakindo�������`�F�b�N���čœK��)
	#send_item3��
	#is_pet_sale.cgi���쐬
	&begin;
	return;
}
#================================================
#�N���i�i�󂯎��
#================================================
sub tp_300 {
	return if &is_ng_cmd(1);
	unless(-f "$userdir/$id/is_get_greeting_card.cgi"){
		$mes .= "�܂����I�m�F����K�v������܂�<br>";
		&begin;
		return;
	}
	if(-f "$userdir/$id/is_on_greeting_card.cgi"){
		$mes .= "���Ɍi�i��������Ă��܂�<br>";
		&begin;
		return;
	}#�ꉞ�����ɂ��z�u
	my $count_no_lot = 0;#���I���Ȃ������񐔂��J�E���g
	open my $fh, "< $userdir/$id/greeting_card_switch.cgi" or &error("���̂悤��$userdir/$id/greeting_card_switch.cgi�����݂��܂���");
	while(my $line = <$fh>){
		my($prize_grade,$won_sum_newyear) = split /<>/, $line;
		my $money = $lot_grade_money[$prize_grade - 1] * $won_sum_newyear;
		$m{money} += $money;
		$mes .= "$prize_grade����$money G���󂯎��܂���<br>";
		$count_no_lot++ if $money eq 0;
#		push @line_lotnum, "$yname<>$mname<>$newyear_lot_num<>\n";
#      push @line_lotnum, ($yname,$mname,$newyear_lot_num);
#		push @line_id, $yname;
	}
	close $fh;
	if($count_no_lot - 1 == $#lot_last_n_digit){#1������I���Ȃ������l��ȵʽ�ڂ�ʽ��
		if(rand(2) == 0){
			&send_item($m{name}, 2, 53, 0, 0, 1);
		}else{
			&send_item($m{name}, 2, 53, 0, 0, 1);
		}
		$mes .= "�Q���܂��󂯎��܂���<br>";
	}
	#�t�@�C�������2��ȏ�i�i����Ȃ��悤�ɂ���
	open my $fh, ">> $userdir/$id/is_on_greeting_card.cgi"or &error("$userdir/$id/is_on_greeting_card.cgi���J���܂���");
	close $fh;

	unlink "$userdir/$id/is_get_greeting_card.cgi" or &error("$userdir/$id/is_get_greeting_card.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	&begin;
}

1;#�폜�s��
