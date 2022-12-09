from pancakekit import Pancake, Button, Label

cake = Pancake()
button = cake.add(Button(0))
label = cake.add(Label(1))

def button_click(x):
    button.value = label.value
    label.value += x
    

button.clicked = button_click

cake.serve()