const root_id = '{{ SELF.uid }}';
let revisions = {};
let registered_functions = {};
let post_rendering_functions = [];
let registered_functions_for_init = [];
let current_cake = '-';
let init_done = false;
let selected_toppings = [];

function register_function(fname, f) {
    registered_functions[fname] = f;
}

function register_post_rendering_function(f) {
    post_rendering_functions.push(f);
}

function defocus() {
    document.activeElement.blur();
}

function send_event(topping_id, event_name, params = {}) {
    wait_indicator(true);
    let request = {'cake': current_cake, 'params': params};
    fetch('{{SELF.url}}/event/' + topping_id + '/' + event_name, { method: 'POST', body: JSON.stringify(request) })
        .then(response => response.json())
        .then(data => {
            wait_indicator(false);
            if (data['status'] == 'ok') {
                process_commands(data['commands']);
                check_revisions(data['updates']);
            }
        })
        .catch(response => {console.log(response);wait_indicator(false);});
}

function value_changed(element_id) {
    let value_dict = {};
    let request = {}
    const element = document.getElementById(element_id);
    if (!element) {
        return;
    }
    wait_indicator(true);
    value_dict[element_id] = element.value;
    request["values"] = value_dict;
    fetch('{{SELF.url}}/value_changed/'+current_cake, { method: 'POST', body: JSON.stringify(request) })
        .then(response => response.json())
        .then(data => {
            wait_indicator(false);
            if (data['status'] == 'ok') {
                process_commands(data['commands']);
                check_revisions(data['updates']);
            }
        })
        .catch(response => {console.log(response);wait_indicator(false);});
}

function process_commands(commands) {
    commands.forEach(function(request) {
        let command = request["command"];
        let parameters = request["parameters"];
        if (command == "go_to") {
            go_to_cake(parameters['cake'], parameters['request']);
        }
        if (command == 'show_message') {
            show_messages([parameters["msg"]]);
        }
        if (command == 'refresh') {
            go_to_cake("_refresh_");
        }
        if (command == 'reload') {
            window.location.reload();
        }
    })
}

function check_revisions(updates) {
    let update_targets = [];
    if (updates['_root_'] != root_id) {
        window.location.reload();
        return;
    }
    for (let [element_id, value] of Object.entries(updates['_value_'])) {
        const element = document.getElementById(element_id);
        if (element) {
            element.value = value;
        }
    }
    for (let [element_id, value] of Object.entries(updates['_inner_html_'])) {
        const element = document.getElementById(element_id);
        if (element) {
            element.innerHTML = value;
        }
    }
    for (let [element_id, styles] of Object.entries(updates['_style_'])) {
        const element = document.getElementById(element_id);
        if (element) {
            for (let [key, value] of Object.entries(styles)) {
                if (value == "-") {
                    value = null;
                }
                element.style[key] = value;
            }
        }
    }
    for (let [element_id, styles] of Object.entries(updates['_attr_'])) {
        const element = document.getElementById(element_id);
        if (element) {
            for (let [key, value] of Object.entries(styles)) {
                if (value == "-") {
                    element.removeAttribute(key);
                } else {
                    element.setAttribute(key, value);
                }
            }
        }
    }
    delete updates['_root_'];
    delete updates['_value_'];
    delete updates['_inner_html_'];
    delete updates['_style_'];
    delete updates['_attr_'];
    for (let [topping_id, revision] of Object.entries(updates)) {
        if (revisions[topping_id] !== revision) {
            update_targets.push(topping_id);
        }
    }
    refresh(update_targets);
}

function refresh(update_targets) {
    if (update_targets.length == 0) return;
    fetch('{{ SELF.url }}/revision/'+current_cake, {method: 'POST', body: JSON.stringify(update_targets) })
        .then(response => response.json())
        .then(data => {
            if (data['status'] == 'ok') {
                for (let [topping_id, payload] of Object.entries(data['payload'])) {
                    const element = document.getElementById(topping_id);
                    if (element) {
                        element.innerHTML = payload['content'];
                        call_registered_function(payload['function_call']);
                    }
                    revisions[topping_id] = payload['revision'];
                }
            }
        })
        .catch(response => {console.log(response)});
}

