from django.test import TestCase
from unittest import mock
from .services import partial
from urllib.parse import urljoin
from requests.exceptions import HTTPError


class MainPostSerializerTest(TestCase):

    @mock.patch('main.services.requests')
    def test_success_request(self, mock_get):

        data = '''
        <html>
            <head>
                <title>Title</title>
                <link rel="icon" href="/favicon.ico">
                <meta name="description" content="Smth there">
            </head>
        </html>
        '''
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = data

        mock_get.get.return_value = mock_response
        url = 'http://test.com'
        result = partial(url)

        favicon = urljoin(url, '/favicon.ico')
        self.assertEqual(result, {
            "url": url,
            "name": "Title",
            "favicon": favicon,
            "description": "Smth there",
        })
        self.assertNotIn("error", result)

    @mock.patch('main.services.requests')
    def test_part_success_request(self, mock_get):
        data = '''
            <html>
                <head>
                    <link rel="icon" href="/favicon.ico">
                </head>
            </html>
            '''
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = data

        mock_get.get.return_value = mock_response
        url = 'http://test.com'
        result = partial(url)

        favicon = urljoin(url, '/favicon.ico')
        self.assertEqual(result, {
            "url": url,
            "name": "No title",
            "favicon": favicon,
            "description": "",
        })
        self.assertNotIn("error", result)

    @mock.patch('main.services.requests')
    def test_error_request(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        mock_response.raise_for_status.side_effect = HTTPError('404 Client Error: Not Found')
        mock_get.get.return_value = mock_response

        url = 'http://test.com'
        result = partial(url)

        self.assertIn('error', result)
        self.assertEqual(result['url'], url)

