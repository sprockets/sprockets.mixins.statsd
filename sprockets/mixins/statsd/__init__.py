"""
StatsD Handler Mixin
====================
The ``RequestMetricsMixin`` mixin will automatically instrument requests by
sending statsd increment and timing values as each request finishes.

The default statsd server that is used is ``localhost:8125``. The
``STATSD_HOST`` and ``STATSD_PORT`` environment variables can be used to
set the statsd server connection parameters. Note that the socket for
communicating with statsd is created once upon module import and will not
change until the application is restarted or the module is reloaded.

In the ``RequestMetricsMixin``, the statsd metrics are prefixed by default
with ``sprockets``. To change this value, set the new prefix with the
``STATSD_PREFIX`` environment variable.

Each request will send metrics ``on_finish`` in the following format:

.. code::

    <STATSD_PREFIX>.counters.package[.module].Class.METHOD.STATUS
    <STATSD_PREFIX>.timers.package.[.module].Class.METHOD.STATUS

``RequestMetricsMixin`` Example:

.. code:: python

    from sprockets.handlers.mixins import statsd
    from tornado import web

    class MyRequestHandler(stats.RequestMetricsMixin,
                           web.RequestHandler):

        def get(self, *args, **kwargs):
            self.finish({'hello': 'world'})

"""
import os

from sprockets.clients import statsd

version_info = (1, 0, 4)
__version__ = '.'.join(str(v) for v in version_info)


class RequestMetricsMixin(object):
    """Automatically sends statsd metrics upon the completion of each request.

    As with all mixins, ensure that you inherit from the mixin classes
    *before* you inherit from a concrete class.  In addition to this, alway
    remember to ``super`` the ``on_finish`` and ``prepare`` methods should
    you decide to extend them.

    Example Usage
    -------------

    class MyRequestHandler(
            sprockets.mixins.statsd.RequestMetricsMixin,
            tornado.web.RequestHandler):

        def prepare(self):
            super(RequestMetricsMixin, self).prepare()
            do_prepare_stuff()

        @gen.coroutine
        def post(self):
            self.write(yield self.foo())

    """

    statsd_prefix = os.getenv('STATSD_PREFIX', 'sprockets')

    def on_finish(self):
        """Invoked once the request has been finished. Increments a counter
        created in the format:

        .. code::

            <STATSD_PREFIX>.counters.package[.module].Class.METHOD.STATUS
            sprockets.counters.tornado.web.RequestHandler.GET.200

        Adds a value to a timer in the following format:

        .. code::

            <STATSD_PREFIX>.timers.package[.module].Class.METHOD.STATUS
            sprockets.timers.tornado.web.RequestHandler.GET.200

        """
        if hasattr(self, 'request') and self.request:
            statsd.add_timing(self.statsd_prefix,
                              'timers',
                              self.__module__,
                              self.__class__.__name__,
                              self.request.method,
                              str(self._status_code),
                              value=self.request.request_time() * 1000)

            statsd.incr(self.statsd_prefix,
                        'counters',
                        self.__module__,
                        self.__class__.__name__,
                        self.request.method,
                        str(self._status_code))

        super(RequestMetricsMixin, self).on_finish()
