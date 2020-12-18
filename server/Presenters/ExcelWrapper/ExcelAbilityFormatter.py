from Entities.Skill.AbilityEnum import AbilityEnum


class ExcelAbilityFormatter:

    SKILL_NAME_MAPPING = {
        AbilityEnum.SOLUTION_ARCHITECTURE: 'Архитектура решения',
        AbilityEnum.SYSTEM_ANALYSIS: 'Системный анализ',
        AbilityEnum.DEVELOPMENT: 'Разработка',
        AbilityEnum.SYSTEM_TESTING: 'Системное тестирование',
        AbilityEnum.INTEGRATION_TESTING: 'Интеграционное тестирование',
        AbilityEnum.PRODUCT_OWNERSHIP: 'Управление продуктом',
        AbilityEnum.PROJECT_MANAGEMENT: 'Управление проектом'
    }

    def format(self, ability: AbilityEnum):
        return self.SKILL_NAME_MAPPING[ability]
