from django.test import TestCase
from unittest import mock
from main.serializers import MainPostSerializer


class MainPostSerializerTest(TestCase):

    @mock.patch('main.serializers.partial')
    def test_create_new_bookmark_success(self, mock_partial):
        mock_partial.return_value = {
            'url': 'http://fdsfsd.com',
            'name': 'trhrthtrhrt',
            'favicon': 'http://fdsfsd.com/favicon.ico',
            'description': 'trhyrtjuyh ythu ty hyrt hrth rthrt'
        }

        data = {'url': 'http://fdsfsd.com'}
        serializer = MainPostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        bookmark = serializer.save()

        self.assertEqual(bookmark.url, 'http://fdsfsd.com')
        self.assertEqual(bookmark.title, 'trhrthtrhrt')
        self.assertEqual(bookmark.favicon, 'http://fdsfsd.com/favicon.ico')
        self.assertEqual(bookmark.description, 'trhyrtjuyh ythu ty hyrt hrth rthrt')

        mock_partial.assert_called_once_with('http://fdsfsd.com')
