from django.core.exceptions import ValidationError


def hex_validator(value):
    """Валидатор для поля color (Цвет в HEX) модели Tag.

    Args:
        value (color): str

    Raises:
        ValidationError: HEX строка должна начинаться с "#"!
        ValidationError: Некорректная длина HEX строки!
        ValidationError: Некорректный символы в HEX строке!
    """
    HEX = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
        'e', 'f'
    ]

    if value[0] != '#':
        raise ValidationError('HEX строка должна начинаться с "#"!')

    value = value.lower().lstrip('#')
    if len(value) != 6 and len(value) != 3:
        raise ValidationError('Некорректная длина HEX строки!')

    for item in value:
        if item not in HEX:
            raise ValidationError('Некорректный символы в HEX строке!')
