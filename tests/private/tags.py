
from ..common import ApiTestBase


class TagsTests(ApiTestBase):
    """Tests for TagsEndpointsMixin."""

    @staticmethod
    def init_all(api):
        return [
            {
                'name': 'test_tag_info',
                'test': TagsTests('test_tag_info', api)
            },
            {
                'name': 'test_tag_related',
                'test': TagsTests('test_tag_related', api)
            },
            {
                'name': 'test_tag_search',
                'test': TagsTests('test_tag_search', api)
            },
        ]

    def test_tag_info(self):
        results = self.api.tag_info('catsofinstagram')
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(results.get('media_count'), 0, 'No media_count returned.')

    def test_tag_related(self):
        results = self.api.tag_related('catsofinstagram')
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('related', [])), 0, 'No media_count returned.')

    def test_tag_search(self):
        results = self.api.tag_search('cats')
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('results', [])), 0, 'No results returned.')
