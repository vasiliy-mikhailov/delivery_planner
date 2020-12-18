from Entities.Skill.AbilityEnum import AbilityEnum


class TeamMemberInput:

    def __init__(self, system: str, ability: AbilityEnum, resource_ids_and_or_quantities: [str]):
        if not isinstance(system, str):
            raise ValueError('TeamMemberInput __init__ parameter "system" must be str.')

        if not isinstance(ability, AbilityEnum):
            raise ValueError('TeamMemberInput __init__ parameter "ability" must be AbilityEnum.')

        if not isinstance(resource_ids_and_or_quantities, list):
            raise ValueError('TeamMemberInput __init__ parameter "resource_ids_and_or_quantities" must be list.')

        if any([not isinstance(resource_id_and_or_quantity, str) for resource_id_and_or_quantity in resource_ids_and_or_quantities]):
            raise ValueError('TeamMemberInput __init__ parameter "resource_ids_and_or_quantities" must contain strs only.')

        self.system: str = system
        self.ability: AbilityEnum = ability
        self.resource_ids_and_or_quantities: [str] = resource_ids_and_or_quantities