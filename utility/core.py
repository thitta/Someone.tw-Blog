from typing import Iterable

from bs4 import BeautifulSoup

from config_module import general_cfg


def customized_html_parse(html_txt: str, tag_configs: Iterable["general_cfg.TagConfig"]) -> str:
    """ append class and property to html tag via BeautifulSoup according to configs)"""
    soup = BeautifulSoup(html_txt, "html.parser")
    for tag_config in tag_configs:
        # find tags
        tags = soup.find_all(tag_config.tagName)
        for tag in tags:
            for key, val in tag_config.propKV.items():
                tag[key] = val
    return soup.__str__()
