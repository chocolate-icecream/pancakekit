import os, ast
import traceback
from typing import Optional, Union, Any
from ..pancakekit import Topping, Tag
from ..utils import get_number, pk_wrapped_dict

class Button(Topping):
    def __init__(self, title:str, style: dict=None, **kwargs):
        super().__init__(title, style, **kwargs)
        self.clicked = lambda :None

    def prepare(self, title, style):
        self.value = title
        properties = {"class": "button"}
        
        base_style = {}
        if style is not None:
            base_style.update(style)
        self.button = Tag("button", properties, style=base_style, value_ref=self)
        
    def html(self):
        self.button.set_click_response()    
        return self.button.render()

    def event_preprocessor(self, event):
        if event.event_type == "onclick":
            return self.value
    
    def set_title(self, title):
        self.value = title

    @property
    def title(self):
        return self.value
    
    @title.setter
    def title(self, value):
        self.set_title(value)

class Label(Topping):
    def __init__(self, text: str="", style: dict=None, **kwargs):
        super().__init__(text, style, **kwargs)

    def prepare(self, text: str, style: dict):
        if style is None:
            style = {"text-shadow": f"1px 1px 1px #bbb"}
        self.value = text
        self.label = Tag("label", style=style, value_ref=self)
        
    def html(self):
        return self.label.render()

class Text(Topping):
    def __init__(self, text="", align: str=None, shadow: int=None, shadow_blur: int=None, style: dict=None, **kwargs):
        super().__init__(text, align, shadow, shadow_blur, style, **kwargs)

    def prepare(self, text="", align=None, shadow=None, shadow_blur=None, style=None):
        self.value = text
        if style is None:
            style = {}
        if align is not None:
            style["text-align"] = align
        if shadow is not None:
            shadow_blur = shadow if shadow_blur is None else shadow_blur
            style["text-shadow"] = f"{shadow}px {shadow}px {shadow_blur}px #bbb"
        self.div = Tag("div", style=style, value_ref=self)
        
    def html(self):
        return self.div.render()

class Paragraph(Topping):
    def __init__(self, text: str="", style: dict=None, **kwargs):
        super().__init__(text, style, **kwargs)

    def prepare(self, text: str, style: dict):
        if style is None:
            style = {}
        self.value = text
        self.p = Tag("p", style=style)

    def html(self):
        return self.p.render()
    

class Input(Topping):
    def __init__(self, label: Optional[str]=None, default: Union[str, int, float]=None, placeholder: Any=None, **kwargs):
        super().__init__(label=label, default=default, placeholder=placeholder, **kwargs)

    def prepare(self, label, default, placeholder):
        self.value_type = type(default)
        self.label = label
        self.value = default if default is not None else ""
        if placeholder is None:
            placeholder = default
        style = {"max-width": "12em", "padding-bottom":"2px", "padding-top":"2px"}
        self.user_input = Tag("input", {"class": "w3-input w3-border w3-round-large", "type": "text", "placeholder": placeholder}, value_ref=self)
        self.user_input.style = style

    def html(self):
        div = Tag("div", style={"display": "flex", "flex-flow": "column"})
        if self.label is not None:
            label = div.add("div", {"class": "w3-left w3-small w3-monospace"})
            label.add_html(self.label)
        div.add(self.user_input)
        return div.render()
    
    def value_getter(self):
        if self.value_type is type(None):
            return get_number(self._value)
        try:
            return self.value_type(self._value)
        except:
            pass
        return self._value

