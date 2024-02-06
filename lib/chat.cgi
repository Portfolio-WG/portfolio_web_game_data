require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
require './lib/_auto_loader_js.cgi';
#================================================
# Chat Created by Merino
#================================================

# �A���������݋֎~����(�b)
$bad_time    = 5;

# �ő�۸ޕۑ�����
$max_log     = 60;

# �ő���Đ�(���p)
$max_comment = 200;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60 * 3;

# �����۰�ގ���
@reload_times = (0, 30, 60, 90, 120);

#================================================
sub run {
	for my $deny (@denies) {
		$deny =~ s/\./\\\./g;
		$deny =~ s/\*/\.\*/g;
		if ($is_mobile) {
			$in{comment} = '' if $agent =~ /$deny/;
		}
		else {
			$in{comment} = '' if $addr =~ /^$deny$/i;
			$in{comment} = '' if $host =~ /^$deny$/i;
		}
	}
	if ($in{comment} && $m{silent_time} > $time) {
		if($m{silent_kind} ne '4' && &on_december_end){
			$in{comment} = '���[�˂�܂�';
			$in{comment} = '���[�˂�' if rand(10) < 1;
		} elsif ($m{silent_kind} eq '0') {
			$in{comment} = '��[�I��[�I';
		} elsif ($m{silent_kind} eq '1') {
			$in{comment} = '̫��I';
		} elsif ($m{silent_kind} eq '2') {
			$in{comment} = '�ߩ�I';
		} elsif ($m{silent_kind} eq '3') {
			$in{comment} .= '�ۂۂۂہ[��';
		} elsif ($m{silent_kind} eq '4') {
			$in{comment} .= $m{silent_tail};
		}
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member) = &get_member;

	if ($is_appli) {
		&show_page_switcher;
	}
	else {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|�����۰��<select name="reload_time" class="select1"><option value="0">�Ȃ�|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]�b| : qq|<option value="$i">$reload_times[$i]�b|;
		}
		print qq|</select>|;

		print qq|<span style="font-size:14px;">|;
		print qq|�@<span onClick="textset('�z�H�V')"><font color="#FFD700">��</font></span>|;
		print qq|�@<span onClick="textset('�I�D�v')"><font color="#00FA9A">��</font></span>|;
		print qq|�@<span onClick="textset('�n�@�g')"><font color="#FFB6C1">&hearts;</font></span>|;
		print qq|</span>|;
	}

	print qq|<div id="body_mes">|;
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|</form><font size="2">$member_c�l</font><hr>|;
	}else{
		print qq|</form><font size="2">$member_c�l:$member</font><hr>|;
	}
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	my $blacklist_on = 0;#���ؽ���_�����y���p

	if(-f "$userdir/$id/blacklist_chatpublic.cgi"){#������
		open my $fh5, "< $userdir/$id/blacklist_chatpublic.cgi" or &error("$userdir/$id/blacklist_chatpublic.cgi ̧�ق��J���܂���");
		@blacklist_p_chat = ();
		while (my $line_b = <$fh5>) {
			my($blackname) = split /<>/, $line_b;
			push @blacklist_p_chat, $blackname;
		}
		close $fh5;
		$blacklist_on = 1;
	}

	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		my $blacklist_on_person = 0;
		if($blacklist_on){
			for my $i (0..$#blacklist_p_chat){
				if($blacklist_p_chat[$i] eq $bname){
					$blacklist_on_person = 1;
					$bcomment = '';
				}
			}
		}
#		if($blacklist_on_person eq 1){
#			next;
#		}
		$bname = &name_link($bname);
		unless ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
			$bname .= "[$bshogo]" if $bshogo;
		}
		$bcomment = &comment_change($bcomment, 1);

		if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
			print qq|<font color="#ffffff">$bname�F$bcomment <font size="1">(�����Ȃ�: $bdate)</font></font><hr size="1">\n|;
		}else{
			print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		}
	}
	close $fh;
	print qq|</div>|;
}


#================================================
# chat�pheader
#================================================
sub header {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	&load_RWD;
#	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
}

sub header2 {
	#=====�w�i�摜�̎擾(�X�V���s�t�@�C����_changer_from_date.cgi)===================
	open my $fhc, "< $logdir/changer_date/backpicture_chatpiblic.cgi" or &error("$logdir/changer_date/backpicture_chatpiblic.cgi ̧�ق��J���܂���");
	my $line_c = <$fhc>;
	my ($back_picture) = split /<>/, $line_c;
	close $fhc;

	#=====�w�i�摜�̐ݒ�===================
	my $backg_pic_size = "800px 150px";
	my $init_background = "icon/back_black_pub.png";#���w�i�A�ݒ��off�ɂ�����
	my $background_picture = "icon/$back_picture";#�w�i�摜
	if($m{is_back_picture}){
		$background_picture = $init_background;
	}
	#=====header===================
	if ($is_mobile) {
		print <<"EOM";
<style type="text/css"><!--  body{
background:
url("https://www.sora17.xyz/bj/$background_picture") no-repeat;
image-rendering: pixelated;
image-rendering: -webkit-crisp-edges;
image-rendering: -moz-crisp-edges;
-ms-interpolation-mode: nearest-neighbor;
background-size: $backg_pic_size;
background-color: #000000;
}
--></style></head><body $body><a name="top"></a>
EOM
	}
	else {
		my $container = '';
		my $css = '';
		my $rwd = '';
		if ($is_appli) {
			$container = qq|<div id="container"><div id="contents">|;
			$css = qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj_appli.css">|;
		}
		else {
			if($is_smart){
				$backg_pic_size = "100% 140px";
			}
			$rwd = qq|<meta name="viewport" content="width=device-width">\n<link rel="stylesheet" media="screen and (max-width: 480px)" href="$htmldir/smart.css" />\n<link rel="stylesheet" media="screen and (min-width: 481px)" href="$htmldir/tablet.css" />| if $is_smart;
			$css = qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj_exp.css">|;
		}
		$auto_loader_head = &auto_loader($this_file);
		print <<"EOM";
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
$css
$rwd
<script language="JavaScript">
<!--
function textset(text){
	document.form.comment.value = document.form.comment.value + text;
}
function textfocus() {
	document.form.comment.focus();
	return true;
}
-->
</script>
<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js"></script>
$auto_loader_head
<style type="text/css">
<!--
body{
	color: #CCC;
	font-family: -apple-system;
	font-size: 90%;
	background:
	url("https://www.sora17.xyz/bj/$background_picture") no-repeat;
	image-rendering: pixelated;
	image-rendering: -webkit-crisp-edges;
	image-rendering: -moz-crisp-edges;
	-ms-interpolation-mode: nearest-neighbor;
	background-size: $backg_pic_size;
	background-color: #000000;
}
-->
</style>

</head>
<body>$container
EOM
	}
}

1; # �폜�s��
