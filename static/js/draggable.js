selection = null;

window.onmousedown = select = function(ev) {

    var isDraggable = ev.target.classList.contains("draggable");

    if (isDraggable) {

        selection = ev.target;
        selection.style.zIndex += 1000;
        x_offset = ev.layerX;
        y_offset = ev.layerY;

    }

}

window.onmousemove = drag = function(ev) {

    if (ev.buttons !== 1 || !selection) { return false }

    selection.style.left = ev.clientX - x_offset + "px";
    selection.style.top = ev.clientY - y_offset + "px";

}

window.onmouseup = release = function(ev) {

    if (selection && ws) {

        var i = selection.id,
            x = selection.style.left.replace("px", ""),
            y = selection.style.top.replace("px", ""),
            data = [i, x, y],
            json = JSON.stringify(data);

        ws.send(json);

    }

    selection = null;

}
