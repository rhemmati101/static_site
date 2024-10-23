from textnode import TextNode
from textnode import TextType

def main():
    test_node = TextNode("hi", TextType.BOLD, "https://pokemondb.net")

    print(test_node)
    print("worked?")

main()
