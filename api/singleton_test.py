import unittest

from api.singleton import Singleton

class TestSingleton(unittest.TestCase):

    def test_singleton_inheritees_have_one_instance(self):
        class Store(metaclass=Singleton):
            def __init__(self) -> None:
                self.store = {}

        store1 = Store()
        store1.store["foo"] = "bar"

        store2 = Store()
        self.assertEqual(store2.store["foo"], "bar")
