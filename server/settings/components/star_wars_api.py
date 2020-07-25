STAR_WARS_API_URL = 'https://swapi.dev/api'
STAR_WARS_CHARACTERS_BASE_FIELDS = [
    'name',
    'height',
    'mass',
    'hair_color',
    'skin_color',
    'eye_color',
    'birth_year',
    'gender',
]
STAR_WARS_CHARACTERS_INPUT_API_FIELDS = STAR_WARS_CHARACTERS_BASE_FIELDS + [
    'homeworld',
    'edited',
]
STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS = STAR_WARS_CHARACTERS_BASE_FIELDS + ['date', 'homeworld']  # noqa
