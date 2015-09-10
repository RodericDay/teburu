window.oncontextmenu = disable = function() {

    return false

}

window.onload = connect = function() {

    var loc = window.location.toString().replace("http", "ws");

    ws = new WebSocket(loc);

    ws.onmessage = update;
    ws.onopen = function() { ws.send(window.sessionStorage.getItem("keycode")) }
    ws.onclose = function() { info.innerHTML = "You were disconnected" }

}

update = function(message) {

    var data = JSON.parse(message.data);

    if (data.info) {

        var i = data.info[0], n = data.info[1], k = data.info[2];
        info.innerHTML = "You are Player "+i+" ("+n+" online)";
        myArea = "z"+(i);
        if (k) { window.sessionStorage.setItem("keycode", k) }

    }

    (data.moves || []).forEach(function(entry) { move.apply(this, entry) } );

}

move = function(id, x, y, z, classes, label) {

    var el = document.getElementById(id) || newPiece(id, classes, label);

    el.style.left = x + "px";
    el.style.top = y + "px";
    el.style.zIndex = z;

    transfer(el);

}

newPiece = function(id, classes, label) {

    el = document.createElement("div");

    el.id = id;
    el.className = classes + " noselect";
    el.innerHTML = label;

    document.body.appendChild(el);

    return el

}

transfer = function(el) {

    if (!el.classList.contains("card")) { return }

    var pieceRect = el.getBoundingClientRect(),
        nodeList = document.getElementsByClassName("zone"),
        nodeArray = [].slice.call(nodeList);

    var known = nodeArray.some(function(zone) {

        var zoneRect = zone.getBoundingClientRect(),
            inside =    (zoneRect.left < pieceRect.left) &&
                        (zoneRect.top < pieceRect.top) &&
                        (zoneRect.right > pieceRect.right) &&
                        (zoneRect.bottom > pieceRect.bottom)
            blind = (zone.id == myArea);

        if (inside & !blind) {

            el.classList.remove("facedown");
            return true

        }

    });

    if (!known) { el.classList.add("facedown") }

}
