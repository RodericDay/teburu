disable = function() { return false }

window.oncontextmenu = disable;

window.onload = connect = function() {

    var loc = window.location.toString().replace("http", "ws");

    ws = new WebSocket(loc);
    ws.onmessage = update;

}

update = function(message) {

    myArea = "stash" + message.data[0]; // super bad
    var data = JSON.parse(message.data.substring(1));

    data.forEach(function(entry) {

        var el = document.getElementById(entry[0]) || createNew(entry[0], entry[3], entry[4]);

        el.style.left = entry[1] + "px";
        el.style.top = entry[2] + "px";

        if (el.classList.contains("draggable") &&
            el.classList.contains("card")) { transfer(el) };

    });

}

createNew = function(id, classes, label) {

    var el = document.createElement("div");
    el.className = classes;
    el.classList.add("noselect");
    el.id = id;
    el.innerHTML = label;
    document.body.appendChild(el);
    return el

}
