sub run {
	if ($method eq 'GET') {
		if ($lib[1] eq "chat_public") {
			&read_chat_public;
		}
		elsif ($lib[1] eq "world_news") {
			&read_world_news;
		}
	}
}

sub read_chat_public {
	my $name = $cgi->param("name");
	$name = decode("UTF-8", $name);
	my @names = split /,/, $name;

	my $ryaku = decode("UTF-8", "(略");
	my $count = 0;
	open my $fh, "< $root/log/chat_public.cgi" or &error("chat_public.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		$line = decode("Shift_JIS",$line);
#		$line =~ s/(?![^\\]+([\\]{1,}))[^\\]+[\\]//gxms;
		chomp($line);
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		if ($name) {
			my $find = 0;
			for my $n (0 .. $#names) {
				last if $find;
				$find = 1 if $bname eq $names[$n];
			}
			next unless $find;
		}

		$bshogo =~ s/\(.$/$ryaku/g;
#		unless ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
#			$bname .= "[$bshogo]" if $bshogo;
#		}

#		if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16'))

		$hash_data{'log'}{'time'}[$count] = $btime;
		$hash_data{'log'}{'date'}[$count] = $bdate;
		$hash_data{'log'}{'name'}[$count] = $bname;
		$hash_data{'log'}{'country'}[$count] = $bcountry;
		$hash_data{'log'}{'shogo'}[$count] = $bshogo;
#		$hash_data{'log'}{'addr'}[$count] = $baddr;
		$hash_data{'log'}{'content'}[$count] = $bcomment;
		$hash_data{'log'}{'icon'}[$count] = $bicon;

		$count++;
	}
	$hash_data{'log'}{'length'} = $count;
	close $fh;
}

#use LWP::UserAgent;
#	require '../lib/_write_tag.cgi';
sub write_chat_public {
#	my $in{comment} = $cgi->param("comment");

#	our $ua = LWP::UserAgent->new;
#	our $url = 'http://www.pandora.nu/nyaa/cgi-bin/bj_test/chat_public.cgi';
#	our $query_string = "id=$id&pass=$pass&comment=$comment";

#	my $req = HTTP::Request->new(POST => $url);
#	$req->content_type('application/x-www-form-urlencoded');
#	$req->content($query_string);

#	my $res = $ua->request($req);
#	print $res->as_string;

	&get_data;

	my %m;
	for my $key (keys(%{$hash_data{'user'}})) {
		$m{$key} = ${$hash_data{'user'}}{$key};
	}

	my %w;
	for my $key (keys(%{$hash_data{'world'}})) {
		$w{$key} = ${$hash_data{'world'}}{$key};
	}

	my $addr = $ENV{REMOTE_ADDR};
	my $time = time();
	my($min,$hour,$mday,$mon,$year) = (localtime($time))[1..4];
	$date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);

	my $max_log = 60;
	my $max_comment = 200;
	# 連続書き込み禁止時間(秒)
	my $bad_time    = 5;
	$in{comment} = $cgi->param("comment");
#	$in{comment} =~ s/\+/ /g;
#	$in{comment} =~ s/%([0-9a-fA-F]{2})/pack("H2",$1)/eg;
#	$in{comment} = #decode("Shift_JIS", $in{comment});
#	$in{comment} = uri_unescape( $in{comment} );

	my $mname = $m{name};
#	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	my $mcountry = $m{country};


	my @lines = ();
	open my $fh, "+< $root/log/chat_public.cgi" or &error("../log/chat_public.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };

	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bicon_pet) = split /<>/, $line;

	# 同一本文の投稿をスルー
	if ($in{comment} eq $hcomment) {
#		close $fh;
#		return 0;
	}

	if ($hname eq $m{name} && $htime + $bad_time > $time) {
#		&error("連続投稿は禁止しています。<br>しばらく待ってから書き込んでください");
	}

	# 手紙に関しては、同一本文であっても送信者が違うなら手紙を受信するようにし、
	# 同一人物からの同一本文の手紙は古い方を削除し新しい方を受信し直すタイムスタンプ更新方式に
	push @lines, $head_line unless $in{comment} eq $hcomment && $hname eq $m{name};

	if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16'))) {
		$mname = "名無し";
	}

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}

	my %bbs_config = ();
	$bbs_config{shogo_limit} = 16;
	my $mshogo = length($m{shogo}) > $bbs_config{shogo_limit} ? substr($m{shogo}, 0, $bbs_config{shogo_limit}) : $m{shogo};
	unshift @lines, encode("Shift_JIS", "$time<>$date<>$mname<>$mcountry<>$mshogo<>$addr<>").$in{comment}.encode("Shift_JIS", "<>$m{icon}<>$m{icon_pet}<>\n");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

}

sub read_world_news {
	my $count = 0;
	open my $fh, "< $root/log/world_news.cgi" or &error("world_news.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
#		$line = decode("Shift_JIS",$line);
		chomp($line);

#		$line =~ s/<.*?>//g;
		$hash_data{'log'}{'content'}[$count] = $line;

		$count++;
	}
	$hash_data{'log'}{'length'} = $count;
	close $fh;
}

=pod
	my %bbs_config = ();
	$bbs_config{shogo_limit} = 16;
	my $mshogo = length($m{shogo}) > $bbs_config{shogo_limit} ? substr($m{shogo}, 0, $bbs_config{shogo_limit}) : $m{shogo};
		unshift @lines, "$time<>$date<>$mname<>$mcountry<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>$m{icon_pet}<>\n";
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
=cut
1;