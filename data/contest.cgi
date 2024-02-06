#=================================================
# ｺﾝﾃｽﾄ設定 Created by Merino
#=================================================
# contest.cgi, shopping_contest.cgi

# 上位ﾗﾝｷﾝｸﾞの賞品
@c_prizes = (
#[0]ﾀﾏｺﾞNo,[1]賞金
	[3,	300000],
	[2,	50000],
	[1,	10000],
);


# 最低ｴﾝﾄﾘｰ数(この人数以上集まらないと開催されない)
$min_entry_contest = 5;

# 最大ｴﾝﾄﾘｰ数
$max_entry_contest = 30;

# ｺﾝﾃｽﾄ周期(日)
$contest_cycle_day = 15;

# 連続ｴﾝﾄﾘｰ(0:不可能[現ｺﾝﾃｽﾄにｴﾝﾄﾘｰしている場合は、次回のｺﾝﾃｽﾄに参加できない],1:可能)
$is_renzoku_entry_contest = 1;

# 表示するもの(./log/contestにあるもの) ◎追加/変更/削除/並べ替え可能
@contests = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名','種類'],
	['絵画ｺﾝﾃｽﾄ',	'picture',	'img',	'★画伯爵'],
	['物語ｺﾝﾃｽﾄ',	'book',		'html',	'★名作家'],
	['お題ｺﾝﾃｽﾄ',	'etc',		'html',	'★題作家'],
);



1; # 削除不可
