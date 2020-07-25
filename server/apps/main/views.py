from functools import partial

import petl as etl
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from server.apps.main.helpers.aggregate_parameters import parse_parameters
from server.apps.main.logic import fetch_data
from server.apps.main.logic.save_data import save_characters_to_file
from server.apps.main.logic.transform_data import transform_characters_data
from server.apps.main.models import StarWarsCollection


@require_http_methods(['GET'])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/collection_list.html', {
        'collections': StarWarsCollection.objects.all(),
    })


@require_http_methods(['POST'])
def create_collection(request: HttpRequest) -> HttpResponse:
    """
    Fetching data from swapi should be moved to celery tasks because:
     - fetching might take a lot time and every request has a timeout
     - a proper retry mechanism can be implemented in case the swapi is not
       available 100% time

    A file might not be the best choice to hold a large amount of data.
    Involving a more suitable NoSQL database like DynamoDB with EMR/Hive
    might be considered instead.
    """
    collection = StarWarsCollection.objects.create()
    url_to_name_map = fetch_data.fetch_planet_url_to_name_map()
    characters_pages = fetch_data.fetch_all_characters_data()
    save_characters_to_file(
        collection.filepath,
        map(
            partial(
                transform_characters_data,
                url_to_name_map=url_to_name_map,
            ),
            characters_pages,
        ),
    )
    return redirect('index')


@require_http_methods(['GET'])
def head_collection(request: HttpRequest, collection_id: int) -> HttpResponse:
    collection = get_object_or_404(StarWarsCollection, id=collection_id)
    more_data = int(request.GET.get('more', 0))
    table = etl.fromcsv(collection.filepath)
    original_size = len(table)
    table = table.head(10 + 10 * more_data)
    return render(
        request,
        'main/collection_head.html',
        {
            'show_more': len(table) < original_size,
            'collection': collection,
            'headers': settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS,
            'data': etl.data(table),
            'more_data': more_data + 1,
        },
    )


@require_http_methods(['GET'])
def aggregate_collection(
    request: HttpRequest,
    collection_id: int,
) -> HttpResponse:
    """
    Value count computations could be also moved into a celery task that
    would prepare the answer for the user and bring it to him later
    (via email or on page with results).
    """
    collection = get_object_or_404(StarWarsCollection, id=collection_id)
    table = etl.fromcsv(collection.filepath)
    aggregate_keys, parameters_settings = parse_parameters(
        request.GET.get(
            'current_parameters',
            '0000001001',
        ),
    )
    if len(aggregate_keys) == 1:  # aggregate does not work correctly
        # if list with 1 element is passed
        aggregate_keys = aggregate_keys[0]
    if len(aggregate_keys) == 0:  # show no table if every option is disabled
        table = etl.empty()
    else:
        table = table.aggregate(key=aggregate_keys, aggregation=len)
    return render(
        request,
        'main/collection_aggregate.html',
        {
            'collection': collection,
            'parameters_settings': parameters_settings,
            'headers': etl.header(table),
            'data': etl.data(table),
        },
    )
