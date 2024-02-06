#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/move_player.cgi';
require "$datadir/skill.cgi";
use File::Copy::Recursive qw(rcopy);
use File::Path;
my $this_script = 'admin.cgi';
#=================================================
# �v���C���[�Ǘ� Created by Merino
#=================================================

# ���я���
my %e2j_sorts = (
	country	=> '����',
	name	=> '���O��',
	ldate	=> '�X�V������',
	addr	=> 'νĖ�/IP��',
	agent	=> 'UA(��׳��)',
	check	=> '���d����',
	player	=> '�v���C���[����',
);

# ��̫�Ă̕��я�
$in{sort} ||= 'addr';


#=================================================
# ���C������
#=================================================
&header;
&decode;
&error('�߽ܰ�ނ��Ⴂ�܂�') unless $in{pass} eq $admin_pass;
&read_cs;

if    ($in{mode} eq 'admin_delete_user') { &admin_delete_user; }
elsif ($in{mode} eq 'admin_get_depot_data')   { &admin_get_depot_data; }
elsif ($in{mode} eq 'admin_get_akindo_data')   { &admin_get_akindo_data; }
elsif ($in{mode} eq 'admin_get_bank_log')     { &admin_get_bank_log; }
elsif ($in{mode} eq 'admin_wt0')     { &admin_wt0; }
elsif ($in{mode} eq 'admin_refresh')     { &admin_refresh; }
elsif ($in{mode} eq 'admin_go_neverland')     { &admin_go_neverland; }
elsif ($in{mode} eq 'admin_violate')   { &admin_violate; }
elsif ($in{mode} eq 'admin_repaire')     { &admin_repaire; }
elsif ($in{mode} eq 'junk_sub')          { &junk_sub($in{j_del}); }
elsif ($in{mode} eq 'junk_show')          { &junk_show; }
elsif ($in{mode} eq 'country_reset')     { &country_reset; }
elsif ($in{mode} eq 'kinotake_god')      { &kinotake_god; }
elsif ($in{mode} eq 'bug_prize')      { &bug_prize; }
elsif ($in{mode} eq 'boss_make')         { &boss_make; }
elsif ($in{mode} eq 'all_reset_point')   { &all_reset_point; }
elsif ($in{mode} eq 'all_set_default')   { &all_set_default; }
elsif ($in{mode} eq 'reset_monster')   { &reset_monster; }
elsif ($in{mode} eq 'modify_cha')   { &modify_cha; }
elsif ($in{mode} eq 'admin_losstime')   { &admin_losstime; }
elsif ($in{mode} eq 'admin_summer_lot_list_up')   { &admin_summer_lot_list_up; }
elsif ($in{mode} eq 'admin_summer_end')   { &admin_summer_end; }
elsif ($in{mode} eq 'admin_summer_radio_end')   { &admin_summer_radio_end; }
elsif ($in{mode} eq 'admin_summer_reset')   { &admin_summer_reset; }
elsif ($in{mode} eq 'admin_expendable')   { &admin_expendable; }
elsif ($in{mode} eq 'admin_parupunte')   { &admin_parupunte; }
elsif ($in{mode} eq 'admin_compare')   { &admin_compare; }
elsif ($in{mode} eq 'migrate_reset')   { &migrate_reset; }
elsif ($in{mode} eq 'admin_all_pet_check')   { &admin_all_pet_check; }
elsif ($in{mode} eq 'admin_letter_log_check')   { &admin_letter_log_check; }
elsif ($in{mode} eq 'admin_incubation_log_check')   { &admin_incubation_log_check; }
elsif ($in{mode} eq 'admin_shopping_log_check')   { &admin_shopping_log_check; }
elsif ($in{mode} eq 'admin_hunt_log_check')   { &admin_hunt_log_check; }

&top;
&footer;
exit;

