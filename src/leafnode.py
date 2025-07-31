from htmlnode import HTMLNode
from textnode import TextNode
from textnode import TextType

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("Leaf node must have a value")
        if self.tag == None:
            return self.value
        if self.props:
            if "href" in self.props:  #link
                return f'<a href="{self.props["href"]}"{self.value}</a>'
            elif "src" in self.props:  #image
                return f'<img src="{self.props["src"]}" alt="{self.props["alt"]}" />'
        return f"<{self.tag}>{self.value}</{self.tag}>"
        

