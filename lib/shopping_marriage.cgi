my $entry_file = $m{sex} eq '1' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
#my $this_file  = $m{sex} eq '2' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
my $this_file;
if (($m{sex} eq '2' && $pets[$m{pet}][2] ne 'marriage_y') || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b')) {
	$this_file  = "$logdir/marriage_man.cgi";
}
else {
	$this_file = "$logdir/marriage_woman.cgi";
}
#================================================
# 結婚相談所 Created by Merino
#================================================

# 最大登録数:古い人は自動削除
my $max_marriage_list = 20;

# ﾚﾍﾞﾙ制限:このﾚﾍﾞﾙ以上でないと利用できない
my $need_lv = 20;

# 登録料,ﾌﾟﾛﾎﾟｰｽﾞ料
my $need_money = $m{sedai} > 20 ? int(40000+$m{lv}*1000) : int($m{sedai}*2000+$m{lv}*1000);

#================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($m{lv} < $need_lv) { # Lv
		$mes .= "結婚相談所は、Lv.$need_lv以上の方でないと入れません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{marriage}) { # 既婚
		$mes .= "不倫することはできません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{job} eq '24') { # 魔法少女
		$mes .= "魔法少女は永遠の14歳です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ここは結婚相談所でございます<br>';
		$mes .= '本日はどのようなご用件でしょうか?<br>';
	}

	&menu('やめる','ﾊﾟｰﾄﾅｰを探す','登録する','婚約する');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# ﾊﾟｰﾄﾅｰ探す
#================================================
sub tp_100 {
	$layout = 1;
	$mes .= 'こちらが、登録者ﾘｽﾄになります<br>';
	$mes .= '気になる方がいましたらｱﾌﾟﾛｰﾁをしてみてはいかがですか?<br>';

	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>Lv</th><th>階級</th><th>ﾒｯｾｰｼﾞ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		next if $name eq $m{name};
		my $rank_name = &get_rank_name($rank, $name);
		my $bname = &name_link($name);
		$bname .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/Lv$lv/階級$rank\name/$message<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ｱﾌﾟﾛｰﾁする" class="button1"></p></form>|;

	$m{tp} += 10;
}
# ------------------
# ｱﾌﾟﾛｰﾁ
sub tp_110 {
	unless ($cmd) {
		&begin;
		return;
	}

	my $send_to;
	open my $fh, "< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			last;
		}
	}
	close $fh;

	unless ($send_to) {
		$mes .= '登録者ﾘｽﾄに登録されていない人にはｱﾌﾟﾛｰﾁできません<br>';
		&begin;
		return;
	}

	$layout = 1;
	$mes .= "ｱﾌﾟﾛｰﾁ(相手にﾒｯｾｰｼﾞを送る)は無料です<br>";
	$mes .= "ﾌﾟﾛﾎﾟｰｽﾞは、成功しても失敗しても $need_money Gかかりますので、<br>ﾌﾟﾛﾎﾟｰｽﾞは親密な関係になってからにしましょう<br>";

	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$cmd">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|[$send_to]にｱﾌﾟﾛｰﾁ<br>|;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="submit" value="手紙を送る/やめる" class="button1">|;
	$mes .= qq|　 <input type="checkbox" name="is_proposal" value="1"> ﾌﾟﾛﾎﾟｰｽﾞ</form>|;
	$m{tp} += 10;
}
# ------------------
sub tp_120 { # flock
	if (!$in{comment}) {
		$mes .= '本文がありません<br>';
		&begin;
		return;
	}
	elsif ($in{is_proposal}) {
		if ( !&is_entry_marriage($m{name}) ) {
			$mes .= "ﾌﾟﾛﾎﾟｰｽﾞするには登録する必要があります<br>";
			&begin;
			return;
		}
		elsif ($m{money} < $need_money) {
			$mes .= "ﾌﾟﾛﾎﾟｰｽﾞするには $need_money G必要です<br>";
			&begin;
			return;
		}
	}

	my $you = ''; # ｱﾌﾟﾛｰﾁの対象者

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file が開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			if ($name eq $m{name}) { # 性転換により
				$mes .= '自分にｱﾌﾟﾛｰﾁすることはできません<br>';
				$is_rewrite = 1;
			}
			elsif ( &is_unmarried($name) ) { # 存在する + 未婚なら
				$you = $line;
				push @lines, $line;
			}
			else { # 存在する + 既婚 or 存在しない
				if (($m{sex} eq '2' && $pets[$m{pet}][2] eq 'marriage_y') || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b')){
					$is_rewrite = 0; # ﾕﾘﾊﾞﾗだと更新しない？ ﾕﾘﾊﾞﾗのｴﾛｽ効果？
   			}
				else {
					$is_rewrite = 1;
				}
			}
		}
		else {
			# 大したことじゃないけど、すでに登録されている非存在のPCと同じ名前に改名すると登録料踏み倒せそう
			# それよりも非存在のｷｬﾗを表示されても邪魔だから登録時に排除 tp_210
			push @lines, $line;
		}
	}
	# 存在しない人、性転換した人、既婚の人がいたら書き換え
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	if ($you) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $you;
		$in{comment} .= "<hr>【結婚相談所：$m{name}様から$name様宛】";
		$in{comment} .= "☆ﾌﾟﾛﾎﾟｰｽﾞ☆" if $in{is_proposal};
		&send_letter($name);
		$mes .= "$nameにｱﾌﾟﾛｰﾁの手紙を送りました<br>";

		# ﾌﾟﾛﾎﾟｰｽﾞ
		&proposal($name) if $in{is_proposal};
	}

	&begin;
}

