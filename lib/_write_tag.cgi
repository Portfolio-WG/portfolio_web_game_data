require 'config_game.cgi';

sub write_change {
	my ($bname, $bcomment, $chat_flag) = @_;
	while(1){
		if($bcomment =~ /(.*)&amp;dice\((\d+)\)(.*)/){
			my $dice = int(rand($2)+1);
			$bcomment = "$1$m{name}は$2面ダイスを振った。出目は$dice！【ダイス】$3";
			if($2 >= 100 && $dice == 1){
				&dice_fumble($2);
			}
			if($2 == 100){
				&dice_omikuji($2,$dice);
				$bcomment = "$1$m{name}は$2面ダイスを振った。出目は$dice！運勢は$m{shogo}！【ダイス】$3";
			}
		}elsif($bcomment =~ /(.*)&amp;UNKdice\((\d+)\)(.*)/){
			my $num_UNK = $2;
			if($num_UNK >= 6){
				$num_UNK = 5;
			}
			require './data/UNKdice.cgi';
			@UNK_count = (0,0,0,0,0,0);
			$bcomment = "$1$m{name}は$num_UNK面UNKダイスを振った。出目は";
			my $NKO_num = $#UNK_word;
			$NKO_num++;
			for my $i (1..$num_UNK){
				my $dice = int(rand($NKO_num));
				$UNK_count[$dice]++;
				$bcomment .= "$UNK_word[$dice],";
			}
			$bcomment .= "！";
			for my $i(0..$#UNK_dicelist){
				my $count_UNK_a = 1;
				for my $j(0..$#UNK_count){
					my $is_UNK = $UNK_count[$j] - $UNK_dicelist[$i][$j];
					if($is_UNK < 0){
						$count_UNK_a = 0;
						break;
					}
				}
				if($count_UNK_a){
					$bcomment .= $UNK_diceword[$i];
					if($i eq 7 && $m{shogo} ne $shogos[1][0] && $m{shogo_t} ne $shogos[1][0]){#OCHINCHIN
						$m{shogo} = "★OCHINCHIN";
						&write_user;
					}
				}
			}
		}else{
			last;
		}
	}
	while(1){
		if($bcomment =~ /(.*)&amp;(\d+)[dD](\d+)\(\)(.*)/){
			my $dice = 0;
			my $d_num = $2;
			if ($d_num > 100) {
				$d_num = 100;
			}
			$bcomment = "$1$m{name}は$3面ダイスを$d_num個振った。出目は";
			for my $i (1..$d_num){
				my $t_dice = int(rand($3)+1);
				$dice += $t_dice;
				$bcomment .= $i == 1 ? "$t_dice" : ",$t_dice";
			}
			$bcomment .= "合計$dice！【ダイス】$4";
			if($3 ** $d_num >= 100 && $dice == $d_num){
				&dice_fumble($3, $d_num);
			}
		}else{
			last;
		}
	}
	while(1){
		if($bcomment =~ /(.*)&amp;(\d+)[dD](\d+)\((\d+)\)(.*)/){
			my $dice = $4;
			my $d_num = $2;
			if ($d_num > 100) {
				$d_num = 100;
			}
			$bcomment = "$1$m{name}は$3面ダイスを$d_num個振った。出目は";
			for my $i (1..$d_num){
				my $t_dice = int(rand($3)+1);
				$dice += $t_dice;
				$bcomment .= $i == 1 ? "$t_dice" : ",$t_dice";
			}
			$bcomment .= "！固定値は$4。合計$dice！【ダイス】$5";
			if($3 ** $d_num >= 100 && $dice == $d_num){
				&dice_fumble($3, $d_num);;
			}
		}else{
			last;
		}
	}
	$bcomment =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;
	#"
	if($bcomment =~ /&amp;fusianasan/){
		$bname = "$host";
		$bcomment =~ s|&amp;fusianasan||g;
	}
	if($bcomment =~ /&amp;back_changer/){
		require './lib/_changer_from_date.cgi';
		my $b_picture = &changer_run("$logdir/changer_date/backpicture_date.cgi");
		&changer_data("$logdir/changer_date/backpicture_chatpiblic.cgi","$b_picture");
		$bname = "ｼｽﾃﾑﾒｯｾｰｼﾞ";
		$bcomment = "背景画像を更新,$b_picture";
	}
	if($bcomment =~ /&amp;event/ && $this_file eq "$logdir/chat_public"){#交流広場限定
		$bname = "ｼｽﾃﾑﾒｯｾｰｼﾞ";
		require './lib/greeting_card_lot.cgi';
		$bcomment = &lot_system;
	}
	if($bcomment =~ /(.*)&amp;admin_set\((.+)=(\d+)\)(.*)/){
		my $change_mes = '';
		if (&is_sabakan) {
			my $this_config = $this_file . '_config.cgi';
			my %bbs_config = ();
			$bbs_config{shogo_limit} = 16;
			if (-f $this_config) {
				open my $fhc, "< $this_config" or &error("$this_config ﾌｧｲﾙが開けません");
				my $config_line = <$fhc>;
				for my $config_hash (split /<>/, $config_line) {
					my($k, $v) = split /;/, $config_hash;
					$bbs_config{$k} = $v;
				}
			}
			$bbs_config{$2} = $3;
			my $config_line;
			foreach my $key (keys(%bbs_config)) {
				$config_line .= "$key;$bbs_config{$key}<>";
			}

			open my $fhc, "> $this_config" or &error("$this_config ﾌｧｲﾙが開けません");
			print $fhc $config_line;
			close $fhc;

			$change_mes = "【鯖管コマンド】$this_config を修正します。"
		}
		$bcomment = "$1$change_mes$4";
	}
	if($bcomment =~ /&amp;img/){
		$bcomment =~ s|&amp;img|<amp_img>|;
		if($bcomment =~ /&amp;img/){
			&error('imgタグは一つの投稿につき一つまでです');
		}
		$bcomment =~ s|<amp_img>|&amp;img|;
	}

	return ($bname, $bcomment);
}

sub dice_fumble{
	my ($dice_size, $number) = @_;
	if($m{shogo} ne $shogos[1][0] && $m{shogo_t} ne $shogos[1][0]){
		if($number){
			$m{shogo} = "★←$dice_size面ダイス$number個振ってファンブル出した";
		}else{
			$m{shogo} = "★←$dice_size面ダイスでファンブル出した";
		}
		&write_user;
	}
}
sub dice_omikuji{
	my ($dice_size, $number) = @_;
	if($m{shogo} ne $shogos[1][0] && $m{shogo_t} ne $shogos[1][0]){
#大吉・吉・中吉・小吉・末吉・末凶・凶
		if($number <= 5){
			$m{shogo} = "★凶";
		}elsif($number > 5 && $number <= 10){
			$m{shogo} = "★末凶";
		}elsif($number > 10 && $number <= 30){
			$m{shogo} = "★末吉";
		}elsif($number > 30 && $number <= 55){
			$m{shogo} = "★小吉";
		}elsif($number > 55 && $number <= 75){
			$m{shogo} = "★中吉";
		}elsif($number > 75 && $number <= 90){
			$m{shogo} = "★中吉";
		}elsif($number > 90 && $number <= 100){
			$m{shogo} = "★大吉";
		}
		&write_user;
	}
}

1; # 削除不可
