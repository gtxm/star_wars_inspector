
"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import pathlib

import pytest


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory):
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings):
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.fixture(autouse=True)
def _templates_debug(settings):
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture()
def _setup_test_api(requests_mock):
    for resource in ['planets', 'people']:
        requests_mock.get(
            f'http://test.com/{resource}/?format=json',
            json={
                'next': f'http://test.com/{resource}/?page=2&format=json',
                'results': [
                    {
                        'name': f'Test {resource} 1',
                        'url': f'http://test.com/{resource}/1/',
                    },
                ],
            },
        )
        requests_mock.get(
            f'http://test.com/{resource}/?page=2&format=json',
            json={
                'next': f'http://test.com/{resource}/?page=3&format=json',
                'results': [
                    {
                        'name': f'Test {resource} 2',
                        'url': f'http://test.com/{resource}/2/',
                    },
                    {
                        'name': f'Test {resource} 3',
                        'url': f'http://test.com/{resource}/3/',
                    },
                ],
            },
        )
        requests_mock.get(
            f'http://test.com/{resource}/?page=3&format=json',
            json={
                'next': None,
                'results': [
                    {
                        'name': f'Test {resource} 4',
                        'url': f'http://test.com/{resource}/4/',
                    },
                ],
            },
        )


@pytest.fixture()
def _setup_mock_api(requests_mock):
    requests_mock.get(
        'https://swapi.dev/api/people/?format=json',
        json={
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': 'Luke Skywalker',
                    'height': '172',
                    'mass': '77',
                    'hair_color': 'blond',
                    'skin_color': 'fair',
                    'eye_color': 'blue',
                    'birth_year': '19BBY',
                    'gender': 'male',
                    'homeworld': 'http://swapi.dev/api/planets/1/',
                    'films': [
                        'http://swapi.dev/api/films/1/',
                        'http://swapi.dev/api/films/2/',
                        'http://swapi.dev/api/films/3/',
                        'http://swapi.dev/api/films/6/',
                    ],
                    'species': [],
                    'vehicles': [
                        'http://swapi.dev/api/vehicles/14/',
                        'http://swapi.dev/api/vehicles/30/',
                    ],
                    'starships': [
                        'http://swapi.dev/api/starships/12/',
                        'http://swapi.dev/api/starships/22/',
                    ],
                    'created': '2014-12-09T13:50:51.644000Z',
                    'edited': '2014-12-20T21:17:56.891000Z',
                    'url': 'http://swapi.dev/api/people/1/',
                },
                {
                    'name': 'C-3PO',
                    'height': '167',
                    'mass': '75',
                    'hair_color': 'n/a',
                    'skin_color': 'gold',
                    'eye_color': 'yellow',
                    'birth_year': '112BBY',
                    'gender': 'n/a',
                    'homeworld': 'http://swapi.dev/api/planets/1/',
                    'films': [
                        'http://swapi.dev/api/films/1/',
                        'http://swapi.dev/api/films/2/',
                        'http://swapi.dev/api/films/3/',
                        'http://swapi.dev/api/films/4/',
                        'http://swapi.dev/api/films/5/',
                        'http://swapi.dev/api/films/6/',
                    ],
                    'species': [
                        'http://swapi.dev/api/species/2/',
                    ],
                    'vehicles': [],
                    'starships': [],
                    'created': '2014-12-10T15:10:51.357000Z',
                    'edited': '2014-12-20T21:17:50.309000Z',
                    'url': 'http://swapi.dev/api/people/2/',
                },
            ],
        },
    )
    requests_mock.get(
        'https://swapi.dev/api/planets/?format=json',
        json={
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': 'Tatooine',
                    'rotation_period': '23',
                    'orbital_period': '304',
                    'diameter': '10465',
                    'climate': 'arid',
                    'gravity': '1 standard',
                    'terrain': 'desert',
                    'surface_water': '1',
                    'population': '200000',
                    'residents': [
                        'http://swapi.dev/api/people/1/',
                        'http://swapi.dev/api/people/2/',
                        'http://swapi.dev/api/people/4/',
                        'http://swapi.dev/api/people/6/',
                        'http://swapi.dev/api/people/7/',
                        'http://swapi.dev/api/people/8/',
                        'http://swapi.dev/api/people/9/',
                        'http://swapi.dev/api/people/11/',
                        'http://swapi.dev/api/people/43/',
                        'http://swapi.dev/api/people/62/',
                    ],
                    'films': [
                        'http://swapi.dev/api/films/1/',
                        'http://swapi.dev/api/films/3/',
                        'http://swapi.dev/api/films/4/',
                        'http://swapi.dev/api/films/5/',
                        'http://swapi.dev/api/films/6/',
                    ],
                    'created': '2014-12-09T13:50:49.641000Z',
                    'edited': '2014-12-20T20:58:18.411000Z',
                    'url': 'http://swapi.dev/api/planets/1/',
                },
            ],
        },
    )


@pytest.fixture()
def test_data_path():
    return str(pathlib.Path(__file__).parent / 'test_data' / 'example.csv')
