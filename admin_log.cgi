#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
my $this_script = 'admin_log.cgi';
#=================================================
# ログなどの管理 Created by nanamie
#=================================================

#=================================================
# メイン処理
#=================================================
&header;
&decode;
&error('ﾊﾟｽﾜｰﾄﾞが違います') unless $in{pass} eq $admin_pass;
&header_admin;
&read_cs;

if    ($in{mode} eq 'check_matching') { &check_matching; }

&top;
&footer;
exit;

#=================================================
# header+
#=================================================
sub header_admin {
	print <<"EOM";
	<table border="0"><tr><td>
		<form action="$script_index">
			<input type="submit" value="ＴＯＰ" class="button1">
		</form>
	</td><td>
		<form method="$method" action="admin.cgi">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="ﾌﾟﾚｲﾔｰ管理" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="国管理" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="mode" value="now_country">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="現在の国データ" class="button1">
		</form>
	</td></tr></table>
EOM
}

#=================================================
# top
#=================================================
sub top {
	if ($mes) {
		print qq|<div class="mes">$mes</div><br>|;
	}
	else {
		print qq|<div class="mes">ログの表\示やデータの取得などができます</div><br>|;
	}

	print qq|<div class="mes">マッチングチェック<ul>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="check_matching">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|ﾌﾟﾚｲﾔｰ名：<input type="text" name="y_name"><br>|;
	my @countries = (1 .. $w{country});
	print qq|<select name="y_country" class="menu1">|;
	for my $country (@countries) {
		print qq|<option value="$country">$cs{name}[$country]</option>|;
	}
	print qq|</select>|;
	print qq|<p><input type="submit" value="チェック" class="button_s"></p></form></div>|;

}

sub check_matching {
	my ($y_name, $y_country) = ($in{y_name}, $in{y_country});

	local %m = &get_you_datas($y_name);
	local %y = ();
	$y{country} = $y_country;
	local $c_y = $cs{name}[$y{country}];

	local @lines = &get_country_members($y{country});

	my $ambush_num = 0;
	for my $i (1 .. 20) {
		my $is_ambush = &_get_war_you_data; # 待ち伏せされてた場合戻り値あり
		$y{sol} = int($rank_sols[$y{rank}]);
	
		# 待ち伏せ
		if ($is_ambush) {
			$ambush_num++;
			$mes .= "$c_yの$y{name}率いる$y{sol}の$units[$y{unit}][1]が待ち伏せしていました!<br>";
			if ($y{unit} eq '11') { # 暗殺部隊
				my $v = int( $m{sol} * (rand(0.2)+0.2) );
				$m{sol} -= $v;
				$m{sol_lv} = int( rand(15) + 15 ); # 15 ～ 29
				$mes .= "$units[$y{unit}][1]による暗殺で、$vの兵がやられました!<br>";
			}
			elsif ($y{unit} eq '14') { # 幻影部隊
				$m{sol_lv} = int( rand(10) + 5 ); # 5 ～ 14
				$mes .= "$units[$y{unit}][1]による幻術で、兵士達は混乱し大きく士気が下がりました!<br>";
			}
			else {
				$m{sol_lv} = int( rand(15) + 10 ); # 10 ～ 24
				$mes .= "待ち伏せにより兵士達は混乱し大きく士気が下がりました!<br>";
			}
			if ($pets[$y{pet}][2] eq 'no_single' && $w{world} ne '17') {
				$y{wea} = 'no_single';
				$y{sol_lv} = int( rand(10) + 5);
				$mes .= "$pets[$y{pet}][1]の力で絶対に一騎打ちにはなりませんが兵の士気は下がっています<br>";
			}
		}
		else {
			$m{sol_lv} = 80;
			$mes .= "$c_yから$y{name}率いる$y{sol}の兵が出てきました<br>";
		}
	}
	$mes .= "<br>被待ち伏せ数：$ambush_num";
}

