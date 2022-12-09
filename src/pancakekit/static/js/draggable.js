/* The code originates from https://www.w3schools.com/howto/howto_js_draggable.asp */

let draggable_state = {};
function make_draggable(request) {
    let element_id = request["element_id"];
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    let element = document.getElementById(element_id);
    let handle = document.getElementById(element_id+"_handle");
    if (!element) {
        return
    }
    if (handle) {
        handle.onmousedown = dragMouseDown;
    } else {
        element.onmousedown = dragMouseDown;
    }
    
    if (typeof(draggable_state[element_id]) !== 'undefined') {
        element.style.top =  draggable_state[element_id]["top"];
        element.style.left =  draggable_state[element_id]["left"];
    } else {
        element.style.top =  "200px";
        element.style.left =  "50px";
    }
    element.style.visibility = 'visible';

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }
    
    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        let top = (element.offsetTop - pos2);
        let left = (element.offsetLeft - pos1);
        if(top < 40) {
            top = 40;
        }
        if(left < -300) {
            left = -300;
        }
        element.style.top =  top + "px";
        element.style.left =  left + "px";
    }
    
    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
        draggable_state[element_id] = {"top": element.style.top, "left": element.style.left}
    }
}

register_function("make_draggable", make_draggable);