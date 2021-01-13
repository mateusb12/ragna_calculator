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

function forceRender3(){
	var timestamp = new Date().getTime();
	var select_value = document.getElementById("picDD").value;
	var src = "static/assets/" + select_value + ".png?t=" + timestamp;
	document.getElementById("other_info_img").src=src;
}

console.log('Autorefresh.js executed!')