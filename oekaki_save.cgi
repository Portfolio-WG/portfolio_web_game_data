#!/usr/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# お絵描き保存(url_save) Created by Merino
#================================================

# 投稿できる最大ｻｲｽﾞ
$max_data_size = 5000;


#================================================
$ENV{REQUEST_METHOD} =~ tr/a-z/A-Z/;
&error_oekaki("POST以外のﾘｸｴｽﾄﾒｿｯﾄﾞは受信できません") unless $ENV{REQUEST_METHOD} eq 'POST';
&error_oekaki("ﾃﾞｰﾀが大きすぎます") if $ENV{CONTENT_LENGTH} > $max_data_size;

my $buf = '';
binmode STDIN;
read(STDIN, $buf, $ENV{CONTENT_LENGTH});

my $header_magic = substr($buf, 0, 1);
if ($header_magic =~ /^[SP]$/) { &save_img($buf); }
else { &error_oekaki('対応していないｸﾗｲｱﾝﾄです'); }
exit;

#================================================
sub save_img {
	my $buf = shift;
	
	my $header_length      = substr($buf, 1, 8);
	my $send_header_length = index($buf, ";", 1 + 8);
	my $send_header        = substr($buf, 1 + 8, $send_header_length - (1 + 8) );
	my $img_length         = substr($buf, 1 + 8 + $header_length, 8);
	my $img_data           = substr($buf, 1 + 8 + $header_length + 8 + 2, $img_length);
	
	my %p = ();
	for my $pair (split /&/, $send_header) {
		my($k, $v) = split /=/, $pair;
		$p{$k} = $v;
	}
	
	&error_oekaki("ﾌﾟﾚｲﾔｰ登録されていません") unless -d "$userdir/$p{id}";
	my %datas = &get_you_datas($p{id}, 1);
	&error_oekaki("ﾌﾟﾚｲﾔｰﾊﾟｽﾜｰﾄﾞが違います") unless $datas{pass} eq $p{pass};
	
	$p{image_type} =~ tr/A-Z/a-z/;
	&error_oekaki("PNGとJPEG以外の出力は許可されていません") unless $p{image_type} eq 'jpeg' || $p{image_type} eq 'png';
	&error_oekaki("JPEG以外の出力は許可されていません")      if $is_force_jpeg && $p{image_type} ne 'jpeg';
	
	open my $fh, "> $userdir/$p{id}/picture/_$p{time}.$p{image_type}" or &error_oekaki("画像の保存に失敗しました");
	binmode $fh;
	print $fh $img_data;
	close $fh;
	
	print "Content-type: text/plain\n\n";
}

#================================================
# お絵描き側にｴﾗｰ出力
sub error_oekaki {
	my $error_message = shift;
	print "Content-type: text/plain\n\nerror\n";
	print "$error_message\n";
	exit;
}

