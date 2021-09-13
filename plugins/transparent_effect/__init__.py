import re

import mitmproxy.http

from plugin_loader import checkable_action


@checkable_action('屏蔽技能特效')
class Effect:
    SWITCH: bool = False

    def __init__(self):
        self.url_pattern: str = r'fightResource/skill/swf/.*.swf'

    @classmethod
    def switch(cls) -> bool:
        if not hasattr(cls, 'SWITCH'):
            cls.SWITCH = False

        cls.SWITCH = not cls.SWITCH
        return cls.SWITCH

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if re.search(self.url_pattern, flow.request.url, re.I) and self.SWITCH:
            flow.request.url = r"http://127.0.0.1:8000/10001.swf"

