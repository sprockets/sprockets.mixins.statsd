Examples
========
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
