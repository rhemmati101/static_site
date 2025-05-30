from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode

import re


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT.value:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD.value:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC.value:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.CODE.value:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.LINK.value:
            return LeafNode(tag="a",value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE.value:
            return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception(f"{text_node.text_type} is not a supported text type")
        
def split_nodes_delimiter(
        old_nodes: list[HTMLNode], delimiter: str, text_type: TextType
        ) -> list[HTMLNode]:
    new_nodes: list[HTMLNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            split_nodes: list[str] = node.text.split(delimiter)
            if len(split_nodes) == 1: #case: no delims in text
                new_nodes.append(node)
            elif len(split_nodes) == 2: #case: 1 delim? not valid markdown
                raise Exception(f"missing matching delimiter")
            elif len(split_nodes) == 3: #case: 2 delims, expected input!
                new_nodes.extend([
                    TextNode(text=split_nodes[0], text_type=TextType.TEXT),
                    TextNode(text=split_nodes[1], text_type=text_type),
                    TextNode(text=split_nodes[2], text_type=TextType.TEXT)
                ])
            else:
                raise NotImplementedError() #what amazing casework!!!
            
    return new_nodes
            
def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[HTMLNode]) -> list[HTMLNode]:
    new_nodes: list[HTMLNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            txt = node.text
            images: list[tuple[str,str]] = extract_markdown_images(txt)
            if not images:
                new_nodes.append(node)
            else:
                for image in images:
                    img_txt = f"![{image[0]}]({image[1]})"
                    split: list[str] = txt.split(img_txt)

                    # at this point, split should be len 3 with [pre, split, post]
                    # pre and post can be "", which we don't want to turn into a node

                    if split[0] != "":
                        new_nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))

                    new_nodes.append(TextNode(text=image[0],text_type=TextType.IMAGE,url=image[1]))
                    
                    txt = split[1]
                
                if txt != "":    #don't create a new textnode after an image ends the text
                    new_nodes.append(TextNode(text=txt,text_type=TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[HTMLNode]) -> list[HTMLNode]:
    new_nodes: list[HTMLNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            txt = node.text
            links: list[tuple[str,str]] = extract_markdown_links(txt)
            if not links:
                new_nodes.append(node)
            else:
                for link in links:
                    link_txt = f"[{link[0]}]({link[1]})"   #can fail if there is img w same attributes
                    split: list[str] = txt.split(link_txt)

                    # at this point, split should be len 3 with [pre, split, post]
                    # pre and post can be "", which we don't want to turn into a node

                    if split[0] != "":
                        new_nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))

                    new_nodes.append(TextNode(text=link[0],text_type=TextType.LINK,url=link[1]))
                    
                    txt = split[1]
                
                if txt != "":    #don't create a new textnode after an image ends the text
                    new_nodes.append(TextNode(text=txt,text_type=TextType.TEXT))

    return new_nodes


              

    