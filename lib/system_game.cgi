#================================================
# �ް�(bj.cgi)�ł悭�g������ Created by Merino
#================================================
require './lib/jcode.pl';
require './lib/summer_system_game.cgi';
require './lib/seed.cgi';
use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# �� + ���E �f�[�^�������� ./log/countries.cgi�ɏ�������
#================================================
sub write_cs {
	&error("���ް��̏������݂Ɏ��s���܂���") if $cs{name}[1] eq '';

	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���)
	my @keys = (qw/
		name bbs_name prison_name strong barrier tax food money soldier state is_die member capacity color
		win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
		modify_war modify_dom modify_mil modify_pro
		extra extra_limit disaster disaster_limit
		new_commer
	/);
	# �����@�����́@��ǒl�@�ŗ��@�����Ɓ@���Ɨ\�Z�@�����m���@��ԁ@�ŖS�׸ށ@�����l���@����@���F
	# ���ꐔ�@����\�ҁ@��\�ҁ@�Q�d�@�������@��m�@�O�����@�Q�d�߲�ā@�������߲�ā@��m�߲�ā@�O�����߲�ā@��\�N��
	# �e���ݒ�푈�@�����@�R���@�O��
	# �ǉ����ʁ@�ǉ����ʊ����@���ʍЊQ�@���ʍЊQ�L������
	# �V�K��
	# -------------------
	# �����̍ő�l
	my $max_resource = $w{world} eq '14' ? 300000 : 999999; # ���E�[��E�E�Ȃ�500000�܂�]
	$cs{food}[$m{country}]    = $max_resource if $cs{food}[$m{country}]    > $max_resource;
	$cs{money}[$m{country}]   = $max_resource if $cs{money}[$m{country}]   > $max_resource;
	$cs{soldier}[$m{country}] = $max_resource if $cs{soldier}[$m{country}] > $max_resource;

	# �ّ�
	if ($w{world} eq $#world_states - 5) {
		$cs{state}[$m{country}] = 0;
	}


	my $world_line = &_get_world_line; # ���E���
	my @lines = ($world_line);
	for my $i (1 .. $w{country}) {
		my $line;
		for my $k (@keys) {
			$line .= "$k;$cs{$k}[$i]<>";
		}
		push @lines, "$line\n";
	}

	open my $fh, "> $logdir/countries.cgi" or &error("���f�[�^���J���܂���");
	print $fh @lines;
	close $fh;
}

#================================================
# ���E���
#================================================
sub _get_world_line { # Get %w line
	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���)
	my @keys = (qw/
		country year game_lv limit_time reset_time win_countries player world playing world_sub sub_time twitter_bot half_hour_time
	/);
	# ���̐��@�N�@��Փx�@��������@ؾ�Ă��ꂽ���ԁ@�O��̓��ꍑ(����)�@��ڲ԰�l���@���E��@��ڲ���l���@�T�u��@�T�u���ԁ@twitter�p�J�E���g�@�T�u���Ԃ�0.5���Ԕ�

	my $line = '';
	for my $k (@keys) {
		$line .= "$k;$w{$k}<>";
	}

	# -------------------
	# �F�D�x/���
	for my $i (1 .. $w{country}) {
		for my $j ($i+1 .. $w{country}) {
			my $f_c_c  = "f_${i}_${j}";
			my $p_c_c = "p_${i}_${j}";
			$line .= "$f_c_c;$w{$f_c_c}<>";
			$line .= "$p_c_c;$w{$p_c_c}<>";
		}
	}
	$line .= "\n";

	return $line;
}

#================================================
# ��ڲ԰�ް���������
#================================================
# turn value stock y_***** �͎����̽ð���Ɗ֌W�Ȃ��̂Ŏ��R�Ɏ��񂵂Ă悢
sub write_user {
	&error("��ڲ԰�ް��̏������݂Ɏ��s���܂���") if !$id || !$m{name};

	$m{ltime} = $time;
	$m{ldate} = $date;

	# -------------------
	# top��۸޲�ؽĂɕ\��
	if ($time > $m{login_time} + $login_min * 60) {
		$m{login_time} = $time;

		open my $fh2, ">> $logdir/login.cgi";
		print $fh2 "$time<>$m{name}<>$m{country}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
		close $fh2;
	}

	# -------------------
	# �ð���̍ő�l
#	if ($m{cha_org}) {
#		$m{cha} = $m{cha_org};
#	}
	for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
		$m{$k} = 999 if $m{$k} > 999;
	}
	$m{money}  = int($m{money});
	my $money_limit = 4999999;
	if ($m{money_overflow}) { # ����������˔j�Ȃ�
		if ($money_limit >= $m{money}) { # �W���̏���ȉ��Ȃ�
			$m{money_overflow} = 0; # ����˔j�_��
			$m{money_limit} = $money_limit;
		}
		else { # ����˔j���W���̏���𒴂��Ă�Ȃ�
			$m{money_limit} = $m{money} if $m{money_limit} > $m{money}; # �������猸���������V�䉺���Ă�
			$money_limit = $m{money_limit};
		}
	}
	$m{money}  = $money_limit if $m{money} > $money_limit;
	$m{coin}   = 2500000 if $m{coin}  > 2500000;

	# -------------------
	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���(login_time�ȊO))
	my @keys = (qw/
		login_time ldate start_time mail_address name pass magic_word lib tp lib_r tp_r wt act sex shogo sedai vote vote_year
		country job seed lv exp rank rank_exp super_rank rank_name unit sol sol_lv medal money coin skills renzoku renzoku_c total_auction skills_sub skills_sub2 skills_sub3 money_limit
		max_hp hp max_mp mp at df mat mdf ag cha lea wea wea_c wea_lv wea_name gua egg egg_c pet pet_c shuffle master master_c boch_pet
		marriage lot is_full next_salary icon icon_pet icon_pet_lv icon_pet_exp mes mes_win mes_lose mes_touitsu ltime gacha_time gacha_time2 offertory_time trick_time breed_time silent_time
		rest_a rest_b rest_c

		turn stock value is_playing bank
		y_max_hp y_hp y_max_mp y_mp y_at y_df y_mat y_mdf y_ag y_cha y_lea y_wea y_wea_name y_skills
		y_name y_country y_rank y_sol y_unit y_sol_lv y_icon y_mes_win y_mes_lose y_pet y_value y_gua
		y_rest_a y_rest_b y_rest_c

		nou_c sho_c hei_c gai_c gou_c cho_c sen_c gik_c kou_c tei_c mat_c cas_c tou_c shu_c col_c mon_c
		win_c lose_c draw_c hero_c huk_c met_c war_c dom_c mil_c pro_c esc_c res_c fes_c war_c_t dom_c_t mil_c_t pro_c_t boch_c storm_c
		shogo_t icon_t breed breed_c depot_bonus akindo_guild silent_kind silent_tail guild_number disp_casino chat_java disp_top disp_news disp_chat disp_ad disp_daihyo salary_switch no_boss incubation_switch disp_gacha_time delete_shield
		valid_blacklist pet_icon_switch tutorial_switch ambush_on sox_picture hunt_event_stock
		c_turn c_stock c_value c_type cataso_ratio
		no1_c money_overflow random_migrate ceo_c tam_c ban_c wt_c wt_c_latest wt_c_latest_fight

		sox_kind sox_no exchange_count cicada_sound at_e df_e mat_e mdf_e ag_e winter_secret_stage is_back_picture
	/);
	# ۸޲ݎ��ԁ@�X�V�����@�쐬�����@���O�@�߽ܰ�ށ@ײ���؁@���ݸ��߲�ā@�҂����ԁ@��J�x�@���ʁ@�̍��@����@���[�@
	# �������@�E�Ɓ@�푰�@���ف@�o���l�@�ݸ�@�ݸ�o���l�@����@���m���@�m�C�@�M�́@�����@��݁@�Z(����)�@�A���U�߂����@�A�����ā@
	# �ő�HP�@HP�@�ő�MP�@MP�@�́@���@���́@���h�@�f���@���́@�����@����@����ϋv�@�������ف@�h��@���ꕐ�햼�@�Ϻށ@�Ϻސ����@�߯ā@�V���b�t���t���O�@
	# ��������@��ށ@�a���菊���t�׸ށ@���̋��^�@���݁@ү���ށ@������́@������́@�����́@�X�V���ԁ@�������� ��������2 �ΑK���ԁ@��������������ԁ@�����֎~����
	# ��݁@�į��@��ح��@��ڲ���׸ށ@�����ް� �c
	# �_�Ɓ@���Ɓ@�����@�O���@���D�@����@���]�@�U�v�@��@�@�ҕ��@���Ɂ@�����@�C�s�@���Z��@�����@�E���@�~�o�@�Ձ@�����p�@�{�b�`
	# �푈�����@�푈�����@�푈�����@����@�����@�ŖS�@�푈�@�����@�R���@�O���@
	# �^�̍��@�^���݁@��ĉ��P�@��ĉ��Q�@�a�菊�{�[�i�X�@���l�M���h�@�ΐl���ɕ\���@��JAVA�\��
	# ���ɗp �c
	# �B���n���x
	# _c�̓J�E���g(count)�̗�, y_�͑���(you)�̗�

	#����I�ǉ��v�f�@wt_c_latest_fight:�V���b�t���v�Z�p�ғ��� ambush_on:�҂������o���l�ύX�p�ϐ� winter_e_xmas:�~�C�x�N���X�}�X�p�ϐ�
	#at_e df_e mat_e mdf_e ag_e�N���X�}�X�����̃X�e�[�^�X�ǉ��ϐ��@winter_secret_stage �~�C�x�����B���X�e�[�Won

	my $line;
	for my $k (@keys) {
		$line .= $k =~ /^y_(.+)$/ ? "$k;$y{$1}<>" : "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/user.cgi";
	print $fh "$line\n";
	print $fh "$addr<>$host<>$agent<>\n";
	close $fh;
	if (&on_summer) {
		my @keys2 = (qw/radio_time pop_vote blog_time morning_glory morning_glory_time summer_blog cicada_sound dummy/);
		my $line2;
		for my $k (@keys2) {
			$line2 .= "$k;$m{$k}<>";
		}

		open my $fh, "> $userdir/$id/summer.cgi";
		print $fh "$line2\n";
		close $fh;
	}
	&alltime_event;
}