# ------------------
# ﾌﾟﾛﾎﾟｰｽﾞ
sub proposal { # flock
	my $name = shift;
	my $y_id = unpack 'H*', $name;

	my @lines = ();
	open my $fh, "+< $userdir/$y_id/proposal.cgi" or &error("$userdir/$y_id/proposal.cgiﾌｧｲﾙが開きません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pname) = (split /<>/, $line)[2];
		next if $pname eq $m{name};
		push @lines, $line
	}
	my($last_no) = (split /<>/, $lines[0])[0];
	++$last_no;
	unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	$mes .= "ﾌﾟﾛﾎﾟｰｽﾞ代 $need_money Gを支払い、$nameにﾌﾟﾛﾎﾟｰｽﾞしました<br>";
	$m{money} -= $need_money;
}

#================================================
# 登録
#================================================
sub tp_200 {
	$layout = 2;
	my $sex_name   = $m{sex} eq '1' ? '男性' : '女性';

	$mes .= qq|登録するには、$need_money Gかかります<br>|;
	$mes .= qq|<hr>現在登録されている$sex_nameﾘｽﾄ<br>|;
	$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>Lv</th><th>階級</th><th>ﾒｯｾｰｼﾞ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $entry_file" or &error("$entry_fileﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		my $rank_name = &get_rank_name($rank, $name);
		my $bname = &name_link($name);
		$bname .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr>$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/Lv$lv/階級$rank_name/$message<br>|
			 : qq|<tr><td>$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;


	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="submit" value="送信" class="button1">|;
	$mes .= qq|　 <input type="checkbox" name="cmd" value="1" checked>登録する</form>|;
	$m{tp} += 10;
}
sub tp_210 { # flock
	return if &is_ng_cmd(1);

	my $is_find = 0;
	my @lines = ();
	open my $fh, "+< $entry_file" or &error("$entry_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($name eq $m{name}) {
			$is_find = 1;
			last;
		}
		push @lines, $line;# if &you_exists($name); # 非存在のｷｬﾗは消去したいが、タイミングによってはﾃﾞｰﾀの範囲外にアクセスされるためにリスト埋まるようにしている？

		last if @lines >= $max_marriage_list+1;
	}
	if ($is_find) {
		close $fh;
		$mes .= "$m{name}様はすでにご登録済みです<br>";
	}
	elsif ($m{money} < $need_money) {
		close $fh;
		$mes .= "登録するお金が足りません<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		my $comment = $in{comment} . $m{mes};
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$comment<>$m{icon}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "登録料 $need_money Gを支払いました<br>";
		$mes .= "$m{name}様ですね。ご登録いたしました<br>";
		$m{money} -= $need_money;
		&run_tutorial_quest('tutorial_mariage_1');
	}

	&begin;
}

