# Author: Hua Liang [Stupid ET]

jQuery.postJSON = (url, args, callback) ->
    $.ajax
        url: url
        data: $.param(args)
        dataType: "text"
        type: "POST"
        success: (response) ->
            callback?(eval "(#{response})")
            console.log "In postJSON: #{response}"
        error: (response) -> console.log "ERROR:", response

jQuery.fn.formToDict = ->
    fields = @serializeArray()
    json = {}
    for value in fields
        json[value.name] = value.value
    delete json.next if json.next
    json

jQuery.fn.disable = ->
    @enable false
    @

jQuery.fn.enable = (opt_enable) ->
    if arguments.length and not opt_enable
        @attr "disabled", "disabled"
    else
        @removeAttr "disabled"
    @

newMessage = (form) ->
    msg = form.formToDict()
    disabled = form.find "input[type=submit]"
    disabled.disable()

    $.postJSON "/update",
        msg, (response) ->
            console.log response, msg
            if msg.id
                form.parent().remove()
            else
                form.find("input[type=text]").val("").select()
                disabled.enable()


updater =
    cursor:  null
    errorSleepTime: 500

    poll: ->
        args = {}
        args.cursor = updater.cursor if updater.cursor

        $.ajax
            url: "/time"
            type: "POST"
            dataType: "text"
            data: $.param(args)
            success: updater.onSuccess
            error: updater.onError

    onSuccess: (response) ->
        r = eval "(#{response})"
        messages = r.messages
        updater.cursor = messages[messages.length - 1].id

        console.log "In Updater onSuccess: #{response}"

        for msg in messages
            $("#msg").append(msg.html)

        updater.errorSleepTime = 500
        window.setTimeout(updater.poll, 0)

    onError: (response) ->
        updater.errorSleepTime *= 2
        $("#error").val "[ #{response} ]<br/>"
        window.setTimeout(updater.poll, updater.errorSleepTime)


$(document).ready ->
    $("#msgform")
        .on("submit", ->
            newMessage $(@)
            false
        )
        .on("keypress", (e) ->
            if e.keyCode is 13
                newMessage $(@)
                return false
            true
            )

    $("#message").select()

    updater.poll()
