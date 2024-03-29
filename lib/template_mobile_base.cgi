#================================================
# 携帯ｹﾞｰﾑ画面 Created by Merino
#================================================

#================================================
# ﾒｲﾝ
#================================================
print qq|資金 $m{money} G<br>| if $m{lib} =~ /^shopping/;
print qq|<a name="menu">$menu_cmd</a><br>$mes<br>|;

if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif ($m{lib} eq '') {
	&check_flag;
	&status_html;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}
elsif ($m{wt} > 0) {
	&check_flag;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}


#================================================
# ﾄｯﾌﾟﾒﾆｭｰ
#================================================
sub top_menu_html {
	print qq|<hr><a href="$script_index" accesskey="0">0.TOP</a>/|;
	print qq|<a href="./news.cgi?id=$id&pass=$pass" accesskey="1">1.過去の栄光</a>/|;
	print qq|<a href="./bbs_public.cgi?id=$id&pass=$pass" accesskey="2">2.掲示板</a>/|;
	print qq|<a href="./chat_public.cgi?id=$id&pass=$pass" accesskey="3">3.交流広場</a>/|;
	print qq|<a href="./chat_horyu.cgi?id=$id&pass=$pass">改造案投票所</a>/|;
	print qq|<a href="./bbs_ad.cgi?id=$id&pass=$pass" accesskey="4">4.宣伝言板</a>/|;
	print qq|<a href="./letter.cgi?id=$id&pass=$pass" accesskey="5">5.MyRoom</a>/|;
	print qq|<a href="./chat_prison.cgi?id=$id&pass=$pass" accesskey="7">7.牢獄</a>/|;
	print qq|<a href="./bbs_country.cgi?id=$id&pass=$pass" accesskey="8">8.作戦会議</a>/|;
	print qq|<a href="./bbs_union.cgi?id=$id&pass=$pass" accesskey="9">9.同盟会議</a>/| if $union;
	print qq|<a href="./bbs_vs_npc.cgi?id=$id&pass=$pass" accesskey="6">6.+封印会議+</a>/| if $w{world} eq $#world_states && $m{country} ne $w{country};

	print qq|<a href="./chat_casino.cgi?id=$id&pass=$pass">対人ｶｼﾞﾉ</a>/|;
	print qq|<a href="./bbs_daihyo.cgi?id=$id&pass=$pass">代表\評議会</a>/| unless $m{disp_daihyo} eq '0';
}

#================================================
# ｽﾃｰﾀｽ画面
#================================================
sub status_html {
	print qq|<hr><img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|$m{name}<br>|;
	print qq|称号 $m{shogo}<br>| if $m{shogo};
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	print qq|疲労度 <b>$m{act}</b>%<br>|;
	print qq|Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>|;
	print qq|資金 <b>$m{money}</b> G<br>|;
	print qq|<font color="#CC9999">$e2j{hp} [<b>$m{hp}</b>/<b>$m{max_hp}</b>]</font><br>|;
	print qq|<font color="#CC99CC">$e2j{mp} [<b>$m{mp}</b>/<b>$m{max_mp}</b>]</font><br>|;
	print qq|<font color="#9999CC">武器:[$weas[$m{wea}][2]]$weas[$m{wea}][1]★<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>| if $m{wea};
	print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]</font><br>| if $m{pet};
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};

}

#================================================
# 手紙、荷物ﾁｪｯｸ
#================================================
sub check_flag {
	if (-f "$userdir/$id/letter_flag.cgi") {
		print qq|<hr><font color="#FFCC66">手紙が届いています</font><br>|;
		unlink "$userdir/$id/letter_flag.cgi";
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		print qq|<hr><font color="#FFCC00">預かり所に荷物が届いています</font><br>|;
		unlink "$userdir/$id/depot_flag.cgi";
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		$head_mes .= qq|<font color="#FFCC99">ﾏｲﾙｰﾑに荷物が届いています</font><br>|;
		unlink "$userdir/$id/goods_flag.cgi";
	}
}

#================================================
# 戦闘画面
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';

	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">★</font>' : '';

	print "$m_icon$m{name}$m_mes<br>";
	print "$e2j{hp}(<b>$m{hp}</b>/<b>$m{max_hp}</b>)/$e2j{mp}(<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br>";
	print "攻撃[<b>$m_at</b>]/防御[<b>$m_df</b>]/素早[<b>$m_ag</b>]<br>";
	print "$m_tokkou武器:[$weas[$m{wea}][2]]$weas[$m{wea}][1]★$m{wea_lv}($m{wea_c})<br>" if $m{wea};
	print "ﾍﾟｯﾄ:$pets[$m{pet}][1]<br>" if $pets[$m{pet}][2] eq 'battle';
	print "<hr>";
	print "$y_icon$y{name}$y_mes<br>";
	print "$e2j{hp}(<b>$y{hp}</b>/<b>$y{max_hp}</b>)/$e2j{mp}(<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br>";
	print "攻撃[<b>$y_at</b>]/防御[<b>$y_df</b>]/素早[<b>$y_ag</b>]<br>";
	print "$y_tokkou武器:[$weas[$y{wea}][2]]$weas[$y{wea}][1]<br>" if $y{wea};
}

