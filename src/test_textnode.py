import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, "www.helloworld.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "www.helloworld.com")
        self.assertEqual(node1, node2)

    def test_eq_with_url_none(self):
        node1 = TextNode("This is text", TextType.LINK, None)
        node2 = TextNode("This is text", TextType.LINK)
        self.assertEqual(node1, node2)
    
    def test_not_eq(self):
        node1 = TextNode("hi", TextType.LINK, None)
        node2 = TextNode("hi", TextType.LINK, "www.helloworld.com")
        self.assertNotEqual(node1, node2)

if __name__=="__main__":
    unittest.main()