#================================================
# 婚約する
#================================================
sub tp_300 {
	if($pets[$m{pet}][2] eq 'marriage' || (($pets[$m{pet}][2] eq 'marriage_y' || $pets[$m{pet}][2] eq 'marriage_b') && $m{pet_c} >= 5)) {
		$layout = 1;
		$mes .= 'こちらが、登録者ﾘｽﾄになります<br>';
		$mes .= 'ｴﾛｽの力により永遠の愛を誓います<br>';

		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>Lv</th><th>階級</th><th>ﾒｯｾｰｼﾞ<br></th></tr>| unless $is_mobile;

		open my $fh, "< $this_file" or &error("$this_file が開けません");
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			my $rank_name = &get_rank_name($rank, $name);
			my $bname = &name_link($name);
			$bname .= "[$shogo]" if $shogo;
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/Lv$lv/階級$rank_name/$message<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
		}
		close $fh;
		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="永遠の愛を誓う" class="button1"></p></form>|;

		$m{tp} += 10;
	}
	elsif (-s "$userdir/$id/proposal.cgi") {
		$layout = 1;
		$mes .= 'ﾌﾟﾛﾎﾟｰｽﾞ者一覧<br>';

		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>Lv</th><th>階級</th><th>ﾒｯｾｰｼﾞ<br></th></tr>| unless $is_mobile;

		open my $fh, "< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi ﾌｧｲﾙが読み込めません");
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			my $rank_name = &get_rank_name($rank, $name);
			my $bname = &name_link($name);
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/Lv$lv/階級$rank_name/$message<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
		}
		close $fh;
		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="永遠の愛を誓う" class="button1"></p></form>|;

		$m{tp} += 10;
	}
	else {
		$mes .= 'まだ、誰からもﾌﾟﾛﾎﾟｰｽﾞされていないようです<br>';
		$mes .= '待っていても始まりません<br>こちらからｱﾌﾟﾛｰﾁしてみてはいかがでしょう?<br>';
		&begin;
	}
}
# 結婚
sub tp_310 { # flock
	my $you = '';
	# ｴﾛｽ・ﾕﾘ・ﾊﾞﾗ
	if ($cmd && $pets[$m{pet}][2] eq 'marriage' || (($pets[$m{pet}][2] eq 'marriage_y' ||$pets[$m{pet}][2] eq 'marriage_b') && $m{pet_c} >= 5)) {
		my $is_rewrite = 0;
		my @lines = ();
		my $c;
		open my $tfh, "+< $this_file" or &error("$this_file が開けません");
		eval { flock $tfh, 2; };
		while (my $line = <$tfh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($cmd eq $no) {
				if ($name eq $m{name}) { # 性転換により
					$mes .= '自分にｱﾌﾟﾛｰﾁすることはできません<br>';
					$is_rewrite = 1;
				}
				elsif ( &is_unmarried($name) ) {
					$you = $line;
					push @lines, $line;
				}
				else {
					$is_rewrite = 1;
				}
			}
			else {
				push @lines, $line;
			}
		}
		# 存在しない人、性転換した人、既婚の人がいたら書き換え
		if ($is_rewrite) {
			seek  $tfh, 0, 0;
			truncate $tfh, 0;
			print $tfh @lines;
		}
		close $tfh;

		if ($you) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $you;
			my @plines = ();
			open my $pfh, "+< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgiﾌｧｲﾙが開きません");
			eval { flock $pfh, 2; };
			while (my $pline = <$pfh>) {
				my($pname) = (split /<>/, $pline)[2];
				next if $pname eq $name;
				push @plines, $pline
			}
			my($last_no) = (split /<>/, $plines[0])[0];
			++$last_no;
			unshift @plines, "$last_no<>$mdate<>$name<>$country<>$lv<>$rank<>$shogo<>$message<>$icon<>\n";
			seek  $pfh, 0, 0;
			truncate $pfh, 0;
			print $pfh @plines;
			close $pfh;
			$c = $last_no;
		}

		if($c){
			$cmd = $c;
			&remove_pet if($pets[$m{pet}][2] eq 'marriage');
		}else {
			$cmd = 0;
		}
	}

	$you = '';
	if ($cmd) {
		my $is_marriage = 0;
		open my $fh, "+< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi ﾌｧｲﾙが読み込めません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($cmd eq $no) {
				if ( &is_unmarried($name) ) {
					$is_marriage = 1;
					$you = $line;
					last;
				}
			}
			else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines unless $is_marriage; # 結婚を選択したが、何らかの問題で結婚できず、その人を除き上書き
		close $fh;

		if ($is_marriage) {
			my @you_data;

			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $you;
			$mes .= "$nameと結婚することに決めました!<br>";

			# 相手の結婚項目を変更
			push @you_data, (['marriage', $m{name}]);

			$m{marriage} = $name;
			if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
				$m{job} = 0;
			}

			# 相手の思い出ﾌｧｲﾙに書き込み
			&write_memory("$m{name}と結婚しました☆", $name);
			&write_memory("$nameと結婚しました☆");
			my %you_datas = &get_you_datas($name);
			my $v = int( ($rank_sols[$you_datas{rank}] + $rank_sols[$m{rank}]) * 0.5);
			if($m{sex} eq $you_datas{sex}) {
				&write_world_news(qq|<font color="#8a2be2">＜☆:ﾟ*'同性結婚'*ﾟ:☆＞$m{name}と$nameが結婚しました</font>|);
				#&send_twitter("＜☆:ﾟ*'同性結婚'*ﾟ:☆＞$m{name}と$nameが結婚しました");
				if(int(rand(5)) == 0){
					&remove_pet;
				}elsif(int(rand(5)) == 0 && ($pets[$you_datas{pet}][2] eq 'marriage_y' || $pets[$you_datas{pet}][2] eq 'marriage_b')) {
					#&regist_you_data($name, 'pet', 0);
					push @you_data, (
						['pet', 0],
						['icon_pet', ''],
						['icon_pet_lv', 0],
						['icon_pet_exp', 0],
						);
				}
				$v *= 3;
			}else {
				&write_world_news(qq|<font color="#FF99FF">＜☆:ﾟ*'結婚'*ﾟ:☆＞$m{name}と$nameが結婚しました</font>|);
				#&send_twitter("＜☆:ﾟ*'結婚'*ﾟ:☆＞$m{name}と$nameが結婚しました");
			}
			if($you_datas{job} eq '22' || $you_datas{job} eq '23' || $you_datas{job} eq '24'){
				push @you_data, (['job', 0]);
			}
			&regist_you_array($name, @you_data); # ﾌｧｲﾙｵｰﾌﾟﾝ数3回→1回に圧縮
			undef @you_data;

			&send_money($name,    '結婚祝い金', $v);
			&send_money($m{name}, '結婚祝い金', $v);

			# 登録されている名前を削除
			&delete_entry_marriage($m{name}, $name); # ﾌｧｲﾙｵｰﾌﾟﾝ数4回→最高2回に圧縮
		}
	}

	&begin;
}


