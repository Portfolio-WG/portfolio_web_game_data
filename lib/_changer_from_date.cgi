#================================================
#��,��,���ԑтɑΉ����ăf�[�^��Ԃ��֐� created by �����̂� 2021_9_25
#chat�̔w�i�摜�X�V�A�N��󒊑I�A�l�C���[�X�V�ȂǂɎg�p(�\��)
#================================================
require './lib/jcode.pl';#������������������H
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
#�f�[�^�擾
#================================================
sub changer_run {
  my ($file_name) = @_;
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
  $month++;#��r�p�ɒ���
  open my $fh, "< $file_name" or &error("$file_name���J���܂���");
  my $head_line = <$fh>;
  my ($test1,$test2) = split /<>/, $head_line;
  my @lines = ();
  my $c_line = "";
#  my $test_count = 0;
  while (my $line = <$fh>) {
    my($c_month,$c_day,$c_hour,$data1,$data2) = split /<>/, $line;
    #���Ԃ��r
    if($c_month){
      if($c_month > $month){
        last;
      }elsif($c_month eq $month && $c_day > $mday){
        last;
      }elsif($c_month eq $month && $c_day eq $mday && $c_hour >= $hour){
        last;
      }
    }elsif(!$c_month && $c_day){
      if($c_day > $mday || ($c_day eq $mday && $c_hour >= $hour)){
        last;
      }
    }elsif(!$c_month && !$c_day && $c_hour){
      if($c_hour >= $hour){
        last;
      }
    }
    push @lines, $line;
    $c_line = $line;
#    $test_count++;
  }
  close $fh;
#  return $test_count;
  my($e_month,$e_day,$e_hour,$e_data1,$e_data2) = split /<>/, $c_line;#e_data1;picture  e_data2;�摜�o�T
	return "$e_data1";
}
#changer�t�@�C���̃t�H�[�}�b�g�͈ȉ��̒ʂ�
#(�N�P�ʈȏ�̕ω��ɂ͖��Ή��Ȃ̂Œ���)(�����܂������̂͌����Ƃɐݒ肷��K�v������)
#header
#month<>day<>hour<><>data1<>data2
#================================================
#�f�[�^�ύX(changer_run�𒀎��g�p����Əd���Ȃ�̂ŁA�ǂݍ��ݗp�t�@�C�����쐬����)
#================================================
sub changer_data{
  my ($file_name,$change_data) = @_;
  open my $fh, "> $file_name" or &error("$file_name���J���܂���");
  print $fh $change_data;
  return;
}

1;#�폜�s��
