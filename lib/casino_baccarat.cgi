#================================================
# ����
#================================================
use bignum;
require './lib/_casino_funcs.cgi'; # ���ĎQ��

$header_size = 4; # �޶חp��ͯ�ް����
# �e�A��ݶ���D�A��ڲ԰��D�A�f�b�L
($_leader, $_b_cards, $_p_cards, $_deck) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��
$coin_lack = 0; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 2; # �Œ�2�l
$max_entry = 10; # �ō�2�l


my @nums = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K');
my @suits = $is_mobile ? ('S', 'H', 'C', 'D') : ('&#9824;', '&#9825;', '&#9827;', '&#9826;');
my @targets = ('��ڲ԰��', '��ݶ���', '����');

my $max_bet = 200000; # 0.5�{�����̂Ŏ��ۂ̔{�̒l
my @pers = (0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5);

sub run {
	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
#	print qq|�ޯĺ��:$head[$_rate]|;
#	my @deck = &shuffled_deck(6);
#	my $cards = 0;
#	$cards = ($cards << 6) + $deck[$_] for (0..$#deck);
#	print qq|$cards<br>|;
#	for my $i (0..$#deck) {
#		print qq|$deck[$i]<br>|;
#	}
}
#sub show_start_info { # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#}
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_participants_datas], $head[$_rate] ne '', $head[$_leader]) if &is_member($head[$_participants], "$m{name}"); # �ްтɎQ�����Ă���
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
#	$m{coin} = 1500000;
#	&write_user;
}

#================================================
# �Q�����鏈�� ڰĂ̂��߂��ݸ����
#================================================
sub participate {
	&_participate('', '', $m{coin}); # my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;
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
	my @deck = &shuffled_deck(6);
	my $cards = 0;
	$cards = ($cards << 6) + $deck[$_] for (0..$#deck);

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		# ���ɖ��̏���
		$head[$_leader] = $participants[0];
		$head[$_deck] = $cards;
		$$head_line = &h_to_s(@head);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			($mtime, $mturn) = ($time, 2);
			# ���ɖ��̏���

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $participants_datas, $is_bet, $leader) = @_;

	my $is_all_bet = 1; # �q�S�����ޯď��
	my $is_bet = 0; # �������ޯď��
	my @participants = &get_members($participants);
	my @participants_datas = split /;/, $participants_datas;
	my $leader_coin = 0;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		if ($datas[0] eq $leader) { # �e���ޯĂ͍l�������A������݂��擾����
			$leader_coin = $datas[2]; # �e�̏������
			next;
		}
		$is_all_bet = 0 if $datas[1] eq ''; # �N�����ޯĂ��ĂȂ�
		$is_bet = 1 if $m{name} eq $datas[0] && $datas[1] ne ''; # �����͂��ł��ޯĂ��Ă���
	}

	my $is_leader = $participants[0] eq $m{name}; # �e�ł��邩
	if ( (!$is_all_bet && $is_leader) || $is_bet) { # �e���q���ޯèݸނ�҂��Ă邩�A���ł��ޯèݸނ��Ă���q
		print qq|<br>�q���ޯèݸނ�҂��Ă��܂�<br>|;
		return;
	}

	if ($is_leader) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("deal", "�z��");
		print qq|</form>|;
	}
	else {
		my @bet_coins = ();
		my $member_c = @participants - 1;
		my $size = length($leader_coin) - 1;
		my $leader_max_bet = (substr($leader_coin, 0, 1) . '0' x $size) / $member_c;
		@bet_coins = &get_bet_coins($leader_max_bet);

		print qq|<form method="$method" action="$this_script" name="form">|;
		print "�ޯāF".&create_select_menu("bet", 0, @bet_coins)."<br>";
		print "�ΏہF".&create_select_menu("target", 0, @targets);
		print &create_submit("play", "�q����");
		print qq|</form>|;
	}
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @participants = split /,/, $head[$_participants];
	my $is_member = &is_member($head[$_participants], $m{name});

	unless ($is_member) {
		close $fh;
		return;
	}

	my @participants_datas = split /;/, $head[$_participants_datas];
	my $leader_coin = 0;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		if ($datas[0] eq $head[$_leader]) { # �e���ޯĂ͍l�������A������݂��擾����
			$leader_coin = $datas[2]; # �e�̏������
			last;
		}
	}
	my @bet_coins = &get_bet_coins($leader_coin);

	my %sames = ();
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		# �e����Ȃ��A�ޯĂ����ĂȂ��Ȃ珈��
		if ($head[$_leader] ne $mname && $is_member && $mname eq $m{name} && 2 <= $mturn && $mvalue eq '') {
			$mtime = $time;
			$mvalue = $in{target};
			$mstock = $bet_coins[$in{bet}];
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return "$targets[$in{target}] $bet_coins[$in{bet}] ��� �q���܂���";
}

