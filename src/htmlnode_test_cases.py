

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

test_cases = []
test_suite = {"test_repr": test_cases}


desc = "zero input"
tag = "a"
value = "value"
children = None
props = None
case = ()
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value, no other input provided"
tag = "a"
value = "value"
children = None
props = None
case = (tag, value)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with no props but no children"
tag = "a"
value = "link text"
children = None
props = None
case = (tag, value, children, props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with props but no children"
tag = "a"
value = "link text"
children = None
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, children, props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value and props and fake child string"
tag = "a"
value = "link text"
#children = "fake child"
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value,[], props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value and props and fake child list of strings"
tag = "a"
value = "link text"
#children = ["fake child", "fake jim"]
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, [], props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value and props and list of empty nodes"
tag = "a"
value = "link text"
children = [HTMLNode(), HTMLNode(), HTMLNode()]
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, children, props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value and props and list lightly populated nodws"
tag = "a"
value = "link text"
children = [HTMLNode("a", "wordishere"), HTMLNode("b", "also"), HTMLNode("c", "hello there captain skyward")]
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, children, props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

desc = "a tag with value and props and children initiated with a single node (not a list)"
tag = "a"
value = "link text"
children = HTMLNode("q", "additional text")
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, children, props)
test_function = "test_repr"
# automation
desc_string = "test description: " + desc
test_suite[test_function].append( ( desc_string, HTMLNode(*case) ) )

# -------------------------------------------------------- test_init -----------------------------------------------------------------------
test_suite["test_init"] = []


desc = "initialize HTMLNode"
tag = "a"
value = "link text"
children = HTMLNode("q", "additional text")
props = {
        "href": "www.hithere.fake",
        "color": "#ffffff",
}
case = (tag, value, children, props)
test_function = "test_init"
# automation
desc_string = "test description: " + desc
case_tuple = (desc_string, HTMLNode(*case), case)
test_suite[test_function].append(case_tuple)




# -------------------------------------------------------- test_leaf -----------------------------------------------------------------------

test_suite["test_leaf"] = []

desc = "initiallize leaf node"
tag = "h"
value = "value_h"
case = (tag, value)
# automation
test_function = "test_leaf"
desc_string = desc
case_tuple = (desc_string, LeafNode(*case), case)
test_suite[test_function].append(case_tuple)


desc = "initiallize leaf node with props"
tag = "h"
value = "value_h"
props = {"href": "www.hello.com", "color": "red"}
case = (tag, value, props)
# automation
test_function = "test_leaf"
desc_string = desc
case_tuple = (desc_string, LeafNode(*case), case)
test_suite[test_function].append(case_tuple)



desc = "leaf node without value to test ValueError"
tag = "h"
value = None 
props = {"href": "www.hello.com", "color": "red"}
case = (tag, value, props)
# automation
test_function = "test_leaf"
desc_string = desc
case_tuple = (desc_string, LeafNode(*case), case)
test_suite[test_function].append(case_tuple)



# -------------------------------------------------------- test_parent -----------------------------------------------------------------------
test_function = "test_parent"
test_suite[test_function] = []



desc = "ParentNode initializing with 3x leafs"
tag = "h"
children = [LeafNode("leaf1", "leaf1_text"), LeafNode("leaf2",  "leaf2_text"), LeafNode("leaf3", "leaf3_text")]
props = {"href": "www.hello.com", "color": "red"}
case = (tag, children, props)
# automation
desc_string = desc
case_tuple = (desc_string, ParentNode(*case), case)
test_suite[test_function].append(case_tuple)


desc = "ParentNode initializing with inner parent and leaf"
tag = "h"
grand_children = [LeafNode("leaf1", "leaf1_text"), LeafNode("leaf2",  "leaf2_text"), LeafNode("leaf3", "leaf3_text"), LeafNode("leaf4", "leaf4_text")]
children = [ParentNode("child1", grand_children[0:2]), ParentNode("child2", grand_children[2:4])]
props = {"href": "www.hello.com", "color": "red"}
case = (tag, children, props)
# automation
desc_string = desc
case_tuple = (desc_string, ParentNode(*case), case)
test_suite[test_function].append(case_tuple)



desc = "ParentNode initializing with four total generations"
tag = "h"
grand_children = [LeafNode("leaf1", "leaf1_text"), LeafNode("leaf2",  "leaf2_text"), LeafNode("leaf3", "leaf3_text"), LeafNode("leaf4", "leaf4_text")]
children = [ParentNode("child1", grand_children[0:2]), ParentNode("child2", grand_children[2:4])]
children = [ParentNode("mini_parent", children)]
props = {"href": "www.hello.com", "color": "red"}
case = (tag, children, props)
# automation
desc_string = desc
case_tuple = (desc_string, ParentNode(*case), case)
test_suite[test_function].append(case_tuple)



desc = "ParentNode initializing with four total generations"
tag = "h"
grand_children = [LeafNode("leaf1", "leaf1_text"), LeafNode("leaf2",  "leaf2_text"), LeafNode("leaf3", "leaf3_text"), LeafNode("leaf4", "leaf4_text")]
children = [ParentNode("child1", grand_children[0:2], {"prop1": "propval"}), ParentNode("child2", grand_children[2:4], {"prop2": "propval"})]
children = [ParentNode("mini_parent", children)]
props = {"href": "www.hello.com", "color": "red"}
case = (tag, children, props)
# automation
desc_string = desc
case_tuple = (desc_string, ParentNode(*case), case)
test_suite[test_function].append(case_tuple)

























                    






















                    






















                    






















                    






















                    






















                    






















                    






















                    
