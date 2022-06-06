from sunrise.plugin import PluginMenu
from sunrise.rule import Rule, RuleManager

plugin_menu = PluginMenu("插件")


@plugin_menu.checkable_rule_action('屏蔽技能特效', Rule(r'fightResource/skill/swf/.*.swf', r"file/10001.swf"))
class Effect:
    name: str

    def __call__(self, *args, **kwargs):
        RuleManager().switch(self.name)
