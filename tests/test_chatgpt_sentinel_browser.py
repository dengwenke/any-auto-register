import unittest
from unittest import mock

from platforms.chatgpt import sentinel_browser


class SentinelBrowserSdkLoadingTests(unittest.TestCase):
    def test_ensure_sdk_loaded_injects_sdk_after_first_timeout(self):
        page = mock.Mock()
        page.wait_for_function.side_effect = [RuntimeError("timeout"), None]

        sentinel_browser._ensure_sdk_loaded(
            page,
            timeout_ms=60000,
            sdk_url="https://sentinel.openai.com/sentinel/test/sdk.js",
        )

        page.wait_for_load_state.assert_called_once_with("load", timeout=60000)
        self.assertEqual(page.wait_for_function.call_count, 2)
        first_call = page.wait_for_function.call_args_list[0]
        second_call = page.wait_for_function.call_args_list[1]
        self.assertEqual(first_call.kwargs["timeout"], 15000)
        self.assertEqual(second_call.kwargs["timeout"], 30000)
        page.evaluate.assert_called_once()
        self.assertIn("targetSdkUrl", page.evaluate.call_args.args[0])
        self.assertEqual(
            page.evaluate.call_args.args[1],
            "https://sentinel.openai.com/sentinel/test/sdk.js",
        )


if __name__ == "__main__":
    unittest.main()