#================================================
# ���̑�
#================================================
# �҂����Ԃ�b�ɕϊ� + ����
sub wait {
	$m{wt} = $GWT * 60;
	$m{wt_c} += $m{wt};
	$m{wt_c_latest_fight} += $GWT * 12;
	&n_menu;

	$m{is_playing} = 0;
	--$w{playing};
	$w{playing} = 0 if $w{playing} < 0;
	&write_cs;
}
#wait_war����wait_others�܂ł̓V���b�t���ғ����v�Z�p
sub wait_war{#1.2�{
#	$m{wt_c_latest_fight} += $GWT * 60 * 1.2;
	$m{wt_c_latest_fight} += $GWT * 66;
}
sub wait_nou{
	if($GWT >= 80){
		$m{wt_c_latest_fight} += 40 * 48;
	}#80���ȏ�̒��������̓V���b�t���ғ�����40���̗ʂɌ��炷
	#�������Await�֐��Ƃ̊֌W��$GWT * 12������Ⴕ�đ�����
	else{
		$m{wt_c_latest_fight} += $GWT * 48;
 	}
}
sub wait_mil{#0.4�{
#	$m{wt_c_latest_fight} += $GWT * 60 * 0.4;
	$m{wt_c_latest_fight} += $GWT * 12;
}

#sub wait_others{
#	$m{wt_c_latest_fight} += $GWT * 60 * 0.2;
#	$m{wt_c} -= $GWT * 48;
#}

# �ʏ펞�̗��p����
sub is_satisfy { 1 }

# �l��ؾ��
sub refresh {
	$m{lib} = '';
	$m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
}

#================================================
# ��J��Ԃ̂Ƃ��̗��p����
#================================================
sub is_act_satisfy {
	if ($m{act} >= 100) {
		$mes .= '��J�����܂��Ă��܂��B��x�������s���Ă�������<br>';
		&refresh;
		&n_menu;
		return 1;
	}
	return 0;
}

#================================================
# ����މ��������B���҂��Ă���l�ƈႤ�ꍇ�� 1(true) ���Ԃ�&begin(�����ƭ��\��)
#================================================
sub is_ng_cmd {
	my @check_cmds = @_;

	for $check_cmd (@check_cmds) {
		return 0 if $cmd eq $check_cmd;
	}
	&begin;
	return 1;
}

