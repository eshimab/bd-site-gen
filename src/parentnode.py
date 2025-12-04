from htmlnode import HTMLNode



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props
        if self.children and not isinstance(self.children, list):
            self.children = [self.children]

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode class requires a tag")
            return
        if not self.children:
            raise ValueError("ParentNode class requires children")
            return
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        close_tag = f"</{self.tag}>"
        final_string = f"{open_tag}{child_string}{close_tag}"
        return final_string

