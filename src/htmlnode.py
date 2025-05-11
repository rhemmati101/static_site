

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_string = ""
        
        if not self.props:
            return prop_string

        for key, val in self.props.items():
            prop_string += f" {key}=\"{val}\""

        return prop_string

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
