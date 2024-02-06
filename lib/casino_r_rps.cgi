#================================================
# ����
#================================================
require './lib/_casino_funcs.cgi'; # ���ĎQ��

$header_size = 2; # �����ެݹݗp��ͯ�ް����
($_field_card, $_cards) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��
$coin_lack = 0; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 2; # �Œ�2�l
$max_entry = 2; # �ō�2�l

sub run {
	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|�ޯĺ��:$head[$_rate]|;
}
#sub show_start_info { # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#}
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_participants_datas], $head[$_rate] ne '') if &is_member($head[$_participants], "$m{name}"); # �ްтɎQ�����Ă���
}
sub show_tale_info { # ��`���ĂȂ��Ă�����ɖ��Ȃ�
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&show_status($head[$_participants_datas]) if $head[$_participants];
}

#================================================
# �Q������̫��
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "�Q������" : "�e�ɂȂ�";
	# ���ɖ��̏���
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("participate", "$button");
	print qq|</form>|;
}

#================================================
# �Q�����鏈�� ڰĂ̂��߂��ݸ����
#================================================
sub participate {
	&_participate('', $m{coin}, 0); # my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ͯ�ް
	my @participants = split /,/, $head[$_participants];
	my $is_start = 0;
	# ���ɖ��̏���
	my @cards = (0..17);

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		# ���ɖ��̏���
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			($mtime, $mturn) = ($time, 2);
			# ���ɖ��̏���
			my @m_cards = ();
			push @m_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
			$mstock = join(',', @m_cards);

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	# ���ɖ��̏���
	if ($is_start) {
		$head[$_cards] = join(',', @cards);
		$$head_line = &h_to_s(@head);
	}
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $participants_datas, $is_bet) = @_;
	unless (&is_my_turn($participants, $m{name})) {
		print qq|<br>���肪�v�l���ł�<br>|;
		return;
	}

	my @hand_cards = split /,/, $m_stock;
	my @hand_card_names = (); # ��D�̖��̂����z��
	push (@hand_card_names, &get_card_name($hand_cards[$_])) for (0 .. $#hand_cards);

	my @participants = &get_members($participants);
	my @participants_datas = split /;/, $participants_datas;
	my @coins = (); # �����Ƒ���̏������
	unless ($is_bet) {
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
			$coins[ ($m{name} ne $datas[0]) ] = $datas[1];
		}
	}

	my $max_bet = $coins[0] < $coins[1] ? $coins[0] : $coins[1];
	my @bet_coins = (int($max_bet/20), int($max_bet/10), int($max_bet/8), int($max_bet/6), int($max_bet/4), int($max_bet/2));

	print qq|<form method="$method" action="$this_script" name="form">|;
	print "�ޯāF".&create_select_menu("bet", 0, @bet_coins)."<br>" unless $is_bet;
	print "��D�F".&create_select_menu("card", 0, @hand_card_names);
	print &create_submit("play", "���ނ��o��");
	print qq|</form>|;
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my $field_card = $head[$_field_card];
	my @cards = split /,/, $head[$_cards];
	my $is_crash = $head[$_field_card] ne '';
	my $is_bet = $head[$_rate] ne '';
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name} && 2 <= $m{c_turn};
	my @participants_datas = split /;/, $head[$_participants_datas];

	my $turn = 0;
	my @names = (); # �����Ƒ���̖��O
	my @hand_cards = ();
	my @coins = (); # �����Ƒ���̏������
	my @play_cards = ();
	my @m_new_cards = ();
	my @y_new_cards = ();

	my $result_str = '';
	my $result_coin = 0;
	if ($is_my_turn) { # ��������݂̍s��
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
			$names[ ($m{name} eq $datas[0]) ] = $datas[0]; # ��U�̍s���ŏ������邩�� eq �� 1 �ɱ���
			$coins[ ($m{name} ne $datas[0]) ] = $datas[1]; # �ǂ����ł��ǂ����� 0 �������A 1 ������
			@hand_cards = split /,/, $datas[2] if $m{name} eq $datas[0];
		}

		$head[$_field_card] = splice(@hand_cards, $in{card}, 1);
		if ($is_bet) { # �ޯĂ���Ă���
			if ($is_crash) { # ���łɑ��肪���ނ��o���Ă���
				@play_cards = ($field_card % 3, $head[$_field_card] % 3); # ����Ǝ����̶��ނ��擾

				if ($play_cards[1] eq '0') {
					$result_str = $play_cards[0] eq '1' ? '����'
									: $play_cards[0] eq '2' ? '����'
									:								  '������'
									;
				}
				elsif ($play_cards[1] eq '1') {
					$result_str = $play_cards[0] eq '2' ? '����'
									: $play_cards[0] eq '0' ? '����'
									:								  '������'
									;
				}
				elsif ($play_cards[1] eq '2') {
					$result_str = $play_cards[0] eq '0' ? '����'
									: $play_cards[0] eq '1' ? '����'
									:								  '������'
									;
				}

				if ($result_str ne '������' || @hand_cards == 0) { # ����������Ȃ����A��D���Ȃ��Ȃ����痬��
					$result_coin = $head[$_rate];
					$head[$_rate] = '';
					push @m_new_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
					push @y_new_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
					$head[$_cards] = join(',', @cards);
				}
				$head[$_field_card] = '';
			}
			if ($result_str ne '����') { # ��������Ȃ��Ȃ���݌��C�R�[�������������ޯČ�
				$head[$_participants] = &change_turn($head[$_participants]); # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
			}
		}
		else { # �ޯĂ���Ă��Ȃ�
			my $max_bet = $coins[0] < $coins[1] ? $coins[0] : $coins[1];
			my @bet_coins = (int($max_bet/20), int($max_bet/10), int($max_bet/8), int($max_bet/6), int($max_bet/4), int($max_bet/2));
			$head[$_rate] = $bet_coins[$in{bet}];
			$head[$_participants] = &change_turn($head[$_participants]); # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
		}
	}

	my ($winner_coin, $loser_coin) = (0, 0);
	if ($is_my_turn && $is_bet && $is_crash && $result_str && $result_str ne '������') {
		# ������݂̎擾
		($winner_coin, $loser_coin) = $result_str eq '����' ? ($coins[0], $coins[1]) : ($coins[1], $coins[0]);

		if (2500000 < ($winner_coin + $result_coin)) { # ������� + ���麲� �� 2500000 �𒴂���Ȃ�
			$result_coin = (2500000 - $winner_coin); # ���麲݂� 2500000 �����x
			$winner_coin = 2500000; # ������݂� 2500000
			$loser_coin -= $result_coin;
		}
		else { # ��݂̈ړ��ŏ����ł��麲݂̏���≺���Ɉ���������Ȃ�
			$winner_coin += $result_coin;
			$loser_coin -= $result_coin;
		}
	}

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if ($mname eq $game_members[0] && $is_my_turn) {
			$mtime = $time;
			if ($is_bet && $is_crash && (($result_str && $result_str ne '������') || @hand_cards == 0)) {
				if ($result_str && $result_str eq '����') {
					$mvalue = $winner_coin;
				}
				elsif ($result_str && $result_str eq '����') {
					$mvalue = $loser_coin;
				}
				$mstock = join(',', @m_new_cards);
			}
			else {
				$mstock = join(',', @hand_cards);
			}
			$is_find++;
		}
		elsif ($mname eq $game_members[1] && $is_my_turn) {
			if ($is_bet && $is_crash && (($result_str && $result_str ne '������') || @hand_cards == 0)) {
				if ($result_str && $result_str eq '����') {
					$mvalue = $loser_coin;
				}
				elsif ($result_str && $result_str eq '����') {
					$mvalue = $winner_coin;
				}
				$mstock = join(',', @y_new_cards);
				$mes .= "game_members 1 $mturn<br>";
			}
			$is_find++;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

#	if ($is_my_turn && $is_bet && $is_crash && $result_str && @cards == 0 && @hand_cards == 0 && @m_new_cards == 0) {
	if ($is_my_turn && $is_bet && $is_crash && @cards == 0 && $result_str && @m_new_cards == 0 && ( ($result_str ne '������' && @hand_cards < 3) || @hand_cards == 0)) {
#	if ($m{c_turn} == 5 && @m_new_cards == 0) {
		&init_header(\@head);
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $result_mes = '';
	if ($is_my_turn && $is_bet && $is_crash && $result_str && $result_str ne '������') {
		if ($result_str eq '����') {
			$m{coin} = $winner_coin;
			&write_user;
			&regist_you_data($game_members[1], 'coin', $loser_coin);
			$result_mes .= "<br>$game_members[0] �� $result_coin ��� �����܂���<br>";
			$result_mes .= "$game_members[1] �� $result_coin ��� �����܂���";
		}
		else {
			$m{coin} = $loser_coin;
			&write_user;
			&regist_you_data($game_members[1], 'coin', $winner_coin);
			$result_mes .= "<br>$game_members[1] �� $result_coin ��� �����܂���<br>";
			$result_mes .= "$game_members[0] �� $result_coin ��� �����܂���";
		}

	}

	# �I������
	# ��������݁A�ޯĂ���Ă�A����񂯂񂵂Ă�A���ʏo�Ă�A�����ޯ��Ȃ��A��D���Ȃ�
	if ($is_my_turn && $is_bet && $is_crash && @cards == 0 && $result_str && @m_new_cards == 0 && ( ($result_str ne '������' && @hand_cards < 3) || @hand_cards == 0)) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
	}

	if ($is_my_turn) {
		unless ($is_bet && $is_crash) {
			return '����[�񂯁[��I';
		}
		else {
			return "�|�����I $names[0](".&get_card_name($play_cards[0]).") vs $names[1](".&get_card_name($play_cards[1]).")$result_mes";
		}
	}
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
			print "$datas[0]($datas[1]���)";
			print "<br>" if $i != $#participants_datas;
	}
}

sub get_card_name {
	my $card = $_[0] % 3;
	return $card == 1 ? '�`���L'
		  : $card == 2 ? '�p�['
							: '�O�[';
}

1;#�폜�s��