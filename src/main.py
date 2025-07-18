from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

from filemanip import copy_directory
from generatesite import generate_page

def main():
    copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")



main()
