require "$datadir/skill.cgi";
require "$datadir/pet.cgi";
#=================================================
# �ð����� Created by Merino
#=================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['��߂�',		'main'],
	['����ߒ�',		'myself_stamp'],
	['�ڸ���ٰ�',	'myself_collection'],
	['��ٌp��',		'myself_skill'],
	['�̍���ύX',	'myself_shogo'],
	['��̂�ύX',	'myself_mes'],
	['���ȏЉ�',	'myself_profile'],
	['���l�̂��X',	'myself_shop'],
	['��@�J�W�m',	'myself_casino'],
	['ϲ�߸��',		'myself_picture'],
	['ϲ�ޯ�',		'myself_book'],
	['���l�̋�s',	'myself_bank'],
	['�l�ݒ�',	'myself_config'],
	['�ޯ�����',	'myself_backup'],
);

if ($m{valid_blacklist}) {
	push @menus, ['����', 'myself_blacklist'];
	push @menus, ['������', 'myself_blacklist_chatpublic'];
	push @menus, ['��c������', 'myself_blacklist_country_bbs'];
}

#================================================
sub begin {
	if (-f "$userdir/$id/goods_flag.cgi") {
		unlink "$userdir/$id/goods_flag.cgi";
	}

	$layout = 2;
	$is_mobile ? &my_status_mobile : &my_status_pc;
	&menu(map{ $_->[0] }@menus);
}
sub tp_1 {
	# �uϲٰсv���J����TOP�ɖ߂胍�O�C������Ɠ�̋�Ԃɋ��܂�iҲ݉�ʂɂ��邪Ҳ݉�ʂ����r���[�B���܂�j
	# ���� lib �� is_ng_cmd �ź���މ�������Ă����� begin �����s���邽�ߖ��͂Ȃ����Aϲٰт� begin ���Ă�ł��Ȃ��������߃o�O���Ă�
	# is_ng_cmd �������ł��Ȃ�����ނȂ̂ŁA�Ƃ肠��������ނ������͂Ȃ牘������Ă���Ƒz�肵 begin �����s
	# ���̏C���O�̘b���A���̏C���Œ���Ƃ͎v���Ȃ����Aϲٰтɓ�������ԂŃX�}�z���ċN�����ă��O�C�������� begin �֐�����`�G���[�����������Ƃ����񍐂���
	unless ($in{mode}) { # ϲٰїp�̺���މ��������i���g���Ȃ��C�R�[�������j
		return if &is_ng_cmd(1..$#menus); # ϲٰїp�̺���ނƒʏ�̺���ނǂ������������Ă���
		&b_menu(@menus); # ϲٰїp�̺���ނ͉�������Ă��邪�A�ʏ�̺���ނ͉�������Ă��Ȃ�
		return;
	}

	# �߯Ďg�p
	if ($in{mode} eq 'use_pet' && $m{pet} && ($pets[$m{pet}][2] eq 'myself' || ($m{pet} == 31 && &is_ceo))) {
		&refresh;
		&n_menu;

		require './lib/_use_pet_log.cgi';

		# �����Ȃ̏ꍇ
		if ($m{pet} >= 128 && $m{pet} <= 130) {
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A$m{name}�̂��Ƃ������ƌ��Ă���c<br>";
			$m{lib} = 'add_monster';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 168){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�َ����ւ̔����J����<br>";
			open my $fh, "> $userdir/$id/upload_token.cgi";
			close $fh;

			$m{lib} = 'shopping_upload';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 177){
			if ($m{act} >= 100) {
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A$m{name}��S���ւƗU�����Ƃ��������Ă����̂Œf����<br>";
			}else {
				&write_use_pet_log($id, $m{pet});
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A$m{name}��S���ւƗU����<br>";

				$m{lib} = 'prison';
				$m{tp}  = 300;
			}
		}
		elsif ($m{pet} == 175){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A���݂ɂ���������d�|���悤�Ƃ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 176){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�̍��ɂ���������d�|���悤�Ƃ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 200;
		}
		elsif ($m{pet} == 185){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A���z�ɂ���������d�|���悤�Ƃ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 300;
		}
		elsif ($m{pet} == 186){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�����o���Ȃ��悤�ɂ��悤�Ƃ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 400;
		}
		elsif ($m{pet} == 188){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A���̍�����L�p�Ȑl�ނ������������Ƃ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 500;
		}
		elsif ($m{pet} == 189){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�S���ɕ������邭�炢�傫�Ȑ��ŋ���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 600;
		}
		elsif ($m{pet} == 190){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A������������<br>";

			$m{lib} = 'trick';
			$m{tp}  = 700;
		}
		elsif ($m{pet} == 191){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A���E�Ɉ�����̕����������<br>";

			$m{lib} = 'trick';
			$m{tp}  = 800;
		}
		elsif ($m{pet} == 31 && $m{country} && &is_ceo){
			$mes .= "�|�b�|�b�|�[�������n�g�|�b�|�[������������<br>";
			if ($cs{strong}[$m{country}] >= 15000 && !$cs{is_die}[$m{country}]) {
				my $total = 1000;
				for my $i (1..$w{country}) {
					unless ($i eq $m{country} || $i eq $union) {
						my $v = 500 + int(rand(10)) * 100;
						$cs{strong}[$i] += $v;
						$total += $v;
					}
				}
				$cs{strong}[$m{country}] -= $total;
				&write_cs;
				&write_use_pet_log($id, $m{pet});
				&remove_pet;
				my %sames;
				open my $fh, "< $logdir/$m{country}/member.cgi";
				while (my $player = <$fh>) {
					$player =~ tr/\x0D\x0A//d;
					# �������O�̐l����������ꍇ
					next if ++$sames{$player} > 1;
					&regist_you_data($player,'next_salary',$time);
				}
				close $fh;
				$m{next_salary} = $time;
				&mes_and_world_news("<b>$cs{name}[$m{country}]��$cs{name}[$m{country}]�l�����̏��L���ł͂Ȃ�</b>");
			} else {
				$mes .= "���邾���̍��͂Ƃ��Ȃ����炗��������<br>";
			}
		}
		elsif ($m{pet} == 198){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�ςȌ����t���悤�Ƃ��Ă���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 900;
		}
		elsif ($m{pet} == 201){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�́A�����̗��z���悤�Ƃ��Ă���<br>";

			$m{lib} = 'trick';
			$m{tp}  = 1000;
		}
		else {
			my $use_flag = 1;
			if(($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))){
				my @world_pets = (61, 64, 65, 66, 67, 68, 69, 70, 71, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 151, 152);
				for my $i(@world_pets){
					if($m{pet} == $i){
						$use_flag = 0;
						last;
					}
				}
			}
			if($use_flag){
				&write_use_pet_log($id, $m{pet});
				&{ $pets[$m{pet}][3] };
				if ($m{pet} > 0) {
					$mes .= "��ڂ��I���� $pets[$m{pet}][1]��$m{pet_c} �͌��̔ޕ��֏����Ă������c<br>$pets[$m{pet}][1]��$m{pet_c}�@ɼ<br>";
				}
				else {
					$mes .= "��ڂ��I���� $pets[$m{pet}][1] �͌��̔ޕ��֏����Ă������c<br>$pets[$m{pet}][1]�@ɼ<br>";
				}
				&remove_pet;
			}
		}
	} elsif ($in{mode} eq 'use_attack' && $w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		if ($in{luxury}) {
			&super_attack('luxury');
			$mes .= "�K�E�Z�̐ݒ���������܂���<br>�Đݒ�� $coolhour ���Ԍ�ɂł��܂�";
		} else {
			&super_attack('myroom');
		}
		&refresh;
		&n_menu;
	} elsif ($in{mode} eq 'regist_attack' && $w{world} eq $#world_states-4 && $m{country}) {
		if ($in{voice}) {
			require './lib/fate.cgi';
			if (&regist_attack($in{trigger}, $in{timing}, $in{demerit}, $in{max_count}, $in{effect}, $in{voice}, $in{random})) {
				$mes .= '�K�E�Z��ݒ肵�܂����B';
				&refresh;
				&n_menu;
				return;
			}
		}

		&begin;
	}
	else {
		&b_menu(@menus);
	}
}


