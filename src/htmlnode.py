class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            ret = []
            for prop in self.props:
                ret.append(prop + '="' + self.props[prop] + '"')
            return ' '.join(ret)
        return ''

    def __repr__(self):
        text = ''
        if self.value:
            text += self.value
        if self.children and len(self.children) > 0:
            for child in self.children:
                text += child.__repr__()
        if self.tag:
            text = f"<{' '.join([self.tag, self.props_to_html()]).strip()}>{text}</{self.tag}>"
        return text


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        text = ''
        if self.value:
            text += self.value
        if self.tag:
            text = f"<{' '.join([self.tag, self.props_to_html()]).strip()}>{text}</{self.tag}>"
        return text

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(children=children, tag=tag, props=props, value=None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag not provided. ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("no children provided. ParentNode must have at least one child")

        return f"<{' '.join([self.tag, self.props_to_html()]).strip() }>{''.join([child.to_html() for child in self.children])}</{self.tag}>"


