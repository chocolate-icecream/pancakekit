from ..pancakekit import Topping, Tag
from .basic import DictInput, Row, Column, Button, Input, Text
import inspect
import functools
from types import LambdaType


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
        button = self.add(Button(title))
        button.clicked = self.call_function
    
    def call_function(self):
        result = self.function(**self.value)
        if result is not None:
            self.cake.show_message(result)

def topping_from_object(obj):
    if isinstance(obj, dict):
        return DictInput(obj)
    if isinstance(obj, str):
        return Input(obj)
    if isinstance(obj, (float, int)):
        return Text(obj, shadow=1, shadow_blur=1)
    if inspect.isfunction(obj):
        return FromFunction(obj)