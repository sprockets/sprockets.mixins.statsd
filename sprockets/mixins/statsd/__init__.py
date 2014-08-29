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

version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

STATSD_PREFIX = os.getenv('STATSD_PREFIX', 'sprockets')


class RequestMetricsMixin(object):
    """The ``RequestMetricsMixin`` automatically sends statsd metrics upon the
    completion of each request.

    """
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
            statsd.add_timing(STATSD_PREFIX,
                              'timers',
                              self.__module__,
                              self.__class__.__name__,
                              self.request.method,
                              self.request.status_code,
                              value=self.request.request_time() * 1000)
            statsd.incr(STATSD_PREFIX,
                        'counters',
                        self.__module__,
                        self.__class__.__name__,
                        self.request.method,
                        self.request.status_code)
        super(RequestMetricsMixin, self).on_finish()
