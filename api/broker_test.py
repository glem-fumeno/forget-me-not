import unittest

from api.broker import Broker
from api.context import Context


class TestBroker(unittest.TestCase):
    def setUp(self) -> None:
        self.broker = Broker()
        self.ctx = Context()
        self.broker.reset()

    def test_broker_subscribers_can_subscribe_once(self):
        called = 0

        def callback(ctx):
            del ctx
            nonlocal called
            called += 1

        self.broker.subscribe("foo", "bar", callback)
        self.broker.subscribe("foo", "bar", callback)
        self.broker.publish(self.ctx, "bar")
        self.assertEqual(called, 1)

    def test_brokers_have_the_same_events(self):
        called = False

        def callback(ctx):
            del ctx
            nonlocal called
            called = True

        self.broker.subscribe("foo", "bar", callback)
        Broker().publish(self.ctx, "bar")
        self.assertEqual(called, True)
