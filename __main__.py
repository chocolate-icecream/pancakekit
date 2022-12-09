from pancakekit import *


def _run(port, plate, local):
    import webbrowser, threading
    import code
    port = 8000
    t = threading.Timer(1, lambda: webbrowser.open(f"http://127.0.0.1:{port}/"))
    t.daemon = True
    t.start()
    plate.serve(wait_done=False, port=port)
    code.interact(local=local)

_cake = Pancake()
plate = _cake.plate
cake = plate.magic_cake
_run(8000, _cake, locals())
plate.done()
