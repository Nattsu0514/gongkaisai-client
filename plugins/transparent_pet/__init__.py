import mitmproxy.http
import re
from plugin_loader import checkable_action


@checkable_action('精灵变伊优')
class Pet:
    SWITCH: bool = False

    def __init__(self):
        self.url_pattern: str = r'fightResource/pet/swf/((?!3393|3788).)*.swf'

    @classmethod
    def switch(cls) -> bool:

        if not hasattr(cls, 'SWITCH'):
            cls.SWITCH = False

        cls.SWITCH = not cls.SWITCH
        return cls.SWITCH

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if re.search(self.url_pattern, flow.request.url, re.I):
            if self.SWITCH:
                flow.request.url = r"http://seer.61.com/resource/fightResource/pet/swf/4.swf"

