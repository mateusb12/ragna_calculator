$(function() {
	$('a#test').on('click', function(e) {
		e.preventDefault()
		var postData = {
			base_level: {{'form.base_level.dat'a}},
			job_level: {{'form.job_level.data'}}
		}
		$.ajax({
			url: "/background_process_test",
			type: "POST",
			data: JSON.stringify(postData),
		});
		return false;
	});
});

console.log("external_flask_function.js loaded!")