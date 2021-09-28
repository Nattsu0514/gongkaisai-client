import mitmproxy.http

import client
from plugin_loader import PluginMenu

mode_menu = PluginMenu("模式")


@mode_menu.checkable_rule_action('淘汰赛模式')
class Fight:
    SWITCH: bool = False

    def switch(self):
        if not hasattr(self, 'SWITCH'):
            self.SWITCH = False

        self.SWITCH = not self.SWITCH
        client.get_engine().refresh()

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url.startswith("http://seer.61.com/dll/PetFightDLL_201308.swf") and self.SWITCH:
            flow.request.url = r"http://127.0.0.1:8000/fight/ttsfight.swf"

        elif flow.request.url.startswith("http://seer.61.com/dll/PetFightDLL_201308.swf") and not self.SWITCH:
            flow.request.url = r"http://127.0.0.1:8000/fight/fight.swf"

        if flow.request.url.startswith("http://seer.61.com/resource/xml/battleStrategy.xml"):
            flow.request.url = r"http://127.0.0.1:8000/fight/battleStrategy.xml"
