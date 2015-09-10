function createChat() {

    var chat = document.createElement("form"),
        log = document.createElement("div"),
        textInput = document.createElement("input"),
        submitButton = document.createElement("input");

    chat.id = "chatForm";
    log.id = "log";

    textInput.id = "textInput";
    textInput.autocomplete = "off";

    submitButton.id = "submitButton";
    submitButton.type = "submit";
    submitButton.value = "Send";

    chat.appendChild(log);
    chat.appendChild(textInput);
    chat.appendChild(submitButton);

    chat.onsubmit = function() {

        var message = "<b>Player #"+myArea.slice(1)+":</b> "+textInput.value,
            payload = JSON.stringify(["message", message]);
        ws.send(payload);
        textInput.value = '';
        return false

    }

    document.body.appendChild(chat);

}
