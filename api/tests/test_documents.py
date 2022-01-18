import unittest
import json
from . import BaseTestCase


class TestDocuments(BaseTestCase):
    def test_create_document_success(self):
        post_data = {
            'title': 'My super cool document',
            'body': 'Markdown city',
        }
        result = self.app.post('/v1/documents', json=post_data)

        self.assertEqual(result.status_code, 201)

    def test_retrieve_documents_collection_success(self):
        result = self.app.get('/v1/documents')

        self.assertEqual(result.status_code, 200)

    def test_update_document_not_found(self):
        patch_data = {
            'body': 'Markdown town'
        }
        result = self.app.patch('/v1/documents/deadbeef-dead-dead-dead-deaddeafbeef', json=patch_data)

        self.assertEqual(result.status_code, 404)

    def test_delete_document_not_found(self):
        result = self.app.delete('/v1/documents/deadbeef-dead-dead-dead-deaddeafbeef')

        self.assertEqual(result.status_code, 404)

    def test_delete_document_success(self):
        post_data = {
            'title': 'My super cool document',
            'body': 'Markdown city',
        }
        result = self.app.post('/v1/documents', json=post_data)

        new_document_id = result.get_json()['data']['id']

        self.assertEqual(result.status_code, 201)

        result = self.app.delete(f'/v1/documents/{new_document_id}')

        self.assertEqual(result.status_code, 200)

        result = self.app.get('/v1/documents')

        self.assertEqual(result.get_json()['data'], [])
