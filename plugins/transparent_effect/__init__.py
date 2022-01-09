import re

import mitmproxy.http

from sunrise.util import get_file_as_byte
from sunrise.plugin import PluginMenu

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

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if re.search(self.url_pattern, flow.request.url, re.I) and self.SWITCH:
            flow.response.content = get_file_as_byte(r"file/10001.swf")
