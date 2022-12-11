# Pancake Kit

Pancake Kit aims to provide a handy user interface to your Python codes. It provides GUI as a lightweight web app powered by Flask. 

## Installation

```shell
pip3 install pancakekit
```

## Quick Tasting

Assume that there is a function that calculates the n*th* Fibonacci number. In three steps, you can prepare a GUI that wraps this function.

```python
from pancakekit import Pancake

def fibonacci(n=10):
    return (fibonacci(n-1) + fibonacci(n-2)) if n >= 2 else n

cake = Pancake()	# Step 1: Make a Pancake instance.
cake.add(fibonacci)	# Step 2: Add your function to the pancake.
cake.serve()		# Step 3: Serve the cake.
```

When you open `http://127.0.0.1:8000/` in a web browser, you will find an input box for entering `n` and a button that invokes `fibonacci()`.

### Adding toppings

In Pancake Kit, a Pancake instance corresponds to a single web page. Each UI component is added to the pancake as a Topping instance. 

#### Value

```python
cake.add({"a": 0, "b": 1})	# Dictionary -> Multiple inputs

cake.add("a:")		# String ends with ":" -> Value input with the string as a label

cake.add("abc")		# String/Number -> Non-editable text
```

#### Value with @decorator

```python
cake.add("abc@slider(0, 1, 0.1):0.5") # @slider(range_min, range_max, [step])[:value] -> Slider
```

#### Special object

```python
cake.add(image)		# PIL.Image/Path string -> Image view

cake.add(df)		# pandas.DataFrame -> Table
```

#### Function

```python
def f(a, b, c):
	return a * b + c

cake.add(f) # Function -> Multiple inputs & execution button
```

Equivalently, you can decorate the function with a decorator `@cake.topping`:

```python
@cake.topping
def f(a, b, c):
	return a * b + c
```

## Use Pancake Kit in the interactive mode

In the interactive mode, you can perform on-site decoration on your pancake.

```python
# On the Terminal or Command Prompt
from pancakekit import *
cake = Pancake()
cake.serve()
# -> You will find a blank page on http://127.0.0.1:8000/.

d = cake.add({"a": 1, "b":2, "c":3})
# -> A dictionary input appears on the page immediately.

d.value_changed = cake.show_message
# -> As you change the values of the input, you will see a pop-up message.
```

As a shortcut to the instantiation & cake.serve(), you can use MagicPancake. The additional feature of the MagicPancake is that you can access the value of a topping by its name.

```python
from pancakekit import *
cake = MagicPancake()

cake.add("myinput", name="a")
cake.a = 10
cake["a"].value_changed = lambda: cake.show_message(cake.a)
```

More conveniently, execute

```shell
python3 -m pancakekit
```

where the `cake` object and all the toppings in `pancakekit` have already been loaded as local variables.

## How to

### Adding a PancakeKit topping

You can add your favorite toppings to your pancake, as in the following example:

```python
from pancakekit import Pancake, Button, Label

cake = Pancake()
button = cake.add(Button(0))
label = cake.add(Label(1))

def button_click(x):
    button.value = label.value
    label.value += x

button.clicked = button_click

cake.serve()
```

Here, when a `clicked` event is sent to `button_click`, the value of the button is passed as an argument. The value of the topping can be changed by assigning a value to the `value` property.

### Responding to user actions

When a user changes the value of the toppings from the browser, the callback function specified by `topping.value_changed` is invoked. 

```python
from pancakekit import *

cake = Pancake()

dict_input = cake.add({"a": 1, "b": 2, "c": 3})
dict_input.value_changed = lambda: cake.show_message(dict_input.value)

cake.serve()
```

Note that `cake.show_message()` will pop up a message in the browser.

### Accessing a topping by its name

You can access the toppings in the cake by their names.

```python
from pancakekit import *

cake = Pancake()

cake.add(Slider("a", range_min=0, range_max=20), name="slider0")
cake.add(Slider("b", range_min=0, range_max=20), name="slider1")

cake["slider0"].value_changed = lambda x: setattr(cake["slider1"], "value", x+5)
cake["slider1"].value_changed = lambda x: setattr(cake["slider0"], "value", x*2)

cake.serve()
```

## MagicCard

By holding down the shift key and pressing the return key, MagicCard appears with a text box. You can execute the code in the textbox by the command/control key + return. The pancake can be referred to as `cake`. Try the following to see if it actually works.

