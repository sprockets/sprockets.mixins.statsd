"""
Tests for the sprockets.mixins.statsd package

"""
import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from tornado import httputil
from tornado import web

from sprockets.mixins import statsd


class StatsdRequestHandler(statsd.RequestMetricsMixin,
                           web.RequestHandler):
    pass


class Context(object):
    remote_ip = '127.0.0.1'
    protocol = 'http'


class Connection(object):
    context = Context()

    def set_close_callback(self, callback):
        pass


class MixinTests(unittest.TestCase):

    def setUp(self):
        self.application = web.Application()
        self.request = httputil.HTTPServerRequest('GET',
                                                  uri='http://test/foo',
                                                  connection=Connection(),
                                                  host='127.0.0.1')
        self.handler = StatsdRequestHandler(self.application, self.request)
        self.handler._status_code = 200

    @mock.patch('sprockets.clients.statsd.add_timing')
    @mock.patch('sprockets.clients.statsd.incr')
    def test_on_finish_calls_statsd_add_timing(self, incr, add_timing):
        self.request._finish_time = self.request._start_time + 1
        self.duration = self.request._finish_time - self.request._start_time
        self.handler.on_finish()
        add_timing.assert_called_once_with('sprockets', 'timers', 'tests',
                                           'StatsdRequestHandler', 'GET', 200,
                                           value=self.duration * 1000)

    @mock.patch('sprockets.clients.statsd.add_timing')
    @mock.patch('sprockets.clients.statsd.incr')
    def test_on_finish_calls_statsd_incr(self, incr, add_timing):
        self.handler.on_finish()
        incr.assert_called_once_with('sprockets', 'counters', 'tests',
                                     'StatsdRequestHandler', 'GET', 200)
