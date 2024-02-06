#================================================
#月,日,時間帯に対応してデータを返す関数 created by あおのり 2021_9_25
#chatの背景画像更新、年賀状抽選、人気投票更新などに使用(予定)
#================================================
require './lib/jcode.pl';#これ消した方がいい？
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
#データ取得
#================================================
sub changer_run {
  my ($file_name) = @_;
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
  $month++;#比較用に調整
  open my $fh, "< $file_name" or &error("$file_nameが開けません");
  my $head_line = <$fh>;
  my ($test1,$test2) = split /<>/, $head_line;
  my @lines = ();
  my $c_line = "";
#  my $test_count = 0;
  while (my $line = <$fh>) {
    my($c_month,$c_day,$c_hour,$data1,$data2) = split /<>/, $line;
    #時間を比較
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
  my($e_month,$e_day,$e_hour,$e_data1,$e_data2) = split /<>/, $c_line;#e_data1;picture  e_data2;画像出典
	return "$e_data1";
}
#changerファイルのフォーマットは以下の通り
#(年単位以上の変化には未対応なので注意)(月をまたぐものは月ごとに設定する必要がある)
#header
#month<>day<>hour<><>data1<>data2
#================================================
#データ変更(changer_runを逐次使用すると重くなるので、読み込み用ファイルを作成する)
#================================================
sub changer_data{
  my ($file_name,$change_data) = @_;
  open my $fh, "> $file_name" or &error("$file_nameが開けません");
  print $fh $change_data;
  return;
}

1;#削除不可
