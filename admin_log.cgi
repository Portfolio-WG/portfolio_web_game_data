#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
my $this_script = 'admin_log.cgi';
#=================================================
# ���O�Ȃǂ̊Ǘ� Created by nanamie
#=================================================

#=================================================
# ���C������
#=================================================
&header;
&decode;
&error('�߽ܰ�ނ��Ⴂ�܂�') unless $in{pass} eq $admin_pass;
&header_admin;
&read_cs;

if    ($in{mode} eq 'check_matching') { &check_matching; }

&top;
&footer;
exit;

#=================================================
# header+
#=================================================
sub header_admin {
	print <<"EOM";
	<table border="0"><tr><td>
		<form action="$script_index">
			<input type="submit" value="�s�n�o" class="button1">
		</form>
	</td><td>
		<form method="$method" action="admin.cgi">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="��ڲ԰�Ǘ�" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="���Ǘ�" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="mode" value="now_country">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="���݂̍��f�[�^" class="button1">
		</form>
	</td></tr></table>
EOM
}

#=================================================
# top
#=================================================
sub top {
	if ($mes) {
		print qq|<div class="mes">$mes</div><br>|;
	}
	else {
		print qq|<div class="mes">���O�̕\\����f�[�^�̎擾�Ȃǂ��ł��܂�</div><br>|;
	}

	print qq|<div class="mes">�}�b�`���O�`�F�b�N<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="check_matching">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|��ڲ԰���F<input type="text" name="y_name"><br>|;
	my @countries = (1 .. $w{country});
	print qq|<select name="y_country" class="menu1">|;
	for my $country (@countries) {
		print qq|<option value="$country">$cs{name}[$country]</option>|;
	}
	print qq|</select>|;
	print qq|<p><input type="submit" value="�`�F�b�N" class="button_s"></p></form></div>|;

}

sub check_matching {
	my ($y_name, $y_country) = ($in{y_name}, $in{y_country});

	local %m = &get_you_datas($y_name);
	local %y = ();
	$y{country} = $y_country;
	local $c_y = $cs{name}[$y{country}];

	local @lines = &get_country_members($y{country});

	my $ambush_num = 0;
	for my $i (1 .. 20) {
		my $is_ambush = &_get_war_you_data; # �҂���������Ă��ꍇ�߂�l����
		$y{sol} = int($rank_sols[$y{rank}]);
	
		# �҂�����
		if ($is_ambush) {
			$ambush_num++;
			$mes .= "$c_y��$y{name}������$y{sol}��$units[$y{unit}][1]���҂��������Ă��܂���!<br>";
			if ($y{unit} eq '11') { # �ÎE����
				my $v = int( $m{sol} * (rand(0.2)+0.2) );
				$m{sol} -= $v;
				$m{sol_lv} = int( rand(15) + 15 ); # 15 �` 29
				$mes .= "$units[$y{unit}][1]�ɂ��ÎE�ŁA$v�̕�������܂���!<br>";
			}
			elsif ($y{unit} eq '14') { # ���e����
				$m{sol_lv} = int( rand(10) + 5 ); # 5 �` 14
				$mes .= "$units[$y{unit}][1]�ɂ�錶�p�ŁA���m�B�͍������傫���m�C��������܂���!<br>";
			}
			else {
				$m{sol_lv} = int( rand(15) + 10 ); # 10 �` 24
				$mes .= "�҂������ɂ�蕺�m�B�͍������傫���m�C��������܂���!<br>";
			}
			if ($pets[$y{pet}][2] eq 'no_single' && $w{world} ne '17') {
				$y{wea} = 'no_single';
				$y{sol_lv} = int( rand(10) + 5);
				$mes .= "$pets[$y{pet}][1]�̗͂Ő�΂Ɉ�R�ł��ɂ͂Ȃ�܂��񂪕��̎m�C�͉������Ă��܂�<br>";
			}
		}
		else {
			$m{sol_lv} = 80;
			$mes .= "$c_y����$y{name}������$y{sol}�̕����o�Ă��܂���<br>";
		}
	}
	$mes .= "<br>��҂��������F$ambush_num";
}

