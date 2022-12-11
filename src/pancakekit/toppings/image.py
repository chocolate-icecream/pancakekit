import io
import base64
import traceback
from PIL import Image as PILImage
from typing import Any
from ..pancakekit import Topping, Tag, Card


class ImageView(Topping):
    def prepare(self, image=None, format="png", max_length=500):
        self.image_base64 = None
        self.format = format
        self.max_length = max_length
        
        if image is not None:
            self.set(image=image)
    
    def set(self, image):
        image_needs_close = False
        byte_image = None
        try:
            if isinstance(image, str): # if the image is given as a file path
                file_path = image
                image = PILImage.open(file_path)
                image_needs_close = True
            elif isinstance(image, bytes): # if the image is given as a binary of png
                byte_image = image
            elif isinstance(image, PILImage.Image):
                pass
            else:
                if self.cake is not None:
                    self.cake.plate.logger.error("Unsupported image input.")
                return
        except Exception:
            if self.cake is not None:
                self.cake.plate.logger.exception(traceback.format_exc())
            return
        if image is None:
            return
        
        try:
            if byte_image is None:
                if self.max_length is not None:
                    try:
                        max_length = max(image.width, image.height)
                        if max_length > self.max_length:
                            scale = self.max_length/max_length
                            image = image.resize((int(image.width*scale), int(image.height*scale)))
                    except Exception:
                        if self.cake is not None:
                            self.cake.plate.logger.exception(traceback.format_exc())
                        return
                buffer = io.BytesIO()
                image.save(buffer, format=self.format.upper())
                byte_image = buffer.getvalue()
            self.image_base64 = base64.b64encode(byte_image).decode("ascii")
        except Exception:
            if self.cake is not None:
                self.cake.plate.logger.exception(traceback.format_exc())
            self.image_base64 = None
        if image_needs_close:
            image.close()
        self.updated()
    
    def html(self):
        params = {"class": "w3-card"}
        if "shadow" in self.arguments and not self.arguments["shadow"]:
            params["class"] = ""
        card = Tag("div", params)
        if self.image_base64 is not None:
            card.add("img", {"src": f"data:image/{self.format.lower()};base64,{self.image_base64}"}, style={"width": "100%"})
        else:
            card.add("img", style={"width": "100%"})
        return card.render()

class ImageCard(Card):
    def prepare(self, *args, **kwargs):
        super().prepare()
        self.imagebox = self.add(ImageView(*args, **kwargs))
    
    def set(self, *args, **kwargs):
        return self.imagebox.set(*args, **kwargs)