from django.test import TestCase

from settings.general_cfg import TagConfig
from utility import core as general_utility


class Test(TestCase):
    def test_customized_parse(self):
        html = (
            "<div>"
            "<p></p>"
            "<p></p>"
            "</div>"
        )
        html = "<div><p></p><p></p></div>"
        configs = (TagConfig(tagName="p", propKV={"k1": "v1", "class": "c1 c2"}),)
        exp = (
            "<div>"
            '<p class="c1 c2" k1="v1"></p>'
            '<p class="c1 c2" k1="v1"></p>'
            "</div>"
        )
        act = general_utility.customized_html_parse(html, configs)
        self.assertEqual(exp, act)
