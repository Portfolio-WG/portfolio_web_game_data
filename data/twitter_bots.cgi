use POSIX qw(ceil);

@twitter_bots = (
	sub {
		# ������bot
		return "�悧�A�A�A�A";
	},
	sub {
		# ��`
		return "�ɂႠ�IBlind Justice\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# ��`2
		my $job_name = $jobs[int(rand(@jobs))][1];
		return "�y�}��z$job_name\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# ��`3
		return "���̃Q�[���ōŋ��̍����낤��\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		require "$datadir/hunting.cgi";
		my $place = int(rand(@places));
		my $filename =  "$logdir/monster/$places[$place][0].cgi";
		
		my $all_skills = 0;
		my $all_self_burning = 0;
		open my $fh, "< $filename" or &error("$filenamȩ�ق��J���܂���");
		while (my $line = <$fh>) {
			my @datas = split /<>/, $line;
			my $i = 0;
			my %y = ();
			for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
				$y{$k} = $datas[$i];
				++$i;
			}
			my $skill_st = 0;
			my $si = 0;
			my $skill_str = '';
			for my $skill (split /,/, $y{skills}) {
				$si++;
				if ($skills[$skill][2] eq $weas[$y{wea}][2]) {
					$skill_st += $skills[$skill][7];
					if ($skill eq '32') {
						$all_self_burning++;
					}
				} else {
					$skill_st += $skills[0][7];
				}
			}
			for (my $j = $si; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			$all_skills += 5;
		}
		close $fh;
		
		my $sp = int((10 * $all_self_burning / $all_skills) + rand(4) - 2) * 10;
		return "�A���A���Z���o�\\�z�[���~\n���݂�$places[$place][2]��$sp���̃Z���o�m���ł�";
	},
	sub {
		# �d���l��bot
		my $i = 0;
		for my $j (1 .. $w{country}) {
			$i += $cs{member}[$j];
		}
		return "���݂̎d������$i�l�ł�";
	},
	sub {
		# ������bot
		@strs = (
			"���̓�����",
			"�o�c�҂̏��������}�C�i�X�A���a���z��100��G�����A�ڋq�̗a�����񐔂�5�񖢖��ŋ�s���ׂ�܂�",
			"�߯�߂��N�傪���Ɠ�����ʂ𔭓��ł���悤�ɂȂ�܂�",
			"�ް���ޯẮ����グ��Ə��ł���m����������܂�",
			"�ꕔ���߯Ă͐��~��̂ق���ō������邱�Ƃɂ���ċ����ł��܂�",
			"�A�������������Ƃ��ɂ͓������Ƃ̗F�D�x���啝�ɏ㏸���܂�",
			"500���œX�ɒu�����A�C�e���͏��i�ꗗ�ɍڂ�܂���",
			"�q�ɂ��������Ă��Ă������I�����ɑq�ɂ��������Ȃ��̂ł���Έꊇ�����͂ł��܂�",
			"�h��������Ă��鑊��ɑf��ŗ����������ƍU���͂�3���ɂȂ�܂��O�O",
			"�����̕���Ƒ���̖h��̑�������v�����ꍇ�ɂ͍U���͂��������܂�",
			"�\\�N�E���׎��͒D���͂�2.5�{�ɂȂ�܂�",
			"�v�����͒D���͂��ő�7.5�{�ɂ��Ȃ�܂�",
			"�������͒D���͂�1.2�{�ɂȂ�܂�",
			);
		my $i = int(rand(@strs));
		if ($i == 0) {
			if ($w{year} - int($w{year}*0.1)*10 > 5) {
				my @festival_world = ("�g��", 24, "�ّ�", 21, "�O���u", 23, "����", 25);
				my $year = ceil(($w{year}+0.5)*0.1)*10;
				my $world = $year%40*0.1*2;
				$strs[$i] .= "$year�N��$festival_world[$world]�ł�";
			}
			else {
				my $year = int($w{year}*0.1)*10+6;
				$strs[$i] .= ($year =~ /16$/ || $year =~ /36$/ || $year =~ /56$/ || $year =~ /76$/ || $year =~ /96$/) ?
					"$year�N�̈Í��ł�" :
					"$year�N�̉p�Y�ł�";
			}
		}
		return $strs[$i];
	},
	sub {
		# ���ϑ���bot
		my $this_file = "./html/item_";
		my $num = 0;
		# ���[�v�������L�V�������ǂ܂��t�@�C���������ĂȂ��̂ł���[�Ȃ�
		if (rand(2) < 1) {
			$this_file .= "2_";
			$num = int(rand($#eggs)+1);
			while (!(-e $this_file.$num.".csv")) {
				$num = int(rand($#eggs)+1);
			}
		}
		else {
			$this_file .= "3_";
			$num = int(rand($#pets)+1);
			while (!(-e $this_file.$num.".csv")) {
				$num = int(rand($#pets)+1);
			}
		}
		$this_file .= "$num.csv";

		my $item_value = 0;
		my $item_count = 0;
		open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
		my $item_name = <$fh>;
		my $header = <$fh>;
		while (my $line = <$fh>) {
			my($itime, $ivalue, $itype) = split /,/, $line;
			if ($itype ne "�j����" && $ivalue > 500) {
				$item_value += $ivalue;
				$item_count++;
			}
		}
		close $fh;

		chomp($item_name);
		$item_value = int($item_value / $item_count) if $item_count;
		if ($item_value <= 500) {
			return "hinenoya�����i�����̕�\n���݂�$item_name�̓^�_���R���v���s�\\�ł�";
		}
		else {
			return "hinenoya�����i�����̕�\n���݂�$item_name�̕��ϑ����${item_value}G�ł�";
		}
	},
	sub {
		# �V�����Lbot
		my $count = 0;
		my @blogs = ();
		open my $fh, "< $logdir/blog_news.cgi" or &error("$logdir/blog_news.cgi̧�ق��ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			push @blogs, $line;
			$count++;
			last if $count > 9;
		}
		close $fh;

		my $str = $blogs[int(rand(@blogs))];
		$str =~ s|<.*?>(.*?)<a href="(.*?)">(.*?)<.*?(\(.*?\)).*|$1$3 $4\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/$2|g;
		return $str;
	},
);

1;