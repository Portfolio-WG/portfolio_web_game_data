#=================================================
# �ڸ��ݒǉ� Created by Merino
#=================================================
# �g����: require './lib/add_collection.cgi'; ���� &add_collection;
# collction.cgi,depot.cgi�Ŏg�p

#================================================
# �ڸ����ް��擾 + �����������ɂ��ڸ��݂ɂȂ��Ȃ�ǉ�
#=================================================
sub add_collection {
	my @kinds = ('', 'wea', 'egg', 'pet');
	my $kind = 1;
	my $is_rewrite = 0;
	my @lines = ();
	
	open my $fh, "+< $userdir/$id/collection.cgi" or &error("�ڸ���̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d; # \n���s�폜
		
		# �ǉ�
		if ($m{ $kinds[$kind] } && $line !~ /,$m{ $kinds[$kind] },/) {
			$is_rewrite = 1;
			$line .= "$m{ $kinds[$kind] },";
			$mes .= $kind eq '1' ? $weas[$m{wea}][1]
				  : $kind eq '2' ? $eggs[$m{egg}][1]
				  :                $pets[$m{pet}][1]
				  ;
			$mes .= '���V�����}�ӂɒǉ�����܂���<br>';
			
			# sort
			$line  = join ",", sort { $a <=> $b } split /,/, $line;
			$line .= ",";
		}
		
		push @lines, "$line\n";
		++$kind;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	return @lines;
}


1; # �폜�s��
