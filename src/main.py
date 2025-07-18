from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

from filemanip import copy_directory

def main():
    copy_directory("static", "public")


main()
