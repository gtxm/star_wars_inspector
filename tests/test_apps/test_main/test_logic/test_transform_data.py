import petl as etl

from server.apps.main.logic.transform_data import transform_characters_data


def test_transform_characters_data(settings):
    settings.STAR_WARS_CHARACTERS_BASE_FIELDS = ['name']
    url_to_name_map = {
        'http://test.com/planets/1/': 'Test planet 1',
        'http://test.com/planets/2/': 'Test planet 2',
    }
    table = etl.wrap([
        ['name', 'edited', 'homeworld'],
        ['Test 1', '2014-12-09T13:50:51.644000Z', 'http://test.com/planets/1/'],
        ['Test 2', '2014-12-20T21:17:56.891000Z', 'http://test.com/planets/2/'],
    ])
    result = transform_characters_data(
        table,
        url_to_name_map,
    )
    assert list(result.values('name')) == ['Test 1', 'Test 2']
    assert list(result.values('date')) == ['2014-12-09', '2014-12-20']
    assert list(result.values('homeworld')) == [
        'Test planet 1',
        'Test planet 2',
    ]