#=================================================
# top
#=================================================
sub top {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;

	print qq|<form method="$method" action="admin_country.cgi">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="���Ǘ�" class="button1">|;
	print qq|</form>|;

	print qq|<form method="$method" action="admin_log.cgi">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="���" class="button1">|;
	print qq|</form>|;

	print qq|<table border="0"><tr>|;
	print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value=""><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="�Sհ�ް" class="button_s"></form></td>|;
	for my $i (0 .. $w{country}) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$i"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="$cs{name}[$i]" class="button_s"></form></td>|;
	}
	print qq|</tr></table>|;

	print qq|<table border="0"><tr>|;
	while (my($k,$v) = each %e2j_sorts) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$in{country}"><input type="hidden" name="pass" value="$in{pass}">\n|;
		print qq|<input type="hidden" name="sort" value="$k"><input type="submit" value="$v" class="button_s"></form></td>\n|;
	}
	print qq|</tr></table>|;

	print qq|<a href="#util">�@�\\��</a>|;

	print qq|<div class="mes">$mes</div><br>| if $mes;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="mode" value="admin_delete_user"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="country" value="$in{country}"><input type="hidden" name="sort" value="$in{sort}">|;
	print qq|ؾ�ẮA��ʂɉ����\\������Ȃ��Ȃ�����ANext���[�v�ɂ͂܂�����Ԃ��C�����܂��B<br>|;
	print qq|<table class="table1"><tr>|;

	for my $k (qw/�폜 ۸޲� �q�� ���l�̓X ��s۸� ���O ̫��� ؾ�� �������� �� IP���ڽ νĖ� UserAgent(��׳��) �X�V���� ��������/) {
		print qq|<th>$k</th>|;
	}
	print qq|</tr>|;

	# �v���C���[�����擾
	my @lines = $in{country} eq '' ? &get_all_users : &get_country_users($in{country});

	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $count = 0;
	my $pre_line = '';
	my $is_duplicated = 0;
	for my $line (@lines) {
		my($id, $name, $pass, $country, $addr, $host, $agent, $ldate) = split /<>/, $line;

		# �����z�X�g���������Ȃ�ԕ\��
		if ( ($host !~ /admin_login/ && $addr eq $b_addr && $host eq $b_host && $agent eq $b_agent)
			|| ($agent eq $b_agent && ($agent =~ /DoCoMo/ || $agent =~ /KDDI|UP\.Browser/ || $agent =~ /J-PHONE|Vodafone|SoftBank/)) ) {
				unless ($is_duplicated) {
					my($pid, $pname, $ppass, $pcountry, $paddr, $phost, $pagent, $pldate) = split /<>/, $pre_line;
					print qq|<tr class="stripe2">|;
					print qq|<td><input type="checkbox" name="delete" value="$pid"></td>|;
					print qq|<td><input type="button" class="button_s" value="۸޲�" onClick="location.href='$script?id=$pid&pass=$ppass';"></td>|;
					print qq|<td><input type="button" class="button_s" value="�q��" onClick="location.href='?mode=admin_get_depot_data&pass=$in{pass}&id=$pid&name=$pname';"></td>|;
					print qq|<td>|;
					if (-f "$userdir/$pid/shop_sale_detail.cgi") {
						print qq|<input type="button" class="button_s" value="���l�̓X" onClick="location.href='?mode=admin_get_akindo_data&pass=$in{pass}&id=$pid&name=$pname';">|;
					}
					print qq|</td>|;
					print qq|<td>|;
					if (-f "$userdir/$pid/shop_bank_log.cgi") {
						print qq|<input type="button" class="button_s" value="��s۸�" onClick="location.href='?mode=admin_get_bank_log&pass=$in{pass}&id=$pid&name=$pname';">|;
					}
					print qq|</td>|;
					print qq|<td>$pname</td>|;
					print qq|<td>$pid</td>|;
					print qq|<td><input type="button" class="button_s" value="�S��0" onClick="location.href='?mode=admin_wt0&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td><input type="button" class="button_s" value="ؾ��" onClick="location.href='?mode=admin_refresh&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?mode=admin_go_neverland&pass=$in{pass}&id=$pid&country=$pcountry&sort=$in{sort}';"></td>|;
					print qq|<td>$cs{name}[$pcountry]</td>|;
					print qq|<td>$paddr</td>|;
					print qq|<td>$phost</td>|;
					print qq|<td>$pagent</td>|;
					print qq|<td>$pldate</td>|;
					print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td></tr>|;
				}
				print qq|<tr class="stripe2">|;
				$is_duplicated = 1;
		}
		else{
			$is_duplicated = 0;
			if ($in{sort} ne 'check') {
				print ++$count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
			}
		}
		$b_addr  = $addr;
		$b_host  = $host;
		$b_agent = $agent;

		if ($in{sort} ne 'check' || $is_duplicated) {
			print qq|<td><input type="checkbox" name="delete" value="$id"></td>|;
			print qq|<td><input type="button" class="button_s" value="۸޲�" onClick="location.href='$script?id=$id&pass=$pass';"></td>|;
			print qq|<td><input type="button" class="button_s" value="�q��" onClick="location.href='?mode=admin_get_depot_data&pass=$in{pass}&id=$id&name=$name';"></td>|;
			print qq|<td>|;
			if (-f "$userdir/$id/shop_sale_detail.cgi") {
				print qq|<input type="button" class="button_s" value="���l�̓X" onClick="location.href='?mode=admin_get_akindo_data&pass=$in{pass}&id=$id&name=$name';">|;
			}
			print qq|</td>|;
			print qq|<td>|;
			if (-f "$userdir/$id/shop_bank_log.cgi") {
				print qq|<input type="button" class="button_s" value="��s۸�" onClick="location.href='?mode=admin_get_bank_log&pass=$in{pass}&id=$id&name=$pname';">|;
			}
			print qq|</td>|;
			print qq|<td>$name</td>|;
			print qq|<td>$id</td>|;
			print qq|<td><input type="button" class="button_s" value="�S��0" onClick="location.href='?mode=admin_wt0&pass=$in{pass}&id=$id&country=$pcountry&sort=$in{sort}';"></td>|;
			print qq|<td><input type="button" class="button_s" value="ؾ��" onClick="location.href='?mode=admin_refresh&pass=$in{pass}&id=$id&country=$in{country}&sort=$in{sort}';"></td>|;
			print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?mode=admin_go_neverland&pass=$in{pass}&id=$id&country=$in{country}&sort=$in{sort}';"></td>|;
			print qq|<td>$cs{name}[$country]</td>|;
			print qq|<td>$addr</td>|;
			print qq|<td>$host</td>|;
			print qq|<td>$agent</td>|;
			print qq|<td>$ldate</td>|;
			print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td></tr>|;
		}

		$pre_line = $line;
	}
	print qq|</table><br>|;
	print qq|<input type="radio" name="is_delete" value="delete">�폜|;
	print qq| <input type="checkbox" name="is_add_deny" value="1">�o�^�֎~IP/UA�ɒǉ�<br>|;
	print qq|<input type="radio" name="is_delete" value="exile" checked="checked">���O�Ǖ�(3���S��)|;
	print qq|<p style="color: #F00">�v���C���[���폜/�Ǖ�����<br><input type="submit" value="����" class="button_s"></p></form>|;

	print qq|<a name="util"></a>|;
	print qq|<br><br><br>|;
	print qq|<div class="mes">�f�[�^�␳�F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>���ۂ̓o�^�l�����Ⴄ|;
	print qq|<li>�������o�[�ɈႤ���̐l�������Ă�|;
	print qq|<li>�������o�[�ɓ������O�̐l������|;
	print qq|<li>�������o�[�Ƀv���C���[�ꗗ�ɂ͑��݂��Ȃ��l������|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_repaire">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�f�[�^�␳" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�o�O��V<ul>|;
	print qq|<form method="$method" action="$this_script"><p>���M��F<input type="text" name="send_name" class="text_box1"></p><input type="hidden" name="mode" value="bug_prize">|;
	my @prizes = (
		['�z����',	'2_3_999_0'],
		['�z���H',	'2_2_999_0'],
		['��',	'3_62_0_0'],
		['����',	'3_21_0_0'],
		['���',		'3_183_0_0'],
		['̧���',		'3_9_15_0'],
		['�ް��',		'3_8_0_0'],
	);
	print qq|<select name="prize" class="menu1">|;
	for my $pz (@prizes) {
		print qq|<option value="$pz->[1]">$pz->[0]</option>|;
	}
	print qq|</select>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�o�O��V" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">���A�Ď��F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>���C���A�^�f�̂���v���C���[������ꍇ�ɃW�����N�V���b�v�̃��O���Q�Ƃ��܂�|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="junk_sub">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���A�Ď�" class="button_s"></p>|;
	print qq|<input type="radio" name="j_del" value="0">�{��|;
	print qq|<input type="radio" name="j_del" value="1" checked>���O�폜</form>|;
	print qq|<li>�W�����N�V���b�v�̒��g���m�F���܂�|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="junk_show">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�{��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�C��r�F��̍C�̃��O�C���󋵂��r����<ul>|;
	print qq|<li>���C�^�f�̂���v���C���[������ꍇ��r���܂�|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_compare">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���C��r" class="button_s"></p>|;
	print qq|<input type="text" name="comp1" value="">|;
	print qq|<input type="text" name="comp2" value=""></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">��ް���ޑ���F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>�����̌�쓮����ް���ޑ��肳��Ȃ��������i�l�ݒ�ɂ�����炸�S����ް���ޑ���ɂ��܂��j|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="country_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="����ݑ���" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">����������ÁF�����I�ɏ�ύX<ul>|;
	print qq|<li>�Ղ��̂܂܂������ꍇ�ȂǂɎg�p����|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_parupunte">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="����" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�s��ՓV�ً}2<ul>|;
	print qq|<li>�i���j|;
	print qq|<form method="$method" action="$this_script"><p>���M��F<input type="text" name="send_name" class="text_box1"></p><input type="hidden" name="mode" value="kinotake_god">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�s��ՓV�ً}2" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�{�X<ul>|;
	print qq|<li>���݂̃{�X<br>|;
	open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
	my $line = <$bfh>;
	my ($bname, $bcountry, $bmax_hp, $bmax_mp, $bat, $bdf, $bmat, $bmdf, $bag, $bcha, $bwea, $bskills, $bmes_win, $bmes_lose, $bicon, $bwea_name) = split /<>/, $line;
	print qq|$bname HP:$bmax_hp MP:$bmax_mp<br>|;
	print qq|�U��:$bat ���U:$bmat<br>|;
	print qq|�h��:$bdf ���h:$bmdf<br>|;
	print qq|�f��:$bag ����:$bcha<br>|;
	print qq|����:$weas[$bwea][1]<br>|;
	print qq|�Z:|;
	my @bskill = split /,/, $bskills;
	for(@bskill){
		print qq|$skills[$_][1],|;
	}
	print qq|<br>|;
	print qq|<form method="$method" action="$this_script"><p>�V�{�X�쐬</p><input type="hidden" name="mode" value="boss_make">|;
	print qq|<p>�{�X��<input type="text" name="boss_name" class="text_box1"></p>|;
	print qq|<p>HP<input type="text" name="boss_hp" class="text_box1">MP<input type="text" name="boss_mp" class="text_box1"></p>|;
	print qq|<p>�U��<input type="text" name="boss_at" class="text_box1">���U<input type="text" name="boss_mat" class="text_box1"></p>|;
	print qq|<p>�h��<input type="text" name="boss_df" class="text_box1">���h<input type="text" name="boss_mdf" class="text_box1"></p>|;
	print qq|<p>�f��<input type="text" name="boss_ag" class="text_box1">����<input type="text" name="boss_cha" class="text_box1"></p>|;
	print qq|<p>����<select name="boss_wea" class="menu1">|;
	for(0..$#weas){
		print qq|<option value="$_">$weas[$_][1]</option>|;
	}
	print qq|<p>���햼<input type="text" name="boss_weaname" class="text_box1"></p>|;
	print qq|</select></p>|;
	for my $i (1..5){
		print qq|<p>�Z$i<select name="boss_skill$i" class="menu1">|;
		for(0..$#skills){
			print qq|<option value="$_">$skills[$_][1]</option>|;
		}
		print qq|</select></p>|;
	}
	print qq|<p>���j���b�Z�[�W<input type="text" name="boss_winmes" class="textarea1"></p>|;
	print qq|<p>�s�k���b�Z�[�W<input type="text" name="boss_losemes" class="textarea1"></p>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�V�{�X�쐬" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">���Z�b�g<ul>|;
	print qq|<li>�i���j|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="all_reset_point">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���Z�b�g" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�����l�Z�b�g<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="all_set_default">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�����l�Z�b�g" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�����X�^�[���Z�b�g<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="reset_monster">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���Z�b�g�Z�b�g" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">���͏C��<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="modify_cha">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���͏C��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">����<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_losstime">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="����" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�T�}�[�W�����{���X�g�A�b�v<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_lot_list_up">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���X�g��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�ăC�x�I������<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_end">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�I��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�ăC�x���W�I�̑�����(�I������������Ɏ��s���邱��)<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_radio_end">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�I��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�ăC�x����������<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_summer_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�I��" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�K���m���t���O���Z�b�g����<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="migrate_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���Z�b�g" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�Վ������i�A�ł��Ȃ����ƁA�܂������I����R�����g�A�E�g�̂��Ɓj<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_expendable">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="text" name="to_name">|;
	print qq|<p><input type="submit" value="�Վ�����" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�߯ė��ʏ󋵒���<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_all_pet_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="����" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�莆���M����<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_letter_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�`�F�b�N" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�z������<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_incubation_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�`�F�b�N" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">�w������<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_shopping_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�`�F�b�N" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">���������藚��<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_hunt_log_check">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�`�F�b�N" class="button_s"></p></form></div>|;

	print qq|<br><br><br>|;
	my @files = glob "$logdir/monster/*.cgi";
	for my $p_name (@files){
		if ($p_name =~ /boss/ || $p_name =~ /beginner/) {
			next;
		}
		print qq|<div class="mes">$p_name<br>|;
		print qq|<table><tr><th>���O</th><th>�Z</th><th>�댯�x</th></tr>|;
		open my $fh, "<$p_name" or &error("$p_namȩ�ق��J���܂���");
		while (my $line = <$fh>) {
			my @datas = split /<>/, $line;
			my $i = 0;
			my %y = ();
			for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
				$y{$k} = $datas[$i];
				++$i;
			}
			my $skill_st = 0;
			my $si = 0;
			my $skill_str = '';
			for my $skill (split /,/, $y{skills}) {
				$si++;
				if ($skills[$skill][2] eq $weas[$y{wea}][2]) {
					$skill_st += $skills[$skill][7];
					$skill_str .= $skills[$skill][1];
				} else {
					$skill_st += $skills[0][7];
					$skill_str .= $skills[0][1];
				}
			}
			for (my $j = $si; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			print qq|<tr><td>$y{name}</td><td>$skill_str</td><td>$skill_st</td></tr>|;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		print qq|</table></div>|;
	}
}

#=================================================
# �폜�E�Ǖ�����
#=================================================
sub admin_delete_user {
	return unless @delfiles;

	require './lib/move_player.cgi';
	for my $delfile (@delfiles) {
		my %datas = &get_you_datas($delfile, 1);

		if ($in{is_delete} eq 'exile') { # �Ǖ�
			my $id = unpack 'H*', $datas{name};
			return unless -f "$userdir/$id/user.cgi";

			&move_player($datas{name}, $datas{country}, 0);
			$mes .= "$datas{name}��Ǖ����܂���<br>";

			my @data = (
				['wt', 3 * 24 * 3600],
				['country', 0],
				['lib', ''],
				['tp', 0],
				['vote', ''],
			);
			&regist_you_array($datas{name}, @data);
		}
		elsif ($in{is_delete} eq 'delete') {
			&move_player($datas{name}, $datas{country}, 'del');
			$mes .= "$datas{name}���폜���܂���<br>";

			# �ᔽ�҃��X�g�ɒǉ�
			if ($in{is_add_deny}) {
				open my $fh, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgi̧�ق��J���܂���");
				print $fh $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
					|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
				if(-f "$userdir/$id/access_log.cgi"){
					open my $fh2, "< $userdir/$id/access_log.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
					while (my $line_info_add = <$fh2>){
						($d{addr}, $d{host}, $d{agent}) = split /<>/, $line_info_add;
						print $fh ($d{agent} =~ /DoCoMo/ ||
							$d{agent} =~ /KDDI|UP\.Browser/ ||
							$d{agent} =~ /J-PHONE|Vodafone|SoftBank/) ? "$d{agent}\n" : "$d{addr}\n";
					}
				}
				close $fh;
			}
		}
	}
}

#=================================================
# ؾ�ď����F��ʐ^�����@�n�}�����ꍇ�Ɏg�p(��������ُ̈�װ)
#=================================================
sub admin_wt0 {
	$mes .= "$in{id}�̍S�����Ԃ�ؾ�Ă��܂���<br>";
	return unless $in{id};

	my $name = pack 'H*', $in{id};
	&regist_you_data($name, "wt", 0);

	$mes .= "$name�̍S�����Ԃ�ؾ�Ă��܂���<br>";
}

#=================================================
# ؾ�ď����F��ʐ^�����@�n�}�����ꍇ�Ɏg�p(��������ُ̈�װ)
#=================================================
sub admin_refresh {
	return unless $in{id};

	local %m = &get_you_datas($in{id}, 1);
	$m{lib} = '';
	$m{wt} = $m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
	$id = $in{id};
	&write_user;

	$mes .= "$m{name}��lib,tp�Ȃǂ̒l��ؾ�Ă��܂���<br>";
}

#=================================================
# �����������F�����I�ɖ������ɂ���
#=================================================
sub admin_go_neverland {
	return unless $in{id};

	require './lib/move_player.cgi';
	local %m = &get_you_datas($in{id}, 1);
	$m{lib} = '';
	$m{wt} = $m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
	$id = $in{id};
	&move_player($m{name}, $m{country}, 0);
	$m{country} = 0;
	&send_item($m{name}, 3, 134, 0, 0, 1);

	&regist_you_data($m{name}, "random_migrate", 0);

	&write_user;

	$mes .= "$m{name}�̏�������ؾ�Ă��܂���<br>";
}


#=================================================
# �����Ƃ̃��[�U�[�f�[�^���擾
#=================================================
sub get_country_users {
	my $country = shift;
	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��ǂݍ��߂܂���");
	while (my $name = <$fh>) {
		$name =~ tr/\x0D\x0A//d;

		my $id = unpack 'H*', $name;
		open my $fh2, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh2>;
		my $line_info = <$fh2>;
		close $fh2;

		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}
		($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name pass country addr host agent ldate/) {
			$line .= "$m{$k}<>";
		}
		push @lines, "$line\n";
	}
	close $fh;

	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $a->[8] cmp $b->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }

	return @lines;
}


#=================================================
# �S���[�U�[�̃f�[�^���擾
#=================================================
sub get_all_users {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		next if ($in{sort} eq 'player' && $in{checkid} && $in{checkid} ne $id);

		open my $fh, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;

		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}

		if(-f "$userdir/$id/access_log.cgi" && ($in{sort} eq 'check' || ($in{sort} eq 'player' && $in{checkid}))){
			open my $fh2, "< $userdir/$id/access_log.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
			while (my $line_info_add = <$fh2>){
				($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info_add;
				my $line = "$id<>";
				for my $k (qw/name pass country addr host agent ldate/) {
					$line .= "$m{$k}<>";
				}
				unless($m{host} =~ /\.trendmicro\.com$|\.sjdc$|\.iad1$/){
					push @lines, "$line\n";
				}
			}
		}else{
			($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;
			my $line = "$id<>";
			for my $k (qw/name pass country addr host agent ldate/) {
				$line .= "$m{$k}<>";
			}
			push @lines, "$line\n";
		}
	}
	closedir $dh;

	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $b->[8] cmp $a->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'check')   { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'player')  { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] ||$a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }

	return @lines;
}


#=================================================
# �f�[�^�␳�F�l���⍑�����ް�Ȃǂ����������̂���U�����ɂ��Ă��珑������
#=================================================
sub admin_repaire {
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		push @{ $members{$m{country}} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;
	}

	&write_cs;
	$mes .= "<hr>�l���⍑�����ް̧�ق��C�����܂���<br>";
}


#=================================================
# ���A�Ď�
#=================================================
sub junk_sub {
	my $del = shift;
	open my $fh3, "+< $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
	my @lines = <$fh3>;
	my @sell = ();
	my @buy = ();
	$mes .= qq|<table><tr>|;
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @lines;
	$mes .= qq|<td>�A�C�e���\\�[�g<table class="table1"><tr><th>�A�C�e��</th><th>���O</th><th>����/����</th><th>����</th></tr>|;
	for my $line (@lines){
		my($kind, $item_no, $item_c, $name, $jtime, $type) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($jtime);
		$year += 1900;
		$mon++;
		my $jtime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= "<td>";
		$mes .= &get_item_name($kind, $item_no);
		$mes .= "</td><td>$name</td>";
		$mes .= $type ? "<td>����</td>" : "<td>����</td>";
		$mes .= "<td>$jtime2<br></td></tr>";
	}
	$mes .= qq|</table></td>|;
	@lines = map { $_->[0] }
				sort { $a->[5] <=> $b->[5] }
					map { [$_, split /<>/ ] } @lines;
	$mes .= qq|<td>���ԃ\\�[�g<table class="table1"><tr><th>�A�C�e��</th><th>���O</th><th>����/����</th><th>����</th></tr>|;
	for my $line (@lines){
		my($kind, $item_no, $item_c, $name, $jtime, $type) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($jtime);
		$year += 1900;
		$mon++;
		my $jtime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= "<td>";
		$mes .= &get_item_name($kind, $item_no);
		$mes .= "</td><td>$name</td>";
		$mes .= $type ? "<td>����</td>" : "<td>����</td>";
		$mes .= "<td>$jtime2<br></td></tr>";
	}
	$mes .= qq|</table></td>|;
	$mes .= qq|<tr></table>|;

	if($del){
		seek  $fh3, 0, 0;
		truncate $fh3, 0;
	}
	close $fh3;
}

#=================================================
# �ެݸ����߂̒��g�m�F
#=================================================
sub junk_show {
	my $count = 0;
	my $mes_sub;
	open my $fh, "< $logdir/junk_shop.cgi" or &error("$logdir/junk_shop.cgi���J���܂���ł���");
	while (my $line = <$fh>) {
		$count++;
		my($kind, $item_no, $item_c) = split /<>/, $line;
		$mes_sub .= &get_item_name($kind, $item_no, $item_c)."<br>";
	}
	close $fh;
	$mes .= "$count��<br>".$mes_sub;
}

#=================================================
# ��ް���ޑ���
#=================================================
sub country_reset {
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		&regist_you_data($m{name}, 'country', 0);
		for my $k (qw/war dom pro mil/) {
			&regist_you_data($name, $k."_c", $m{$k."_c_t"}+$m{$k."_c"});
		}
		&regist_you_data($m{name}, "random_migrate", 0);

		push @{ $members{0} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	for my $i (1..$w{country}) {
		for my $k (qw/ceo war dom pro mil/) {
			$cs{$k}[$i] = '';
			my $kc = $k . "_c";
			$cs{$kc}[$i] = 0;
		}
	}
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $country - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $country - 1 ? 0:$ave_c;
	}

	&write_cs;
	$mes .= "<hr>�S����ް���ޑ���ɂ��܂���<br>";
}

#=================================================
# �s��ՓV�ً}2
#=================================================
sub kinotake_god {
	my $pid = pack 'H*', $in{send_name};
	open my $fh, ">> $userdir/$pid/ex_c.cgi";
	print $fh "fes_c<>1<>\n";
	close $fh;

	&send_item($in{send_name}, 2, int(rand($#eggs)+1), 0, 0, 1);

#	require './lib/shopping_offertory_box.cgi';
#	&send_god_item(5, $in{send_name});
}

#=================================================
# ���{�X�쐬
#=================================================
sub boss_make {
	open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
	print $bfh "$in{boss_name}<>0<>$in{boss_hp}<>$in{boss_mp}<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$in{boss_wea}<>$in{boss_skill1},$in{boss_skill2},$in{boss_skill3},$in{boss_skill4},$in{boss_skill5}<>$in{boss_losemes}<>$in{boss_winmes}<>$default_icon<>$in{boss_weaname}<>\n";
	close $bfh;
}

#=================================================
# �S��\�|�C���g���Z�b�g
#=================================================
sub all_reset_point {
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);

		for my $k (qw/war dom pro mil/) {
			&regist_you_data($m{name}, $k."_c", 0);
		}
	}
	closedir $dh;
	$mes .= "<hr>�S���̑�\�|�C���g�����Z�b�g���܂���<br>";
}

#=================================================
# �����l�Z�b�g
#=================================================
sub all_set_default {
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		&regist_you_data($m{name}, "start_time", $time);
	}
	closedir $dh;
	$mes .= "<hr>�S���̏����l���Z�b�g���܂���<br>";
}

#=================================================
# �����X�^�[������
#=================================================
sub reset_monster {
	# �������瑗���Ă����Ϻ�
	my @egg_nos = (1..34,42..51);

	my @files = glob "$logdir/monster/*.cgi";
	for my $p_name (@files){
		if ($p_name =~ /boss/ || $p_name =~ /beginner/) {
			next;
		}
		$mes .= "$p_name<br>";
		my @lines = ();
		open my $fh, "+< $p_name" or &error("$p_namȩ�ق��J���܂���");
		&dirflock($pname);
		while (my $line = <$fh>) {
			# �����摜��Ԃ�����
			next unless $default_icon;
			my($ymname, $ymes_win, $yicon, $yname) = (split /<>/, $line)[0,-5,-3,-2];
			next if $yicon eq $default_icon;
			next unless -f "$icondir/$yicon"; # �摜���Ȃ�
			my $y_id  = unpack 'H*', $yname;
			next unless -d "$userdir/$y_id/picture"; # ��ڲ԰�����݂��Ȃ�

			# ���������ւ̎莆
			my $m_message = $m_messages[ int( rand(@m_messages) ) ];
			$in{comment}  = qq|$places[$place][2]�ɏZ�ޖ���$ymname�̍Ō�����͂���$m{name}����̎莆<br><br>|;
			$in{comment} .= qq|$ymname�̍Ō�̌��t�w$m_message$ymes_win�x<br>|;
			$in{comment} .= qq|$ymname�̉摜��ϲ�߸���ɖ߂�܂���<br>|;
			$in{comment} .= qq|$ymname�����Ϻނ�����ꂽ�悤��<br>|;

			&send_letter($yname);
			rename "$icondir/$yicon", "$userdir/$y_id/picture/$yicon";

			my $egg_no = $egg_nos[int(rand(@egg_nos))];
			&send_item($yname, 2, $egg_no, 0, 0, 1);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		&release_dirflock($pname);
	}
	$mes .= "<hr>���������Z�b�g���܂���<br>";
}
#=================================================
# ���͏C��
#=================================================
sub modify_cha {
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		unless ($m{cha}) {
			my $ave_status = int(($m{max_hp} + $m{max_mp} + $m{max_hp} + $m{lea} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag}) /  8);
			&regist_you_data($m{name}, "cha", $ave_status);
		}
	}
	closedir $dh;
	$mes .= "<hr>�S���̖��͂��C�����܂���<br>";
}
#=================================================
# ����
#=================================================
sub admin_losstime {
	$w{limit_time} = $time + 24 * 3600;
	&write_cs;
	$mes .= "<hr>�c�莞�Ԃ�1���ɂ��܂���<br>";
}
#=================================================
# �ăC�x���g�I�� ���E���W�I�E���L�E����
#=================================================
sub admin_summer_end {
	require './lib/shopping_offertory_box.cgi';

	my @morning_glory = ();

	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;

		my %m = &get_you_datas($id, 1);

		# �čՂ�p
		unless (-f "$userdir/$id/summer.cgi") {
			open my $fh, "> $userdir/$id/summer.cgi";
			close $fh;
		}
		open my $fh, "< $userdir/$id/summer.cgi" or &error("���̂悤�Ȗ��O����ڲ԰�����݂��܂���");
		my $line = <$fh>;
		close $fh;

		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$m{$k} = $v;
		}
		$m{dummy} = 0;

		if ($m{summer_blog} > 30) {
			&regist_you_data($m{name}, "shogo", '�����Ư�Ͻ��');
			&send_money($m{name}, '�G���L�D�G��', 2000000);
			&send_god_item(5, $m{name});
		} elsif($m{summer_blog} > 20) {
			&send_money($m{name}, '�G���L�w�͏�', 500000);
			&send_god_item(1, $m{name});
		} elsif($m{summer_blog} > 10) {
			&send_money($m{name}, '�G���L�Q����', 20000);
		}

		push @morning_glory, "$m{name}<>$m{morning_glory}<>\n";
	}
	closedir $dh;

	@morning_glory = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @morning_glory;
	my $rank = 1;
	for my $line (@morning_glory) {
		my ($name, $height) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|���琬����1�ʂ�$name���񂪋P���܂���|);
			&regist_you_data($name, "shogo", '�������޵ϲ���');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? $rank - 7 : 1;
		&send_money($name, "���琬���� $rank ��", 100000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my @pop = ();
	open my $fh, "< $logdir/pop_vote.cgi" or &error('�l�C���[�t�@�C�����J���܂���');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		push @pop, "$name<>$vote<>\n";
	}
	close $fh;
	@pop = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @pop;
	$rank = 1;
	for my $line (@pop) {
		my ($name, $vote) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|�l�C���[(��)��1�ʂ� $name ���񂪋P���܂���|);
			&regist_you_data($name, "shogo", '������');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? $rank - 7 : 1;
		&send_money($name, "�l�C���[(��)�� $rank ��", 100000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my %pop2 = ();
	open my $fh, "< $logdir/pop_vote2.cgi" or &error('�l�C���[�t�@�C�����J���܂���');
	while (my $line = <$fh>) {
		my($pop_name, $vote_name) = split /<>/, $line;
		$pop2{$pop_name}++;
	}
	close $fh;
	@pop = ();
	foreach my $name (keys(%pop2)) {
		push @pop, "$name<>$pop2{$name}<>\n";
	}
	@pop = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @pop;
	$rank = 1;
	for my $line (@pop) {
		my ($name, $vote) = split /<>/, $line;
		if ($rank > 10) {
			last;
		}
		if ($rank == 1) {
			&write_world_big_news(qq|�l�C���[(��)��1�ʂ�$name���񂪋P���܂���|);
			&regist_you_data($name, "shogo", '��������');
		}
		my $v = 11 - $rank;
		my $vv = $rank > 7 ? ($rank - 7) * 3 : 2;
		&send_money($name, "�l�C���[(��)�� $rank ��", 300000 * $v);
		&send_god_item($v, $name) for (1..$vv);
		$rank++;
	}

	my @lot_num = ();
	my $max_lot = 0;
	open my $fhn, "< $logdir/event_lot_name.cgi" or &error('�󂭂�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fhn>) {
		my($name, $lot) = split /<>/, $line;
		push @lot_num, $name;
	}
	close $fhn;

	my $name = $lot_num[int(rand(@lot_num))];
	$mes .= "aaa" . $name;
	my $lot_id = unpack 'H*', $name;
	if (-f "$userdir/$lot_id/user.cgi") {
		&write_world_big_news(qq|�T�}�[�W�����{�̓��I�҂� $name ����ł���|);
		&regist_you_data($name, "shogo", '���ϰ�ެ��ށ�');
		&regist_you_data($name, "money_overflow", 1);
		my %p = &get_you_datas($lot_id, 1);
		&regist_you_data($name, 'money_limit',$p{money} + 50000000);
		&send_money($name, '�ϰ�ެ��ޓ��I��', 50000000);
	}
	my $this_vote_file = "$logdir/pop_vote.cgi";
	my $this_file = "$logdir/pop_vote_result_middle.cgi";

	my %sames = ();
	my @p_ranks;

	my @lines = ();
	open my $fh, "< $this_vote_file" or &error('�l�C���[�t�@�C�����J���܂���');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		my $p_id = unpack 'H*', $name;
		if (-f "$userdir/$p_id/user.cgi") {
			%p = &get_you_datas($p_id, 1);
			push @lines, "$name<>$vote<>$p{country}<>\n";
		}
	}
	# �[���������ɕ��ёւ�
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	close $fh;

	open my $rfh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;

	my $this_vote_file = "$logdir/pop_vote2.cgi";
	my $this_file = "$logdir/pop_vote2_result.cgi";

	my %ranks = ();

	open my $fh, "< $this_vote_file" or &error('�l�C���[�t�@�C�����J���܂���');
	while (my $line = <$fh>) {
		my($pname, $name) = split /<>/, $line;
		my $p_id = unpack 'H*', $pname;
		if (-f "$userdir/$p_id/user.cgi") {
			$ranks{$pname}++;
		}
	}

	my @lines = ();
	for my $name (keys(%ranks)) {
		my $p_id = unpack 'H*', $name;
		my %p = &get_you_datas($p_id, 1);
#		my $rank_name = &get_rank_name($p{rank}, $name);
#		push @lines, "$name<>$rank_name<>$p{country}<>\n";
		push @lines, "$name<>$ranks{$name}<>$p{country}<>\n";
	}
	# �[���������ɕ��ёւ�
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	close $fh;

	open my $rfh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;

=pod
	require 'pop_ranking_gold.cgi';
	&update_pop2_ranking;
	require 'pop_ranking_middle.cgi';
	&update_pop_ranking;
=cut
	$mes .= "<hr>�ăC�x���g�̏I�����������܂���<br>";
}
#=================================================
# �ăC�x���g ���W�I�̑��I���A��V�����@
#=================================================
sub admin_summer_radio_end {
	#���W�I�̑��̕�V�����@�A�z�z��͊���ĂȂ��Ă��܂�g�������Ȃ�

	#�o�ȉ񐔃J�E���g
	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "< $this_radio_dir/$d.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
			while (my $line = <$fh>) {
				my($name, $rtime) = split /<>/, $line;
				if(!-f "$userdir/$id/temp_radio.cgi"){
					open my $fh2, "> $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgi���쐬�ł��܂���");
					close $fh2;
				}
				open my $fh2, "< $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgi���J���܂���");
				my $line = <$fh2>;
				my($radio_num) = split /<>/, $line;
				close $fh2;

				$radio_num++;

				open my $fh2, "> $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgi���쐬�ł��܂���");
				print $fh2 "$radio_num\n";
				close $fh2;

			}
			close $fh;
		}
	}

	#�o�ȉ񐔂���V�������s
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;

		my %m = &get_you_datas($id, 1);
		open my $fh3, "< $userdir/$id/temp_radio.cgi" or &error("$userdir/$id/temp_radio.cgi���J���܂���");
		my $line = <$fh3>;
		my($radio_num) = split /<>/, $line;
		close $fh3;

		if ($radio_num > 30) {
			&regist_you_data($m{name}, "shogo", '����׼޵���N');
			&send_money($m{name}, '���W�I�̑��D�G��', 1000000);
			&send_god_item(5, $m{name});
		} elsif($radio_num > 20) {
			&send_money($m{name}, '���W�I�̑��w�͏�', 250000);
			&send_god_item(1, $m{name});
		} elsif($radio_num > 10) {
			&send_money($m{name}, '���W�I�̑��Q����', 10000);
		}

	}
	closedir $dh;

	#�o�ȉ񐔃t�@�C���폜

}

#=================================================
# �ăC�x���g�f�[�^�������@
#=================================================
sub admin_summer_reset {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
		my $summer_file = "$userdir/$pid/summer.cgi";
		my $summer_file_trash_dir = "$userdir/$pid/summer_trash";
		if (-f "$summer_file") {
			#summer_trash�f�B���N�g���������ꍇ�͍쐬
			mkdir "$summer_file_trash_dir" or &error("$summer_file_trash_dir ̫��ނ����܂���ł���") unless -d "$summer_file_trash_dir";
			#�ߋ���summer.cgi��trash�ɂ������ꍇ
			if(-f "$summer_file_trash_dir/summer.cgi") {
				unlink "$summer_file_trash_dir/summer.cgi" or &error("$summer_file_trash_dir/summer.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
			}
			#rename����trash�ɕۑ�
			rename "$summer_file", "$summer_file_trash_dir/summer.cgi";
			#�f�[�^������
			open my $fh, "> $summer_file" or &error("$summer_file ���ǂݍ��߂܂���");
			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
			close $fh;
		}
	}
	closedir $dh;

	#�ߋ��̃f�[�^��ۑ�
	my $summer_log_trash_dir = "$logdir/summer_trash";
	mkdir "$summer_log_trash_dir" or &error("$summer_log_trash_dir ̫��ނ����܂���ł���") unless -d "$summer_log_trash_dir";

	my $this_vote_file = "$logdir/pop_vote.cgi";
	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	my $this_lot_file = "$logdir/event_lot.cgi";
	my $this_lot2_file = "$logdir/event_lot_name.cgi";
	my $this_blog_vote_file = "$logdir/blog_vote.cgi";

	#�ߋ��̃f�[�^���������ꍇ
	if(-f "$summer_log_trash_dir/pop_vote.cgi") {
		unlink "$summer_log_trash_dir/pop_vote.cgi" or &error("$summer_log_trash_dir/pop_vote.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$summer_log_trash_dir/pop_vote2.cgi") {
		unlink "$summer_log_trash_dir/pop_vote2.cgi" or &error("$summer_log_trash_dir/pop_vote2.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$summer_log_trash_dir/event_lot.cgi") {
		unlink "$summer_log_trash_dir/event_lot.cgi" or &error("$summer_log_trash_dir/event_lot.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$summer_log_trash_dir/event_lot_name.cgi") {
		unlink "$summer_log_trash_dir/event_lot_name.cgi" or &error("$summer_log_trash_dir/event_lot_name.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	if(-f "$summer_log_trash_dir/blog_vote.cgi") {
		unlink "$summer_log_trash_dir/blog_vote.cgi" or &error("$summer_log_trash_dir/blog_vote.cgi̧�ق��폜���邱�Ƃ��ł��܂���");
	}
	#�f�[�^�ړ�
	rename "$this_vote_file", "$summer_log_trash_dir/pop_vote.cgi";
	rename "$this_vote2_file", "$summer_log_trash_dir/pop_vote2.cgi";
	rename "$this_lot_file", "$summer_log_trash_dir/event_lot.cgi";
	rename "$this_lot2_file", "$summer_log_trash_dir/event_lot_name.cgi";
	rename "$this_blog_vote_file", "$summer_log_trash_dir/blog_vote.cgi";

	#�V�K�쐬
	open my $fh, "> $this_vote_file" or &error("$this_vote_file ���ǂݍ��߂܂���");
	close $fh;

	open my $fh2, "> $this_vote2_file" or &error("$this_vote2_file ���ǂݍ��߂܂���");
	close $fh2;

	open my $fh3, "> $this_lot_file" or &error("$this_vote2_file ���ǂݍ��߂܂���");
	close $fh3;

	open my $fh4, "> $this_lot2_file" or &error("$this_vote2_file ���ǂݍ��߂܂���");
	close $fh4;

#�ܑ̖����̂ŋ��N�̂��c��
#	my $this_horror_story_file = "$logdir/horror_story.cgi";
#	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file ���ǂݍ��߂܂���");
#	close $fh;
	open my $fh5, "> $this_blog_vote_file" or &error("$this_blog_vote_file ���ǂݍ��߂܂���");
	close $fh5;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
			close $fh;
		}
	}
}
#=================================================
# �T�}�[�W�����{���X�g��
#=================================================
sub admin_summer_lot_list_up {
	my @list = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;

		my %m = &get_you_datas($pid, 1);
		# �֐�����`����Ă��Ȃ�
		# read_summer ���Ĕԍ����ǂݍ��ނ悤�ɂ���Ηǂ���̧�ٵ���݂���񑝂���̂��Ĕԍ�������ǂݍ��ފ֐��ɂ��Ă��܂��������X�}�[�g
		my %s = &get_summer_datas($pid);
		my @lots = split /,/, $m{event_lot};
		if ($lots[0] ne '') {
			for my $lot (@lots) {
				push @list, "$m{name}<>$lot<>\n"
			}
		}
	}
	@list = map { $_->[0] } sort {$a->[2] <=> $b->[2]} map { [$_, split /<>/] } @list;
	$mes .= qq|<table><tr><th>���O</th><th>����</th></tr>|;
	my $next_lot = 1;
	for my $line (@list) {
		my ($name, $lot) = split /<>/, $line;
		$lot_n = $lot;
		$lot_n =~ s/^0*([1-9])(\d*)$/$1$2/;
		$mes .= qq|<tr>|;
		$mes .= qq|<td>$name</td>|;
		$mes .= qq|<td>|;
		if ($next_lot != $lot_n) {
			$mes .= qq|<font color="#FF0000">$lot</font>|;
		} else {
			$mes .= qq|$lot|;
		}
		$mes .= qq|</td>|;
		$mes .= qq|</tr>|;
		$next_lot = $lot_n + 1;
	}
	$mes .= qq|</table>|;
	closedir $dh;
}

#=================================================
# �o�O������V
#=================================================
sub bug_prize {
	my ($kind, $item_no, $item_c, $item_lv) = split /_/, $in{prize};

	my $item_mes = &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��

	&send_item($in{send_name}, $kind, $item_no, $item_c, $item_lv, 1);
	&write_send_news(qq|�y�o�O������V�z$in{send_name}��$item_mes�𑗂�܂��B|);
	$mes .= "$in{send_name}��$item_mes�𑗂�܂��B";
}

#=================================================
# �I���̑S�߯ĕ\��
#=================================================
sub admin_all_pet_check {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my $depot_file = "$userdir/$pid/depot.cgi";
		my %pm = &get_you_datas($pid, 1);

		my $is_find = 0;
#		if ($pm{pet} && $pm{pet_c} >= 10) {
		if ($pm{pet} == 169) {
			push @lines, "$pm{name}<>3<>$pm{pet}<>$pm{pet_c}<>0<>\n";
			push @lines, "$pm{name}<>3<>$pm{pet}<>$pm{pet_c}<>0<>\n";
		}
		open my $fh, "< $depot_file" or &error("$depot_file ���ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			next if $is_find;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
#			if ($kind eq '3' && $item_c >= 10) {
			if ($kind eq '3') {
				if ($item_no == 169) {
					push @lines, "$pm{name}<>$line";
					$is_find = 1;
				}
			}
		}
		close $fh;
	}
	@lines = map { $_->[0] } sort { $a->[2] <=> $b->[2] || $a->[3] <=> $b->[3] || $a->[4] <=> $b->[4] || $a->[1] cmp $b->[1] } map { [$_, split /<>/] } @lines;
	for my $line (@lines) {
		my($name, $kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$mes .= "$name:".&get_item_name($kind, $item_no, $item_c, $item_lv)."<br>";
	}
}

#=================================================
# �Վ�����(�����炭��x�����̏����̏ꍇ���̓s�x�����ŏ���)
#=================================================
sub admin_expendable {
#	my $num = rmtree("./user/928381588adb");
#	$mes .= "$num";
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
		my $summer_file = "$userdir/$pid/summer.cgi";
		if (-f "$summer_file") {
			open my $fh, "> $summer_file" or &error("$summer_file ���ǂݍ��߂܂���");
			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
			close $fh;
		}
	}
	closedir $dh;
	my $this_vote_file = "$logdir/pop_vote.cgi";
	open my $fh, "> $this_vote_file" or &error("$this_vote_file ���ǂݍ��߂܂���");
	close $fh;

	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	open my $fh, "> $this_vote2_file" or &error("$this_vote2_file ���ǂݍ��߂܂���");
	close $fh;

	my $this_horror_story_file = "$logdir/horror_story.cgi";
	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file ���ǂݍ��߂܂���");
	close $fh;

	my $this_blog_vote_file = "$logdir/blog_vote.cgi";
	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file ���ǂݍ��߂܂���");
	close $fh;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
			close $fh;
		}
	}
=pod
	&send_item("�Ɓ[�邬��", 3, 8, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 21, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 21, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 21, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 22, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 23, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 24, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 56, 0, 8, 1);
	&send_item("�Ɓ[�邬��", 3, 136, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 143, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 143, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 143, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 143, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 143, 0, 0, 1);
	&send_item("�Ɓ[�邬��", 3, 200, 0, 0, 1);
=cut

#	my $from = "$userdir/6e616e616d6965";
#	my $to = "./user_backup/6e616e616d6965";
#	my $i = rcopy($from, $to);
#	my $num = rmtree($to);


#	unlink "$userdir/6e616e616d6965/letter_flag.cgi";
#	chmod '0666', "./user/82ad82a682d082b1/letter_flag.cgi";
#	open my $fh, "> ./user/82ad82a682d082b1/letter_flag.cgi" or &error("$!");
#	open my $fh, "> $userdir/82c6815b82e982ac82b7/shop_bank.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
#	print $fh qq|500<>10<>10<>4999999<>\n304<>�݂���<>2000000<>\n304<>�݂₱<>2000000<>\n304<>�喃����<>2000000<>\n304<>�t���[�c��<>1900000<>\n304<>�U���<>2000000<>\n304<>�Ɓ[�邬��<>4500000<>\n304<>����<>4250000<>\n304<>�i�i�R<>2000000<>\n304<>������<>2000000<>\n|;
#	close $fh;


#	my %p = &get_you_datas('Arthur', 0);
#	my $pt = $p{war_c} * 2;
#	&regist_you_data('�߂��݂�', 'seed', 'new_seed_151852970182df82ae82dd82f1');

#	$mes .= $p{seed};

=pod
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name}<br>";
		my $depot_log_file = "$userdir/$pid/depot_log.cgi";
		if (-f "$depot_log_file") {
			open my $fh, "< $depot_log_file" or &error("$depot_log_file ���ǂݍ��߂܂���");
			while (my $line = <$fh>) {
				$mes .= "$line<br>";
			}
			close $fh;
		}
	}
	closedir $dh;
=cut

#	&regist_you_data('�Ɓ[�邬��', 'wt', 0);
	# 2258560
#	&regist_you_data('nanamie', 'coin', 811275);
#108122��
#	&regist_you_data('����', 'coin', 2258560);
#	&regist_you_data('VIPPER', 'coin', 2500000);
#	&regist_you_data('nanamie', 'coin', 2500000);
#	&regist_you_data('nanamie', "shogo", '��������');

#	open my $fh, "> $userdir/564950504552/casino_pool.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
#	print $fh "11500000<>-325<>135<>\n";
#	close $fh;

#	require './lib/shopping_offertory_box.cgi';

=pod
	my $str = qq|�ۂ��:3<>�G�]�V�J:1<>32:4<>�ӂ�ӂ�:2<>vavaa:1<>��������:7<>��̑�:6<>�̂�:31<>��ݽޱ������:1<>����:1<>�����ǂ��[��:1<>�h�y�j:1<>���Ƃ���:1<>��:16<>�g�ǋg�c:4<>�������a��:1<>�T�u���i:1<>kotobuki:3<>LINKER:1<>����:1<>��@��:31<>�L���R:1<>�L����:1<>1001:2<>���[�j��:8<>�g���[�j�[:1<>�X�e�t�@:1024<>�҂��:6<>���񂿂���:1<>�̂�����ݽ�:1<>���^��:1<>�����:1<>����:62<>su-:1<>�p���c:3<>�łԂ���:13<>����:10<>masa272:3<>�΂�΂�:1<>����ڂ�:2<>21��:1<>�ς炻��:1<>��������:1<>�f�e:1<>�݂₱:5<>�V���:1<>�N:38<>�v���v��:10<>�J�G���Q:2<>�I�l�[�T��:10<>�k�D�B:3<>�Г�:3<>���M��:1<>���̂��炢:1<>�����݂�:10<>�r:5<>�����߂񂳂�:1<>�v���V���J:1<>��avaa:1<>�����N��:4<>����:1<>�邶��:3<>�����r�g�m:4<>���G��:50<>�ʂ�ς�:4<>�n�𔇂���:29<>���޽:1<>�q�A��:1<>�X�l�[�N:23<>�L���J:1<>�J���J��:30<>orz:3<>Axis:2<>Forza:1<>�Z��:1<>��R����:2<>�s�Cchan:30<>LokLok:6<>poppo:5<>�ʂ�ۂ�:15<>���_������:7<>�����Ђ�:1<>�t���[�c��:20<>�A����:2<>���ɂ���:1<>�V�X�e��:1<>��:1<>����:1<>HalLunba:45<>���C�h:1<>Nep:2<>VIPPER:31<>���΂΂Εۋg:5<>adad:10<>�T�؂܂���:125<>�i�i�R:9<>�݂Ȃ�:1<>�}�l���[�Y:10<>��������:5<>������:7<>���{�[��:42<>�܂���:1<>���I��:1<>�g�g��:1<>�������炱:16|;
	my @array = split /<>/, $str;
	my $num = 0;
	for my $i (0 .. $#array) {
		my ($name, $num2) = split /:/, $array[$i];
		$num += $num2;
	}

	my $j = int(rand($num));
	$mes .= "max num $num rand num $j<br>";

	$num = 0;
	for my $i (0 .. $#array) {
		my ($name, $num2) = split /:/, $array[$i];
		$mes .= "$name<br>" if $num <= $j && $j <= ($num+$num2);
		$num += $num2;
	}
=cut

#	my @plys = ('�Ε�', '�U���C�X�L', '�u�I�[��', '����', '��', '�ԍ��j', '���̍זE', '��', '�S����', 'nanamie');
#	my @goods = (500000, 400000, 300000, 200000, 100000, 80000, 60000, 40000, 20000, 10000);
#	for my $i (0 .. $#plys) {
#		my $name = $plys[$i];
#		&send_money($plys[$i], '�ϰ�ެ��ޓ��I��(��)', $goods[$i]);
#		my %datas = &get_you_datas($name);
#		my $v_coin = $datas{coin} + $goods[$i];
#		$v_coin = 2500000 < $v_coin ? 2500000 : $v_coin;
#		&regist_you_data($name, 'coin', $v_coin);
#	}

#�Ε� 500000
#�U���C�X�L 400000
#�u�I�[�� 300000
#���� 200000
#�� 100000
#�ԍ��j 80000
#���̍זE 60000
#��  40000
#�S���� 20000
#nanamie 10000

#50000���
#�ԂԂ� 500000
#���N�K�C�� 400000
#�c�� 300000
#���S��u�� 200000
#���m 100000
#�A�C�X���� 80000
#������ 60000
#cheee 40000
#�Ɓ[�邬�� 20000
#�I�l�[�T�� 10000

=pod
	my $this_file = "$logdir/event_lot_name";

	my %lot_name = ();

	if (-f "$this_file.cgi") {
		open my $fh, "< $this_file.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
		while (my $line = <$fh>) {
			my ($mname, $mtime) = split /<>/, $line;
			$lot_name{$mname}++;
		}
		close $fh;
	}

	foreach my $k (keys(%lot_name)) {
		$mes .= "$k:$lot_name{$k}<br>";
	}
=cut
#		if (30 < $radio{$k}) {
#			if (&you_exists($k)) {
#������:13

#				&send_money('������', '��޵�̑��F�Ώ�', 2000000);
#				&send_god_item(5, '������');
#				&write_world_big_news(qq|��޵�̑����ނ����ׂĖ��߂� ������ ���񂪊F�Ώ܂𐬂������܂���|);
=pod
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
		elsif (20 < $radio{$k}) {
			if (&you_exists($k)) {
				&send_money($k, '��޵�̑��w�͏�', 500000);
				&send_god_item(1, $k);
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
		elsif (10 < $radio{$k}) {
			if (&you_exists($k)) {
=cut
#				&send_money('�����[�̂��', '��޵�̑��Q����', 20000);
=pod
			}
			else {
				$mes .= "$k:$radio{$k}<br>";
			}
		}
	}

	for my $i (0 .. $#top) {
		$mes .= $top[$i];
	}
	for my $i (0 .. $#middle) {
		$mes .= $middle[$i];
	}
	for my $i (0 .. $#bottom) {
		$mes .= $bottom[$i];
	}
=cut
#	for my $i (0 .. $#bottom2) {
#		$mes .= $bottom2[$i];
#	}


=pod
			my ($holy_strong, $dark_strong) = (0, 0);
			$holy_strong += $cs{strong}[$_] for (1 .. $w{country}-1);
			my $holy_strong_ave = int($holy_strong / ($w{country}-1));
			$dark_strong += $cs{strong}[$w{country}];

			# ��{�d�l �Í����͂����ꍑ�͂��牓���قǶ�������㏸
			my $divisor = $touitu_strong;
			# �Í��̍��͂�������قǶ�������ቺ
			# ���󑤂̕��ύ��͂������قǶ�������ቺ���邪�A�Í��������̍��͂Ƃ��ĕ��ύ��͂𑫂��Ă���i���z�����j
			# ���z�����Ƃ��č��͂𑫂��Ȃ��ꍇ�A�����炭�Í������鉣����ō��͂��ϓ������Ƃ��ɶ�������̕ϓ����������Ȃ�
			my $dividend = $touitu_strong-($dark_strong+$holy_strong_ave);

			if ($dark_strong < $holy_strong_ave) { # ����̕��ύ��͂����Í��̍��͂��Ⴂ
				$divisor = 1; # �Í����ɂ��� �C�����[�h
			}
			elsif ($touitu_strong < 50000 && ($touitu_strong*0.5) < $dark_strong) { # ���ꍑ�͂�5���؂��Ă��āA���Í��̍��͂����ꍑ�͂̔�����荂��
				# (���ꍑ�� - (�Í����� + ���󕽋ύ���)) / ((�Í����� + ���󕽋ύ���) / 2 + ���ꍑ��)
				$divisor = ($dark_strong+$holy_strong_ave) / 2 + $touitu_strong; # �Í��Ƃ��̉��z�����̍��͂������قǶ������������
			}
			elsif ($dark_strong < 30000) { # �Í��̍��͂�3���؂�����{�C���[�h
				$divisor -= $holy_strong_ave / 2; # ����̕��ύ��͂������قǈÍ��̶�������㏸ �{�C���[�h
			}

#			$dividend = $divisor * 0.25 if ($holy_strong_ave / $dark_strong) < 0.6;
#			$dividend = $divisor * 0.5 if 0.5 < ($dividend / $divisor);

#			my $base = $dark_strong < 30000 ? $touitu_strong-$holy_strong_ave/2 : $touitu_strong ;
#			my $base = $touitu_strong ;
#			$base = 0 if $dark_strong < $holy_strong_ave;

			$mes .= "touitu_strong $touitu_strong holy_strong $holy_strong holy_strong_ave $holy_strong_ave dark_strong $dark_strong<br>";
			$mes .= "($touitu_strong - ($dark_strong+$holy_strong_ave)) / ($touitu_strong - ($holy_strong_ave/2))<br>";
			$mes .= "$dividend/$divisor<br>";
			$mes .= "% ".($dividend/$divisor)."<br>";
=cut

#	&regist_you_data('VIPPER', "coin", 2500000);
#	&regist_you_data('���C�g', 'money_limit', 300000000);
#	&send_money('���C�g', '�ϰ�ެ��ޓ��I��', 300000000);
#	require './lib/shopping_offertory_box.cgi';
#	&regist_you_data('�}�l���[�Y', "shogo", '�����Ư�Ͻ��');
#	&send_money('�}�l���[�Y', '�G���L�D�G��', 2000000);
#	&send_god_item(5, '�}�l���[�Y');

#my $summer_file = "$userdir/8356835883658380/summer.cgi";
#open my $fh, "> $summer_file" or &error("$summer_file ���ǂݍ��߂܂���");
#print $fh "radio_time;1503695737<>pop_vote;735<>blog_time;1503662907<>morning_glory;6<>morning_glory_time;1503668426<>summer_blog;25<>cicada_sound;<>dummy;0<>";
#close $fh;

#	my @tutorials = ('�Г�', '�h�y�j', '����', '�ۂ��', '�T�u���i', 'BlackBoxNPC', '���Ƃ���', '�I��', 'Luxuria', '���I��');

#	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
#	while (my $id = readdir $dh) {
#		next if $id =~ /\./;
#		next if $id =~ /backup/;

#		my %m = &get_you_datas($id, 1);

#		my $name = pack 'H*', $id;

		# �čՂ�p
#		unless (-f "$userdir/$id/summer.cgi") {
#			$mes .= "summer $name<br>";
#		}

#		unless (-f "$userdir/$id/tutorial.cgi") {
#			$mes .= "tutorial $name<br>";
#			my $output_file = "$userdir/$id/tutorial.cgi";
#			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
#			close $fh;
#		}

#		open my $fh, "< $userdir/$id/summer.cgi" or &error("���̂悤�Ȗ��O����ڲ԰�����݂��܂���");
#		my $line = <$fh>;
#		close $fh;

#		for my $hash (split /<>/, $line) {
#			my($k, $v) = split /;/, $hash;
#			$m{$k} = $v;
#		}
#		$m{dummy} = 0;

#		if ($m{summer_blog} > 30) {
#			&regist_you_data($m{name}, "shogo", '�����Ư�Ͻ��');
#			&send_money($m{name}, '�G���L�D�G��', 2000000);
#			&send_god_item(5, $m{name});
#		} elsif($m{summer_blog} > 20) {
#			&send_money($m{name}, '�G���L�w�͏�', 500000);
#			&send_god_item(1, $m{name});
#		} elsif($m{summer_blog} > 10) {
#			&send_money($m{name}, '�G���L�Q����', 20000);
#		}

#		push @morning_glory, "$m{name}<>$m{morning_glory}<>\n";
#	}
#	closedir $dh;

=pod
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$mes .= "$pm{name} $pm{c_turn}<br>";
#		my $summer_file = "$userdir/$pid/summer.cgi";
#		if (-f "$summer_file") {
#			open my $fh, "> $summer_file" or &error("$summer_file ���ǂݍ��߂܂���");
#			print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#			close $fh;
#		}
	}
	closedir $dh;
=cut
#	require './lib/_rampart.cgi'; # ���
#	for my $i (1 .. 5) {
#		&change_barrier(6, -25);
#	}
#	&write_cs;
#		&regist_you_data('�V�X�e��', 'wt', '0');
#		&regist_you_data('�ӂ�ӂ�', 'c_turn', '0');
#		&regist_you_data('�U���C�X�L', 'c_turn', '0');
=pod
	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			my @members = ();
			open my $fh, "+< $this_radio_dir/$d.cgi" or &error('���ް̧�ق��J���܂���');
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my ($mname, $mtime) = split /<>/, $line;
				if ($mname eq '���񂿂���') {
					push @members, "�V�X�e��<>$mtime<>\n";
				}
				else {
					push @members, "$mname<>$mtime<>\n";
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @members;
			close $fh;
		}
	}
=cut
#	open my $fh, "> $logdir/error.cgi" or &error("$this_vote_file ���ǂݍ��߂܂���");
#	close $fh;

#	&send_item('SOUTH', 3, 168, 0, 0, 1);

#my $this_lot_file = "$logdir/event_lot.cgi";
#my $this_lot_name_file = "$logdir/event_lot_name.cgi";

#my $this_blog_vote_result_file = "$logdir/blog_vote_result.cgi";
=pod
	my $this_vote_file = "$logdir/pop_vote.cgi";
	open my $fh, "> $this_vote_file" or &error("$this_vote_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_vote2_file = "$logdir/pop_vote2.cgi";
	open my $fh, "> $this_vote2_file" or &error("$this_vote2_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_horror_story_file = "$logdir/horror_story.cgi";
	open my $fh, "> $this_horror_story_file" or &error("$this_horror_story_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_blog_vote_file = "$logdir/blog_vote.cgi";
	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
	close $fh;

	my $this_radio_dir = "$logdir/summer_radio";

	for my $d (1..31) {
		if (-f "$this_radio_dir/$d.cgi") {
			open my $fh, "> $this_radio_dir/$d.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
			close $fh;
		}
	}
=cut
#	open my $fh, "> $this_blog_vote_file" or &error("$this_blog_vote_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#	close $fh;

#	my $summer_file = "$logdir/event_lot_name.cgi";
#	open my $fh, "> $summer_file" or &error("$summer_file ���ǂݍ��߂܂���");
#	print $fh "radio_time;<>pop_vote;<>blog_time;<>morning_glory;<>morning_glory_time;<>summer_blog;<>cicada_sound;<>dummy;0<>";
#	close $fh;


=pod
	my $name = '�N';
	my %datas = &get_you_datas($name);
	my $v_coin = $datas{coin} + 1149320;
	$v_coin = $v_coin > 2500000 ? 2500000 : $v_coin;
	&regist_you_data($name, 'coin', $v_coin);

	my $name = '��';
	my %datas = &get_you_datas($name);
	my $v_coin = $datas{coin} - 1149320;
	$v_coin = $v_coin > 2500000 ? 2500000 : $v_coin;
	&regist_you_data($name, 'coin', $v_coin);
=cut
=pod
	my @lines = ();
	open my $fh, "+< $userdir/818e/super.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	push @lines, "26<>0<>3<>3<>0<>12<>���炠���C<>1<>1463841347<>\n";
	push @lines, "46<>4<>0<>3<>0<>0<>���炠���C<>1<>1468403883<>\n";
	push @lines, "66<>0<>1<>8<>0<>0<>���炠���C<>1<>1473019609<>\n";
	push @lines, "86<>1<>13<>13<>0<>12<>���炠���C<>0<>1478220558<>\n";
	push @lines, "106<>2<>13<>10<>0<>4<>���炠���C<>1<>1482969513<>\n";
	push @lines, "126<>7<>12<>7<>0<>4<>���炠���C<>1<>1487737021<>\n";
	push @lines, "146<>7<>19<>8<>0<>8<>�[���A���ꂩ�������I<>1<>1493892431<>\n";
	push @lines, "166<>1<>11<>8<>2<>14<>���炠���C<>0<>1497424101<>\n";
	push @lines, "186<>15<>23<>10<>0<>14<>�[���A���ꂩ�������I<>0<>1500482540<>\n";

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
=cut

#26<>1<>6<>0<>0<>0<>����������<>1<>1463849463<>
#66<>0<>7<>1<>0<>15<>9021192182<>0<>1472933764<>
#86<>2<>27<>8<>2<>10<>�˂�<>2<>1478072043<>
#106<>1<>10<>4<>0<>2<>��<>1<>1482963421<>
#126<>1<>22<>5<>0<>13<>��<>1<>1487666060<>
#146<>0<>26<>11<>0<>3<>���i�H�ׂ���<>1<>1493887062<>
#166<>6<>11<>5<>0<>1<>����<>1<>1497574264<>
#186<>8<>25<>10<>0<>0<>�r�[���܂��[�H<>0<>1500480513<>


=pod
	my @lines = ();
	my $money = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %pm = &get_you_datas($pid, 1);

		$money += $pm{money};

		my $bank_file = "$userdir/$pid/shop_bank.cgi";
		if (-f "$bank_file") {
			open my $fh, "< $bank_file" or &error("$bank_file ���ǂݍ��߂܂���");
			my $hl = <$fh>;
			while (my $line = <$fh>) {
				my @data = split /<>/, $line;
				$money += $data[2];
			}
			close $fh;
		}
	}
	closedir $dh;

	$mes .= $money;
=cut
=pod
	require './lib/_rampart.cgi'; # ���
	for my $i (1 .. 5) {
		&change_barrier($i, 100);
	}
	&write_cs;
=cut
}

#=================================================
# ���C��r
#=================================================
sub admin_compare {
	my @lines = ();
	my @comp = ($in{comp1}, $in{comp2});
	my %addr = ();
	my %host = ();
	my %agent = ();
	my $bit = 1;
	for my $name (@comp) {
		my $id = unpack 'H*', $name;

		open my $fh2, "< $userdir/$id/access_log.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		while (my $line_info_add = <$fh2>){
			my ($maddr, $mhost, $magent) = split /<>/, $line_info_add;
			if (($addr{$maddr} & $bit) == 0) {
				$addr{$maddr} |= $bit;
			}
			if (($host{$mhost} & $bit) == 0) {
				$host{$mhost} |= $bit;
			}
			if (($agent{$magent} & $bit) == 0) {
				$agent{$magent} |= $bit;
			}
		}
		$bit *= 2;
	}

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�A�h���X</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $maddr (keys(%addr)) {
		my $mes_tr = qq|<td>$maddr</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($addr{$maddr} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�z�X�g��</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $mhost (keys(%host)) {
		my $mes_tr = qq|<td>$mhost</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($host{$mhost} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�G�[�W�F���g</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $magent (keys(%agent)) {
		my $mes_tr = qq|<td>$magent</td>|;
		$bit = 1;
		my $count = 0;
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($agent{$magent} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;
}

#=================================================
# �K���m���t���O���Z�b�g
#=================================================
sub migrate_reset {
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		$name = pack 'H*', $id;
		&regist_you_data($name, "random_migrate", '');
	}
	closedir $dh;

}
#=================================================
# �����������
#=================================================
sub admin_parupunte {
	require "$datadir/parupunte.cgi";
	&{$effects[2]};
	$mes .= "<hr>����������Â�ł��܂���<br>";
}

#=================================================
# �莆�̑��M�����i�v���C�o�V�[���l�����A�N���N�ɑ��M���������������M���O���Ă���j
#=================================================
sub admin_letter_log_check {
	$mes .= qq|<table><tr><th>���M��</th><th>��M��</th><th>���M����</th></tr>\n|;

	open my $fh, "< $logdir/letter_log.cgi" or &error("$logdir/letter_log.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($from_name, $to_name, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$from_name</td><td>$to_name</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# ���̛z������
#=================================================
sub admin_incubation_log_check {
	$mes .= qq|<table><tr><th>���O</th><th>��</th><th>�߯�</th><th>�z������</th></tr>\n|;

	open my $fh, "< $logdir/incubation_log.cgi" or &error("$logdir/incubation_log.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($name, $egg, $pet, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$name</td><td>$egg</td><td>$pet</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# �A�C�e���̍w������
#=================================================
sub admin_shopping_log_check {
	$mes .= qq|<table><tr><th>�w����</th><th>�o�c��</th><th>����</th><th>�l�i</th><th>�w������</th></tr>\n|;

	open my $fh, "< $logdir/shopping_log.cgi" or &error("$logdir/shopping_log.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($m_name, $y_name, $item, $price, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$m_name</td><td>$y_name</td><td>$item</td><td>$price</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}

#=================================================
# �q�ɂ̒��g�m�F
#=================================================
sub admin_get_depot_data {
	my $pid = $in{id};

	my $count = 0;
	my $mes_sub;
	$mes .= qq|$in{name}<br>\n|;
	open my $fh2, "< $userdir/$pid/depot.cgi" or &error("�q��̧�ق��J���܂���ł���");
	while (my $line = <$fh2>) {
		$count++;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

		$mes_sub .= &get_item_name($kind, $item_no, $item_c, $item_lv)."<br>";
	}
	close $fh2;
	$mes .= "$count��<br>".$mes_sub;
#	print qq|$</table>\n|;
}

#=================================================
# ���l�̓X�̔̔�����
#=================================================
sub admin_get_akindo_data {
	my $pid = $in{id};

	$mes .= qq|$in{name}<br>\n|;
	$mes .= qq|<table><tr><th>�̔�����</th><th>�w����</th><th>�w������</th></tr>\n|;
	open my $fh2, "< $userdir/$pid/shop_sale_detail.cgi" or &error("���l�̓X̧�ق��J���܂���ł���");
	while (my $line = <$fh2>) {

		my($item, $y_name, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= qq|<tr><td>$item</td><td>$y_name</td><td>$ltime2</td></tr>|;
	}
	close $fh2;
	$mes .= qq|</table>|;
}

#=================================================
# ��s�̎������
#=================================================
sub admin_get_bank_log {
	my $pid = $in{id};

	$mes .= qq|$in{name}<br>\n|;
	$mes .= qq|<table><tr><th>��s</th><th>���z</th><th>���</th><th>�������</th></tr>\n|;
	open my $fh2, "< $userdir/$pid/shop_bank_log.cgi" or &error("��s۸�̧�ق��J���܂���ł���");
	while (my $line = <$fh2>) {

		my($y_name, $type, $money, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);

		$mes .= qq|<tr><td>$y_name</td><td>$type</td><td>$money</td><td>$ltime2</td></tr>|;
	}
	close $fh2;
	$mes .= qq|</table>|;
}

#=================================================
# �����̗����藚��
#=================================================
sub admin_hunt_log_check {
	$mes .= qq|<table><tr><th>������</th><th>�����n</th><th>�E������</th><th>�E������</th><th>����</th></tr>\n|;

	open my $fh, "< $logdir/hunt_log.cgi" or &error("$logdir/hunt_log.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($m_name, $place, $item, $is_get, $ltime) = split /<>/, $line;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($ltime);
		$year += 1900;
		$mon++;
		my $ltime2 = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		$mes .= qq|<tr><td>$m_name</td><td>$place</td><td>$item</td><td>$is_get</td><td>$ltime2</td></tr>\n|;
	}
	close $fh;

	$mes .= qq|</table>|;
}
