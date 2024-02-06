#=================================================
# 討伐ﾌｨｰﾙﾄﾞ設定 Created by Merino
#=================================================
# ◎追加/削除/変更/並び替え可
# ※No10以上増やす場合は./log/monster/にﾌｧｲﾙを追加してね

# *その数値以上のﾓﾝｽﾀｰが生息：例> 森なら300以上600未満の強さの魔物が生息
@places = (
#[0]No,[1]*強さ,[2]名前,			[3]拾えるﾀﾏｺﾞ [4]イベント討伐地かどうか
	['beginner',	0,		'新兵訓練場',		[51],	0],
	['event',	100,	'白銀の庭園',			[1..50],		1],#山
	['event',	100,	'極夜海',			[2..41],	1],#空白の跡地
	[0,	30,		'ﾎﾟｶﾎﾟｶ平原',		[4..24,42,43,50,51],	0],
	[1,	300,	'ﾓﾘﾓﾘ森',			[1,4..24,43,50],		0],
	[2,	600,	'ﾃﾞﾛﾃﾞﾛ沼',			[1,4..31,33,43,48,50],	0],
	[3,	1000,	'ｿｰﾀﾞｰ海',			[1,4..31,33,43..46,48],	0],
	[4,	1500,	'ｶｯｻﾘ砂漠',			[1..33,43..50],			0],
	[5,	2500,	'ｺﾞﾂｺﾞﾂ山',			[1..50],				0],
	[6,	4000,	'空白の跡地',		[2..41],				0],
	[7,	6000,	'封印されし魔界',	[2..41],				0]
);
#@places_winter_secret = (#隠しステージ
#	[10,	10000,	'Hyperborea',			[2,3,27,32,38,40,41,45,46,47],	]#君の銀の庭とだいたい同じ卵
#);
