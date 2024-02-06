#!/usr/bin/perl --
use CGI;
use JSON;
#use utf8;
use Encode;
use lib ('cgi-bin/bj');
#@INC = ("/cgi-bin/bj/")

$root = "../..";

$cgi = new CGI;
$data = [];
%hash_data;
$method = '';

$id = unpack 'H*', $cgi->param("id");
$pass = $cgi->param("pass");
$uri = $ENV{'REQUEST_URI'};
$uri =~ s|.*/api/v1/([^\?]*).*|$1|;
@lib = split "/", $uri;

$hash_data{'id'} = $id;
$hash_data{'pass'} = $pass;
$hash_data{'lib'} = $lib[0];
if ($cgi->request_method() eq 'POST') { $method = 'POST'; }
else { $method = 'GET'; }

require "$lib[0].cgi" if $lib[0] ne 'main';
#require "logs.cgi";
&run;

push(@{$data}, {%hash_data});

#my $json = JSON->new->utf8(0)->encode($data);
#my $json = JSON->new->utf8(0)->encode(\%hash_data);
my $json = JSON->new->encode(\%hash_data);
print $cgi->header(-type => 'application/json', -charset => 'shift_jis', -status => 200);

#my $data2 = JSON->new->utf8(0)->decode($json);

#print "$data2->{'log'}{'content'}[0]";
#print "\n\n";

print $json;

sub run {
	&get_user;
}

sub error {
	$hash_data{'id'} = '';
	$hash_data{'pass'} = '';
}

sub get_user {
	open my $fh, "< $root/user/$id/user.cgi" or &error("そのような名前$idのﾌﾟﾚｲﾔｰが存在しません");
	my $line = <$fh>;
	close $fh;

#	$line = decode("Shift_JIS", $line);
	$line =~ s/\n//g;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$hash_data{'user'}{$k} = $v;
	}

#	require '../../../lib/jcode.pl';
#	require '../../../lib/summer_system_game.cgi';
#	require '../../../lib/seed.cgi';
#	require '../../../lib/system_game.cgi';
#	require '../../../secret_shogos.cgi';
	require 'config_game.cgi';
#	my $wname = $hash_data{'user'}{'wea_name'} ? $hash_data{'user'}{'wea_name'} : $weas[$hash_data{'user'}{'wea'}][1];
#	print qq|<font color="#9999CC">武器:[$weas[$m{wea}][2]]$wname★<b>$m{wea_lv}</b></font><br>| if $m{wea};

#	$hash_data{'user'}{'wea'} = "<font color=\"#9999CC\">武器:[$weas[$hash_data{'user'}{'wea'}][2]]$wname★<b>$hash_data{'user'}{'wea_lv'}</b></font>";


#	if ($hash_data{'user'}{'pass'} ne $pass) {
#		print $cgi->header(-type => 'application/json', -charset => 'Shift_JIS', -status => 200);
#		print "error";
#		return;
#	}
}

sub get_countries {
	$hash_data{'countries'}{'name'}[0] = "ﾈﾊﾞｰﾗﾝﾄﾞ";
	$hash_data{'countries'}{'color'}[0] = "#CCCCCC";

	my $i = 1;
	open my $fh, "< $root/log/countries.cgi" or &error("国ﾃﾞｰﾀが読み込めません");
	my $world_line = <$fh>;
	while (my $line = <$fh>) {
		$line = decode("Shift_JIS",$line);
		$line =~ tr/\x0D\x0A//d;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			if ($hash_data{'id'} && $hash_data{'pass'}) {
				next if $k =~ /^modify_/ || $k =~ /.*_c/ || $k =~ /extra.*/ || $k =~ /disaster.*/;
				for my $ok (qw/name color food money soldier strong is_die tax state member ceo war dom pro mil/) {
					$hash_data{'countries'}{$k}[$i] = $v if $k eq $ok;
				}
			}
			else {
				for my $ok (qw/name color/) {
					$hash_data{'countries'}{$k}[$i] = $v if $k eq $ok;
				}
			}
		}
		++$i;
	}
	$hash_data{'countries'}{'length'} = $i;
	close $fh;
#	for my $hash (qw/food money soldier state  tax disaster disaster_limit extra extra_limit/) {
#		for my $i (1 .. $hash_data{'world'}{'country'}) {
#			undef $hash_data{'countries'}{$hash}[$i] if $hash_data{'user'}{'country'} ne $i && $hash_data{'world'}{'union'} ne $i;
#		}
#	}

	$world_line = decode("Shift_JIS", $world_line);
	$world_line =~ s/\n//g;
	$union = 0;
	for my $hash (split /<>/, $world_line) {
		my($k, $v) = split /;/, $hash;

		if ($hash_data{'id'} && $hash_data{'pass'}) {
			$hash_data{'world'}{$k} = $v;

			# 自分が所属している国に同盟国があるなら $union に set
			if ($k =~ /^p_(\d)_(\d)$/ && $v eq '1') {
				if ($hash_data{'user'}{'country'} eq $1) {
					$hash_data{'world'}{'union'} = $2;
				}
				elsif ($hash_data{'user'}{'country'} eq $2) {
					$hash_data{'world'}{'union'} = $1;
				}
			}
		}

	}

	if ($hash_data{'id'} && $hash_data{'pass'}) {
#		for my $hash (qw/food money soldier state  tax disaster disaster_limit extra extra_limit/) {
#			for my $i (1 .. $hash_data{'world'}{'country'}) {
#				undef $hash_data{'countries'}{$hash}[$i] if $hash_data{'user'}{'country'} ne $i && $hash_data{'world'}{'union'} ne $i;
#			}
#		}
	}
	else {
#		for my $hash (qw/food money soldier state  tax disaster disaster_limit extra extra_limit/) {
#			for my $i (1 .. $hash_data{'world'}{'country'}) {
#				undef $hash_data{'countries'}{$hash}[$i] if $hash_data{'user'}{'country'} ne $i && $hash_data{'world'}{'union'} ne $i;
#			}
#		}
	}
}

sub get_data {
	&get_user;
	&get_countries;
}

sub read_chat_public {
	my $count = 0;
	open my $fh, "< $root/log/chat_public.cgi" or &error("chat_public.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		$line = decode("Shift_JIS",$line);
#		$line =~ s/(?![^\\]+([\\]{1,}))[^\\]+[\\]//gxms;
		chomp($line);
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bshogo =~ s/\(.$/(略/g;
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
		$hash_data{'log'}{'comment'}[$count] = $bcomment;
		$hash_data{'log'}{'icon'}[$count] = $bicon;

		$count++;
	}
	$hash_data{'log'}{'length'} = $count;
	close $fh;
}

#use LWP::UserAgent;
#	require '../lib/_write_tag.cgi';
use URI::Escape;
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