#================================================
# Ҳ��ƭ��Ȃǂ̏��� main.cgi country.cgi myself.cgi shopping.cgi
#================================================
=pod
sub b_menu {
	my @menus = @_;

	if (!$m{is_playing} && $w{playing} >= $max_playing) {
		$mes .= qq|<font color="#FFFF00">��ڲ�K���� $w{playing}/$max_playing�l</font><br>���΂炭���҂���������|;
		&begin;
	}
	elsif (defined $menus[$cmd]) {
		$m{lib} = $menus[$cmd][1];
		$m{tp}   = 1;
		require "./lib/$m{lib}.cgi";

		# lib���s����ok�Ȃ�begin�ƭ�
		&begin if &is_satisfy;

		unless ($m{is_playing}) {
			$m{is_playing} = 1;
			++$w{playing};
			&write_cs;
		}
	}
	else {
		&begin;
	}
}
=cut
sub b_menu {
	my @menus = @_;

	if ($m{wt} > 0) {
		if (defined $menus[$cmd]) {
			$m{lib_r} = $menus[$cmd][1];
			$m{tp_r}   = 1;
			require "./lib/$m{lib_r}.cgi";

			# lib_r���s����ok�Ȃ�begin�ƭ�
			&begin if &is_satisfy;
		}
		else {
			&begin;
		}
	}
	else {
		if (!$m{is_playing} && $w{playing} >= $max_playing) {
			$mes .= qq|<font color="#FFFF00">��ڲ�K���� $w{playing}/$max_playing�l</font><br>���΂炭���҂���������|;
			&begin;
		}
		elsif (defined $menus[$cmd]) {
			$m{lib} = $menus[$cmd][1];
			$m{tp}   = 1;
			require "./lib/$m{lib}.cgi";

			# lib���s����ok�Ȃ�begin�ƭ�
			&begin if &is_satisfy;

			unless ($m{is_playing}) {
				$m{is_playing} = 1;
				++$w{playing};
				&write_cs;
			}
		}
		else {
			&begin;
		}
	}
}
#================================================
# �ƭ������
#================================================
sub menu {
	my @menus = @_;
	my $rest = $m{wt} > 0 ? 1 : 0;
	if ($is_smart) {
		$menu_cmd .= qq|<table boder=0 cols=4 width=110 height=110>|;
		for my $i (0 .. $#menus) {
			if($i % 4 == 0){
				$menu_cmd .= qq|<tr>|;
			}
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 4 == 3){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#menus % 4 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;

	}
	elsif ($is_appli) {
		$menu_cmd .= qq|<div align="left" id="commands">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|<br class="cmd_br" />| if ($i+1) % 7 == 0;
		}
		$menu_cmd .= qq|<br class="cmd_br" /></div>|;
	}
	else{
		$menu_cmd .= qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<option value="$i">$menus[$i]</option>|;
		}
		$menu_cmd .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
		$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
		$menu_cmd .= $is_mobile ? qq|<br><input type="submit" value="�� ��" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="�� ��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}

#	return $menu_cmd if $rest; # �S������ $menu_cmd ���\������Ȃ����[�g��ʂ�̂ŁA�Ƃ肠�����S�����̃R�}���h�͂����ŕԂ镶����� $mes �ɑ����ĕ\������
=pod
	if($is_smart){
		$menu_cmd .= qq|<div>|;
#		$menu_cmd .= qq|<div style="float:right;">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<form method="$method" action="$script" class="cmd_form">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button2s"><input type="hidden" name="cmd" value="$i">|;
#			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
#			print "$i ", ($i+1) % 4, " " , ($i+1) % 6, "<br>";

#			$menu_cmd .= qq|</div>| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
			$menu_cmd .= qq|<br class="smart_br" />| if ($i+1) % 4 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr" />| if ($i+1) % 4 == 0;
			$menu_cmd .= qq|<br class="tablet_br" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="tablet_hr" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr">| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
		}
		$menu_cmd .= qq|</div>|;
#		$menu_cmd .= qq|<br style="display:none;">|;
	}
=cut

}
#================================================
# Next�ƭ�
#================================================
sub n_menu {
	$menu_cmd  = qq|<form method="$method" action="$script">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="Next" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}
#================================================
# �g�їpPager ���֑O�� shopping_hospital.cgi
#================================================
sub pager_next {
	my $page = shift;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�����߰��" class="button1"></form>|;
}
sub pager_back {
	my $page = shift;
	$page = 0 if $page < 0;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�O���߰��" class="button1"></form>|;
}

#================================================
# �n���x����
#================================================
sub c_up { # count up
	my $c = shift;
	++$m{$c};

	# �A����c_up�����p�Ƃ��ĸ�۰��قȑޔ�ϐ��Ɣ���ɕK�v�Ȕz��쐬
	if ($cash_c ne $c) {
		$cash_c = $c;
		@cash_shogos = ();
		for my $shogo (@shogos) {
			my($k) = keys %{ $shogo->[1] }; # �Ȃ���each����2��ڂ��Ƃ�Ȃ��c
			push @cash_shogos, [$shogo->[0], $shogo->[1]->{$k}, $shogo->[2]] if $c eq $k;
		}
	}

	for my $cash_shogo (@cash_shogos) {
		if ($cash_shogo->[1] eq $m{$c}) {
			&mes_and_world_news("$cash_shogo->[0]�̏̍���^�����܂���", 1);
			$m{money} += $cash_shogo->[2];
			$mes .= "$cash_shogo->[2]G�̕񏧋����󂯎��܂���<br>";
		}
	}
}

#================================================
# ��\���߲�ı���
#================================================
sub daihyo_c_up {
	my $c = shift;
	++$m{$c};

	my($k) = $c =~ /^(.+)_c$/;
	if ($cs{$k}[$m{country}] eq $m{name}) {
		$cs{$c}[$m{country}] = $m{$c};
	}
	elsif (!&is_daihyo && $m{$c} > $cs{$c}[$m{country}] && $m{$c} >= 10) {
		&mes_and_world_news(qq|<font color="#FF9999">�������̍��ւ̍v�����F�߂��$cs{name}[$m{country}]��\\��$e2j{$k}�ɔC������܂�����</font>|,1);
		$cs{$k}[$m{country}] = $m{name};
		$cs{$c}[$m{country}] = $m{$c};
	}
}



#================================================
# ���ɂ���v���C���[���擾
#================================================
sub get_country_members {
	my $country = shift;
	&error("��No[ $country ] ���̍������݂��Ȃ���") unless -d "$logdir/$country";

	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("��$country�v���C���[�f�[�^���J���܂���");
	push @lines, $_ while <$fh>;
	close $fh;

	return @lines;
}


#================================================
# ����ڲ԰�ɱ��т�X��
#================================================
sub send_item {
	my($send_name, $kind, $item_no, $item_c, $item_lv) = @_;
	my $send_id = unpack 'H*', $send_name;
	$item_c  ||= 0;
	$item_lv ||= 0;

	if (-f "$userdir/$send_id/depot.cgi") {
		open my $fh, ">> $userdir/$send_id/depot.cgi";
		print $fh "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		close $fh;

		open my $fh2, "> $userdir/$send_id/depot_flag.cgi";
		close $fh2;
	}
}
=pod
sub send_item {
	my($send_name, $kind, $item_no, $item_c, $item_lv, $force_send) = @_;
	my $send_id = unpack 'H*', $send_name;
	my $s_mes;
	$item_c  ||= 0;
	$item_lv ||= 0;

	unless(-f "$userdir/$send_id/user.cgi"){
		return;
	}
	my %datas = &get_you_datas($send_name);

	if (-f "$userdir/$send_id/depot.cgi" && ($force_send || !$datas{is_full})) {
		open my $fh, ">> $userdir/$send_id/depot.cgi";
		print $fh "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		close $fh;

		open my $fh2, "> $userdir/$send_id/depot_flag.cgi";
		close $fh2;
	}

	$s_mes = &get_item_name($kind, $item_no); # �A�C�e��������
	if (-f "$userdir/$send_id/depot_watch.cgi"){
#		my $depot_line = '';
#		open my $rfh, "< $userdir/$send_id/depot.cgi";
#		while (my $line = <$rfh>){
#			my ($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
#			$depot_line .= "$rkind,$ritem_no,$ritem_c,$ritem_lv<>";
#		}
#		close $rfh;

		open my $wfh, ">> $userdir/$send_id/depot_watch.cgi";
		my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
		$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
#		print $wfh "$send_name����$s_mes ($tdate)<>$depot_line\n";
		print $wfh "$send_name����$s_mes ($tdate)<>$kind<>$item_no<>$item_c<>$item_lv\n";
		close $wfh;
	}
	unless ($send_name eq $m{name}){
		if (-f "$userdir/$send_id/money.cgi") {
			open my $fh, ">> $userdir/$send_id/money.cgi";
			print $fh "$m{name}<>$s_mes<>2<>\n";
			close $fh;
		}
	}
}
=cut
#================================================
# ����ڲ԰�ɂ����𑗋�
#================================================
sub send_money {
	my($send_name, $from_name, $money, $is_shop_sale) = @_;
	my $send_id = unpack 'H*', $send_name;
	$is_shop_sale||= 0;

	if (-f "$userdir/$send_id/money.cgi") {
		open my $fh, ">> $userdir/$send_id/money.cgi";
		print $fh "$from_name<>$money<>$is_shop_sale<>\n";
		close $fh;
	}
}


