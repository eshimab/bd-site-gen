print("hello world")

from textnode import TextType, TextNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from blocknode import BlockType
import re
import os
import shutil
from parsers import *
#from dotenv import load_dotenv
#load_dotenv()
#root_dir = os.environ.get("ROOT_DIR")

def main():
    static_list = gather_files("static") 
    print(static_list)
    #send_to_public(static_list)
main()
