import unittest

from api.context import Context


class TestContext(unittest.TestCase):

    def test_empty_context_get_returns_default(self):
        ctx = Context()
        self.assertEqual(ctx.get("user_id", 1), 1)
        self.assertEqual(ctx.get("pi", 3.14), 3.14)
        self.assertEqual(ctx.get("hash", "00000000"), "00000000")

    def test_add_value_preserves_old_ctx(self):
        old_ctx = Context()
        cur_ctx = old_ctx.add("user_id", 2)
        new_ctx = cur_ctx.add("user_id", 3)

        self.assertEqual(old_ctx.get("user_id", 1), 1)
        self.assertEqual(cur_ctx.get("user_id", 1), 2)
        self.assertEqual(new_ctx.get("user_id", 1), 3)

    def test_add_value_get_value_type_mismatch_raises_error(self):
        ctx = Context().add("user_id", 3)

        with self.assertRaises(ValueError):
            ctx.get("user_id", "12")