#================================================
# �K���Ɠ������������炢�̑���������_���ŒT���B������Ȃ��ꍇ�͗p�ӂ��ꂽNPC
#================================================
sub _get_war_you_data {
	my $war_mod = &get_modify('war');
	
	if (@lines >= 1) {
		my $retry = ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000      ? 0 # ���E��y�S�ǁz�U�߂����̍��͂�3000�ȉ��̏ꍇ�͋���NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # ���E��y�Í��z�U�߂�����NPC���Ȃ���ڲ԰ϯ�ݸނ͂P��
				  : $w{world} eq $#world_states - 5 ? 3 # ���E��y�ّ��z��ڲ԰ϯ�ݸނ�3��
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 15 && $w{world} ne '17') ? 	1
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && $w{world} ne '17') ? 	2
				  :																5 # ���̑���ڲ԰ϯ�ݸނ��ō��T��ق���ײ����
				  ;
		$retry = int($retry / $war_mod);
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # �����l�Ȃ玟
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp �]���ȉ��s�폜

#			my $c = int(rand(@lines));
#			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp �]���ȉ��s�폜
#			next if $sames{$lines[$c]}++; # �����l�Ȃ玟

			$mes .= "$lines[$c]<br>";
			my $y_id = unpack 'H*', $lines[$c];
			
			# ���Ȃ��ꍇ�͎�
			next unless -f "$userdir/$y_id/user.cgi";

			my %you_datas = &get_you_datas($y_id, 1);
			
			$y{name} = $you_datas{name};
			
			next if $you_datas{lib} eq 'prison'; # �S���̐l�͏���
			next if $you_datas{lib} eq 'war'; # �푈�ɏo�Ă���l�͏���
			next if ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 20 && $w{world} ne '17'); # ��20̧���
			
			if ($m{win_c} < $new_entry_war_c) {
				if ( $m{rank} >= ($you_datas{rank} + int(rand(2)) ) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} elsif ($cs{disaster}[$y{country}] eq 'mismatch' && $cs{disaster_limit}[$y{country}] >= $time) {
				# �w���n��������
				if ( $you_datas{rank} <= $m{rank}) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} else {
				# �K���Ɠ������߂��l�B���̐�����0�ɂ���΂�苭���̋߂�����傫������ΐF�X�ȑ���
				if ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
				# �҂��������Ă���l��������
				elsif ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 1;
				}
			}
		}
	}
	
	# ���޳ or NPC
	# %y �Ɋi�[����Ă����ް��̈ꕔ�������p�����Ȃ��悤�ɏ������i���޳�ENPC�����ʂ������Ă�����h��������Ă�����j
	# ��݂͑҂����������ɓ���Ɣ�������̂ż��޳ or NPC�ɂ͒��ڊ֌W�Ȃ�
	# ���́A��ݎ������ǂ����𕐊�ɂ��Ĕ��肵�Ă���i��R�ł����Ȃ����ϐ��g���񂵂��Ⴆ�H�j�̂ŁA����ɂ�铝���␳�������炭�o�O���Ă邱��
	$y{gua} = 0; # �h��ɂ��Ă̓C�W��]�n����H�@�C�s�ƈ�R�ł��Ō��ʈ�����Ⴄ��
	$y{pet} = 0;
	($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17') || int(rand(3 / $war_mod)) == 0 || ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7'))
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] �` [4] �� 5�l([0]���� >>> [4]�ア)
#================================================
sub _get_war_npc_data {
	&error("���荑($y{country})��NPC�f�[�^������܂���") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	my $war_mod = &get_modify('war');
	
	require "$datadir/npc_war_$y{country}.cgi";

	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2) * $war_mod)
		  : $m{lea} > 250 ? int((rand(2)+1) * $war_mod)
		  : $m{lea} > 120 ? int((rand(2)+2) * $war_mod)
		  :                 int((rand(2)+3) * $war_mod)
		  ;

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	# ���͒Ⴂ�ꍇ�͋���NPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country} || $w{world} eq $#world_states - 5) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		unless($k eq 'name' && $pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && rand(2) < 1){
			$y{$k} = $v;
		}
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';
	
	return 0;
}

#================================================
# ���޳
#================================================
sub _get_war_shadow_data {
	# ���͒Ⴂ�ꍇ��1.5�{
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = '���޳�R�m(NPC)';
	
	return 0;
}
