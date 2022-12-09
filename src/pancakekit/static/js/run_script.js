function run_script(force=false) {
    const element_id = current_cake + '.magic_card';
    const element = document.getElementById(element_id);
    console.log(element_id);
    if (element) {
        if (element.style.display == "none" && !force) {
            return;
        }
        document.activeElement.blur();
        setTimeout(send_event.bind(this, element_id, "run_script"), 100);
    }
}


document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.keyCode == 13) {
        run_script();
        e.preventDefault();
    } else if (e.shiftKey && e.keyCode == 13) {
        switch_card(current_cake+'.magic_card');
        e.preventDefault();
    } else if ((e.ctrlKey || e.metaKey) && (e.keyCode == 38 || e.keyCode == 40)) {// keyup
        if (switch_card(current_cake+'.magic_card', 'get_state')) {
            send_event(current_cake+'.magic_card', 'recall_honeypod', {increment: e.keyCode-39});
            e.preventDefault();
        }
    }
    if (e.keyCode == 9) {
        const element = document.activeElement;
        if(element.id.startsWith("script_")) {
            document.execCommand("insertText", false, '  ');
            e.preventDefault();
        }
    }
});