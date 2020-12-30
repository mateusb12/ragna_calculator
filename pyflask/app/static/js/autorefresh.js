function forceSubmit(){
	document.getElementById("submit").click();
}

function forceRender(){
	var timestamp = new Date().getTime();
	var src = "static/assets/custom.png?t=" + timestamp
	return src;
}

function forceRender2(){
	var timestamp = new Date().getTime();
	var src = "static/assets/equip_custom.png?t=" + timestamp
	return src;
}

console.log('Autorefresh.js executed!')