#================================================
# �g�їp�ð���\��
#================================================
sub my_status_mobile {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1] ����$e2j{mp} $skills[$m_skill][3]<br>";
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_lea  = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
		$mes .= qq|�y������z<br><ul>|;
		$mes .= qq|<li>���O:$wname|;
		$mes .= qq|<li>����:$weas[$m{wea}][2]|;
		$mes .= qq|<li>����:$weas[$m{wea}][3]|;
		$mes .= qq|<li>�ϋv:$weas[$m{wea}][4]|;
		$mes .= qq|<li>�d��:$weas[$m{wea}][5]</ul><hr>|;
		if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $sub_at  = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $sub_mat = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }

		my $m_min_wea;
		if ($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 1;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 6;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 11;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 16;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 21;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 26;
		} elsif($m{wea} == 0) {
			$m_min_wea = 0;
		} else {
			$m_min_wea = 33;
		}
		$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
		$m_wea_modify = 100 if ($m{wea} == 14) || ($m{wea} == 32);
		$m_wea_modify = 0 if ($m{wea} == 31);
		$sub_lea = ($m_wea_modify >= 0) ? "+$m_wea_modify" : "-".abs($m_wea_modify);
	}
	else {
		$sub_lea = "-100";
	}
	if ($m{gua}) {
		$mes .= qq|�y�h����z<br><ul>|;
		$mes .= qq|<li>���O:$guas[$m{gua}][1]|;
		$mes .= qq|<li>����:$guas[$m{gua}][2]|;
		$mes .= qq|<li>����:$guas[$m{gua}][3]|;
		$mes .= qq|<li>�ϋv:$guas[$m{gua}][4]|;
		$mes .= qq|<li>�d��:$guas[$m{gua}][5]</ul><hr>|;
		if    ($guas[$m{gua}][2] =~ /��|��|��|��/) { $sub_df  = "+$guas[$m{gua}][3]"; $sub_ag .= "-$guas[$m{gua}][5]"; }
		elsif ($guas[$m{gua}][2] =~ /��|��|��/)    { $sub_mdf = "+$guas[$m{gua}][3]"; $sub_ag .= "-$guas[$m{gua}][5]"; }
	}

	if ($m{pet}) {
		my $pet_c = $m{pet} > 0 ? "��$m{pet_c}" : "($m{pet_c}/$pets[$m{pet}][5])";
		$mes .= qq|�y�߯ď��z<br><ul>|;
		$mes .= qq|<li>���O:$pets[$m{pet}][1]$pet_c|;
		$mes .= qq|<li>����:$pet_effects[$m{pet}]|;
		if($pet_sub_effects[$m{pet}]){
			$mes .= qq|<li>�ǉ�����:$pet_sub_effects[$m{pet}]|;
		}
		$mes .= qq|</ul>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="�߯Ă��g�p����" class="button1"></form>|;
		}
		$mes .= qq|<hr>|;
	}

	if ($w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
		$mes .= '<hr>';
	}
	my $m_st = &m_st;
	$mes .=<<"EOM";
		<b>$m{sedai}</b>�����<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>
		�M�� <b>$m{medal}</b>��<br>
		���ɺ�� <b>$m{coin}</b>��<br>
		��ށy$m{lot}�z<br>
		<hr>
		�y�ð���z����:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/$e2j{max_mp} [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>$sub_at]/$e2j{df} [<b>$m{df}</b>$sub_df]/<br>
		$e2j{mat} [<b>$m{mat}</b>$sub_mat]/$e2j{mdf} [<b>$m{mdf}</b>$sub_mdf]/<br>
		$e2j{ag} [<b>$m{ag}</b>$sub_ag]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>$sub_lea]<br>
		<hr>
		�y�o���Ă���Z�z<br>
		 $skill_info
		<hr>
		�y�n���x�z<br>
		�_�� <b>$m{nou_c}</b>/���� <b>$m{sho_c}</b>/���� <b>$m{hei_c}</b>/�O�� <b>$m{gai_c}</b>/�ҕ� <b>$m{mat_c}</b>/<br>
		���D <b>$m{gou_c}</b>/���� <b>$m{cho_c}</b>/���] <b>$m{sen_c}</b>/�E�� <b>$m{esc_c}</b>/�~�o <b>$m{res_c}</b>/<br>
		��@ <b>$m{tei_c}</b>/�U�v <b>$m{gik_c}</b>/�U�� <b>$m{kou_c}</b>/���� <b>$m{cas_c}</b>/���� <b>$m{mon_c}</b>/<br>
		�C�s <b>$m{shu_c}</b>/���� <b>$m{tou_c}</b>/���Z <b>$m{col_c}</b>/ڰ�  <b>$m{cataso_ratio}</b>/no1 <b>$m{no1_c}</b>/<br>
		���� <b>$m{hero_c}</b>/���� <b>$m{huk_c}</b>/�ŖS <b>$m{met_c}</b>/�� <b>$m{fes_c}</b>/<br>
		<hr>
		�y��\\���߲�āz<br>
		�푈 <b>$m{war_c}</b>/���� <b>$m{dom_c}</b>/�R�� <b>$m{mil_c}</b>/�O�� <b>$m{pro_c}</b>/
		<hr>
		�y����z<br>
		<b>$war_c</b>�� <b>$m{win_c}</b>�� <b>$m{lose_c}</b>�� <b>$m{draw_c}</b>��<br>
		���� <b>$win_par</b>%
