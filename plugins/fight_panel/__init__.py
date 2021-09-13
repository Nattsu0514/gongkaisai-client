import mitmproxy.http

from plugin_loader import checkable_action


@checkable_action('淘汰赛模式')
class Fight:
    SWITCH: bool = False

    @classmethod
    def switch(cls) -> bool:

        if not hasattr(cls, 'SWITCH'):
            cls.SWITCH = False

        cls.SWITCH = not cls.SWITCH
        return cls.SWITCH

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url.startswith("http://seer.61.com/dll/PetFightDLL_201308.swf"):
            if self.SWITCH:
                flow.request.url = r"http://127.0.0.1:8000/fight/ttsfight.swf"
                return

            else:
                flow.request.url = r"http://127.0.0.1:8000/fight/fight.swf"


        if flow.request.url.startswith("http://seer.61.com/resource/xml/battleStrategy.xml"):
            flow.request.url = r"http://127.0.0.1:8000/fight/battleStrategy.xml"
            return
