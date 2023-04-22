from pancakekit import *
import sys, importlib, os


def _run(port, plate, local):
    import webbrowser, threading
    import code
    port = 8000
    t = threading.Timer(1, lambda: webbrowser.open(f"http://127.0.0.1:{port}/"))
    t.daemon = True
    t.start()
    plate.serve(wait_done=False, port=port)
    code.interact(local=local)

local_variables = locals()

_cake = Pancake()
plate = _cake.plate
cake = plate.magic_cake

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(file_path))[0], file_path)
    target_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(target_module)
    variables = {name: obj for name, obj in inspect.getmembers(target_module) if not inspect.isbuiltin(obj)}
    local_variables.update(variables)
    for name, obj in variables.items():
        if callable(obj):
            _cake.add(obj, name=name)

_run(8000, _cake, local_variables)
plate.done()
