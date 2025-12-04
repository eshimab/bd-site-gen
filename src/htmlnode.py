
import json


class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        if self.children: 
            if not isinstance(self.children,list):
                self.children = [self.children]
                print(f"Warning: HTMLNode.__init__: Children not given as list, converting to list with length 1")
            #if not isinstance(self.children[0], HTMLNode):
            #    raise Exception("\n ---> Children must be html nodes")
        
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        if self.props == None or len(self.props) == 0:
            return ""
        for key in list(self.props.keys()):
            value = self.props[key]
            html_string = html_string + f' {key}="{value}"'
        return html_string

    def __repr__(self):
        prop_dict = {
                "tag": self.tag, 
                "value": self.value,
                "children": self.children,
                "props": self.props,
        }
        if self.children:
            children_list = []
            for node in self.children:
                if not isinstance(node, HTMLNode):
                    continue
                if node.tag == None:
                    tag_string = 'null'
                else:
                    tag_string = node.tag
                if node.value == None:
                    val_string = 'null'
                else:
                    val_string = node.value[0:min(10,len(node.value))]
                child_string = f"HTMLNode: <{tag_string}> {val_string}..."
                children_list.append(child_string)
            prop_dict["children"] = children_list
        return json.dumps(prop_dict, sort_keys = False, indent = 2)



