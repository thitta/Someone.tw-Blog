# trim the _sample suffix of this file to run this app

import collections


class SiteConfig:
    Button = collections.namedtuple('Button', ['text', 'url', 'target'])
    title = "Someone Blog"
    subtitle = "For Lightweight & Productive Blogging"
    buttons = (
        Button(text="Home", url="/", target="_self"),
        Button(text="About", url="/post/1/about", target="_self"),
        Button(text="Copyright", url="/post/2/copyright", target="_self"),
    )
    image_host = "http://[mydomain]/[directory]/"
