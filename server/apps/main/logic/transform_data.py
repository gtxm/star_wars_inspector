from collections import OrderedDict

import petl as etl
from django.conf import settings


def transform_characters_data(characters_page, url_to_name_map):
    transformations = OrderedDict()
    for field in settings.STAR_WARS_CHARACTERS_BASE_FIELDS:
        transformations[field] = field
    transformations['date'] = 'edited', lambda v: v[:10]  # the width of the
    # date is always the same
    transformations['homeworld'] = 'homeworld', lambda v: url_to_name_map[v]
    return etl.fieldmap(characters_page, transformations)
