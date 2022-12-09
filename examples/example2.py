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

plate.cake.add(Label("Greediness:"))
plate.cake.add(0, name="greediness")
Crape(plate)
Waffle(plate)
Taiyaki(plate)
		
plate.serve()