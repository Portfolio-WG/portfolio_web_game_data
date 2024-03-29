require 'lib/_write_tag.cgi';
#=================================================
# BBS,CHAT補助ｻﾌﾞﾙｰﾁﾝ Created by Merino
#=================================================

#=================================================
# 書き込み処理
#=================================================
sub write_comment {
	return 0 if ($ENV{REQUEST_METHOD} ne 'POST') && !$is_mobile;
	&error('本文に何も書かれていません') if $in{comment} eq '';
	&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;
	&error('書き込み権限がありません') if (!&writer_check);

	my $mcountry = $m{country};
	if ($this_file =~ /$userdir\/(.*?)\//) {
		my $wid = $1;
		if (-f "$userdir/$wid/blacklist.cgi") {
			open my $fh, "< $userdir/$wid/blacklist.cgi" or &error("$userdir/$wid/blacklist.cgiﾌｧｲﾙが開けません");
			while (my $line = <$fh>) {
				my($blackname) = split /<>/, $line;
				if ($blackname eq $m{name}) {
					&error('ﾌﾞﾗﾀﾓﾘ');
				}
			}
			close $fh;

		}
		# 匿名時の手紙は国名非表示
		# 0 はﾈﾊﾞﾗﾝになるのでとりあえず -1 にして letter.cgi 側で処理
		# 宣伝言板での手紙レスは匿名にしない
		$mcountry = '-1' if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) && $in{comment} !~ "<hr>【宣伝言板へのレス】");
	}

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	if ($this_file =~ /blog/) {
		my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	}
	else {
		my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bicon_pet) = split /<>/, $line;
	}
	# 手紙じゃないなら同一人物・同一本文の投稿をスルー、手紙は再受信
	if ($m{name} eq $hname && $in{comment} eq $hcomment && $this_file !~ /letter/) {
		close $fh;
		return 0;
	}
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("連続投稿は禁止しています。<br>しばらく待ってから書き込んでください");
	}
	# 手紙に関しては、同一本文であっても送信者が違うなら手紙を受信するようにし、
	# 同一人物からの同一本文の手紙は古い方を削除し新しい方を受信し直すタイムスタンプ更新方式に
	push @lines, $head_line unless $in{comment} eq $hcomment && $hname eq $m{name};

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}

	# この位置で判断すると情勢を取得できるプログラムからの呼び出しと、
	# そうでないプログラムからの呼び出しで匿名が効いたり効かなかったり
	# 情勢を取得できるプログラムからの呼び出しだった場合には強制的に匿名になるため、
	# 手っ取り早い対処法として「<hr>【宣伝言板へのレス】」を含んでいるならば匿名にはしない
	if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) && $in{comment} !~ "<hr>【宣伝言板へのレス】") {
		$mname = "名無し";
	}
#	elsif (($this_file =~ /chat/ || $this_file =~ /bbs/) && $seeds{$m{seed}}[0] eq 'ｶｼﾗﾊﾟﾝﾀﾞ') {
	elsif ($seeds{$m{seed}}[0] eq 'ｶｼﾗﾊﾟﾝﾀﾞ') {
		# 匿名じゃなく種族がｶｼﾗﾊﾟﾝﾀﾞなら投稿内容を各行に分解し空行以外の文末に「かしら」を追加
		# どう考えても正規表現でできそうだけどなんだかエラーになるし調べるの面倒だからこれでとりあえず　※投稿内容の「改行」は「<br>」
		my @data = split('<hr>', $in{comment}); # 日記投稿や宣伝での手紙レスは行末にそれぞれのデータが入るのでそれ対策
		my @comments = split('<br>', $data[0]);
		$in{comment} = '';
		for my $i (0 .. $#comments) {
			$in{comment} .= "$comments[$i]かしら" if $comments[$i] ne '';
			$in{comment} .= '<br>' if $i < $#comments;
		}
		$in{comment} .= "<hr>$data[1]" if $#data > 0;
	}

	my %bbs_config = ();
	$bbs_config{shogo_limit} = 16;
	my $this_config = $this_file . '_config.cgi';
	if (-f $this_config) {
		open my $fhc, "< $this_config" or &error("$this_config ﾌｧｲﾙが開けません");
		my $config_line = <$fhc>;
		for my $config_hash (split /<>/, $config_line) {
			my($k, $v) = split /;/, $config_hash;
			$bbs_config{$k} = $v;
		}
	}
	my $mshogo = length($m{shogo}) > $bbs_config{shogo_limit} ? substr($m{shogo}, 0, $bbs_config{shogo_limit}) : $m{shogo};
	if ($this_file =~ /blog/) {
		unshift @lines, "$time<>$date<>$mname<>$mcountry<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	}
	else {
		unshift @lines, "$time<>$date<>$mname<>$mcountry<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>$m{icon_pet}<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('voice');
	}
	
	return 1;
}


#=================================================
# ﾒﾝﾊﾞｰ取得
#=================================================
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub writer_check {
	if (@writer_member > 0) {
		for my $member (@writer_member) {
			if ($m{name} eq $member) {
				return 1;
			}
		}
		return 0;
	}
	return 1;
}

1; # 削除不可
