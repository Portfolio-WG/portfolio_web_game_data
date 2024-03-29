#================================================
# 種族関数
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

# 追加種族ディレクトリ
$add_seeds_dir = "$datadir/add_seeds";

# 転生成功確率(%)
$change_percent = 100;

# 新種族確率(%)
$change_new_seed_percent = 10;

# 相手方種族転生確率(%)
$change_marriage_percent = 30;

# 未婚時ﾋｭｰﾏﾝになる確率(%)
$unmarried_human_percent = 50;

%seeds = &get_seeds;

# 基本種族
$default_seed = 'human';

# 種族数閾値
$seeds_max = 10;

#================================================
# 種族情報
#================================================
sub get_seeds {
=pod
	require "$datadir/seeds.cgi";
	my %all_seeds = ();
	for my $i (0..$#default_seeds) {
		$all_seeds{$default_seeds[$i][1]} = $default_seeds[$i][2];
	}
	opendir my $dh, "$add_seeds_dir" or &error("追加種族ﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $fname = readdir $dh) {
		next if $fname !~ /\.cgi/;
		$fname =~ s/\.cgi//g;
		require "$add_seeds_dir/$fname.cgi";
		$all_seeds{$fname} = \@$fname;
	}
	closedir $dh;

	return %all_seeds;
=cut
	return 1;
}

#================================================
# 種族ボーナス
#================================================
sub seed_bonus {
=pod
	my $lib = shift;
	my $v = shift;
	if ($m{seed} eq '' || !defined($seeds{$m{seed}})) {
		$m{seed} = $default_seed;
	}
	if (defined($seeds{$m{seed}}[1]{$lib})) {
		$v = &{$seeds{$m{seed}}[1]->{$lib}}($v);
	}
	return $v;
=cut
	return $v;
}

#================================================
# 種族変更
#================================================
sub seed_change {
=pod
	my $sta = shift;
	if ($sta eq 'keep') {
		return;
	}
	$before = $m{seed};

	if ($sta eq 'change' && rand(100) < $change_percent) {
		if (rand(100) < $change_new_seed_percent) {
			&create_new_seed;
		} else {
			my @seed_keys = ();
			foreach $key (keys(%seeds)) {
				push @seed_keys, $key for 1..$seeds{$key}[2];
			}
			$m{seed} = $seed_keys[int(rand(@seed_keys))];
		}
	} else {
		if ($m{marriage} && &you_exists($m{marriage})) {
			my %datas = &get_you_datas($m{marriage});
			if (rand($seeds{$m{seed}}[2] * 100) <= rand($seeds{$datas{seed}}[2] * 100)) {
				$m{seed} = $datas{seed};
			}
		} elsif (rand(100) < $unmarried_human_percent)  {
			$m{seed} = $default_seed;
		}
	}

	if ($before ne $m{seed}) {
		$mes .= "$seeds{$m{seed}}[0]に転生しました。";
	}

	&seed_overflow;
=cut
	return 1;
}

#================================================
# 新種族
#================================================
sub create_new_seed {
=pod
	$m{lib} = 'seed_create';
	$m{tp} = 100;
	$m{stock} = int(rand(2)) + 1;
	$mes .= "新たな血脈が誕生する。<br>";
=cut
	return 1;
}

#================================================
# 絶滅
#================================================
sub seed_overflow {
=pod
	my $seeds_num = keys(%seeds);
	if ($seeds_num > $seeds_max) {
		my %seed_players = ();

		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $uid = readdir $dh) {
			next if $uid =~ /\./;
			next if $uid =~ /backup/;
			my %datas = &get_you_datas($uid, 1);
			$seed_players{$datas{seed}}++;
		}
		closedir $dh;
		for my $key (keys(%seeds)) {
			if (!$seed_players{$key}) {
				if (-f "$add_seeds_dir/$key.cgi") {
					unlink "$add_seeds_dir/$key.cgi";
				}
			}
		}
	}
=cut
	return 1;
}
1; # 削除不可
