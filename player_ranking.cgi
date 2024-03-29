#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 廃人ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

my @rank_status = (
#変数,表示名,最低値
    ['str','強さ',3000,0],
    ['sedai','世代',7,0],
    ['rank','階級',15,0],
    ['nou_c','農業',300,0],
    ['sho_c','商業',300,0],
    ['hei_c','徴兵',200,0],
    ['gai_c','外交',60,0],
    ['gou_c','強奪',300,0],
    ['cho_c','諜報',500,0],
    ['sen_c','洗脳',400,0],
    ['gik_c','偽計',100,0],
    ['kou_c','攻城',100,0],
    ['tei_c','偵察',70,0],
    ['mat_c','待伏',100,0],
    ['cas_c','ｶｼﾞﾉ',4000,0],
    ['tou_c','討伐',4000,0],
    ['shu_c','修行',5000,0],
    ['col_c','闘技場',5,0],
    ['mon_c','魔物',5,0],
    ['win_c','武功',100,0],
    ['hero_c','統一',1,0],
    ['huk_c','復興',1,0],
    ['met_c','滅亡',1,0],
    ['esc_c','脱獄',5,0],
    ['res_c','救出',5,0],
    ['lose_c','不屈',30,0],
    ['fes_c','お祭り野郎',5,0],
    ['shogo_p','やりこみ',70,0],
    ['no1_c','NO.1',10,0],
    ['wt_c_latest','稼働率',100,50],
);

my $max_ranking = 10;

#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @rank_status;
my $type = $rank_status[$in{no}][0] ? "_$rank_status[$in{no}][0]" : '';

my $this_file = "$logdir/player_ranking${type}.cgi";
my $player_ranking_cycle_day = 1;

&update_player_ranking if -M $this_file > $player_ranking_cycle_day;
#&update_player_ranking; #すぐに更新したい場合はここのコメントアウトを外す（ただし処理が重くなるので速やかに戻すこと）
&run;
&footer;
exit;


#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	for my $i (0 .. $#rank_status) {
		print $i eq $in{no} ? qq|$rank_status[$i][1] / | : qq|<a href="?no=$i">$rank_status[$i][1]</a> / |;
	}
	print qq|<a href="use_pet_ranking.cgi?no=0">国ﾍﾟﾗﾝｷﾝｸﾞ</a> / |;

	print qq|<h1>$rank_status[$in{no}][1]廃人ﾗﾝｷﾝｸﾞ</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞは$player_ranking_cycle_day日ごとにﾘｾｯﾄされ更新されます</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th></tr>| unless $is_mobile;
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		if($rank_status[$in{no}][0] eq 'rank'){
			my $tempn = $number;
			my $sran = 0;
			while ($tempn =~ /★/){
				$tempn =~ s/★//;
				$sran++;
			}
			if($sran){
				$d_rank = $rank if ($pre_number != $sran);
				$pre_number = $sran;
			}else {
				$d_rank = $rank if ($pre_number ne $number);
				$pre_number = $number;
			}
		}else {
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
		}
		print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# 廃人ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_player_ranking  {

	my %sames = ();
	my @line = ();
	my @p_ranks = (1,'','');
	my $status = $rank_status[$in{no}][0];
	my $rank_min = $rank_status[$in{no}][2];
	if ($rank_status[$in{no}][3]) {
		$max_ranking = $rank_status[$in{no}][3];
	}

	for my $country (0 .. $w{country}) {

		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");

		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/user.cgi") {
				next;
			}
			my %p = &get_you_datas($player_id, 1);
			$p{str} = int($p{max_hp} + $p{max_mp} + $p{at} + $p{df} + $p{mat} + $p{mdf} + $p{ag} + $p{cha} * 0.5);
			if (&get_rank_name($p{rank}, $p{name}) eq '皇帝') {
				$p{rank}++;
			}
			$p{rank} += $p{super_rank};

			my $count = 0;
			for my $i (1 .. $#shogos) {
				my @shk = keys %{ $shogos[$i][1] };
				my $k = $shk[0];
				my $v = $shogos[$i][1]{$k};
				++$count if $p{$k} >= $v;
			}
			my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
			$comp_par = 100 if $comp_par > 100;
			$p{shogo_p} = $comp_par;

			next if $p{$status} < $rank_min;

			my @datas = ();
			my @rdata = ();
			my $i = 1;

			while ($i <= $max_ranking){
				$rdata[0] = shift @p_ranks;
				$rdata[1] = shift @p_ranks;
				$rdata[2] = shift @p_ranks;
				if ($rdata[0] <= $p{$status}) {
					push @datas, $p{$status}, $p{name}, $p{country};
					push @datas, $rdata[0], $rdata[1], $rdata[2] unless $i >= $max_ranking && $p{$status} != $rdata[0];
					$i++;
					my $last_number = $datas[-3];
					while($i <= $max_ranking || $last_number == $p_ranks[0]){
						my $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$last_number = $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						last if $cash eq '';
						$i++;
					}
				}else {
					push @datas, $rdata[0], $rdata[1], $rdata[2];
					$i++;
				}
				last if $rdata[1] eq '';
			}
			@p_ranks = ();
			push @p_ranks, @datas;
		}
		close $cfh;
	}
	while ($p_ranks[1] ne '') {
		my @data;
		for my $j (0..2){
			$data[$j] = shift @p_ranks;
		}
		if($status eq 'rank'){
			$data[1] =~ tr/\x0D\x0A//d;
			my $player_id = unpack 'H*', $data[1];
			my %p = &get_you_datas($player_id, 1);
			my $rank_name = &get_rank_name($p{rank}, $p{name});
			if ($p{super_rank}){
				$rank_name = '';
				$rank_name .= '★' for 1 .. $p{super_rank};
				$rank_name .= $p{rank_name};
			}
			push @line, "$rank_name<>$data[1]<>$data[2]\n";
		}else {
			push @line, "$data[0]<>$data[1]<>$data[2]\n";
		}
	}

	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

