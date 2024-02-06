function nokori_time_wt(now_time) {
	if (now_time > 0) {
		min = Math.floor(now_time / 60);
		sec = Math.floor(now_time % 60);
		sec = ("00" + sec).substr(("00" + sec).length-2, 2);
		nokori = min + 'ï™' + sec + 'ïb';
		document.getElementById("nokori_time").innerHTML = nokori;
		next_time = now_time - 1;
		setTimeout("nokori_time_wt(next_time)",1000);
	}
	else {
		document.getElementById("nokori_time").innerHTML = '<font color="#FF0000"><b>ÇnÇjÅI<b></font>';
	}
}

function nokori_time(now_time) {
	if (now_time >= 0) {
		hour = Math.floor(now_time / 3600);
		min  = Math.floor(now_time % 3600 / 60);
		sec  = Math.floor(now_time % 60);
		min  = ("00" + min).substr(("00" + min).length-2, 2);
		sec  = ("00" + sec).substr(("00" + sec).length-2, 2);
		nokori = hour + 'éû' + min + 'ï™' + sec + 'ïb';
		document.getElementById("nokori_time").innerHTML = nokori;
		next_time = now_time - 1;
		setTimeout("nokori_time(next_time)",1000);
	}
}