let check_count = 0;
function check_for_updates() {
    check_count += 1;
    let update_interval = Number('{{ update_interval_ms }}');
    fetch('{{ SELF.url }}/revision/'+current_cake)
        .then(response => response.json())
        .then(data => {
            if (data['status'] == 'ok') {
                process_commands(data['commands']);
                check_revisions(data['updates']);
            }
        })
        .catch(response => {console.log(response);update_interval += 3000;})
        .finally(response => {setTimeout(check_for_updates, update_interval);});
}

function call_registered_function(request) {
   request.forEach(function(fc) {
        let func = registered_functions[fc[0]];
        if( typeof (func) !== 'undefined' ) {
            func(fc[1]);
            // setTimeout(func.bind(this, fc[1]), 100);
        }
    })
}

function call_post_rendering_functions() {
    post_rendering_functions.forEach(function(func) {
        func();
    });
 }

function go_to_cake(cake_name, request = {}) {
    if (cake_name == current_cake) return;
    if (cake_name == "_refresh_") {
        cake_name = current_cake
    }
    if (typeof (request) === 'undefined') { request = {}; }
    fetch('{{ SELF.url }}/go_to/' + cake_name, { method: 'POST', body: JSON.stringify(request) })
        .then(response => response.json())
        .then(data => {
            if (data['status'] == 'ok') {
                let element = document.getElementById('container');
                if (element) {
                    element.innerHTML = data['content'];
                    current_cake = cake_name;
                }
                element = document.getElementById('floating_container');
                if (element) {
                    element.innerHTML = data['floating_content'];
                }
                revisions = data['revisions'];
                current_cake = data['cake_name'];
                call_registered_function(data['function_call']);
                call_post_rendering_functions();
                // if (!init_done) {
                //     registered_functions_for_init.forEach(function(f) {
                //         f();
                //     })
                //     init_done = true;
                // }
            } else { console.log(data);}
        })
        .catch(response => {console.log(response)});
}

function wait_indicator(state) {
    change_visibility('wait_indicator', state);
}

function switch_card(element_id, action='switch') {
    const element = document.getElementById(element_id);
    if (element) {
        if (action == 'get_state') {
            return element.style.display != 'none'
        }
        if (action == 'switch')
        {
            action = (element.style.display == 'none') ? 'open' : 'close';
        }
        if (action == 'close' && element.style.display != 'none') {
            document.activeElement.blur();
            element.style.display = 'none';
        }
        if (action == 'open' && element.style.display == 'none') {
            element.style.display = 'initial';
        }
        if (element_id.endsWith('.magic_card')) {
            const script_indicator = document.getElementById('script_indicator');
            if (script_indicator) {
                script_indicator.innerHTML = action == 'open' ? "&#11088;" : "&starf;";
            }
        }
    }
}

let pancake_state = {};
function save_state(key, state, lasting=False) {
    key = current_cake+"."+key;
    if(lasting) {
        localStorage.setItem("a", "Smith");
    }
}

function recall_state(key, state) {
    localStorage.setItem("lastname", "Smith");
}

function change_visibility(element_id, state='change') {
    const element = document.getElementById(element_id);
    if (element) {
        if(state == 'change') {state = element.style.display == 'none';}
        if (state) { element.style.display = 'initial'; } else { element.style.display = 'none'; }
    }
}

function show_messages(msgs) {
    if (msgs.length == 0) return;
    const toast = document.getElementById("msg_box");
    console.log(toast);
    msgs.forEach(function(msg) {toast.innerHTML = msg; toast.className = "show"; setTimeout(function(){ toast.className = toast.className.replace("show", ""); toast.innerHTML="";}, 3000);})
}

function modified_click_handler(element_id, e) {
    if(!(e.ctrlKey || e.metaKey)) {
        return;
    }
    if(e.shiftKey) {
        selected_toppings.push(element_id);
    } else {
        selected_toppings = [element_id];
    }
    send_event(current_cake, "select", selected_toppings);
    e.preventDefault();
}

function set_topping_click_with_modifier_key() {
    let elements = document.getElementsByClassName("topping");
    let num_elements = elements.length;
    selected_toppings = [];
    for(let i = 0; i < num_elements; i++) {
         let element = elements[i];
         element.addEventListener("mousedown", modified_click_handler.bind(this, element.id), false);
    }
}

register_post_rendering_function(set_topping_click_with_modifier_key);
go_to_cake('');
setTimeout(check_for_updates, Number('{{ update_interval_ms }}'));
