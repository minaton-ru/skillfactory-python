class HTML:
    def __init__(self, tag, output=False):
        self.tag = tag
        self.output = output
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.output:
            with open(self.output, "w") as targetfile:
                targetfile.write("<%s>" % self.tag)
                for child in self.children:
                    targetfile.write(str(child))
                targetfile.write("\n</%s>" % self.tag)
        else:
            print("<%s>" % self.tag)
            for child in self.children:
                print(child)
            print("\n</%s>" % self.tag)

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.attributes = {}
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            opening = "\n<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.tag
            return opening + internal + ending
        else:      
            if self.is_single:
                return "\n<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "\n<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text)

# Класс Tag создается с наследованием от класса TopLevelTag
class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

# Если не указать параметр output для объекта класса HTML, то сгенерированный html-код будет выведен на экран, а не в файл
with HTML("html") as html:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head.children.append(title)
            html.children.append(head)
    with TopLevelTag("body") as body:
        body.attributes["class"] = "main-text"
        with Tag("h1") as h1:
            h1.text = "Test"
            h1.attributes["class"] = "main-text"
            body.children.append(h1)
        with Tag("div") as div:
            div.attributes["class"] = "container container-fluid"
            div.attributes["id"] = "lead"
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div.children.append(paragraph)
            with Tag("img", is_single=True) as img:
                img.attributes["src"] = "/icon.png"
                img.attributes["data-image"] = "responsive"
                div.children.append(img)
            body.children.append(div)
    html.children.append(body)