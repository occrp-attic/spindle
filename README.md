# Spindle

``spindle`` is the web front-end for the [loom](https://github.com/occrp/loom)
graph processing stack. It can be used to search, browse and edit entities that
are stored in a loom-generated statement database.

It is implemented as an AngularJS-based single page application, which requests
data from a Flask-based backend service. Assets are managed via ``bower`` and
compiled using ``webassets``.

Please read the [loom](https://github.com/occrp/loom) introduction before
installing or developing ``spindle``.

## Installation

For spindle to run, you need to first make sure to have a ``loom`` statement
database and ElasticSearch index prepared and for these services to be
accessible from ``spindle``.

You will also need to install the following dependencies:

* ``sass`` (usually installed via ruby gems, ``ruby-sass`` on Debian)
* ``node`` and ``npm`` are needed to install both ``bower`` and ``uglifyjs``

It is recommended to run ``spindle`` inside a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
to separate it's dependencies from the system Python. In that case, you can
install ``spindle`` and it's dependencies like this:

```bash
# If you haven't yet:
$ sudo npm install -g bower uglifyjs
$ sudo apt-get install ruby-sass
# Then, the application itself:
$ git clone git@github.com:occrp/spindle.git
$ cd spindle
$ virtualenv pyenv
$ source pyenv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ bower install
```

You also need to create configuration file to define local settings, such as
database access and the location of the ElasticSearch index:

```bash
$ cp settings.tmpl.py settings.py
# Now edit the settings.py and replace any configuration variables to match
# your local environment.
```

Finally, you can run ``spindle``:

```bash
# If you open a new console, make sure to enter the virtual environment:
$ source pyenv/bin/activate
# Set the path of the configuration file:
$ export SPINDLE_SETTINGS=`pwd`/settings.py
# Run the server:
$ spindle runserver
```

When using ``spindle`` in production, consider using a proper WSGI web server
such as ``gunicorn`` instead of the built-in development server. A
``Dockerfile`` is provided for containerized deployment.

## Running the tests

In order to run the tests, you need to have an instance of ElasticSearch
running and configured in the current spindle configuration. The tests will
create their own index (``spindle_test_idx_``) and destroy it automatically
upon teardown.

Run tests like this:
```bash
$ pip install nose coverage
$ nosetests --with-coverage --cover-package=spindle --cover-erase
```

## License

``spindle`` is free software; it is distributed under the terms of the Affero
General Public License, version 3.
