print("hello world")

from textnode import TextType, TextNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from blocknode import BlockType, BlockNode
import re
import os
import shutil

def text_node_to_html(text_node):
    if text_node.text_type == TextType.TEXT:
        html_node = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        html_node = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        html_node = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        html_node = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        html_node = LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        html_node = LeafNode("img","",{"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("TextType is incorrect")
        return
    return html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        # Get indicies of delimiter
        delim_indicies = [i for i in range(len(old_node.text)) if old_node.text.startswith(delimiter, i)]
        if len(delim_indicies) % 2 != 0:
            raise Warning(f'Delimiter mistach for {old_node}!!')
            new_nodes.append(old_node)
            continue
        # Initialize loop
        i, prev_end = (0, -len(delimiter))
        while i < len(delim_indicies)/2:
            code_beg = delim_indicies[i * 2]
            code_end = delim_indicies[i * 2 + 1]
            if code_beg != 0:
                new_nodes.append(TextNode(old_node.text[prev_end+len(delimiter):code_beg], TextType.TEXT))
            new_nodes.append(TextNode(old_node.text[code_beg+len(delimiter):code_end], text_type))
            # Reset loop
            i, prev_end = (i + 1, code_end)
        if prev_end < len(old_node.text) - len(delimiter):
            #print(f"split_nodes_delimiter: adding final node")
            #print(f"split_nodes_delimiter: start new_nodes = {new_nodes}")
            #print(f"split_nodes_delimiter: old_node.text = {old_node.text}")
            #print(f"split_nodes_delimiter: prev_end = {prev_end} and len(old_node.text) = {len(old_node.text)}")
            new_nodes.append(TextNode(old_node.text[prev_end+len(delimiter):], TextType.TEXT))
            #print(f"split_nodes_delimiter: end new_nodes = {new_nodes}")
    return new_nodes


def split_nodes_links(old_nodes):
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links_list = re.findall(r"(!)?\[(.*?)\]\((.*?)\)", node_text)
        if not links_list:
            new_nodes.append(node)
            continue
        for link_tuple in links_list:
            exmark, alt_text, link_text = link_tuple
            mark = exmark or ""
            link_string = f"{mark}[{alt_text}]({link_text})"
            link_start = node_text.index(link_string)
            link_end = link_start + len(link_string)
            text_type = TextType.LINK
            if exmark == "!":
                text_type = TextType.IMAGE
            if link_start != 0:
                pre_text = node_text[:link_start]
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, text_type, link_text))
            node_text = node_text[link_end:]
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_links(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    return node_list

def markdown_to_blocks(markdown):
    md_split = markdown.split("\n\n")
    md_blocks = list(map(lambda line: line.strip(), md_split))
    md_final = [line for line in md_blocks if line]
    return md_final


def get_md_block_type(md_block):
    if not md_block:
        return BlockType.PAR
    block_lines = md_block.split("\n")
    if block_lines[0].startswith("#"):
        heading_hash = re.findall(r"^#{1,6}\s", block_lines[0])
        if heading_hash:
            return BlockType.HEAD
    if len(block_lines) >= 2:
        if block_lines[0].startswith("```") and block_lines[-1].strip().endswith("```"):
            return BlockType.CODE
    if all(line.strip().startswith(">") for line in block_lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block_lines):
        return BlockType.ITEM_LIST
    if block_lines[0].startswith("1. "):
        block_list = list(map(lambda line: re.match(r"(?<=^)(\d+)(?=\.\s)", line)[0], block_lines))
        block_nums = list(map(lambda block_num: int(block_num), block_list))
        if block_nums == [i for i in range(1,len(block_list) + 1)]:
            return BlockType.ENUM_LIST
    # Otherwise
    return BlockType.PAR

def md_block_to_html_node(md_block):
    print(f"\n========= Parsing md_block =========")
    verb = False
    print(f"verb = {verb}")
    if verb: print(f"Verbose reporting on\n")
    if verb: print(f"Parse Init: md_block:\n{md_block}")
    block_type = get_md_block_type(md_block)
    if verb: print(f"Parse Init: block_type: {block_type}")
    match block_type:
        case BlockType.CODE:
            print(f"------ Parsed As Code -------")
            code_type = re.match(r"```.*\s*\n",md_block)
            code_string = ""
            if code_type:
                code_string = code_type[0][3:]
            block_text = re.sub(r"^```.*\n","",md_block)
            block_text = re.sub(r"```\s*$","",block_text).strip()
            code_node = LeafNode("code", block_text)
            pre_node = ParentNode("pre", code_node)
            return pre_node
    
        case BlockType.QUOTE:
            print(f"------ Parsed As Blockquote -------")
            block_lines = md_block.split("\n")
            block_text = "\n".join(list(map(lambda line: re.sub(r"^\s*>\s?","",line), block_lines)))
            html_node = grow_leaves(block_text, "blockquote")
            return html_node

        case BlockType.PAR:
            print(f"----- Parsed as PAR ------")
            p_node = grow_leaves(md_block, "p")
            return p_node

        case BlockType.HEAD:
            heading_hash = re.match(r"(?<=^)(#{1,6})(?=\s)", md_block)[0]
            header_tag = f"h{len(heading_hash)}"
            header_text = re.sub(r"#{1,6}\s*", "", md_block)
            html_node = LeafNode(header_tag, header_text)
            return html_node
        
        case BlockType.ITEM_LIST:
            print(f"----- Parsed as ITEM_LIST -----")
            html_node = md_block_to_nodes(md_block, r"^-\s", "ul")
            return html_node

        case BlockType.ENUM_LIST:
            print(f"------- Parsed as ENUM_LIST -----")
            html_node = md_block_to_nodes(md_block, r"\d+\.\s", "ol")
            return html_node

def md_block_to_nodes(md_block, sub_string, tag_string):
    md_lines = md_block.split("\n")
    line_nodes = []
    for line in md_lines:
        line_text = re.sub(sub_string,"",line)
        line_node = grow_leaves(line_text, "li")
        line_nodes.append(line_node)
    html_node = ParentNode(tag_string, line_nodes)
    return html_node

def grow_leaves(md_block,tag_string):
    text_nodes = text_to_textnodes(md_block)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_node = text_node_to_html(text_node)
        leaf_nodes.append(leaf_node)
    parent_node = ParentNode(tag_string, leaf_nodes)
    return parent_node


def md_text_to_html_nodes(markdown_text):
    md_blocks = markdown_to_blocks(markdown_text)
    html_nodes = []
    for md_block in md_blocks:
        html_node = md_block_to_html_node(md_block)
        html_nodes.append(html_node)
    div_node = ParentNode("div", html_nodes)
    return div_node



def gather_files(dir_input):
    if not isinstance(dir_input, list):
        dir_input = [dir_input]
    root_dir = "/Users/eshim/bootdev/bd-site-gen"
    target_path = os.path.join(root_dir, *dir_input)
    public_dir = target_path.replace("/static","/public")
    if os.path.exists(public_dir):
        print(f"deleting {public_dir}")
        os.rmdir(public_dir)
    print(f"target_path = {target_path}")
    file_paths = []
    dir_list = list(os.listdir(target_path))
    print(f"dir_list = {dir_list}")
    for dir_item in dir_list:
        print(f"dir_item = {dir_item}")
        new_path = os.path.join(target_path, dir_item)
        print(f"new_path = {new_path}")
        if os.path.isfile(new_path):
            file_paths.append(new_path)
            os.makedirs(public_dir)
            public_path = os.path.join(public_dir, dir_item)
            shutil.copy(new_path, public_path)
        else:
            dir_input = dir_input + [dir_item]
            print(f"dir_input new = {dir_input}")
            file_paths.extend(gather_files(dir_input))
    return file_paths

def send_to_public(file_list):
    static_dir = "/Users/eshim/bootdev/bd-site-gen/static"
    public_dir = "/Users/eshim/bootdev/bd-site-gen/public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    for file_path in file_list:
        target_path = file_path.replace(static_dir, public_dir)
        print(f"copy from {file_path}")
        print(f"copy to   {target_path}")
        shutil.copy(file_path, target_path)
    return