#================================================
# �\������ƭ���ɂ���������
#================================================
sub mes_and_world_news {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '������';
	}
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_world_news("<b>$c_m��$w_name��</b>$message", @_)
	: $message =~ /^<i>/  ? &write_world_news("<i>$c_m��$w_name��</i>$message", @_)
	: $message =~ /^<em>/ ? &write_world_news("<em>$c_m��$w_name��</em>$message", @_)
	:					    &write_world_news("$c_m��$w_name��$message", @_)
	;
}
sub mes_and_send_news {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '������';
	}
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_send_news("<b>$c_m��$w_name��</b>$message", @_)
	: $message =~ /^<i>/  ? &write_send_news("<i>$c_m��$w_name��</i>$message", @_)
	: $message =~ /^<em>/ ? &write_send_news("<em>$c_m��$w_name��</em>$message", @_)
	:					    &write_send_news("$c_m��$w_name��$message", @_)
	;
}

#================================================
# �ߋ��̉h���A������񃍃O�������ݏ���
#================================================
#sub write_world_news     { &_write_news('world_news', @_) }
sub write_world_news     {
	my($message, $is_memory, $memory_name) = @_;
	if ($m{cicada_sound} > $time) {
		my @cicada_sounds = ('а�������������а���������а�������������а���������', '�ށc�ށc�ށ[�[�[�[�[�[�[�[�[�ށ[�[�[�[�[�[�[�[�[�ށ[�[�[�[�[�[�[�[�[','¸¸�ޫ���������@¸¸�ޫ���������@¸¸���[ց[-��@¸���[ց[-��@¸���[ց[-��@¸���[ց[-��@�����������������[�[�[�[�[�c�c�c�c�c');
		$message = $cicada_sounds[int(rand(@cicada_sounds))];
	}
	if ($w{world} ne '10' || $message =~ /^</) { # �h���E��y���فz�ȊO�h�܂��͑傫�ȏo����
		&_write_news('world_news',  ($message, $is_memory, $memory_name));
	}
	elsif ($is_memory) { # ���E��y���فz�Ő���t���O���������ꍇ
		$message = &coloration_country($message);
		&write_memory($message, $memory_name);
	}
}
sub write_send_news      { &_write_news('send_news',  @_) }
sub write_blog_news      { &_write_news('blog_news',  @_) }
sub write_colosseum_news { &_write_news('colosseum_news',  @_) }
sub write_picture_news   { &_write_news('picture_news',  @_) }
sub write_book_news      { &_write_news('book_news',  @_) }
sub write_entry_news      { &_write_news('entry_news',  @_) }
sub _write_news {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	&write_world_big_news($message) if $message =~ /^</;
	$message = &coloration_country($message);

	my @lines = ();
	open my $fh, "+< $logdir/$file_name.cgi" or &error("$file_name.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}
#================================================
# ���E�̗���
#================================================
sub write_world_big_news {
	my $message = shift;

	$message = &coloration_country($message);
	my @lines = ();
	open my $fh, "+< $logdir/world_big_news.cgi" or &error("$logdir/world_big_news.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# ����������ΐF�t��
sub coloration_country {
	my $message = shift;
	return $message if $w{country} < 1;
	for my $i (0 .. $w{country}) {
		my $add_color_country = qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		$message =~ s/\Q$cs{name}[$i]\E/$add_color_country/g;
	}
	return $message;
}

#================================================
# �Δ�
#================================================
sub write_legend {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	my @lines = ();
	open my $fh, "+< $logdir/legend/$file_name.cgi" or &error("$logdir/legend/$file_name.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	$message = &coloration_country($message);
	unshift @lines, qq|$world_name��$w{year}�N�y$world_states[$w{world}]�z�F$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}

#================================================
# �v���o���O�������ݏ���
#================================================
# �����ɖ��O������ꍇ�́A���̐l�̐���ɁA�Ȃ��ꍇ�͎����̐���ɏ������܂��
sub write_memory {
	my($message, $memory_name) = @_;
	$m_id = $memory_name ? unpack 'H*', $memory_name : $id;

	return unless -f "$userdir/$m_id/memory.cgi";

	my @lines = ();
	open my $fh, "+< $userdir/$m_id/memory.cgi" or &error("Memory̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#================================================
# �����Ƒ���̋�������  2:���� 1:���� 0:�ア
#================================================
sub st_lv {
	my $y_st = shift || &y_st;
	my $m_st =          &m_st;

	return $y_st > $m_st * 1.5 ? 2
		:  $y_st < $m_st * 0.5 ? 0
		:                        1
		;
}
sub y_st { int($y{max_hp} + $y{max_mp} + $y{at} + $y{df} + $y{mat} + $y{mdf} + $y{ag} + $y{cha}*0.5) }
sub m_st { int($m{max_hp} + $m{max_mp} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag} + $m{cha}*0.5) }

#================================================
# �ЊQ �ŖS����m���A���Ďg�p��
#================================================
sub disaster {
	my $more = shift;
	my @disasters = (
		['���R�ЊQ','food'],
		['�o�ϔj�]','money'],
		['��n�k','soldier'],
	);
	if ($more) {
		push @disasters, ['��莞�ԍ��h���Ǝ㉻','paper'];
		push @disasters, ['��莞�Ԏw���n��������','mismatch'];
		push @disasters, ['��D�_���o��','concentrate'];
		unless ($w{world} eq $#world_states || $w{world} eq $#world_states-1 || $w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-4 || $w{world} eq $#world_states-5) {
			push @disasters, ['���l����','strong'];
		}
		if ($w{world} eq '12') {
			push @disasters, ['��Q�[', 'big_food'];
			push @disasters, ['�勰�Q', 'big_money'];
			push @disasters, ['��Ôg', 'big_soldier'];
		}
	}
	my $v = int(rand(@disasters));
	if ($disasters[$v][1] eq 'food' || $disasters[$v][1] eq 'money' || $disasters[$v][1] eq 'soldier') {
		for my $i (1 .. $w{country}) {
			next if $cs{ is_die }[$i];
			$cs{ $disasters[$v][1] }[$i] = int($cs{ $disasters[$v][1] }[$i] * 0.5);
		}
		&write_world_news("<b>���E���� $disasters[$v][0] ���N����܂���</b>");
	} elsif ($disasters[$v][1] eq 'strong' && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{ $disasters[$v][1] }[$target] -= int(rand(10)+5) * 100;
		&write_world_news("<b>$cs{name}[$target]�� $disasters[$v][0] ���N����܂���</b>");
	} elsif (($disasters[$v][1] eq 'paper' || $disasters[$v][1] eq 'mismatch') && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{disaster}[$target] = $disasters[$v][1];
		$cs{disaster_limit}[$target] = $time + 1 * 60 * 60;
		&write_world_news("<b>$cs{name}[$target]�� $disasters[$v][0] ���܂���</b>");
	} elsif ($disasters[$v][1] eq 'concentrate') {
		my @rlist = ('food', 'money', 'soldier');
		my $r = $rlist[int(rand(@rlist))];
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			next if $i eq $m{country};
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.5);
			$cs{$r}[$m{country}] += $cs{$r}[$i];
		}
		&write_world_news("<b>���E���� $disasters[$v][0] ���܂���</b>");
	} elsif ($disasters[$v][1] =~ 'big_(.*)') {
		$r = $1;
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.1);
		}
		&write_world_news("<b>���E���� $disasters[$v][0] ���N����܂���</b>");
	}
}

#================================================
# �����ް������邩�`�F�b�N
#================================================
sub you_exists {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;

	if (-f "$userdir/$y_id/user.cgi") {
		return 1;
	}
	return 0;
}
#================================================
# �����ް���Get �߂�l�̓n�b�V��
#================================================
# �g����: &get_you_datas('����̖��O');
sub get_you_datas {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;

	open my $fh, "< $userdir/$y_id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
	my $line_data = <$fh>;
	my $line_info = <$fh>;
	close $fh;

	my($paddr, $phost, $pagent) = split /<>/, $line_info;

	my %you_datas = (
		addr	=> $paddr,
		host	=> $phost,
		agent	=> $pagent,
	);
	for my $hash (split /<>/, $line_data) {
		my($k, $v) = split /;/, $hash;
		next if $k =~ /^y_/;

		$you_datas{$k} = $v;
	}
# �čՂ�p
	if (&on_summer) {
#		unless (-f "$userdir/$y_id/summer.cgi") {
#			open my $fh, "> $userdir/$y_id/summer.cgi";
#			close $fh;
#		}
		open my $fh, "< $userdir/$y_id/summer.cgi" or &error("�čՂ�p̧�ق����݂��܂���");
		my $line = <$fh>;
		close $fh;

		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$you_datas{$k} = $v;
		}
		$you_datas{dummy} = 1;
	}

	return %you_datas;
}

#================================================
# �����ް��ύX  �������Ɠ��Z��̏n���xUP���Ɏg�p
#================================================
# �g����: &regist_you_data('����̖��O', '�ύX�������ϐ�', '�l');
sub regist_you_data {
	my($name, $k, $v) = @_;
	return if $name eq '' || $k eq '';

	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	$line =~ s/<>($k;).*?<>/<>$1$v<>/;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}
#================================================
# �����ް��ύX  �������Ɠ��Z��̏n���xUP���Ɏg�p
#================================================
# my @array = (['�ύX�������ϐ�1', '�l1'], ['�ύX�������ϐ�2', '�l2']);
# &regist_you_array('����̖��O', @array);
sub regist_you_array {
	my $name = shift;
	my @data = @_;
	return if $name eq '' || !@data;

	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	# ���������Ώۂɂ���Ă͑҂����������� 1�x���΍ςނ̂�2��ڈȍ~�͂Ȃ�
	my $bool = 0;
	for my $i (0 .. $#data) {
		last if $bool;
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if ($k eq 'lib' || $k eq 'value') {
			my %you_datas = &get_you_datas($y_id,1);
			if(($k eq 'lib' && $you_datas{lib} eq 'military' && $you_datas{tp} eq '610') || ($k eq 'value' && $you_datas{value} eq 'military_ambush')){
				$bool = 1;
				my @lines = ();
				open my $fh, "+< $logdir/$you_datas{country}/patrol.cgi" or &error("$logdir/$you_datas{country}/patrol.cgi̧�ق��J���܂���");
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($pat_time,$p_name) = split /<>/, $line;
					next if $p_name eq $name;
					push @lines, $line;
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}
		}
	}

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	for my $i (0 .. $#data) {
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if(index($line, "<>$k;") >= 0){
			$line =~ s/<>($k;).*?<>/<>$1$v<>/;
		}else{
			$line = "$k;$v<>" . $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}

#================================================
# �S���ɒǉ�
#================================================
sub add_prisoner {
	$mes .= "$m{name}�́A�G�����Ɏ��͂܂�߂܂��Ă��܂���!<br>";
	$mes .= "$cs{prison_name}[$y{country}]�֘A�s����܂��B���ɍs���ł���̂�$GWT����ł�<br>";
	$m{lib} = 'prison';
	$m{renzoku_c} = $m{act} = 0;
	$m{tp} = 100;
	&wait;
	my $flag = 0;
	$flag = 1 if ($pets[$m{pet}][2] eq 'no_rescue');
	# �S��ؽĂɒǉ�
	open my $fh, ">> $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	print $fh "$m{name}<>$m{country}<>$flag<>\n";
	close $fh;

	require './lib/_bbs_chat.cgi';
	$this_file = "$logdir/$y{country}/bbs";
	my $w_name = ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) ? '������':$m{name};
	$in{comment} = "$m{mes_lose}�y�N��z$w_name��$cs{prison_name}[$y{country}]�ɘA�s����܂���";
	$bad_time = 0;
	&write_comment;
}
#================================================
# ���͂���ԍ�����
#================================================
=pod
sub get_most_strong_country {
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		next if $i eq $m{country};
		next if $i eq $union;
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}
=cut
sub get_most_strong_country {
	my $skip_my_country = shift;
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		if (!$skip_my_country) {
			next if $i eq $m{country};
			next if $i eq $union;
		}
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}

#================================================
# ��N�����L���O�f�[�^��������
# write_yran(����������v�f, �l, ���[�h [, ����������v�f2, �l2, ���[�h2]);
# �����̍��ڂ���x�ɓn���邯�� ����*3 �̈����Œ�
#================================================
sub write_yran {
	my @data = @_;
	my $size = 3;
	my $count = @data / $size;

	my @lines = ();
	my $new_line = '';
	if(-e "$userdir/$id/year_ranking.cgi"){
		open my $fh, "< $userdir/$id/year_ranking.cgi" or &error("̧�ق��J���܂���");
		while (my $line = <$fh>) {
			# �ߋ�3�N�����Â��f�[�^�͍폜
			if ($line =~ /year;(.*?)<>/ && $1 ne $w{year}) {
				push @lines, $line if $1 >= $w{year} - 3;
				next;
			}
			$line =~ tr/\x0D\x0A//d;
			$new_line = $line if index($line, "year;$w{year}") > -1;
		}
		close $fh;
	}

	$new_line = "year;$w{year}<>" unless $new_line;
	for my $i (1 .. $count) {
		my ($data_name, $data_value, $is_add) = splice(@data, 0, $size);
		next if !$data_name || !$data_value;
		if ($new_line =~ /$data_name;(.*?)<>/) {
			my $value = $is_add
				? $1 + $data_value # �݌v�L�^
				: ($1 < $data_value ? $data_value : $1) ; # �ō��L�^
			$new_line =~ s/$data_name;.*?<>/$data_name;$value<>/;
		}
		else {
			$new_line .= "$data_name;$data_value<>";
		}
	}

	unshift @lines, "$new_line\n"; # push ���ƏW�v���Ƀ��[�v���[���Ȃ�̂� unshift
	open my $fh, "> $userdir/$id/year_ranking.cgi" or &error("̧�ق��J���܂���");
	print $fh @lines;
	close $fh;
}
#================================================
# ���v���W�v
#================================================
sub summary_contribute {
	return if $w{year} !~ /[1-6]$/;
	return unless (-e "$userdir/$id/year_ranking.cgi");

	my %action_log = ();
	my @lines = ();
	open my $fh, "< $userdir/$id/year_ranking.cgi" or &error("̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my $new_line = '';
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			if ($k =~ /contr_(.*)/) {
				$action_log{$1} += $v;
				$v = 0;
			}
			$new_line .= "$k;$v<>";
		}
		push @lines, "$new_line\n";
	}
	close $fh;

	open my $fh, "> $userdir/$id/year_ranking.cgi" or &error("̧�ق��J���܂���");
	print $fh @lines;
	close $fh;

	unless (-e "$logdir/action_log_country_$m{country}.cgi") {
		open my $fht, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgi���J���܂���");
		print $fht "\n";
		close $fht;
	}

	open $fh1, "< $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgi���J���܂���");
	$line = <$fh1>;
	$line =~ tr/\x0D\x0A//d;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} += $v;
	}
	close $fh1;

	for my $k (keys(%action_log)) {
		$nline .= "$k;$action_log{$k}<>";
	}

	open $fh1, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgi���J���܂���");
	print $fh1 "$nline\n";
	close $fh1;
}

