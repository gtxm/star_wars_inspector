import os
import pathlib

import petl as etl

from server.apps.main.logic.save_data import save_characters_to_file


def test_save_characters_to_file(settings):
    path_to_test_file = str(
        pathlib.Path().absolute() / 'runtime' / 'test.csv',
    )
    if os.path.exists(path_to_test_file):  # pragma: no cover
        os.remove(path_to_test_file)
    settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS = [
        'name',
    ]
    save_characters_to_file(
        path_to_test_file,
        [
            etl.wrap([
                ['name'],
                ['Test 1'],
                ['Test 2'],
                ['Test 3'],
            ]),
            etl.wrap([
                ['name'],
                ['Test 4'],
                ['Test 5'],
                ['Test 6'],
                ['Test 7'],
                ['Test 8'],
                ['Test 9'],
            ]),
            etl.wrap([
                ['name'],
                ['Test 10'],
            ]),
        ],
    )
    assert list(etl.fromcsv(path_to_test_file).values('name')) == [
        f'Test {i}' for i in range(1, 11)
    ]
    os.remove(path_to_test_file)
