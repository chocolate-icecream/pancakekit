from pancakekit import Topping, Tag

class Button(Topping):
    def init(self, title):
        self.title = title
        
    def html(self):
        properties = {"class": "button"}
        properties.update(self.attributes)
        button = Tag("button", properties)
        if self.clicked:
            button.set_click_response()
                
        button.add_html(self.title+"!!!")
        return button.render()