# NPC�f�[�^�쐬
sub add_npc_data {
	my $country = shift;

	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]����[1]����No	[2]�K�E�Z
		['��', [0],			[61..65],],
		['��', [1 .. 5],	[1 .. 5],],
		['��', [6 ..10],	[11..15],],
		['��', [11..15],	[21..25],],
		['��', [16..20],	[31..35],],
		['��', [21..25],	[41..45],],
		['��', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) �T�̉ƒ��w(NPC) pigure(NPC) �E�F��(NPC) vipqiv(NPC) DT(NPC) �n��(NPC) �A�V�����C(NPC) �S�~�N�Y(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;

		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}

		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;

	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}
#================================================
# �펞�����C�x���g
#================================================
sub alltime_event {
	if ($w{world} eq '20') {
		my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
		if ($hour >= 6 && $hour <= 18) {
			if (rand(50000) < 1) {
				for my $i (1..$w{country}) {
					for my $j ($i+1..$w{country}) {
						$w{"f_${i}_${j}"} = int(rand(20));
						$w{"p_${i}_${j}"}=2;
					}
				}
				&write_cs;
				&write_world_news("<b>���E����覐΂��~�蒍���ł���</b>");
			}
		} else {
			if (rand(5000) < 1) {
				for my $i (1..$w{country}) {
					for my $j ($i+1..$w{country}) {
						unless ($w{"p_${i}_${j}"} == 1) {
							$w{"f_${i}_${j}"} = int(rand(20));
							$w{"p_${i}_${j}"} = 2;
						}
					}
				}
				&write_cs;
				&write_world_news("<b>�ԉΑ��J�n�̂��m�点</b>");
			}
		}
	}
	if ( $w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12') ) {
		if (rand(5000) < 1) {
			&disaster(1);
			&write_cs;
		}
	}
	if ($w{world} eq $#world_states-4) {
		if (rand(500) < 1) { # ����1000 ��ڲ԰�S�̂ɂ�锭���ł͂Ȃ��\������������ڲ԰�P�̂ɂ�锭���Ȃ̂Ōl�l��1000�͎኱�����C������ �Z�t�@�C���̓ǂݍ��݂��N����̂���肩
			require './lib/fate.cgi';
			&super_attack('random');
		}
	}
#	&debug_log("$m{lib}:$m{tp}", 'play_log');
}

