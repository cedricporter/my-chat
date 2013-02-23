$(document).ready(function() {

    $("#msgform").on("submit", function() {
	newMessage($(this));
	return false;
    });

    $("#msgform").on("keypress", function(e) {
	if (e.keyCode == 13) {
	    newMessage($(this));
	    return false;
	}
	return true;
    });

    $("#message").select();

    updater.poll();
});


jQuery.postJSON = function(url, args, callback) {
    // args._xsrf = getCookie("_xsrf");
    $.ajax({url: url,
            data: $.param(args),
            dataType: "text",
            type: "POST",
            success: function(response) {
                if (callback)
                    callback(eval("(" + response + ")"));
            },
            error: function(response) {
                console.log("ERROR:", response);
            }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};


function newMessage(form) {
    var msg = form.formToDict();
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    console.log("in newMessage");

    $.postJSON("/update", msg, function(response) {
        if (msg.id) {
	    form.parent().remove();
	    console.log("in newMessage msg.id");
        }
        else {
	    form.find("input[type=text]").val("").select();
	    disabled.enable();
	    console.log("val");
        }
    });
}


var updater = {
    poll: function () {
	$.ajax({url: "/time",
		type: "POST",
		dataType: "text",
		success: updater.onSuccess,
		error: updater.onError,
	       });
    },

    onSuccess: function(response) {
        var r = eval("(" + response + ")");
        var messages = r.messages;
	$("#msg").append(messages[messages.length - 1].html);

	window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
	$("#error")[0].innerHTML = "[ " + response + " ]" + "<br/>";
	window.setTimeout(updater.poll, 500);
    },

};
