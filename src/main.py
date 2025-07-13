from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("hi", TextType.BOLD, "https://pokemondb.net")
    html_node = HTMLNode("hey")

    print(f"test text node: {text_node}")
    print(f"test html node: {html_node}")
    print("worked?")


main()
