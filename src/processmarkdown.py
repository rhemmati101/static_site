from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from processinlinetext import text_to_textnodes, text_node_to_html_node
from processblocktext import markdown_to_blocks, BlockType, block_to_blocktype

import re


#return parent htmlnode
def markdown_to_html_node(markdown: str) -> ParentNode:
    html_blocks: list[ParentNode] = []

    #split string into blocks
    text_blocks: list[str] = markdown_to_blocks(markdown)

    #for each block, create htmlnode with tag based on blocktype
    for text_block in text_blocks:
        block_type: BlockType = block_to_blocktype(text_block)
        text: str = extract_text(text_block, block_type)
        
        if block_type != BlockType.CODE:
            children: list[HTMLNode] = text_to_children(text, block_type)
            tag: str = get_block_tag(text_block)
            html_block = ParentNode(tag=tag, children=children)
        else:
            inner_block = LeafNode(tag="code", value=text)
            html_block = ParentNode(tag="pre", children=[inner_block])

        html_blocks.append(html_block)

    return ParentNode(tag="div", children=html_blocks)


def extract_text(text_block: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.QUOTE:
            return "\n".join(re.findall(r"^> *([^\n]*)$", text_block, flags=re.MULTILINE))
        case BlockType.CODE:
            return text_block.strip("```").lstrip()
        case BlockType.HEADING:
            match = re.match(r"^#{1,6} +([^\n]*)$", text_block)
            if match:
                return match.group(1)
            raise ValueError("invalid heading block??")
        case BlockType.UNOLIST:
            return "\n".join(re.findall(r"^- +([^\n]*)$", text_block, flags=re.MULTILINE))
        case BlockType.OLIST:
            return "\n".join(re.findall(r"^\d+\. +([^\n]*)$", text_block, flags=re.MULTILINE))
        case BlockType.PARAGRAPH:
            return " ".join(text_block.split("\n"))
        case _:
            raise NotImplementedError()


def text_to_children(text: str, block_type: BlockType) -> list[HTMLNode]:
    children: list[HTMLNode] = []

    if block_type != BlockType.OLIST and block_type != BlockType.UNOLIST:
        children = list(map(text_node_to_html_node, text_to_textnodes(text)))
    else:
        items: list[str] = text.split("\n")
        for item in items:
            item_children = list(map(text_node_to_html_node, text_to_textnodes(item)))
            item_block = ParentNode(tag="li", children=item_children)
            children.append(item_block)

    return children


def get_block_tag(text_block: str) -> str:
    block_type: BlockType = block_to_blocktype(text_block)
    
    match block_type:
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNOLIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            header = re.match(r'^(#+)', text_block)
            if header:
                return f"h{len(header.group(0))}"
            raise Exception("not a valid header?! space-time distortion contradicts contradiction")
        case _:
            raise Exception("no valid block type tag found (or not implemented!!)")