#================================================
# ��ڲ�̏���2
#================================================
sub deal {
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @participants = split /,/, $head[$_participants];

	my $is_all_bet = 1; # �q�S�����ޯď��
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		next if $datas[0] eq $participants[0]; # �e���ޯĂ͍l�����Ȃ�
		$is_all_bet = 0 if $datas[2] eq ''; # �N�����ޯĂ��ĂȂ�
		last unless $is_all_bet;
	}
	unless ($is_all_bet) {
		close $fh;
		return;
	}

	my @p_cards = ();
	my @b_cards = ();
	for my $i (0 .. 1) {
		push @p_cards, $head[$_deck] & 63;
		$head[$_deck] >>= 6;

		push @b_cards, $head[$_deck] & 63;
		$head[$_deck] >>= 6;
	}

	my @points = (&calc(@p_cards), &calc(@b_cards));
	my @is_hit = (0, 0);
	if ($points[0] < 8 && $points[1] < 8) { # Player �� Banker �ǂ���� 8 9 ����Ȃ��Ȃ����āi�ǂ��炩�� 8 9 �Ȃ����Ĕ�΂��ď����j
		if ($points[0] < 6) { # 0�`5 Hit
			push @p_cards, $head[$_deck] & 63;
			$head[$_deck] >>= 6;
			$is_hit[0] = 1;
		}

		if ($points[1] < 3 || (!$is_hit[0] && $points[1] < 7) ) { # 0�`2 �� 3�`6 �� Player ��3���ڂ������ĂȂ��Ȃ� Hit
			push @b_cards, $head[$_deck] & 63;
			$head[$_deck] >>= 6;
			$is_hit[1] = 1;
		}
		elsif (2 < $points[1] && $points[1] < 7 && $is_hit[0]) { # 4�`6 �� Player ��3���ڂ������Ă���
			my $p_3_pt = &calc($p_cards[2]); # Player ��3���ڂ��߲��
			if (	($points[1] == 3 && $p_3_pt != 8) # 3 Player ��3���ڂ� 8 ����Ȃ��Ȃ� Hit
				||	($points[1] == 4 && $p_3_pt != 0 && $p_3_pt != 1 && $p_3_pt != 8 && $p_3_pt != 9) # 4 Player ��3���ڂ� 0 1 8 9 ����Ȃ��Ȃ� Hit
				||	($points[1] == 5 && ($p_3_pt == 4 || $p_3_pt == 5 || $p_3_pt == 6 || $p_3_pt == 7)) # 5 Player ��3���ڂ� 4 5 6 7 �Ȃ� Hit
				||	($points[1] == 6 && ($p_3_pt == 6 || $p_3_pt == 7))) { # 6 Player ��3���ڂ� 6 7 �Ȃ� Hit
				push @b_cards, $head[$_deck] & 63;
				$head[$_deck] >>= 6;
				$is_hit[1] = 1;
			}
		}

		@points = (&calc(@p_cards), &calc(@b_cards));
	}

	my $result = $points[1] < $points[0] ?		0	# Tie
				  : $points[0] < $points[1] ?		1	# Player����
				  :										2;	# Banker����

	my %sames = ();
	my @members = ();
	my @winners = ();
	my @win_bets = ();
	my @losers = ();
	my @lose_bets = ();
	my @leader = ();
	my @game_members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟
		if ($participants[0] eq $mname) {
			$mtime = $time;
			@leader = ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock);
			next;
		}

		my $is_find = 0;
		for my $participant (@participants) {
			if ($participant eq $mname && 2 <= $mturn) {
				push @game_members, $mname;
				$is_find = 1;
				last;
			}
		}
		# �Q���҂Ȃ珈��
		if ($is_find) {
			if ($mvalue == $result) {
				push @winners, $mname;
				push @win_bets, $mstock;
			}
			else {
				push @losers, $mname;
				push @lose_bets, $mstock;
			}
			$mtime = $time;
			$mvalue = $mstock = '';
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	for $i (0 .. $#winners) {
		my $v = 0;
		$v = $result == 0 ? $win_bets[$i] * 1 # Player���� �z��1�{
			: $result == 1 ? int($win_bets[$i] * 0.95) # Banker����  �z��0.95�{
			:					  $win_bets[$i] * 8; # Tie �z��8�{
		$leader[5] = ($leader[5] - $v) < 0 ? 0 : $leader[5] - $v;
	}
	if ($result != 2) {
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			$leader[5] = 2500000 < ($leader[5] + $v) ? 2500000 : $leader[5] + $v;
		}
	}
	unshift @members, "$time<>$leader[1]<>$leader[2]<>$leader[3]<>$leader[4]<>$leader[5]<>\n"; # leader

	my $leader = $head[$_leader];
	if (4 <= $m{c_turn}) {
		&init_header(\@head);
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $result_mes = 'Player�F';
	for my $i (0 .. $#p_cards) {
		my ($num, $suit) = &get_card($p_cards[$i]);
		$result_mes .= "$suits[$suit]$nums[$num]";
		$result_mes .= ' ' if $i < $#p_cards;
	}
	$result_mes .= "($points[0]) Banker�F";

	for my $i (0 .. $#b_cards) {
		my ($num, $suit) = &get_card($b_cards[$i]);
		$result_mes .= "$suits[$suit]$nums[$num]";
		$result_mes .= ' ' if $i < $#b_cards;
	}
	$result_mes .= "($points[1])";

	my $total_v = 0;
	for $i (0 .. $#winners) {
		my $v = 0;
		$v = $result == 0 ? $win_bets[$i] * 1 # Player���� �z��1�{
			: $result == 1 ? int($win_bets[$i] * 0.95) # Banker����  �z��0.95�{
			:					  $win_bets[$i] * 8; # Tie �z��8�{
		my $vv = &coin_move($v, $winners[$i], 1);
		&coin_move(-1 * $vv, $leader, 1);
		$total_v -= $v;
		$result_mes .= "<br>$winners[$i] �� $v ��� �����܂���";
#		$result_mes .= '<br>' if $i < $#winners;
	}

	if ($result != 2) {
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			my $vv = &coin_move(-1 * $v, $losers[$i], 1);
			&coin_move(-1 * $vv, $leader, 1);
			$total_v += $v;
			$result_mes .= "<br>$losers[$i] �� $v ��� �����܂���";
		}
	}
	else { # Tie ���O���Ă������ɂȂ炸�ޯĖ߂��Ă���
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			$result_mes .= "<br>$losers[$i] �� $v ��� �̕����߂��ł�";
		}
	}

	$result_mes .= "<br>$leader �� $total_v ��� ���܂���";

	$m{c_turn}++;
	if (5 <= $m{c_turn}) {
		$m{c_turn} = 0;

		for my $game_member (@game_members) {
			&regist_you_data($game_member, 'c_turn', '0');
		}
	}
	&write_user;

	return $result_mes;
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
			print "$datas[0]($datas[2]���)";
			print "<br>" if $i != $#participants_datas;
	}
}

