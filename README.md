# star_wars_inspector

Star Wars Inspector

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [63b4d78db15add4dbc9b37cb631571c7c7f40854](https://github.com/wemake-services/wemake-django-template/tree/63b4d78db15add4dbc9b37cb631571c7c7f40854). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/63b4d78db15add4dbc9b37cb631571c7c7f40854...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services) 
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Prerequisites

You will need:

- `python3.7` (see `pyproject.toml` for full version)

## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`


## Documentation

To setup the environment, please create a virtualenv for the project.

Then run:

`pip3 install poetry`
`poetry install`

In order to launch the application from the root of the project, run:

`python3 manage.py migrate`

`python3 manage.py runserver`
