sprockets.mixins.statsd
=======================
The ``RequestMetricsMixin`` mixin will automatically instrument requests by
sending statsd increment and timing values as each request finishes.

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
sprockets.mixins.statsd is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.mixins.statsd>`_
and can be installed via ``pip`` or ``easy_install``:

.. code:: bash

  pip install sprockets.mixins.statsd

Documentation
-------------
https://sprocketsmixinsstatsd.readthedocs.org

Requirements
------------
-  `sprockets.client.statsd <https://github.com/sprockets/sprockets.client.statsd>`_

Example
-------
The following ``RequestHandler`` will automatically increment a request counter
and add a request duration timing value to statsd when the request finishes.

.. code:: python

    from sprockets.handlers.mixins import statsd
    from tornado import web

    class MyRequestHandler(stats.RequestMetricsMixin,
                           web.RequestHandler):

        def get(self, *args, **kwargs):
            self.finish({'hello': 'world'})

When the request has finished, the following keys would be used:

- Counter: ``sprockets.counter.example.RequestHandler.GET.200``
- Timing: ``sprockets.timers.example.RequestHandler.GET.200``

Version History
---------------
Available at https://sprocketsmixinsstatsd.readthedocs.org/en/latest/history.html

.. |Version| image:: https://badge.fury.io/py/sprockets.mixins.statsd.svg?
   :target: http://badge.fury.io/py/sprockets.mixins.statsd

.. |Status| image:: https://travis-ci.org/sprockets/sprockets.mixins.statsd.svg?branch=master
   :target: https://travis-ci.org/sprockets/sprockets.mixins.statsd

.. |Coverage| image:: https://img.shields.io/coveralls/sprockets/sprockets.mixins.statsd.svg?
   :target: https://coveralls.io/r/sprockets/sprockets.mixins.statsd

.. |Downloads| image:: https://pypip.in/d/sprockets.mixins.statsd/badge.svg?
   :target: https://pypi.python.org/pypi/sprockets.mixins.statsd

.. |License| image:: https://pypip.in/license/sprockets.mixins.statsd/badge.svg?
   :target: https://sprocketsmixinsstatsd.readthedocs.org