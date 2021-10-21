import mitmproxy.http

import sunrise
from sunrise.options import get_file_as_byte
from sunrise.plugin import PluginMenu

mode_menu = PluginMenu("模式")


@mode_menu.checkable_rule_action('淘汰赛模式')
class Fight:
    SWITCH: bool = False

    def switch(self):
        if not hasattr(self, 'SWITCH'):
            self.SWITCH = False

        self.SWITCH = not self.SWITCH
        sunrise.get_engine().refresh()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if "xml/battleStrategy.xml" in flow.request.pretty_url:
            flow.response.content = get_file_as_byte(r"file\fight\battleStrategy.xml")

        if "dll/PetFightDLL_201308.swf" in flow.request.pretty_url and self.SWITCH:
            flow.response.content = get_file_as_byte(r"file/fight/ttsfight.swf")

        elif "dll/PetFightDLL_201308.swf" in flow.request.pretty_url and not self.SWITCH:
            flow.request.url = get_file_as_byte("file/fight/fight.swf")