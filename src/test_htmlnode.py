import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode_test_cases import test_suite
from test_helpers import *
from parsers import *
from blocknode import BlockType, BlockNode
from main import *
import re
import json

print(f"=================================================== BEGIN HTMLNODE TEST ===============================================")
class TestHTMLNode(unittest.TestCase):
    def test_0_repr(self): 
        return
        test_function = "test_repr"
        print(f"--------------------------- {test_function} --------------------------")
        test_cases = test_suite[test_function]

        for test_case in test_cases:
            desc, node = test_case
            print(desc)
            print(node)      
            print(f"node.props_to_html(): {node.props_to_html()}")
            print("")
    
        test_function = "test_init"
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        test_cases = test_suite[test_function]

        for test_case in test_cases:
            desc, node, inputs = test_case
            print(desc)
            print(node)

        test_function = "test_leaf"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        test_cases = test_suite[test_function]

        for test_case in test_cases:
            # Unpack test case tuple
            desc, node, inputs = test_case
            test_command_string = create_input_string("LeafNode", inputs)
            if not node.value:
                test_case_string = "All leaf nodes must have a value"
            elif not node.tag:
                test_case_string = node.value
            else:
                props_string = ""
                if node.props:
                    props_string = node.props_to_html()
                test_case_string = f"<{node.tag}{props_string}>{node.value}</{node.tag}>"

            create_report(test_case, test_command_string, test_case_string)
            # Perform Test
            if not node.value:
                with self.assertRaises(ValueError) as context_mgr:
                    node.to_html()
                self.assertEqual(str(context_mgr.exception), test_case_string)
            else:
                self.assertEqual(node.to_html(), test_case_string)


    def test_1_parent(self):
        return
        test_function = "test_parent"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        test_cases = test_suite[test_function]

        for test_case in test_cases:
            desc, node, inputs = test_case
            print(node.to_html())


    def test_2_node_to_html(self):
        test_function = "test_node_to_html"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")

        node = TextNode("This is a text node", TextType.TEXT)
        htmlnode = text_node_to_html(node)
        print(node)
        print(htmlnode)
        node = TextNode("This is a bold node", TextType.BOLD)
        htmlnode = text_node_to_html(node)
        print(node)
        print(htmlnode.to_html())
        node = TextNode("This is a link node", TextType.LINK, "www.linkhere.com")
        htmlnode = text_node_to_html(node)
        print(node)
        print(htmlnode.to_html())
        node = TextNode("This is an image node", TextType.IMAGE, "www.imgurl.com")
        htmlnode = text_node_to_html(node)
        print(node)
        print(htmlnode.to_html())

        ttype = TextType(2)
        print(ttype)
        tnode = TextNode("here are worlds", ttype)
        print(tnode)

    def test_3_split_nodes(self):
        test_function = "test_split_nodes"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")

        node = TextNode("A line with `start code` this is text with a `code block` word and a `end code block` with end txt.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)   
        print(new_nodes)
        print("")

        node = TextNode("A line with **start bold** this is text with a **bold block** word and a **end bold block** with end txt.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)   
        print(new_nodes)
        print("")

        node = TextNode("A line with __start ital__ this is text with a __ital block__ word and a __end bold block__ with end txt.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)   
        print(new_nodes)
        print("")


    def test_4_markdown_img(self):
        test_function = "test_markdown_img"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        
        text_string = "This is text with a ![rick roll](https://image.com) and ![obi wan](https://hellothere.com)"
        alt_text = re.findall("(?<=!\[)(.*?)(?=\])", text_string)
        url_text = re.findall("(?<=\]\()(.*?)(?=\))", text_string)
        #match = re.findall("rick", text_string)
        print(alt_text)
        print(url_text)
        tup_list = list(map(lambda alt, url: (alt, url), alt_text, url_text))
        print(tup_list)



    def test_5_split_links(self):
        test_function = "test_split_links"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        
        node_link = TextNode("This is text with a link [link text](https://www.boot.dev) and a link2 [link2 text](https://www.youtube.com/@dev) end text.", TextType.TEXT)
        node_imgs = TextNode("This is text with an img ![img text](https://www.boot.dev) and a img2 ![img2 text](https://www.youtube.com/@dev) end text.", TextType.TEXT)
        node_both = TextNode("This is text with an img ![img text](https://www.boot.dev) and a link [link text](https://www.youtube.com/@dev) end text.", TextType.TEXT)

        #print(f"{node_link.text}")
        #list_links = split_nodes_link(node_link) 
        #print(list_links)

        #print(f"{node_imgs.text}")
        #list_links = split_nodes_image(node_imgs) 
        #print(list_links)

        print(f"{node_both.text}")
        list_links = split_nodes_links(node_both) 
        print(list_links)

    def test_6_text_to_node(self):
        test_function = "test_text_to_node"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        
        test_text = "This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) the end."

        stringis = re.findall(r"(!)?\[(.*?)\]\((.*?)\)", "hello world")
        print(stringis)
        node_list = TextNode(test_text, TextType.TEXT)
        print("start text:")
        print(f"{test_text}\n")

        node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
        print(f"split_code: {node_list}\n")
        self.assertEqual(len(node_list), 3)
        self.assertEqual(node_list[1].text, "code block")
        node_list = split_nodes_links(node_list)
        print(f"split_images: {node_list}\n")
        self.assertEqual(len(node_list), 7)
        self.assertEqual(node_list[3].text_type, TextType.IMAGE)
        self.assertEqual(node_list[3].text, "obi wan image")
        self.assertEqual(node_list[5].text_type, TextType.LINK)
        self.assertEqual(node_list[5].text, "link")
        node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        print(f"split_italic: {node_list}\n")
        self.assertEqual(len(node_list),9)
        self.assertEqual(node_list[1].text, "italic")
        node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(len(node_list),11)
        self.assertEqual(node_list[1].text, "bold text")
        print(f"split_bold: {node_list}\n")

        node_list2 = text_to_textnodes(test_text)
        print(f"node_list2: {node_list2}\n")
        for i in range(len(node_list)):
            self.assertEqual(node_list[i], node_list2[i])
        

    def test_7_markdown_blocks(self):
        test_function = "test_markdown_blocks"
        print(f"\n\n\n")
        print(f"--------------------------- {test_function} -----------------------------------------------------------------------------\n")
        
        markdown_text = """

#      A header h1 [0]

##     A header h2 [1]

###    A header h3 [2]

####   A header h4 [3]

#####  A header h5 [4]

###### A header h6 [5]

This is another paragraph with _italic text_ and [6]
`**weird _code_ [stuff](to be annoying)` here.
This is the same paragraph on a new line with **bold text**.
We also want ![image links](www.scarymonster.com)
and [regular links](www.normalperson.com) to be thorough.

- This is an **itemized** list [7]
- with `items`
- and a _third thing_
- with an ![image](www.notsketchy.com)
- and a [link](www.yourmom.com)

1. this is an enum [8]
2. list with **bold items**
3. and _italic items_ too
4. and ![enum image](www.stockimages.com)
5. or maybe [links to](www.happyplace.com)




```
this is a code block [9]
with multiple lines
displaying **raw**
_markdown_
with ```` annoying backticks
and [links](www.links.com)
```

> this is a **very poetic** [10]
>     quote block
> where `pen > sword`
> 
> and an empty line for _emphasis_




```py
this is a python code block [11]
with multiple lines
```

```html
this is a html code block [12]
with multiple lines
```

"""

        md_blocks = markdown_to_blocks(markdown_text)

        print(f"\n---- parsing header nodes ----")
        for i in range(6):
            header_block = md_blocks[i]
            header_node = md_block_to_html_node(header_block)
            print(f"header_node:")
            print(header_node)
            header_html = header_node.to_html()
            print(f"header_html:")
            print(header_html)

        print(f"\n---- parsing par node ----")
        par_block = md_blocks[6]
        par_node = md_block_to_html_node(par_block)
        print(f"par_node:")
        print(par_node)
        par_html = par_node.to_html()
        print(f"par_html:")
        print(par_html)
        par_test_string = '<p>This is another paragraph with <i>italic text</i> and [6]\n<code>**weird _code_ [stuff](to be annoying)</code> here.\nThis is the same paragraph on a new line with <b>bold text</b>.\nWe also want <img src="www.scarymonster.com" alt="image links">\nand <a href="www.normalperson.com">regular links</a> to be thorough.</p>'
        self.assertEqual(par_node.to_html(), par_test_string)

        print(f"\n---- parsing item list nodes ----")
        item_block = md_blocks[7]
        item_node = md_block_to_html_node(item_block)
        print(f"item_node")
        print(item_node)
        item_html = item_node.to_html()
        print(f"item_html:")
        print(item_html)
        item_test_string = '<ul><li>This is an <b>itemized</b> list [7]</li><li>with <code>items</code></li><li>and a <i>third thing</i></li><li>with an <img src="www.notsketchy.com" alt="image"></li><li>and a <a href="www.yourmom.com">link</a></li></ul>'
        self.assertEqual(item_node.to_html(), item_test_string)
        #for child in item_html.children:
        #    print(child)

        print(f"\n---- parsing enum list node ----")
        enum_block = md_blocks[8]
        enum_node = md_block_to_html_node(enum_block)
        print(f"enum_html:")
        print(enum_node)
        enum_html = enum_node.to_html()
        print(f"enum_html:")
        print(enum_html)
        enum_test_string = '<ol><li>this is an enum [8]</li><li>list with <b>bold items</b></li><li>and <i>italic items</i> too</li><li>and <img src="www.stockimages.com" alt="enum image"></li><li>or maybe <a href="www.happyplace.com">links to</a></li></ol>'
        self.assertEqual(enum_node.to_html(), enum_test_string)
        #for child in enum_html.children:
        #    print(child)


        print(f"\n---- parsing code node ----")
        code_block = md_blocks[9]
        code_node = md_block_to_html_node(code_block)
        print(f"code_node:")
        print(code_node)
        code_html = code_node.to_html()
        print(f"code_html:")
        print(code_html)
        code_test_string = '<pre><code>this is a code block [9]\nwith multiple lines\ndisplaying **raw**\n_markdown_\nwith ```` annoying backticks\nand [links](www.links.com)</code></pre>'
        self.assertEqual(code_node.to_html(), code_test_string)

        print(f"\n---- parsing quote node ----")
        quote_block = md_blocks[10]
        quote_node = md_block_to_html_node(quote_block)
        print(f"quote_node:")
        print(quote_node)
        quote_html = quote_node.to_html()
        print(f"quote_html:")
        print(quote_html)
        quote_test_string = '<blockquote>this is a <b>very poetic</b> [10]\n    quote block\nwhere <code>pen > sword</code>\n\nand an empty line for <i>emphasis</i></blockquote>'
        self.assertEqual(quote_node.to_html(), quote_test_string)


        print(f"\n---- parsing more code blocks ------")
        code_block = md_blocks[11]
        code_node = md_block_to_html_node(code_block)
        print(f"code_node:")
        print(code_node)
        code_html = code_node.to_html()
        print("code_html:")
        print(code_html)
        code_test_string = '<pre><code>this is a python code block [11]\nwith multiple lines</code></pre>'

        print(f"\n---- parsing more code blocks ------")
        code_block = md_blocks[12]
        code_node = md_block_to_html_node(code_block)
        print(f"code_node:")
        print(code_node)
        code_html = code_node.to_html()
        print("code_html:")
        print(code_html)
        code_test_string = '<pre><code>this is a html code block [12]\nwith multiple lines</code></pre>'


        html_final = md_text_to_html_nodes(markdown_text)
        print(html_final)
        
        print(f"\n=========================================== RUNNING main.py ===========================================\n")

        main()        
           
if __name__=="__main__":
    unittest.main()


