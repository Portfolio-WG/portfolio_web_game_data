#================================================
# �Ċ֐�
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
# �ăC�x
#================================================
sub on_summer {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 7) {
		return 1;
	}
	return 0;
}
#================================================
# �n���E�B���C�x
#================================================
sub on_halloween {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 9 && $mday >= 29) {
		return 1;
	}
	return 0;
}
#================================================
# �N���C�x
#================================================
sub on_december {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 11) {
		return 1;
	}
	return 0;
}
#================================================
# �N���C�x�A�N���X�}�X��
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
# �V�t�C�x
#================================================
sub on_new_year {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0) {
		return 1;
	}
	return 0;
}
#================================================
# �V�t�C�x�I��
#================================================
sub on_new_year_end {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0 && $mday >= 21) {
		return 1;
	}
	return 0;
}
#================================================
# �V�t�C�x�I��2(�N��󂭂��J�n�����p)
#================================================
sub on_new_year_end_lot {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 0 && $mday >= 20 && $hour >= 22) {
		return 1;
	}
	return 0;
}
#================================================
# �t�C�x(�{�[�h�Q�[��)
#================================================
sub on_may_june {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($month == 10 || ($month == 11 && $mday <= 10)) {
		return 1;
	}
	return 0;
}


1; # �폜�s��
