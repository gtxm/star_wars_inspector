from unittest.case import TestCase

from server.apps.main.helpers.aggregate_parameters import parse_parameters


def test_parse_parameters(settings):
    test_case = TestCase()
    settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS = [
        'name',
        'height',
        'mass',
        'hair_color',
        'skin_color',
        'eye_color',
        'birth_year',
        'gender',
        'date',
        'homeworld',
    ]
    all_enabled = '1111111111'
    keys, parameters_settings = parse_parameters(all_enabled)
    test_case.assertCountEqual(
        keys,
        settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS,
    )
    for i, (header, enabled, toggled) in enumerate(parameters_settings):
        assert header in settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS
        assert enabled
        assert toggled[i] == '0'
    all_disabled = '0000000000'
    keys, parameters_settings = parse_parameters(all_disabled)
    assert keys == []
    for i, (header, enabled, toggled) in enumerate(parameters_settings):
        assert header in settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS
        assert not enabled
        assert toggled[i] == '1'
    some_enabled = '1001011100'
    chosen_parameters = [
        'name',
        'hair_color',
        'eye_color',
        'birth_year',
        'gender',
    ]
    missing_parameters = [
        'height',
        'mass',
        'skin_color',
        'date',
        'homeworld',
    ]
    keys, parameters_settings = parse_parameters(some_enabled)
    test_case.assertCountEqual(keys, chosen_parameters)
    for i, (header, enabled, toggled) in enumerate(parameters_settings):
        if some_enabled[i] == '1':
            assert header in chosen_parameters
            assert header not in missing_parameters
            assert toggled[i] == '0'
            assert enabled
        else:
            assert header not in chosen_parameters
            assert header in missing_parameters
            assert toggled[i] == '1'
            assert not enabled