EOM
}

#================================================
# PC�p�ð���\��
#================================================
sub my_status_pc {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td><td align="right">$skills[$m_skill][3]<br></td></tr>|;
	}

	$mes .= '<hr>';
	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_lea  = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
		$mes .= qq|�y������z<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>���O</th><td>$wname</td>|;
		$mes .= qq|<th>����</th><td>$weas[$m{wea}][2]</td>|;
		$mes .= qq|<th>����</th><td>$weas[$m{wea}][3]</td>|;
		$mes .= qq|<th>�ϋv</th><td>$weas[$m{wea}][4]</td>|;
		$mes .= qq|<th>�d��</th><td>$weas[$m{wea}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $sub_at  = "��$weas[$m{wea}][3]"; $sub_ag = "��$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $sub_mat = "��$weas[$m{wea}][3]"; $sub_ag = "��$weas[$m{wea}][5]"; }

		my $m_min_wea;
		if ($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 1;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 6;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 11;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 16;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 21;
		} elsif($weas[$m{wea}][2] eq '��') {
			$m_min_wea = 26;
		} elsif($m{wea} == 0) {
			$m_min_wea = 0;
		} else {
			$m_min_wea = 33;
		}
		$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
		$m_wea_modify = 100 if ($m{wea} == 14) || ($m{wea} == 32);
		$m_wea_modify = 0 if ($m{wea} == 31);
		$sub_lea = ($m_wea_modify >= 0) ? "��$m_wea_modify" : "��".abs($m_wea_modify);
	}
	else {
		$sub_lea = "��100";
	}
	if ($m{gua}) {
		$mes .= qq|�y�h����z<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>���O</th><td>$guas[$m{gua}][1]</td>|;
		$mes .= qq|<th>����</th><td>$guas[$m{gua}][2]</td>|;
		$mes .= qq|<th>����</th><td>$guas[$m{gua}][3]</td>|;
		$mes .= qq|<th>�ϋv</th><td>$guas[$m{gua}][4]</td>|;
		$mes .= qq|<th>�d��</th><td>$guas[$m{gua}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($guas[$m{gua}][2] =~ /��|��|��|��/) { $sub_df  = "��$guas[$m{gua}][3]"; $sub_ag .= "��$guas[$m{gua}][5]"; }
		elsif ($guas[$m{gua}][2] =~ /��|��|��/)    { $sub_mdf = "��$guas[$m{gua}][3]"; $sub_ag .= "��$guas[$m{gua}][5]"; }
	}

	if ($m{pet}) {
		my $pet_c = $m{pet} > 0 ? "��$m{pet_c}" : "($m{pet_c}/$pets[$m{pet}][5])";
		$mes .= qq|�y�߯ď��z<br>|;
		$mes .= qq|<table class="table1" cellpadding="3">|;
		$mes .= qq|<tr><th>���O</th><td>$pets[$m{pet}][1]$pet_c</td>|;
		$mes .= qq|<th>����</th><td>$pet_effects[$m{pet}]</td></tr>|;
		if($pet_sub_effects[$m{pet}]){
			$mes .= qq|<tr><th>�ǉ�����</th><td colspan="3">$pet_sub_effects[$m{pet}]</td></tr>|;
		}

		$mes .= qq|</table>|;
		if ($pets[$m{pet}][2] eq 'myself' || ($m{pet} == 31 && &is_ceo)) {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="�߯Ă��g�p����" class="button1"></form>|;
		}
		$mes .= qq|<hr size="1">|;

		if (&on_december_end || (&on_new_year && !&on_new_year_end)) {
			$mes .= qq|�y����Ľð���z<br>|;
			$mes .= qq|<table class="table1" cellpadding="3">|;
			$mes .= qq|<tr><th>�U��</th><td>$m{at_e}</td>|;
			$mes .= qq|<th>�h��</th><td>$m{df_e}</td>|;
			$mes .= qq|<th>����</th><td>$m{mat_e}</td>|;
			$mes .= qq|<th>���h</th><td>$m{mdf_e}</td>|;
			$mes .= qq|<th>�f����</th><td>$m{ag_e}</td></tr>|;
			$mes .= qq|</table>|;
		}


	}

	if ($w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
		$mes .= '<hr size="1">';
	}

	my $m_st = &m_st;
	$mes .= <<"EOM";
		�y�ð���z�����F$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}$sub_at</td>
			<th>$e2j{df}</th><td align="right">$m{df}$sub_df</td>
		</tr><tr>
			<th>$e2j{max_mp}</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}$sub_mat</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}$sub_mdf</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}$sub_lea</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}$sub_ag</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		�y�o���Ă���Z�z<br>
		<table class="table1" cellpadding="3">
		<tr><th>����</th><th>�Z��</th><th>����$e2j{mp}</th></tr>
		$skill_info
		</table>

		<hr size="1">
		�y�n���x�z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�_��</th><td align="right">$m{nou_c}</td>
			<th>����</th><td align="right">$m{sho_c}</td>
			<th>����</th><td align="right">$m{hei_c}</td>
			<th>�O��</th><td align="right">$m{gai_c}</td>
			<th>�ҕ�</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>���D</th><td align="right">$m{gou_c}</td>
			<th>����</th><td align="right">$m{cho_c}</td>
			<th>���]</th><td align="right">$m{sen_c}</td>
			<th>�E��</th><td align="right">$m{esc_c}</td>
			<th>�~�o</th><td align="right">$m{res_c}</td>
		</tr>
		<tr>
			<th>��@</th><td align="right">$m{tei_c}</td>
			<th>�U�v</th><td align="right">$m{gik_c}</td>
			<th>�U��</th><td align="right">$m{kou_c}</td>
			<th>����</th><td align="right">$m{cas_c}</td>
			<th>����</th><td align="right">$m{mon_c}</td>
		</tr>
		<tr>
			<th>�C�s</th><td align="right">$m{shu_c}</td>
			<th>����</th><td align="right">$m{tou_c}</td>
			<th>���Z</th><td align="right">$m{col_c}</td>
			<th>ڰ�</th><td align="right">$m{cataso_ratio}</td>
			<th>no1</th><td align="right">$m{no1_c}</td>
		</tr>
		<tr>
			<th>����</th><td align="right">$m{hero_c}</td>
			<th>����</th><td align="right">$m{huk_c}</td>
			<th>�ŖS</th><td align="right">$m{met_c}</td>
			<th>��</th><td align="right">$m{fes_c}</td>
			<th>�@</th><td align="right">�@</td>
		</tr>
		</table>

		<hr size="1">
		�y��\\���߲�āz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�푈</th><td align="right">$m{war_c}</td>
			<th>����</th><td align="right">$m{dom_c}</td>
			<th>�R��</th><td align="right">$m{mil_c}</td>
			<th>�O��</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>

		<hr size="1">
		�y����z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>���</th><td align="right">$war_c</td>
			<th>����</th><td align="right">$m{win_c}</td>
			<th>����</th><td align="right">$m{lose_c}</td>
			<th>����</th><td align="right">$m{draw_c}</td>
			<th>����</th><td align="right">$win_par %</td>
		</tr>
		</table>
EOM
}


1; # �폜�s��