#================================================
# 未婚かどうか
#================================================
sub is_unmarried {
	my $name = shift;
	my $y_id = unpack 'H*', $name;

	unless (-f "$userdir/$y_id/user.cgi") {
		$mes .= "残念なことに$name様はすでに他界してしまったようです…<br>";
		return 0;
	}

	my %you_datas = &get_you_datas($name);

	if ($m{sex} eq $you_datas{sex}) {
		if(($m{sex} eq '2' && $pets[$m{pet}][2] eq 'marriage_y' && ($m{pet} == $you_datas{pet} || $m{pet_c} >= 5)) || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b' && ($m{pet} == $you_datas{pet} || $m{pet_c} >= 5))) {
			if ($you_datas{marriage} eq '') { # 未婚
				return 1;
			}
			else {
				$mes .= "残念なことに$name様はすでに他の人と結婚してしまったようです…<br>";
				return 0;
			}
		}else {
			$mes .= "残念なことに$name様は性別が変わってしまったようです…<br>";
			return 0;
		}
	}
	elsif ($you_datas{marriage} eq '') { # 未婚
		return 1;
	}
	else {
		$mes .= "残念なことに$name様はすでに他の人と結婚してしまったようです…<br>";
		return 0;
	}
}

#================================================
# 登録者かどうか
#================================================
sub is_entry_marriage {
	my $entry_name = shift || $m{name};

	open my $fh, "< $entry_file" or &error("$entry_fileﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[2];
		return 1 if $name eq $entry_name;
	}
	close $fh;

	return 0;
}

#================================================
# 登録削除
#================================================
sub delete_entry_marriage { # flock
#	my $del_name = shift || $m{name};
	my @del_names = @_;

	# ﾌｧｲﾙｵｰﾌﾟﾝ数削減
	# 無改造だと男女両方のﾌｧｲﾙを操作するため必ず2回開く必要があるが、ﾕﾘﾊﾞﾗは1回に済むので省略
	# また、性転換した場合などを想定すると取りこぼす可能性があるが黒豚鯖からそうだし別の処理で排除されるため無視
	my @files;
	@files = $entry_file eq $this_file ? ($entry_file) : ($entry_file, $this_file);

	for my $file (@files) {
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $file" or &error("$fileﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			my $is_not_find = 0;
			for my $del_name (@del_names) {
				if ($name eq $del_name) {
					$is_rewrite = 1;
					$is_not_find = 0;
					last;
				}
				else {
					$is_not_find = 1;
				}
			}
			push @lines, $line if $is_not_find;
		}
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;
	}
}

1; # 削除不可
