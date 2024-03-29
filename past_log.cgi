#!/usr/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#================================================
# 過去ﾛｸﾞ閲覧 Created by Merino
#================================================
&get_data;
&error("過去ﾛｸﾞﾌｧｲﾙ($in{this_file}_log.cgi)が存在しません") unless -f "$in{this_file}_log.cgi";
&error("他の国の過去ﾛｸﾞは見れません")   if $in{this_file} =~ m|/(\d+)/| && $1 ne $m{country};
&error("他の国の過去ﾛｸﾞは見れません")   if $in{this_file} =~ m|/(\d+?)_(\d+?)| && !($1 eq $m{country} || $2 eq $m{country});
&error("国の代表\者でないと見れません") if $in{this_file} =~ /daihyo/ && !&is_daihyo;
if($in{mode} eq "delete_log"){
	&delete_log($in{delete_time}, $in{this_file});
}
&run;
&footer;
exit;

#================================================
sub run {
	print qq|<form method="$method" action="$in{this_script}.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>過去ﾛｸﾞ/$in{this_title}</h2><hr>|;

	print qq|<form method="$method" action="past_log.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="this_title" value="$in{this_title}"><input type="hidden" name="mode" value="delete_log"><input type="hidden" name="this_file" value="$in{this_file}"><input type="hidden" name="this_script" value="$in{this_script}">|;
	open my $fh, "< $in{this_file}_log.cgi" or &error("$in{this_file}_log.cgi ﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bcomment = &comment_change($bcomment, 0);
		if($m{name} eq $cs{ceo}[$m{country}]){
			print qq|削除<input type="radio" name="delete_time" value="$btime">|;
			print qq|<br>|;
		}
		print qq|<font color="$cs{color}[$bcountry]">$bname <font size="1">($cs{name}[$bcountry] : $bdate)</font><br>$bcomment</font>|;
		print qq|<hr size="1">\n|;
	}
	close $fh;
	print qq|<input type="submit" value="削除" class="button_s">|;
	print qq|</form><br>|;
}

sub delete_log{
	my ($d_time, $d_file) = @_;
	my @lines = ();
	
	my $f_name = $d_file . "_log.cgi";
	open my $fh, "+< $f_name" or &error("$f_name ﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		next if($btime == $d_time);
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

1; # 削除不可