class Slider(Topping):
    def __init__(self, label:str, range_min:float, range_max:float, value:Optional[float]=None, step: float=1.0, **kwargs):
        super().__init__(label, range_min, range_max, value=value, step=step, **kwargs)

    def prepare(self, label, range_min, range_max, value=None, step=1.0):
        self.label_str = label
        self.value_display_func = None
        self.ranges = (range_min, range_max, step)
        if value is None:
            value = self.ranges[0]
        
        self.label = self.add(Label(self.label_str))
        self.user_input = Tag("input", {"type": "range"}, style={"width":"100%"}, value_ref=self)
        
        self.set_value(value, skip_update=True)
        
    def html(self):
        div = Tag("div")
        label = div.add("div", {"class": "w3-left w3-small w3-monospace"})
        label.add_html(self.children_html)
        self.user_input.properties["min"] = self.ranges[0]
        self.user_input.properties["max"] = self.ranges[1]
        self.user_input.properties["step"] = self.ranges[2]
        div.add(self.user_input)
        return div.render()
    
    def value_preprocessor(self, value):
        label_str = self.label_str +": "
        label_str += str(self.value_display_func(value) if self.value_display_func is not None else value)
        self.label.value =  label_str
        return value
    
    def value_getter(self):
        return get_number(self._value)
            
    @property
    def display(self):
        return self.value_display_func
    
    @display.setter
    def display(self, func):
        self.value_display_func = func
        if self.value is not None:
            self.set_value(self.value, force_update=True)

class DictInput(Topping):
    def __init__(self, default:dict, horizontal:bool=False, **kwargs):
        super().__init__(default, horizontal=horizontal, **kwargs)

    def prepare(self, default:dict, horizontal:bool=False):
        self.horizontal = horizontal
        self.input_dict = {}
        self._set(default)

    def _set(self, d):
        if not isinstance(d, dict):
            return
        if not self.horizontal:
            grid = self.add(Row(centering=False, padding=False))
        else:
            grid = self.add(Column())
        for key, value in d.items():
            label = key.replace("_", " ").capitalize() if len(key) > 1 else key
            self.input_dict[key] = grid.add(Input(label, value, _dict_input_key=key))

    def html(self):
        border = "" if len(self.input_dict) <= 2 or self.horizontal else ' w3-border w3-round-large'
        div = Tag("div", {"class": f"w3-container{border}"}, style={"width": "fit-content", "padding-bottom":"6px", "margin": "5px"})
        div.add_html(self.children_html)
        return div.render()

    def items(self):
        return self.value.items()

    def converted_dict(self):
        return {k: self[k] for k in self.input_dict.keys()}
    
    def value_preprocessor(self, d:dict):
        for key, value in d.items():
            if key in self.input_dict:
                self.input_dict[key].value = value
        return None # to prevent value substitution

    def value_getter(self):
        def setitem_callback(key, value):
            self.__setitem__(key, value)
        return pk_wrapped_dict(setitem_callback, {key:self[key] for key in self.input_dict.keys()})
    
    def event_preprocessor(self, event):
        if event.event_type == "value_changed" and event.origin is not None:
            return (event.origin.arguments["_dict_input_key"], event.value)

    def __getitem__(self, key):
        if key not in self.input_dict:
            return
        try:
            return ast.literal_eval(self.input_dict[key].value)
        except:
            return self.input_dict[key].value

    def __setitem__(self, key, value):
        if key not in self.input_dict:
            return
        self.input_dict[key].value = value
    
    def __str__(self):
        return_str = ""
        for key, item in self.input_dict.items():
            return_str += f"{key}:{item.value}" + os.linesep
        return return_str

class Column(Topping):
    def __init__(self, toppings:list[Topping]=[], padding:bool=True, **kwargs):
        super().__init__(toppings, padding, **kwargs)

    def prepare(self, toppings, padding):
        self.padding = padding
        for topping in toppings:
            self.add(topping)
        
    def html(self):
        css = "w3-row-padding" if self.padding else "w3-row"
        row = Tag("div", {"class": "w3-row-padding"})
        space = 12//len(self.child_htmls)
        for child in self.child_htmls:
            column = row.add("div", {"class": f"w3-col s{space} w3-center"})
            column.add_html(child)
        return row.render()

class Row(Topping):
    def __init__(self, toppings:list[Topping]=[], centering:bool=True, padding:bool=True, **kwargs):
        super().__init__(toppings, centering, padding, **kwargs)
        
    def prepare(self, toppings, centering, padding):
        self.centering = centering
        self.padding = padding
        for topping in toppings:
            self.add(topping)
        
    def html(self):
        css = "w3-col"
        if self.centering:
            css += " w3-center"
        column = Tag("div", {"class": css})
        css = "w3-row"
        if self.padding:
            css += " w3-margin-bottom"
        for child in self.child_htmls:
            row = column.add("div", {"class": css})
            row.add_html(child)
        return column.render()