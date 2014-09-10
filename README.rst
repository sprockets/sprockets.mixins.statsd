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
https://sprocketsmixinsstatsd.readthedocs.org/

Requirements
------------
-  `sprockets.client.statsd <https://github.com/sprockets/sprockets.client.statsd>`_

Example
-------
The following ``RequestHandler`` will automatically increment a request counter
and add a request duration timing value to statsd when the request finishes.

.. code:: python

    from sprockets.mixins import statsd
    from tornado import web

    class MyRequestHandler(statsd.RequestMetricsMixin,
                           web.RequestHandler):

        def prepare(self):
            self.statsd_prefix = 'some.overriden.value'
            super(MyRequestHandler, self).prepare()

        def get(self, *args, **kwargs):
            self.finish({'hello': 'world'})

        def on_finish(self):
            super(MyRequestHandler, self).on_finish()
            self.do_cleanup_things()


When the request has finished, the following keys would be used:

- Counter: ``sprockets.counter.example.RequestHandler.GET.200``
- Timing: ``sprockets.timers.example.RequestHandler.GET.200``

Mixin Behavior
--------------
Whenever you mix in a class in Python always ensure that the mixins, which
should inherit from ``object``, are the first ones in the inheritance list.
The concrete class, in this case `web.RequestHandler` should be the final
class inherited.

Should your Request Handler extend the ``finish`` or the ``prepare`` methods
ensure that your call ``super`` otherwise you may run into strange behavior.

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
