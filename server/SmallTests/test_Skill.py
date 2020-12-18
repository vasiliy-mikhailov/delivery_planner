from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Skill.Skill import Skill


def test_skill_holds_attributes():
    skill = Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)

    assert skill.system == 'Foo'
    assert skill.ability == AbilityEnum.DEVELOPMENT