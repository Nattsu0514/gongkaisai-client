from sunrise.rule import RuleManager
RuleManager().new_rule("对战xml", "xml/battleStrategy.xml", r"file\fight\battleStrategy.xml", enable=True)
RuleManager().new_rule("对战面板", "dll/PetFightDLL_201308.swf", r"file/fight/fight.swf", enable=True)

