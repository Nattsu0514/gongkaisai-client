import sunrise
from sunrise.options import setMute, clear_cache
from sunrise.plugin import PluginMenu

base = PluginMenu("菜单")


@base.button_action("刷新")
def refresh():
    sunrise.get_engine().refresh()


@base.button_action("清缓")
def clear_cache():
    clear_cache.start()


@base.checkable_action("静音")
class mute:
    SWITCH: bool = False

    def switch(self):
        setMute(self.SWITCH)
        self.SWITCH = not self.SWITCH

