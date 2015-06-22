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
import socket

from sprockets.clients import statsd

__version__ = '1.3.0'


add_timing = statsd.add_timing
incr = statsd.incr
set_gauge = statsd.set_gauge
execution_timer = statsd.execution_timer


class RequestMetricsMixin(object):
    """Automatically sends statsd metrics upon the completion of each request.

    As with all mixins, ensure that you inherit from the mixin classes
    *before* you inherit from a concrete class.  In addition to this, always
    remember to ``super`` the ``on_finish`` and ``prepare`` methods should
    you decide to extend them.

    If the :envvar:`STATSD_USE_HOSTNAME` variable is set to `False` then
    the hostname will not be reported as part of the metrics path.  This
    is useful for collecting metrics in a containerized environment.  By
    default the hostname is part of the metric path.

    Example Usage
    -------------

    class MyRequestHandler(
            sprockets.mixins.statsd.RequestMetricsMixin,
            tornado.web.RequestHandler):

        statsd_prefix = 'my_awesome_app'
        use_hostname = True

        def prepare(self):
            super(RequestMetricsMixin, self).prepare()
            do_prepare_stuff()

        @gen.coroutine
        def post(self):
            self.write(yield self.foo())

    """
    statsd_prefix = os.getenv('STATSD_PREFIX', 'sprockets')
    statsd_use_hostname = os.getenv('STATSD_USE_HOSTNAME', True)

    def on_finish(self):
        """Invoked once the request has been finished. Increments a counter
        created in the format:

        .. code::

            <PREFIX>.counters.<host>.package[.module].Class.METHOD.STATUS
            sprockets.counters.localhost.tornado.web.RequestHandler.GET.200

        Adds a value to a timer in the following format:

        .. code::

            <PREFIX>.timers.<host>.package[.module].Class.METHOD.STATUS
            sprockets.timers.localhost.tornado.web.RequestHandler.GET.200

        """
        if self.statsd_prefix != statsd.STATSD_PREFIX:
            statsd.set_prefix(self.statsd_prefix)

        if hasattr(self, 'request') and self.request:
            if self.statsd_use_hostname:
                timer_prefix = 'timers.{0}'.format(socket.gethostname())
                counter_prefix = 'counters.{0}'.format(socket.gethostname())
            else:
                timer_prefix = 'timers'
                counter_prefix = 'counters'

            statsd.add_timing(timer_prefix,
                              self.__module__,
                              str(self.__class__.__name__),
                              self.request.method,
                              str(self._status_code),
                              value=self.request.request_time() * 1000)

            statsd.incr(counter_prefix,
                        self.__module__,
                        self.__class__.__name__,
                        self.request.method,
                        str(self._status_code))

        super(RequestMetricsMixin, self).on_finish()
