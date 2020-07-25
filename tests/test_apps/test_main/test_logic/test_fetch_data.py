from itertools import chain
from unittest.case import TestCase

import pytest

from server.apps.main.logic import fetch_data


@pytest.mark.usefixtures('_setup_test_api')
def test_fetch_all_data_by_pages():
    test_case = TestCase()
    results = list(
        fetch_data.fetch_all_data_by_pages(
            'http://test.com/planets/?format=json',
        ),
    )
    test_case.assertCountEqual(
        [result['name'] for result in chain(*results)],
        [
            'Test planets 1',
            'Test planets 2',
            'Test planets 3',
            'Test planets 4',
        ],
    )


@pytest.mark.usefixtures('_setup_test_api')
def test_fetch_planet_url_to_name_map(settings):
    settings.STAR_WARS_API_URL = 'http://test.com'
    url_to_name_map = fetch_data.fetch_planet_url_to_name_map()
    assert url_to_name_map == {
        'http://test.com/planets/1/': 'Test planets 1',
        'http://test.com/planets/2/': 'Test planets 2',
        'http://test.com/planets/3/': 'Test planets 3',
        'http://test.com/planets/4/': 'Test planets 4',
    }


@pytest.mark.usefixtures('_setup_test_api')
def test_fetch_all_characters_data(settings):
    settings.STAR_WARS_API_URL = 'http://test.com'
    settings.STAR_WARS_CHARACTERS_INPUT_API_FIELDS = [
        'name',
        'url',
    ]
    assert [
        list(
            result.values('name'),
        ) for result in fetch_data.fetch_all_characters_data()
    ] == [
        [
            'Test people 1',
        ],
        [
            'Test people 2',
            'Test people 3',
        ],
        [
            'Test people 4',
        ],
    ]
