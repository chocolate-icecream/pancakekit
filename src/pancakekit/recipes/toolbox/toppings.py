from pancakekit import *

class ToolBox(FloatingCard):
    topping_list = ["Button", "Input", "Label"]
    def prepare(self):
        super().prepare()
        row = self.add(Row(padding=False))
        for topping in self.topping_list:
            button = row.add(Button(topping))
            button.clicked = self.make
    
    def make(self, class_name, cake):
        if class_name in globals():
            new_topping = cake.add(globals()[class_name](class_name))
            show_message(f"{class_name} {new_topping.name} is created.")
