import os
from unittest import mock
from unittest.case import TestCase

import pytest
from django.urls import reverse

from server.apps.main.models import StarWarsCollection

pytestmark = pytest.mark.django_db


def test_index(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert list(response.context['collections']) == []

    StarWarsCollection.objects.create()
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert list(
        response.context['collections'],
    ) == list(StarWarsCollection.objects.all())


@pytest.mark.usefixtures('_setup_mock_api')
def test_create_collection(client):
    assert list(StarWarsCollection.objects.all()) == []
    response = client.post(reverse('main:create_collection'), {})
    assert response.status_code == 302
    assert len(StarWarsCollection.objects.all()) == 1
    os.remove(StarWarsCollection.objects.all()[0].filepath)


def test_head_collection(client, test_data_path):
    star_wars_collection = StarWarsCollection.objects.create()
    with mock.patch(
        'server.apps.main.models.StarWarsCollection.filepath',
        new_callable=mock.PropertyMock,
    ) as filepath_mock:
        filepath_mock.return_value = test_data_path
        response = client.get(
            reverse(
                'main:head_collection',
                kwargs={
                    'collection_id': star_wars_collection.id,
                },
            ),
        )
    assert response.status_code == 200
    assert response.context['show_more']
    assert response.context['more_data'] == 1
    assert len(response.context['data']) == 10

    with mock.patch(
        'server.apps.main.models.StarWarsCollection.filepath',
        new_callable=mock.PropertyMock,
    ) as filepath_mock:
        filepath_mock.return_value = test_data_path
        response = client.get(
            reverse(
                'main:head_collection',
                kwargs={
                    'collection_id': star_wars_collection.id,
                },
            ),
            data={
                'more': 1,
            },
        )
    assert response.status_code == 200
    assert not response.context['show_more']
    assert len(response.context['data']) == 14


def test_aggregate_collection(client, test_data_path):
    test_case = TestCase()
    star_wars_collection = StarWarsCollection.objects.create()
    with mock.patch(
        'server.apps.main.models.StarWarsCollection.filepath',
        new_callable=mock.PropertyMock,
    ) as filepath_mock:
        filepath_mock.return_value = test_data_path
        response = client.get(
            reverse(
                'main:aggregate_collection',
                kwargs={
                    'collection_id': star_wars_collection.id,
                },
            ),
            data={
                'current_parameters': '0000000000',
            },
        )
    assert response.status_code == 200

    with mock.patch(
        'server.apps.main.models.StarWarsCollection.filepath',
        new_callable=mock.PropertyMock,
    ) as filepath_mock:
        filepath_mock.return_value = test_data_path
        response = client.get(
            reverse(
                'main:aggregate_collection',
                kwargs={
                    'collection_id': star_wars_collection.id,
                },
            ),
            data={
                'current_parameters': '0000000001',
            },
        )
    assert response.status_code == 200
    test_case.assertCountEqual(
        list(response.context['data']),
        [
            ('Tatooine', 8),
            ('Naboo', 1),
            ('Alderaan', 1),
            ('Stewjon', 1),
            ('Eriadu', 1),
            ('Kashyyyk', 1),
            ('Corellia', 1),
        ],
    )

    with mock.patch(
        'server.apps.main.models.StarWarsCollection.filepath',
        new_callable=mock.PropertyMock,
    ) as filepath_mock:
        filepath_mock.return_value = test_data_path
        response = client.get(
            reverse(
                'main:aggregate_collection',
                kwargs={
                    'collection_id': star_wars_collection.id,
                },
            ),
        )
    assert response.status_code == 200
    for year, planet, value in response.context['data']:
        assert value == (2 if planet == 'Tatooine' and year == '41.9BBY' else 1)
