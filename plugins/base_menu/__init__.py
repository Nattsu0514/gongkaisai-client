import client
from options import setMute
from plugin_loader import PluginMenu

base = PluginMenu("菜单")


@base.button_action("刷新")
def refresh():
    client.get_engine().refresh()


@base.button_action("清缓")
def clear_cache():
    client.clear_cache.start()


@base.checkable_action("静音")
class mute:
    SWITCH: bool = False

    def switch(self):
        setMute(self.SWITCH)
        self.SWITCH = not self.SWITCH

