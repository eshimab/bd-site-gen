
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        self_closing_tags = ["img"]
        if not self.value:
            if self.tag and self.tag not in self_closing_tags:
                raise ValueError("All leaf nodes must have a value")
                return 
        if not self.tag:
            return self.value
        if self.tag in self_closing_tags:
            html_string = f"<{self.tag}{self.props_to_html()}>"
        else:
            html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_string

