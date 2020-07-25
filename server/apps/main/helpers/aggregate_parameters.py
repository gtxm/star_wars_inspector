from django.conf import settings


def parse_parameters(current_parameters):
    aggregate_keys = []
    parameters_settings = []
    for index, header in enumerate(
        settings.STAR_WARS_CHARACTERS_OUTPUT_FILE_HEADER_FIELDS,
    ):
        parameters_settings.append(
            (
                header,
                current_parameters[index] == '1',
                current_parameters[:index] + (
                    '0' if current_parameters[index] == '1' else '1'
                ) + current_parameters[index + 1:],
            ),
        )
        # for each header option we render a triple for the templates
        # (header name, is enabled, toggled settings)
        if current_parameters[index] == '1':
            aggregate_keys.append(header)
    return aggregate_keys, parameters_settings
