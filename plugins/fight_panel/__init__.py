from sunrise.filter.mitmproxy import FilterRuleManager

FilterRuleManager().new_rule("对战xml", "xml/battleStrategy.xml", r"file\fight\battleStrategy.xml")
FilterRuleManager().new_rule("对战面板", "dll/PetFightDLL_201308.swf", r"file/fight/fight.swf")

