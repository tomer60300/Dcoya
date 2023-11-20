from scripts.config import url, cert_path

import requests
from datetime import datetime
import asyncio
from pyppeteer import launch

import ssl
import socket
import unittest


class TestSite(unittest.TestCase):
    url = None
    certificate_path = None

    def test_web_page(self):
        response = requests.get(self.url, verify=self.certificate_path)
        self.assertEqual(response.status_code, 200, msg=f"Web page returned status code: {response.status_code}")

    def test_date_being(self):
        asyncio.run(self.async_test_date_being())

    def test_date_accurate(self):
        asyncio.run(self.async_test_date_accurate())

    async def async_test_date_being(self):
        browser = await launch(ignoreHTTPSErrors=True, headless=True)
        page = await browser.newPage()
        await page.goto(self.url)
        await asyncio.sleep(2)
        try:
            # Get the text from the element
            datetime_text = await page.evaluate('''() => {
                const datetimeElement = document.querySelector('#datetime');
                return datetimeElement ? datetimeElement.innerText : 'Date and time element not found.';
            }''')
            self.assertIsNotNone(datetime_text, msg="There no date in the site")
        except Exception as ex:
            self.fail(f"An error occurred while evaluating the page: {ex}")
        finally:
            await browser.close()

    async def async_test_date_accurate(self):
        browser = await launch(ignoreHTTPSErrors=True, headless=True)

        page = await browser.newPage()
        await page.goto(self.url)
        await asyncio.sleep(2)

        try:
            datetime_text = await page.evaluate('''() => {
                const datetimeElement = document.querySelector('#datetime');
                return datetimeElement ? datetimeElement.innerText : 'Date and time element not found.';
            }''')
            site_date = datetime.strptime(datetime_text.split(',')[0], '%m/%d/%Y').date()

            self.assertEqual(site_date, datetime.now().date(),
                             f"Site date f{site_date} isn't the current date {datetime.now().date()}")
        finally:
            await browser.close()

    def test_ssl_handshake(self):
        context = ssl.create_default_context(cafile=self.certificate_path)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED

        url_components = self.url.split("://")[-1].split(":")
        hostname = url_components[0]
        port = int(url_components[1].split("/")[0])

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                try:
                    ssock.do_handshake()  # Perform SSL handshake
                except ssl.SSLError as e:
                    self.fail(f"SSL handshake failed: {e}")


TestSite.url = url
TestSite.certificate_path = cert_path

if __name__ == '__main__':
    unittest.main()