#================================================
# login.cgi��bj.cgi
# ���O�C�������[�U�[�f�[�^�̎擾��A�^����ɌĂяo�����
# �����̓ǂݍ��݂�������ۂ��@��F��ǂ̗򉻂� alltime_event �ł��ƃ^�C�~���O�I�Ȗ�肩�����e���|�Y����
#================================================
sub before_bj {

	my($lmin,$lhour,$lmday,$lmon,$lyear) = (localtime($m{ltime}))[1..5];
	my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..5];

	# ���̓��ŏ��̃A�N�Z�X�Ȃ�
	if ($lmday ne $tmday || $lmon ne $tmon || $lyear ne $tyear) {
		# �a�����v���[���g
		my %datas = ();
		open my $fh, "< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgi̧�ق��J���܂���");
		my $line = <$fh>;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$datas{$k} = $v;
		}
		close $fh;

		if ($datas{birthday} && $datas{birthday} =~ /(\d{4})\/(\d{2})\/(\d{2})/) {
			if ($tmon + 1 == $2 && $tmday == $3) {
				$mes .= "Happy Birthday $m{name}!!<br>�a�������߂łƂ�!!<br>";
				require './lib/shopping_offertory_box.cgi';
				my $gvar = $m{sedai};
				if ($m{start_time} + 30 * 24 * 60 * 60 < $time) {
					$gvar += 7;
				}
				&get_god_item($gvar);
			}
		}
	}

	if (&on_summer) {
		if (rand(100) < 1) {
			$mes .= "��������u�N�A��������̓��[���������悤�v<br>";
			$m{pop_vote}++;
		}
	}
=pod
	if ($w{half_hour_time} < $time) {
		if ($w{reset_time}) { # �I����Ԓ�
			$w{half_hour_time} = $time + $w{reset_time}; # 2017/08/10 �I����ԏI���܂ŗ򉻃X�g�b�v �����񕜖����Ƒ҂�����20%�Œ�̒����ɍ��킹
		}
		else {
			my $span = 30 * 60; # 30������ -1%
			# �O��̏�������30���o�ߖ��� -1% ���ꊇ�����Ƃ������݌v�Ƃ�����
			my $t = $time;
			my $v = ($t - $w{half_hour_time} + $span) / $span;
			$w{half_hour_time} = $t + $span;
			require './lib/_rampart.cgi'; # ���
			for my $i (1 .. $w{country}) {
				&change_barrier($i, -$v) unless $cs{is_die}[$i];
			}
		}
		&write_cs;
	}
