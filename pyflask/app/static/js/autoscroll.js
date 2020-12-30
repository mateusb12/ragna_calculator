var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);




$(window).scroll(function () {
	sessionStorage.scrollTop = $(this).scrollTop();
});
$(document).ready(function () {
	if (sessionStorage.scrollTop != "undefined") {
		$(window).scrollTop(sessionStorage.scrollTop);
	}
});

console.log('Autoscroll.js executed!')