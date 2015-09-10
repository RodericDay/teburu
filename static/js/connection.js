window.oncontextmenu = disable = function() {

    return false

}

window.onload = connect = function() {

    var loc = window.location.toString().replace("http", "ws");

    ws = new WebSocket(loc);

    ws.onmessage = update;
    ws.onopen = function() { ws.send(window.sessionStorage.getItem("keycode")) }
    ws.onclose = function() { infoBar.innerHTML = "You were disconnected" }

    createChat();

}

update = function(message) {

    var actions = JSON.parse(message.data);

    actions.forEach(function(entry) {

        var fname = entry[0], args = entry.slice(1);
        try { window[fname].apply(this, args); }
        catch (TypeError) { console.log("Misunderstood:", fname); }

    });

}

move = function(id, x, y, z, classes, label) {

    var el = document.getElementById(id) || newPiece(id, classes, label);

    el.style.left = x + "px";
    el.style.top = y + "px";
    el.style.zIndex = z;

    transfer(el);

}

info = function(playerN, totalN, keycode) {

    infoBar.innerHTML = "You are Player "+playerN+" ("+totalN+" online)";
    myArea = "z"+playerN;
    if (keycode) { window.sessionStorage.setItem("keycode", keycode) }

}

message = function(message) {

    log.innerHTML += message + "<br>";
    log.scrollTop += 1000;

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
