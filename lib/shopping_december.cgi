#================================================
# �N���C�x���g
#=================================================

# �N�����o
@shop_list = (
#    cmd, ���i, ���z
	[1, '�N�z������', 10000],
);

# �C���A�N���𔃂��l�i
my $buy_price  = 500;

# �N�����o �y�b�g���p�z
my $sell_pet_price = 30000;

#�����l���瓯���l���Ă̔N���̖������
my $no_duplicate_num = 5;

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '�����[�V�c�a����<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�悢�N�z����<br>';
	}

	&menu('��߂�','�C���𔃂�','�N���𑗂�','�N���s');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;

	if ($cmd eq '1') {
		if(&on_december_end) {
			$mes .= '�N���X�}�X�͂܂����N<br>';
			&begin;
			return;
		}
		$mes .= "�C��������?<br>�Е������Ȃ����� $buy_price G�ł��<br>";
		&menu('��߂�','����');
	}elsif ($cmd eq '2') {
		$mes .= "���ǂ����܂� $buy_price G�ő���<br>";
		&menu('��߂�', '����');
	}elsif ($cmd eq '3') {
		$mes .= "�N������!<br>";
		if(&on_december_end) {
			&menu('��߂�', '����', '����');
		}else{
			&menu('��߂�', '����');
		}
	#		if(!&on_december_end) {
	#			$mes .= '�ؽϽ��܂ŏ������݂����E�E�E<br>';
	#			&begin;
	#			return;
	#		}
	}else{
		&begin;
	}
}

#=================================================
# �C��
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);

	if ($m{money} < $buy_price) {
		$mes .= '���O�n�R�B���킢������������B�Е������Ȃ����ǂȁB<br>';
	}
	else {
		$m{money} -= $buy_price;
	}
	if ($m{sox_kind}) {
		$mes .= '�����C���͗p�ӂ��Ă��邯�Ǖʂ̂Ǝ��ւ��悤<br>';
	}
	$mes .= '�C���ɂǂ�Ȋ肢����悤��';

	$m{tp} += 10;
	&menu('��ٍ��m', '�̫��', '���̊G���~����', '�������������킪�~����');
}

