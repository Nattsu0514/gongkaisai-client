import sunrise
from sunrise.plugin import PluginMenu
from sunrise.util import setMute, clear_cache

base = PluginMenu("菜单")


@base.button_action("刷新")
def refresh():
    sunrise.get_engine().refresh()


@base.button_action("清缓")
def clear():
    clear_cache.start()


@base.checkable_action("静音")
class mute:
    SWITCH: bool = False

    def __call__(self, *args, **kwargs):
        setMute(self.SWITCH)
        self.SWITCH = not self.SWITCH

