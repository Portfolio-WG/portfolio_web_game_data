#================================================
# 夏関数
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
# 夏イベ
#================================================
sub on_summer {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 7) {
		return 1;
	}
	return 0;
}
#================================================
# ハロウィンイベ
#================================================
sub on_halloween {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 9 && $mday >= 29) {
		return 1;
	}
	return 0;
}
#================================================
# 年末イベ
#================================================
sub on_december {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 11) {
		return 1;
	}
	return 0;
}
#================================================
# 年末イベ、クリスマス後
#================================================
sub on_december_end {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 11 && $mday >= 26) {
#	if ($month == 11) {
		return 1;
	}
	return 0;
}

#================================================
# 新春イベ
#================================================
sub on_new_year {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0) {
		return 1;
	}
	return 0;
}
#================================================
# 新春イベ終了
#================================================
sub on_new_year_end {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0 && $mday >= 21) {
		return 1;
	}
	return 0;
}
#================================================
# 新春イベ終了2(年賀状くじ開始処理用)
#================================================
sub on_new_year_end_lot {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0 && $mday >= 20 && $hour >= 22) {
		return 1;
	}
	return 0;
}
#================================================
# 春イベ(ボードゲーム)
#================================================
sub on_may_june {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 10 || ($month == 11 && $mday <= 10)) {
		return 1;
	}
	return 0;
}


1; # 削除不可
