from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNOLIST = "unordered list"
    OLIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    
    text_lines: list[str] = markdown.split("\n\n")
    
    #remove whitespace and extra empty lines
    blocks = list(filter(lambda line: line != "", map(lambda text: text.strip(), text_lines)))

    return blocks

def block_to_blocktype(block: str) -> BlockType:
    if re.match(r"^#{1,6} +[^\n]*$", block):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNOLIST
    
    if all(re.match(r"^\d+\. ", line) for line in block.split("\n")):
        #oh boy is this convoluted!
        nums: list[str] = re.findall(r"^(\d+)\. ", block, flags=re.MULTILINE)
        if all(nums[i] == str(i + 1) for i in range(len(nums))):
            return BlockType.OLIST

    return BlockType.PARAGRAPH