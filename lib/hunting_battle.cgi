$boss = 0;
$metal = 0;

if($places[$m{stock}][0] eq 'event'){#冬イベ用,全ダメージ,回復量減少(固定値を覗く)、1000以上のHP非表示
  require './lib/_battle_core_event.cgi';
}else{
  require './lib/_battle_core.cgi';
}

1; # 削除不可
