import re

import mitmproxy.http

from plugin_loader import PluginMenu

plugin_menu = PluginMenu("插件")


@plugin_menu.checkable_rule_action('屏蔽技能特效')
class Effect:
    SWITCH: bool = False

    def __init__(self):
        self.url_pattern: str = r'fightResource/skill/swf/.*.swf'

    def switch(self):
        if not hasattr(self, 'SWITCH'):
            self.SWITCH = False

        self.SWITCH = not self.SWITCH

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if re.search(self.url_pattern, flow.request.url, re.I) and self.SWITCH:
            flow.request.url = r"http://127.0.0.1:8000/10001.swf"


@plugin_menu.checkable_rule_action('精灵变伊优')
class Pet:
    SWITCH: bool = False

    def __init__(self):
        self.url_pattern: str = r'fightResource/pet/swf/((?!3393|3788).)*.swf'

    def switch(self):
        if not hasattr(self, 'SWITCH'):
            self.SWITCH = False

        self.SWITCH = not self.SWITCH

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if re.search(self.url_pattern, flow.request.url, re.I):
            if self.SWITCH:
                flow.request.url = r"http://seer.61.com/resource/fightResource/pet/swf/4.swf"
