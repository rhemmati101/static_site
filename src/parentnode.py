from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node requires a tag")
        if self.children == None:
            raise ValueError("Parent node requires a list of children")
        
        children_in_html: str = ""
        for child in self.children:
            children_in_html += child.to_html()
        
        return f"<{self.tag}>{children_in_html}</{self.tag}>"