sub tp_110 {
	if ($cmd eq '0') {#��ٍ��m
		$m{sox_kind} = 10;
		$m{sox_no} = 183;
		&begin;
	} elsif ($cmd eq '1') {#�̫��
		if (rand(10) < 1) {
			$m{sox_kind} = 20;
			$m{sox_no} = 168;
		} else {
			$m{sox_kind} = 50;
			$m{sox_no} = 191;
		}
		&begin;
	} elsif ($cmd eq '2') {#���̊G���~����
		$mes .= '�ǂ̊G���~�����H';
		$m{tp} += 10;
		&menu('��ý�', '���̐l�̊�G');
	} else {#�������������킪�~����
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
	$m{sox_picture} = $in{file_name};#�t�@�C�������C���̒��g�ɂ���
	$mes .= "�T���^����ɂ��肢���܂����I<br>";
	&begin;
}
#=================================================
# �N���
#=================================================
sub tp_200 {
	return if &is_ng_cmd(1);
	$mes .= "�N�ɔN���𑗂�܂���?<br>";
	$mes .= "���ʂ͈���ς݂Ȃ̂ŏ����K�v�͂Ȃ���?<br>";

	$mes .= qq|<form method="$method" action="$script"><p>�����F<input type="text" name="to_name" class="text_box1"></p>|;
	$mes .= qq|<p>�����F<input type="text" name="from_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">����<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_210 {
	return if &is_ng_cmd(1);

	if ($m{money} < $buy_price) {
		$mes .= '�͂����㑫��Ȃ��B�A��B<br>';
	}
	elsif($in{to_name} eq $m{name}){
		$mes .= '�����ɑ��邱�Ƃ͂ł��܂���<br>';
	}
	else {
		my $to_id = unpack 'H*', $in{to_name};
		unless(-f "$userdir/$to_id/greeting_card.cgi"){
			open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("�|�X�g���J���܂���");
			close $fh;
		}
		my $count_for_duplicate = 0;#�����l����̎莆��5�ʂ܂�
		open my $fh2, "< $userdir/$to_id/greeting_card.cgi" or &error("�|�X�g���J���܂���");
		while(my $lines = <$fh2>){
			my($from_name_g,$id_g,$number_g) = split /<>/, $lines;
			$count_for_duplicate++ if $id_g eq $id;
		}
		close $fh;
		if ($no_duplicate_num < $count_for_duplicate) {
			$mes .= "�����l��$no_duplicate_num����葽���N���͑���܂���<br>";
			&begin;
			return;
		}
		$m{money} -= $buy_price;
		my $number = int(rand(1000000000));
		open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("�|�X�g���J���܂���");
		print $fh "$in{from_name}<>$id<>$number<>\n";
		close $fh;
	}
	&begin;
}
sub seek_from_contest{
	#���ʂȏ����������Ă���Ǝv���̂ł��������C��������by�C��
	my $this_file      = "$userdir/$id/shop_$goods_dir.cgi";
	my $this_path_dir  = "$userdir/$id/$goods_dir";
	my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
	$layout = 2;
	my $count = 0;
	my $sub_mes .= qq|<form method="$method" action="$script"><hr><input type="radio" name="file_name" value="0" checked>��߂�|;
	require "$datadir/contest.cgi";
	open my $fh, "< $logdir/legend/picture.cgi" or &error("$logdir/legend/picture.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($round, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
		$sub_mes .= qq|<hr><img src="$logdir/legend/picture/$file_name" style="vertical-align:middle;"> ��$round��$contests[$in{no}][0]�D�G��i�w$file_title�x��: $name|;
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">|;
	}
	close $fh;
	$mes .= qq|���ɂ̔�<br>|;
	$mes .= qq|$sub_mes<hr>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�������ɂ��肢" class="button1"></p></form>|;

}


#=================================================
# �N�����o
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..2);

	if($cmd eq 1){
		$mes .= "�����Ă����߯Ă� $sell_pet_price G�Ŕ��邱�Ƃ��ł����<br>";
		$mes .= '�ǂ�����?';
		$m{tp} += 20;
		&menu('��߂�', '����');
	}elsif($cmd eq 2){
		$layout = 1;
		$mes .= '�����������H<br>';

		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= $is_mobile ? qq|<hr>���i/���z<br>|
			: qq|<table class="table1" cellpadding="3"><tr><th>���i</th><th>���z<br></th>|;

		for my $shop_ref (@shop_list) {
			my @shop = @$shop_ref;
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$shop[0]">$shop[1]/$shop[2] G<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$shop[0]">$shop[1]</td><td align="right">$shop[2] G<br></td></tr>|;
		}

		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;

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

			#�t�@�C���쐬
			open my $fh, "> $userdir/$id/december_soba.cgi" or &error("$userdir/$id/december_soba.cgi̧�ق��ǂݍ��߂܂���");
			close $fh;
			$mes .= 'hp��mp���S�񕜂��܂���<br>';
			$mes .= '��J�x�������񕜂��܂���<br>';
			$mes .= '���x����I���N����낵���ȁI<br>';
		}elsif(-f "$userdir/$id/december_soba.cgi"){
			$mes .= '�N�z����1��ŏ\�������I�I<br>';
		}else{
			$mes .= '�悭���Ă݂�I�@�[�j������˂����I�I<br>';
		}
	}else{
		$mes .= '��߂܂���<br>';
	}
	&begin;
	return;
}

sub tp_320{
	return if &is_ng_cmd(1);

	if($cmd eq 1){
		if($m{pet} > 0){
			$m{money} += $sell_pet_price;

			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�𔄂�܂���<br>";
			#�t�@�C���쐬�����A�폜������greeting_card_lot.cgi��lot_delete�֐��ɖ��ߍ��݂���===============================
			if(!-f "$logdir/december_pet_sale.cgi"){
				open my $fh, "> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgi���J���܂���");
				close $fh;
			}
			#=================
			open my $fh, ">> $logdir/december_pet_sale.cgi" or &error("$logdir/december_pet_sale.cgi���J���܂���");
			print $fh "$m{name}<>3<>$m{pet}<>$m{pet_c}<>0<>\n";#3�Ƃ����͓̂���̎��(pet��3)��\�����́@0��item_lv ���㕐��◑�𔄂邱�Ƃ�z��
			close $fh;
			$m{pet} = 0;
			$m{pet_c} = 0;

			#=================
		}else{
			$mes .= "�߯Ă������Ă��܂���<br>";
		}
	}else{
		$mes .= '��߂܂���<br>';
	}
	&begin;
	return;
}
1; # �폜�s��
