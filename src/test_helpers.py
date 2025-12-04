from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def create_input_string(func_name, input_tuple):
    input_strings = []
    for item in input_tuple:
        if isinstance(item, HTMLNode) or isinstance(item, LeafNode) or isinstance(item, ParentNode):
            input_add = f"'{type(item)}'"
        elif isinstance(item, str):
            input_add = f'"{item}"'
        else:
            input_add = f'{item}'
        input_strings.append(input_add)
    input_case_string = "(" + ", ".join(input_strings) + ")"
    test_command_string = func_name + input_case_string
    return test_command_string


def create_report(test_case_tuple, test_command_string, test_case_string):
    desc, node, inputs = test_case_tuple
    print(f"test description: {desc}")
    print(f"test command:     {test_command_string}")
    print(f"output type:      {type(node)}")
    print(f"object fields:    {list(node.__dict__.keys())}")
    print(f"object props:     {node.__dict__}")
    print(f"test_case_string: {test_case_string}")
    print("")


