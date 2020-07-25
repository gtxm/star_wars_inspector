import logging

import petl as etl
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def fetch_all_data_by_pages(next_url):
    while next_url:
        logger.info('Fetching %s', next_url)
        response = requests.get(next_url)  # TODO error handling
        logger.info(
            'Fetching time %s: %f',
            next_url,
            response.elapsed.total_seconds(),
        )
        data = response.json()
        next_url = data['next']
        yield data['results']


def fetch_planet_url_to_name_map():
    """
    A naive approach to fetch the planets' names would be to download them via
    the urls provided in the homeworld fields. A better approach would be to
    cache the names in order to avoid making more than one requests to get
    a planet's name.
    However, while playing with the data it seems that almost all the planets
    in the API are connected to a character. That means that it is better to
    use the /planets/ endpoint and get all the planets' names than to hit
    /planets/:id/ endpoint for every planet.
    If the assumption is not valid anymore, the second approach has to be
    used.
    """
    url_to_name_map = {}
    for planets_page in fetch_all_data_by_pages(
        f'{settings.STAR_WARS_API_URL}/planets/?format=json',
    ):
        for planet in planets_page:
            url_to_name_map[planet['url']] = planet['name']
    return url_to_name_map


def fetch_all_characters_data():
    for characters_page in fetch_all_data_by_pages(
        f'{settings.STAR_WARS_API_URL}/people/?format=json',
    ):
        yield etl.fromdicts(
            characters_page,
            header=settings.STAR_WARS_CHARACTERS_INPUT_API_FIELDS,
        )
