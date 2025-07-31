import sys

from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

from filemanip import copy_directory
from generatesite import generate_page, generate_pages_recursive

def main():
    basepath: str = "/" #default
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)



main()
