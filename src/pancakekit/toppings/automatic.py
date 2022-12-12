from ..pancakekit import Topping, Tag
from .basic import DictInput, Row, Column, Button, Input, Text, Slider
from .image import ImageView
from .table import Table
import inspect
import functools
from types import LambdaType
import re
from ..utils import *


class FromFunction(DictInput):
    def __init__(self, function, **kwargs):
        super().__init__(function, **kwargs)

    def prepare(self, function):
        self.arg_dict = {}
        self.function = function
        for key, param in inspect.signature(function).parameters.items():
            self.arg_dict[param.name] = param.default if param.default != inspect.Parameter.empty else 0
        super().prepare(self.arg_dict)
        title = function.__name__ if not isinstance(function, LambdaType) else "lambda"
        button = self.add(Button(title, style={"display": "flex"}))
        button.clicked = self.call_function
    
    def call_function(self):
        result = self.function(**self.value)
        if result is not None:
            self.cake.show_message(result)

def topping_from_object(obj):
    if isinstance(obj, str):
       return topping_from_string(obj)
    if isinstance(obj, (float, int)):
        return Text(obj, shadow=1, shadow_blur=1)
    if obj.__class__.__module__.startswith("PIL."):
        return  ImageView(obj)
    if is_pandas_dataframe(obj) or (isinstance(obj, dict) and all([isinstance(value, list) for value in obj.values()])):
        return  Table(obj)
    if isinstance(obj, dict):
        return DictInput(obj)
    if inspect.isfunction(obj):
        return FromFunction(obj)

def topping_from_string(obj):
    slider_re = r"([\S ^@]*)@slider\(([\d\.\-\s]*),([\d\.\-\s]*)(,[\d\.\-\s]*)?\)"
    image_re = r"([\S ]*).(png|PNG|jpg|JPG|jpeg|JPEG|tiff|TIFF|tif|TIFF|bmp|BMP|gif|GIF)"
    m = re.match(r"([\S ^:]*):([\S ]*)", obj)
    if m is not None:
        label, value_str = m.groups()
        m = re.match(slider_re, label)
        if m is not None:
            return topping_from_string_slider(m, value_str)
        value = get_number(value_str.strip())
        value = value if isinstance(value, (int, float)) else value_str
        kwargs = {"default": value} if len(value_str) > 0 else {}
        return Input(label+":", **kwargs)
    m = re.match(slider_re, obj)
    if m is not None:
        return topping_from_string_slider(m)

    m = re.match(image_re, obj)
    if m is not None:
        return topping_from_string_image(m)
    return Text(obj, shadow=1, shadow_blur=1)

def topping_from_string_slider(m, value_str = ""):
    value = get_number(value_str.strip())
    label, r_min_str, r_max_str, step_str = m.groups()
    kwargs = {"value": value} if len(value_str) > 0 else {}
    kwargs["range_min"] = get_number(r_min_str.strip())
    kwargs["range_max"] = get_number(r_max_str.strip())
    if step_str is not None:
        kwargs["step"] = get_number(step_str[1:].strip())
    return Slider(label, **kwargs)

def topping_from_string_image(m):
    path, extension = m.groups()
    return ImageView(path+"."+extension)