=cut
}
#================================================
# �e���ݒ�l�擾
#================================================
sub get_modify {
	my $var = shift;
	my $modify = $cs{'modify_' . $var}[$m{country}] <= 0 ? ($var eq 'pro' ? 1.0 + 0.05 * $cs{'modify_' . $var}[$m{country}] : 1.0 + 0.1 * $cs{'modify_' . $var}[$m{country}]):
				$cs{'modify_' . $var}[$m{country}] <= 5 ? (1.0 + 0.04 * $cs{'modify_' . $var}[$m{country}]):
													(1.1 + 0.02 * $cs{'modify_' . $var}[$m{country}]);
	return $modify;
}
#================================================
# �f�[�^�C��
#================================================
sub cs_data_repair{
	&read_cs;
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %p = &get_you_datas($pid, 1);

		if ($p{country} > $w{country}) {
			if ($p{name} ne $m{name}) {
				&regist_you_data($p{name}, 'country', 0);
			} else {
				$m{country} = 0;
			}
			$p{country} = 0;
		}

		push @{ $members{$p{country}} }, "$p{name}\n";
		++$count;
	}
	closedir $dh;
	$w{player} = $count;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;

		for my $k (qw/dom war mil pro/) {
			if ($cs{$k}[$i] eq '') {
				$cs{$k . '_c'}[$i] = 0;
			}
		}
	}
	&write_cs;
}
#================================================
# ����r�b�O�f�[�^
#================================================
sub sale_data_log {
	return 1;
=pod
	my ($kind, $item_no, $item_c, $item_lv, $price, $place) = @_;

	my $sale_data_file = "$logdir/shop_big_data.cgi";
	open my $fh, ">> $sale_data_file" or &error("$sale_data_file���J���܂���");
	print $fh "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$place<>$time<>\n";
	close $fh;
=cut
}
#================================================
# ����r�b�O�f�[�^�擾
#================================================
sub get_sale_data_log {
	return 1;
=pod
	my ($k, $n) = @_;
	my @lines = ();

	my $sale_data_file = "$logdir/shop_big_data.cgi";
	open my $fh, "< $sale_data_file" or &error("$sale_data_file���J���܂���");
	while (my $line = <$fh>) {
		my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
		if (($kind eq $k && $item_no eq $n) || (!$k && !$n)) {
			push @lines, $line;
		}
	}
	close $fh;

	return @lines;
=cut
}
#================================================
# ����r�b�O�f�[�^HTML�o��
#================================================
sub create_sale_data_chart {
	return 1;
=pod
	my ($k, $n) = @_;
	my @lines = &get_sale_data_log($k, $n);

	if (@lines > 1) {
		my @data_lines = @lines;
		while (@lines > 30) {
			shift @lines;
		}

		@lines = map { $_->[0] } sort { $a->[5] <=> $b->[5] } map { [$_, split /<>/ ]} @lines;
		my $max_price = (split /<>/, $lines[-1])[4];
		my $min_price = (split /<>/, $lines[0])[4];

		if ($max_price == $min_price) {
			$max_price++;
		}

		@lines = map { $_->[0] } sort { $a->[7] <=> $b->[7] } map { [$_, split /<>/ ]} @lines;
		my $max_time = (split /<>/, $lines[-1])[6];
		my $min_time = (split /<>/, $lines[0])[6];

		if ($max_time == $min_time) {
			$max_time++;
		}

		my @x = ();
		my @y = ();

		my $c_str = $k eq '1' ? '�ϋv�l':
				$k eq '2' ? '�z���l':
				$k eq '3' ? '��':
							'';

		my $lv_str = $k eq '1' ? '��':
				$k eq '2' ? '':
				$k eq '3' ? '':
							'';

		my $csv = "����,���z,���,$c_str,$lv_str\n";
		my $price_table = "<table><tr><th>����</th><th>���z</th><th>���</th><th>$c_str</th><th>$lv_str</th></tr>";
		for my $line (@lines) {
			my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
			push @x, (($i_time - $min_time) / ($max_time - $min_time) * 100);
			push @y, (($price - $min_price) / ($max_price - $min_price) * 100);
		}
		my ($inc_c, $inc_total_price, $inc_ave_price) = (0, 0, 0);
		my ($egg_c, $egg_total_price, $egg_ave_price) = (0, 0, 0);
		for my $line (0 .. $#data_lines) {
#		for my $line (@data_lines) {
			my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $data_lines[$#data_lines - $line];
			my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($i_time);
			$year += 1900;
			$mon++;
			if ($k eq '2') {
				if ($eggs[$item_no][2] <= $item_c) {
					$inc_c++;
					$inc_total_price += $price;
				}
				elsif (10 < $price && $place < 4) {
					$egg_c++;
					$egg_total_price += $price;
				}
			}

			my $time_str = "$year�N$mon��$mday�� $hour��$min��$sec�b";
			my $time_str_csv = "$year-$mon-$mday $hour:$min:$sec";
			my $type_str = $place eq '1' ? '���l�̓X':
							$place eq '2' ? '������':
							$place eq '3' ? '�����݁i�����j':
							$place eq '4' ? '�ެݸ�����':
											'�j����';
			$price_table .= "<tr><td>$time_str</td><td>$price</td><td>$type_str</td><td>$item_c</td><td>$item_lv</td></tr>";
			$csv .= "$time_str_csv,$price,$type_str,$item_c,$item_lv\n";
		}
		$price_table .= '</table>';
		if ($k eq '2') {
			$inc_ave_price = int($inc_total_price / $inc_c) if 0 < $inc_c;
			$egg_ave_price = int($egg_total_price / $egg_c) if 0 < $egg_c;
		}

		my $chdx = join ',', @x;
		my $chdy = join ',', @y;
		my $item_title = &get_item_title($k, $n);;
		$csv = $item_title . "\n" . $csv;
		# CSV̧�ٍ쐬
		my $csv_file = "./html/item_$k" . "_" . "$n.csv";
		open my $out_csv, "> $csv_file";
		print $out_csv $csv;
		close $out_csv;

		my $html = '';
		$html .= qq|<html><head>|;
		$html .= qq|<meta http-equiv="Pragma" content="no-cache">|;
		$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
		$html .= qq|<meta http-equiv="Expires" content="0">|;
		$html .= qq|<title>$title</title>|;
		$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		$html .= qq|</head><body $body>|;
		$html .= qq|<p>�X�V���� $date</p>|;
		$html .= qq|<hr size="1"><h1>$item_title�̑���</h1>|;
		$html .= qq{<img src="http://chart.apis.google.com/chart?cht=lxy&chs=500x350&chxt=y&chxl=0:|$min_price|$max_price}
			  .  qq{&chd=t:$chdx|$chdy">};
		$html .= qq|<br><table><tr><td>�z�����������</td><td>$inc_c��</td></tr><tr><td>���ϋ��z</td><td>${inc_ave_price}G</td></tr><tr><td>���̑������</td><td>$egg_c��</td></tr><tr><td>���ϋ��z</td><td>${egg_ave_price}G</td></tr></table>| if $k eq '2';
		$html .= qq|<br>$price_table|;
		$html .= qq|<br><a href="item_${k}_${n}.csv">csv�t�@�C���_�E�����[�h</a>|;
		$html .= qq|<br><div align="right" style="font-size:11px">|;
		$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama�y.net</a><br>|;  # ����\��:�폜�E��\�� �֎~!!
		$html .= qq|$copyright|;
		$html .= qq|</div></body></html>|;

		# HTMĻ�ٍ쐬
		my $html_file = "./html/item_$k" . "_" . "$n.html";
		open my $out, "> $html_file";
		print $out $html;
		close $out;
	}
=cut
}

#================================================
# �K�����擾
#================================================
sub get_rank_name {
	my($rank, $name) = @_;
	my $is_ceo = 0;
	if ($name) {
		for my $i (1..$w{country}) {
			if ($name eq $cs{ceo}[$i]) {
				$is_ceo = 1;
			}
		}
	}
	if ($rank == $#ranks && $is_ceo) {
		return '�c��';
	}
	return $ranks[$rank];
}

#================================================
# �A�C�e�����擾
# ��P�����Ƒ�Q���������Ŗ��O
# ��R�����܂ł��߯Ă��������ǉ� �ެݸ���߯Ă��������g���̂�
# ��S�����܂Ŏw�肷��ƑS�A�C�e�����ǉ�
# ��T�����̓A�C�e���̎�ނ��\�� �V���b�v�Ȃǈꕔ�ł͎�ނ���\���Ȃ̂�
# $kind �A�C�e���̎��(1���� 2�� 3�߯� 4�h��)
# $item_no �A�C�e���̔ԍ�
# $item_c �A�C�e���������l(�ϋv�l �z���l �� �Ȃ�)
# $item_lv �A�C�e���̃��x��(�� �Ȃ� �Ȃ� �Ȃ�)
# $flag 1 �Ŏ�ޕ\���I�t
# �V�����A�C�e�����ǉ������炱����ύX���邱��
#================================================
sub get_item_name {
	my($kind, $item_no, $item_c, $item_lv, $flag) = @_;

	my $result;
	if (defined($item_lv)) { # �S�����L���Ȃ�A�C�e�����
		$result = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : $kind eq '3' ? "[��]$pets[$item_no][1]��$item_c"
				  :                "[$guas[$item_no][2]]$guas[$item_no][1]"
			  ;
		$result = substr($result, 4) if $flag; # $flag ���L���Ȃ�A�C�e������\��
	}
	else { # �S�����L������Ȃ��Ȃ�A�C�e����
		$result = $kind eq '1' ? "$weas[$item_no][1]"
				  : $kind eq '2' ? "$eggs[$item_no][1]"
				  : $kind eq '3' ? (defined($item_c) ? "$pets[$item_no][1]��$item_c" : "$pets[$item_no][1]") # ��R�����L�������߯ĂȂ烌�x���t��
				  :                "$guas[$item_no][1]"
				  ;
	}
	return $result;
}

#================================================
# Twitter�{�b�g
#================================================
sub twitter_bot {
	require "$datadir/twitter_bots.cgi";
#	my $mes = &{$twitter_bots[$w{twitter_bot}]};
#	my $mes = &{$twitter_bots[int(rand(@twitter_bots))]};
#	&send_twitter($mes);
#	$w{twitter_bot}++;
#	if ($w{twitter_bot} >= @twitter_bots) {
#		$w{twitter_bot} = 0;
#	}
#	&write_cs;
}

#================================================
# ��{�s���̑O��̋��ʏ���
# ��{�s�����ǂ������邩�͊e�J���҂ɂ����̂ł͂��邪�A
# �ɂႠ�I�ł͓����E�O���E�R���E�푈�̎l��Ƃ���
#================================================
sub before_action { # �s���O�̋��ʏ���
	return 1;
=pod
	my $action = shift;

	if ($m{icon_pet} && ($action eq 'icon_pet_exp')) {
		my $this_file = "$userdir/$id/pet_icon.cgi";
		open my $fh, "+< $this_file" or &error("$this_file ̧�ق��J���܂���");
		eval { flock $fh, 2; };
		my $line = <$fh>;

		$m{icon_pet_exp} -= int($_[0]);
		if ($m{icon_pet_exp} <= 0) {
			++$m{icon_pet_lv};
			$m{icon_pet_exp} = int(20 * (1.1 ** $m{icon_pet_lv}));
		}

		$line =~ s/<>($m{pet});.*?;.*?;.*?<>/<>$1;$m{icon_pet};$m{icon_pet_lv};$m{icon_pet_exp}<>/;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh $line;
		close $fh;
	}
=cut
}


sub after_success_action { # �s���̐�����̋��ʏ���
	my $action = shift; # �s����
	my $v = shift; # �s���ɔ������炩�̃f�[�^

	#if ($w{world} eq $#world_states-4) {
		#require './lib/fate.cgi';
		#&super_attack($action);
		#&super_attack('single') if ($action eq 'war') && $v;
	#}
}
sub remove_pet { # �߯ĊO������
	$m{pet} = 0;
	$m{icon_pet} = '';
	$m{icon_pet_lv} = 0;
	$m{icon_pet_exp} = 0;
}

# ���ĒB���Ɋւ���s���̐������ɌĂяo���Ɣ����B�������Ȃǂ�����Ă����
# �����ɂ͸��ķ���z��œn��
sub run_tutorial_quest {
	return 1;
=pod
	return unless $m{tutorial_switch};
	my @ks = @_;
	my $is_bbs = 0;
	require './lib/tutorial.cgi';

	for my $k (@ks) {
		++$m{$k};
		if ($m{$k} eq $tutorial_quests{$k}[1]) {
			$is_bbs = 1 if $k eq 'tutorial_bbsc_write_1';
			my $str = &success_quest_result($k);
			&success_quest_mes("���āu$tutorial_quests{$k}[4]�v��B�����܂����I<br>��V�Ƃ���$str<br><br>$tutorial_quests{$k}[6]");

			++$m{tutorial_quest_stamp_c};
			for my $i (0 .. $#tutorial_stamps) {
				if ($tutorial_stamps[$i][1] eq $m{tutorial_quest_stamp_c}) {
					my $str = &{$tutorial_stamps[$i][2]};
					&success_quest_mes("����߂�$tutorial_stamps[$i][1]�W�߂܂����I<br>��V�Ƃ���$str");
				}
			}
		}
	}

	# ����ߺ���ذ�
	if ($m{tutorial_quest_stamp_c} eq $tutorial_quest_stamps) {
		&success_quest_mes("���ׂĂ̽���߂��W�߂܂����I<br>����ر�Ӱ�ނ��I�����܂��B����ر�Ӱ�ނ̐؂�ւ���ϲٰс��l�ݒ肩��ł��܂�");
		&write_tutorial;
		$m{tutorial_switch} = 0;
	}

	&write_user if $is_bbs;
=cut
}


1; # �폜�s��
