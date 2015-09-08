transfer = function(draggable) {

    var pieceRect = draggable.getBoundingClientRect(),
        nodeList = document.getElementsByClassName("stash"),
        nodeArray = [].slice.call(nodeList);

    var known = nodeArray.some(function(zone) {

        var zoneRect = zone.getBoundingClientRect(),
            inside =    (zoneRect.left < pieceRect.left) &&
                        (zoneRect.top < pieceRect.top) &&
                        (zoneRect.right > pieceRect.right) &&
                        (zoneRect.bottom > pieceRect.bottom)
            blind = (zone.id == myArea);

        if (inside & !blind) {

            draggable.classList.remove("facedown");
            return true

        }

    });

    if (!known) { draggable.classList.add("facedown") }

}
