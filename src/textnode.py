
from enum import Enum

class TextType(Enum):
    TEXT   = 1
    BOLD   = 2
    ITALIC = 3
    CODE   = 4
    LINK   = 5
    IMAGE  = 6


class TextNode:
    def __init__(self, text, text_type = TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode):
        if self.text == TextNode.text and self.text_type.value == TextNode.text_type.value and self.url == TextNode.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"

