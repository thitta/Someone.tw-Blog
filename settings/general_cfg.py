from collections import namedtuple
from typing import Iterable

from markdown.extensions.extra import ExtraExtension

# ---------- Template ----------
Button = namedtuple('Button', ['text', 'url', 'target'])

TagConfig = namedtuple(
    typename="TagConfig",
    field_names=["tagName", "propKV"]
)


# ---------- Site Config ----------
class SiteConfig:
    title = "Someone.tw"
    subtitle = "軟體工程／遊戲設計／隨筆"
    image_host = "https://storage.googleapis.com/blog-someone-tw-static/post/"
    buttons = (
        Button(text="Home", url="/", target="_self"),
        Button(text="About", url="/post/1/about", target="_self"),
        Button(text="Copyright", url="/post/2/copyright", target="_self"),
    )


# ---------- Post Parsing Config ----------
class PostParsingConfig:
    tag_configs: Iterable["TagConfig"] = (
        TagConfig(tagName="a", propKV={"target": "_blank"}),
    )
    markdown_exts = (ExtraExtension(),)
