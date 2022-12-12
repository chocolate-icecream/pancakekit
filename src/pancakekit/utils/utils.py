import threading, traceback, os, inspect
import importlib
import __main__

def get_number(value):
    try:
        return int(value)
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        pass
    return value

def get_formatted_number_str(value):
    if isinstance(value, int):
        return str(value)
    try:
        a = float(value)
        if abs(a) > 10:
            return f"{a:.0f}"
        return f"{a:.2}"
    except Exception:
        pass
    return value

def style_dict_to_style_str(style_dict):
    return "".join([f"{k}:{v};" for k, v in style_dict.items()])

def join_path_or_none(*args):
    if any([x is None for x in args]):
        return None
    return os.path.join(*args)



def get_caller(target_class):
    frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(frame)
    for f in caller_frame:
        if "self" in inspect.getargvalues(f[0]).locals:
            obj = inspect.getargvalues(f[0]).locals["self"]
            if isinstance(obj, target_class):
                return obj
    return None

def skip_exception(func, *args, error_msg=None, return_value=None, error_return_value=None, logger=None, **kwargs):
    try:
        result = func(*args, **kwargs)
    except Exception:
        if logger is None:
            pass
        elif error_msg:
            if len(error_msg) > 0:
                logger.exception(error_msg)
        else:
            logger.exception(traceback.format_exc())
        return error_return_value
    if return_value is not None:
        return return_value
    return result


def is_mode_interactive():
    return not hasattr(__main__, "__file__")

def import_module_if_available(module_name: str):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return None
    return importlib.import_module(module_name)


class pk_wrapped_dict(dict):
    def __init__(self, setitem_callback, *args):
        super().__init__(*args)
        self.__setitem_callback = setitem_callback
    def __setitem__(self, key, value):
        self.__setitem_callback(key, value)
        return super().__setitem__(key, value)
    def __setattr__(self, name: str, value):
        if name in self:
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)
    def __getattr__(self, name: str):
        if name in self:
            return self.__getitem__(name)
        else:
            return super().__getattribute__(name)


def is_pandas_dataframe(obj):
    if obj.__class__.__module__ == "pandas.core.frame":
        return True
    return False

def is_pil_image(obj):
    if obj.__class__.__module__.startswith("PIL"):
        return True
    return False

### Decorators ###

def periodic(interval=1):
    def decorate_func(func):
        def wrapper(*args, **kwargs):
            def run_periodic_thread():
                t = threading.Timer(interval, run_periodic_thread)
                t.daemon = True
                t.start()
                try:
                    func(*args, **kwargs)
                except:
                    pass
            run_periodic_thread()
        return wrapper
    return decorate_func

def new_thread(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrapper