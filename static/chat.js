$(document).ready(function() {
    updater.poll();
});

var updater = {
    poll: function () {
	$.ajax({url: "/time",
		type: "GET",
		dataType: "text",
		success: updater.onSuccess,
		error: updater.onError,
	       });
    },

    onSuccess: function(response) {
	$("#msg")[0].innerHTML = response;

	window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
	$("#error")[0].innerHTML += "[ " + response + " ]" + "<br/>";
	window.setTimeout(updater.poll, 500);
    },

};
