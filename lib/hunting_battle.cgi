$boss = 0;
$metal = 0;

if($places[$m{stock}][0] eq 'event'){#�~�C�x�p,�S�_���[�W,�񕜗ʌ���(�Œ�l��`��)�A1000�ȏ��HP��\��
  require './lib/_battle_core_event.cgi';
}else{
  require './lib/_battle_core.cgi';
}

1; # �폜�s��
