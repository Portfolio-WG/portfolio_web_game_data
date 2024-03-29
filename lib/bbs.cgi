require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
#================================================
# BBS Created by Merino
#================================================

# 連続書き込み禁止時間(秒)
$bad_time    = 10;

# 最大ﾛｸﾞ保存件数
$max_log     = 50;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 2000;

# ﾒﾝﾊﾞｰに表示される時間(秒)
$limit_member_time = 60 * 4;

# 最大過去ﾛｸﾞ保存件数
$max_bbs_past_log = 50;


#================================================
sub run {
	if ($in{mode} eq "write" && $in{comment}) {
		&write_comment;

		# 保存ﾛｸﾞ用
		if ($in{is_save_log}) {
			if (&is_daihyo) {
				my $sub_this_file = $this_file;
				$this_file .= "_log";
				$max_log = $max_bbs_past_log;
				&write_comment;
				$this_file = $sub_this_file;
				$mes .= "書き込みをﾛｸﾞ保存しました<br>";
			}
			else {
				$mes .= "国の代表\者以外はﾛｸﾞ保存はできません<br>";
			}
		}
	}

	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;

	my $this_script_p = $this_script;
	$this_script_p =~ s/\.cgi//;
	print qq|<form method="$method" action="past_log.cgi"><input type="hidden" name="this_title" value="$this_title">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="this_file" value="$this_file"><input type="hidden" name="this_script" value="$this_script_p">|;
	print qq|<input type="submit" value="過去ﾛｸﾞ" class="button_s"></form>|;

	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="書き込む" class="button_s">|;
	print qq|　 <input type="checkbox" name="is_save_log" value="1">ﾛｸﾞ保存</form><br>|;
	# 匿名処理 ここを有効にすると匿名情勢時に 同盟会議室 掲示板 運営掲示板 封印会議室(暗黒時は有効には成り得ない) もメンバー非表示になる
#	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
#		print qq|<font size="2">$member_c人:</font><hr>|;
#	}
#	else {
		print qq|<font size="2">$member_c人:$member</font><hr>|;
#	}

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	my $blacklist_on = 0;#ﾌﾞﾗﾘｽｲｯﾁ_処理軽減用

	if(-f "$userdir/$id/blacklist_country_bbs.cgi"){#会議室ﾌﾞﾗﾘ
		open my $fh5, "< $userdir/$id/blacklist_country_bbs.cgi" or &error("$userdir/$id/blacklist_country_bbs.cgi ﾌｧｲﾙが開けません");
		@blacklist_p_chat = ();
		while (my $line_b = <$fh5>) {
			my($blackname) = split /<>/, $line_b;
			push @blacklist_p_chat, $blackname;
		}
		close $fh5;
		$blacklist_on = 1;
	}
	while (my $line = <$fh>) {
		my $blacklist_on_person = 0;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bicon_pet) = split /<>/, $line;
		if($blacklist_on){
			for my $i (0..$#blacklist_p_chat){
				if($blacklist_p_chat[$i] eq $bname){
					$bcomment = " ";
					$blacklist_on_person = 1;
				}
			}
		}
		next if $blacklist_on_person eq 1;
		$bname = &name_link($bname);
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bicon_pet = $m{pet_icon_switch} && $bicon_pet ? qq| <img src="$icondir/pet/$bicon_pet" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bcomment = &comment_change($bcomment, 0);
		if ($is_mobile) {
			print qq|<div>$bicon$bicon_pet<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font></div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon$bicon_pet<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br></td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}


1; # 削除不可
