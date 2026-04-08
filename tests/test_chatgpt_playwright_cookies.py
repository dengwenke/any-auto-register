import unittest

from platforms.chatgpt.payment import _parse_cookie_str
from platforms.chatgpt.utils import build_oai_device_playwright_cookie


class PaymentCookieParsingTests(unittest.TestCase):
    def test_parse_cookie_str_ignores_set_cookie_attributes(self):
        cookies = _parse_cookie_str(
            (
                "__Secure-next-auth.session-token=session-value; "
                "Path=/; Domain=.chatgpt.com; Secure; HttpOnly; SameSite=Lax; "
                "oai-did=device-value"
            ),
            "https://chatgpt.com/",
        )

        self.assertEqual(
            cookies,
            [
                {
                    "name": "__Secure-next-auth.session-token",
                    "value": "session-value",
                    "url": "https://chatgpt.com/",
                },
                {
                    "name": "oai-did",
                    "value": "device-value",
                    "url": "https://chatgpt.com/",
                },
            ],
        )


class DeviceCookieBuilderTests(unittest.TestCase):
    def test_build_oai_device_cookie_uses_url_shape_only(self):
        cookie = build_oai_device_playwright_cookie(
            "device-fixed",
            url="https://auth.openai.com/",
        )

        self.assertEqual(
            cookie,
            {
                "name": "oai-did",
                "value": "device-fixed",
                "url": "https://auth.openai.com/",
            },
        )


if __name__ == "__main__":
    unittest.main()