```python
cake.add(Button("Hi"))
cake(cake.toppings) # In the magic card, the direct call of cake() pops up a message.
```

## Toppings

### Toppings for user interaction

##### `Button(title: str)`

```python
btn = cake.add(Button("Button"))
btn.clicked = lambda x: print(x)
btn.value = "My button"
```

##### `Input(label: str, default=None, placeholder=None)`

```python
myinput = cake.add(Input("input", default=1))
myinput.value_changed = lambda x: print(x)
myinput.value += 1
```

##### `DictInput(input_dict: dict)`

```
dict_input = cake.add(DictInput({"a": 0, "b": 2}))
print(dict_input.value) # -> {"a": 0, "b": 2}
dict_input["a"] = 1
print(dict_input["a"]) # -> 1
dict_input.value_changed = cake.show_message
```

##### `Slider(key: str, range_min: float, range_max: float, value: float=None)`

```python
slider = cake.add(Slider("myslider", range_min=0, range_max=10, value=5))
slider.value_changed = cake.show_message
```

### Toppings for display

##### `Label(text: str)`

##### `Text(text: str)`

##### `Paragraph(text: str)`

##### `ImageView(image: PIL.Image|str)`

- image argument should be PIL.Image or a path to a image file.

##### `ImageCard(image: PIL.Image|str)`

##### `Table(df: pandas.DataFrame)`

### Toppings for arrangement

##### `Row()`

```python
cake = Pancake()
row = cake.add(Row())
my_input = row.add(Input("Input"))
button = row.add(Button("Go!"))
button.clicked = lambda: cake.show_message(my_input.value)
```

##### `Column()`

```python
cake = Pancake()
column = cake.add(Column())
my_input = column.add(Input("Input"))
button = column.add(Button("Go!"))
button.clicked = lambda: cake.show_message(my_input.value)
```

##### `Card()`

Make its content draggable such as ImageCard.

```python
cake = Pancake()
card = cake.add(Card())
row = card.add(Row())
for key in ["a", "b", "c"]:
	row.add(Slider(key, 0, 10))
```

##### `FloatingCard()`

A Card topping floating above other toppings with a classic-style draggable handle.

### Automated toppings

##### `FromFunction(function)`



## Serving multiple pancakes

As you know, a pacanke should be served on a plate. That is,

```python
from pancakekit import *

plate = Plate()

class Crape(Pancake):
	def decorate(self):
		b = self.add(Button("I want to have a waffle!"))
		b.clicked = lambda: plate.go_to("Waffle")
	def show_up(self):
		plate.cake["greediness"].value += 1
    
class Waffle(Pancake):
	def decorate(self):
		b = self.add(Button("I want to have a taiyaki!"))
		b.clicked = lambda: plate.go_to("Taiyaki")
	def show_up(self):
		plate.cake["greediness"].value += 2

class Taiyaki(Pancake):
	def decorate(self):
		b = self.add(Button("I want to have a crape!"))
		b.clicked = lambda: plate.go_to("Crape")
	def show_up(self):
		plate.cake["greediness"].value += 3

Crape(plate)
Waffle(plate)
Taiyaki(plate)
plate.cake.add(Label("Greediness:"))
plate.cake.add(0, name="greediness")
		
plate.serve()
```

When subclassing Pancake, describe the procedure to be performed once when instantiating in the `decorate()`  and the procedure to be performed each time the page is displayed in `show_up()`.

## Making a custom topping

One of the simplest custom topping is as follows:

```python
class MyLabel(Topping):
    def prepare(self, text):
        self.value = text
        style = {"text-shadow": f"1px 1px 1px #bbb"}
        self.label = Tag("label", style = style, value_ref=self)
        
    def html(self):
        return self.label.render()
```

`prepare(self, *args, **kwargs)` is called once when the topping is added to a pancake. `html(self)` returns a HTML string to be rendered. 

Other than `prepare` and `html`, you can override the following methods:

- value_getter(self) -> Any

  This method returns a value of the topping. The default behavior is to return `self._value`.

- value_preprocessor(self, value: Any) ->Any

  This method processes `value` and returns a value to be stored in `self._value`. The default behavior is to return `value`.

- web_value_preprocessor(self, tag: Tag, value: Any) ->Any

  This method processes `value` from the browser input and returns a value to be stored in `self._value`. The default behavior is to return `value`.

- event_preprocessor(self, event: Event)->Any

  This value processes event and returns a value to be passed to an user-defined function. The default behavior is to return `event.value`.