#================================================
# 戦争画面
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';

	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';

	print qq|$m_icon<font color="$cs{color}[$m{country}]">$m{name}$m_mes</font><br>|;
	print qq|$m_tokkou$units[$m{unit}][1]/<b>$m{sol}</b>兵/士気[<b>$m{sol_lv}</b>%]/統率[<b>$m{lea}</b>]<br>|;
	print qq|<hr>|;
	print qq|$y_icon<font color="$cs{color}[$y{country}]">$y{name}$y_mes</font><br>|;
	print qq|$y_tokkou$units[$y{unit}][1]/<b>$y{sol}</b>兵/士気[<b>$y{sol_lv}</b>%]/統率[<b>$y{lea}</b>]<br>|;
}

#================================================
# 自国/同盟国の情報
#================================================
sub my_country_info {
	my $next_rank = $m{rank} * $m{rank} * 10;
	my $nokori_time = $m{next_salary} - $time;
	$nokori_time = 0 if $nokori_time < 0;

	print qq|<hr>$ranks[$m{rank}] $e2j{rank_exp} [<b>$m{rank_exp}/$next_rank</b>]<br>|;
	print qq|敵国<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font>連続<b>$m{renzoku_c}</b>回<br>| if $m{renzoku_c};
	printf ("次の給与<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後<br>", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
	print qq|<hr><font color="$cs{color}[$m{country}]">$c_m</font><br>|;
	print qq|$e2j{strong}:$cs{strong}[$m{country}]<br>|;
	print qq|$e2j{tax}:$cs{tax}[$m{country}]%<br>|;
	print qq|$e2j{state}:$country_states[ $cs{state}[$m{country}] ]<br>|;
	print qq|$e2j{food}:$cs{food}[$m{country}]<br>|;
	print qq|$e2j{money}:$cs{money}[$m{country}]<br>|;
	print qq|$e2j{soldier}:$cs{soldier}[$m{country}]<br>|;

	if ($union) {
		print qq|<hr><font color="$cs{color}[$union]">$cs{name}[$union]</font><br>|;
		print qq|$e2j{strong}:$cs{strong}[$union]<br>|;
		print qq|$e2j{tax}:$cs{tax}[$union]%<br>|;
		print qq|$e2j{state}:$country_states[ $cs{state}[$union] ]<br>|;
		print qq|$e2j{food}:$cs{food}[$union]<br>|;
		print qq|$e2j{money}:$cs{money}[$union]<br>|;
		print qq|$e2j{soldier}:$cs{soldier}[$union]<br>|;
	}
}

#================================================
# 各国国力の情報
#================================================
sub countries_info {
	print  "<hr>各国の$e2j{strong}<br>";
	for my $i (1 .. $w{country}) {
		print qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		print $w{world} eq '10' ? ''
			: $cs{is_die}[$i]   ? "滅亡"
			:                     "$cs{strong}[$i]"
			;

		if ($m{country} && $m{country} ne $i) {
			my $c_c = &union($m{country}, $i);
			print qq|[$w{'f_'.$c_c}%]|;
			if   ($w{'p_'.$c_c} eq '1') { print qq|<font color="#009900">同盟</font>|; }
			elsif($w{'p_'.$c_c} eq '2') { print qq|<font color="#FF0000">交戦</font>|; }
		}
		print "<br>";
	}

	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . '時間' : int($limit_hour / 24) . '日';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>時間<b>%02d</b>分<b>%02d</b>秒後", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<hr><font color="#FF0000">●</font>| : qq|<hr><font color="#00FF00">●</font>|;
	print qq|ﾌﾟﾚｲ中 $w{playing}/$max_playing人|;
	print qq|<hr>統一期限 残り$limit_day<br>|;
	if ($reset_rest > 0){
		print qq|終戦期間【残り$reset_time_mes】<br>|;
	}
	print qq|難易度 Lv.$w{game_lv}<br>統一$e2j{strong} $touitu_strong<br>| unless $w{world} eq '10';
	print $c2 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>同盟<br>|
		: $c1 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><br>|
		:       ''
		;
	print qq|世界情勢 $world_states[$w{world}]<br>|;
	print qq|$world_name暦$w{year}年<br>|;
}



1; # 削除不可
