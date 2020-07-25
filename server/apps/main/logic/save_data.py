import logging

import petl as etl
from django.conf import settings

logger = logging.getLogger(__name__)


def save_characters_to_file(generated_file_path, characters_pages):
    etl.setheader(
        etl.empty(),
        settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS,
    ).tocsv(generated_file_path)
    logger.info('Created file: %s', generated_file_path)
    for characters_page in characters_pages:
        etl.appendcsv(
            characters_page,
            generated_file_path,
            write_header=False,
        )
        logger.info('Added data to file: %s', generated_file_path)