#================================================
# 階級と統率が同じくらいの相手をランダムで探す。見つからない場合は用意されたNPC
#================================================
sub _get_war_you_data {
	my $war_mod = &get_modify('war');
	
	if (@lines >= 1) {
		my $retry = ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000      ? 0 # 世界情勢【鉄壁】攻めた国の国力が3000以下の場合は強制NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # 世界情勢【暗黒】攻めた国がNPC国ならﾌﾟﾚｲﾔｰﾏｯﾁﾝｸﾞは１回
				  : $w{world} eq $#world_states - 5 ? 3 # 世界情勢【拙速】ﾌﾟﾚｲﾔｰﾏｯﾁﾝｸﾞは3回
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 15 && $w{world} ne '17') ? 	1
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && $w{world} ne '17') ? 	2
				  :																5 # その他ﾌﾟﾚｲﾔｰﾏｯﾁﾝｸﾞを最高５回ほどﾘﾄﾗｲする
				  ;
		$retry = int($retry / $war_mod);
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # 同じ人なら次
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp 余分な改行削除

#			my $c = int(rand(@lines));
#			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp 余分な改行削除
#			next if $sames{$lines[$c]}++; # 同じ人なら次

			$mes .= "$lines[$c]<br>";
			my $y_id = unpack 'H*', $lines[$c];
			
			# いない場合は次
			next unless -f "$userdir/$y_id/user.cgi";

			my %you_datas = &get_you_datas($y_id, 1);
			
			$y{name} = $you_datas{name};
			
			next if $you_datas{lib} eq 'prison'; # 牢獄の人は除く
			next if $you_datas{lib} eq 'war'; # 戦争に出ている人は除く
			next if ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 20 && $w{world} ne '17'); # ★20ﾌｧﾝﾄﾑ
			
			if ($m{win_c} < $new_entry_war_c) {
				if ( $m{rank} >= ($you_datas{rank} + int(rand(2)) ) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} elsif ($cs{disaster}[$y{country}] eq 'mismatch' && $cs{disaster_limit}[$y{country}] >= $time) {
				# 指揮系統混乱時
				if ( $you_datas{rank} <= $m{rank}) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} else {
				# 階級と統率が近い人。左の数字を0にすればより強さの近い相手大きくすれば色々な相手
				if ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
				# 待ち伏せしている人がいたら
				elsif ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 1;
				}
			}
		}
	}
	
	# ｼｬﾄﾞｳ or NPC
	# %y に格納されているﾃﾞｰﾀの一部を引き継がせないように初期化（ｼｬﾄﾞｳ・NPCがﾌﾞﾚﾊを持っていたり防具を持っている問題）
	# ﾁｷﾝは待ち伏せ処理に入ると発動するのでｼｬﾄﾞｳ or NPCには直接関係ない
	# 問題は、ﾁｷﾝ持ちかどうかを武器にして判定している（一騎打ちしないし変数使い回しちゃえ？）ので、武器による統率補正がおそらくバグってること
	$y{gua} = 0; # 防具についてはイジる余地あり？　修行と一騎打ちで結果違っちゃうし
	$y{pet} = 0;
	($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17') || int(rand(3 / $war_mod)) == 0 || ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7'))
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] ～ [4] の 5人([0]強い >>> [4]弱い)
#================================================
sub _get_war_npc_data {
	&error("相手国($y{country})のNPCデータがありません") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	my $war_mod = &get_modify('war');
	
	require "$datadir/npc_war_$y{country}.cgi";

	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2) * $war_mod)
		  : $m{lea} > 250 ? int((rand(2)+1) * $war_mod)
		  : $m{lea} > 120 ? int((rand(2)+2) * $war_mod)
		  :                 int((rand(2)+3) * $war_mod)
		  ;

	# 統一国の場合はNPC弱体
	my($c1, $c2) = split /,/, $w{win_countries};
	# 国力低い場合は強いNPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country} || $w{world} eq $#world_states - 5) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		unless($k eq 'name' && $pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && rand(2) < 1){
			$y{$k} = $v;
		}
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';
	
	return 0;
}

#================================================
# ｼｬﾄﾞｳ
#================================================
sub _get_war_shadow_data {
	# 国力低い場合は1.5倍
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# 統一国の場合はNPC弱体
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = 'ｼｬﾄﾞｳ騎士(NPC)';
	
	return 0;
}