sub shuffled_deck {
	my $deck_n = shift; # �ޯ���
	my $size = 52; # ���ޖ���
	my @deck = ();
	for my $i (0..$deck_n) {
		push @deck, $_ for (1 ..$size);
	}
	for my $i (0 .. $#deck) {
		my $j = int(rand($i + 1)); # ���񂷂�x�ɗ����͈͂��L����
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}

sub get_card {
	my $card = shift;
	my $num = ($card-1) % 13; # 1�`52 �̒l���� -1 �������̂� 13 �Ŋ������]�肪 0�`12 �ɂȂ�
	my $suit = int(($card-1)/13); # 0��߰�� 1ʰ� 2���� 3�޲�
	return ($num, $suit);
}

sub calc {
	my @cards = @_;
	my $tmp_pt = 0;
	my $pt = 0;
	for my $i (0 .. $#cards) {
		$tmp_pt = (($cards[$i]-1) % 13) + 1; # 1�`13
		if ($tmp_pt < 10) {
			$pt += $tmp_pt;
		}
	}
	return substr($pt, -1);
}

sub get_bet_coins {
	my $bet = $max_bet < $_[0] ? $max_bet : $_[0];
	my @bet_coins = ();
	for my $i (0..$#pers) {
		my $v = int($bet * $pers[$i]);
		push @bet_coins, $v if $v <= $m{coin};
	}
	return @bet_coins;
}

1;#�폜�s��