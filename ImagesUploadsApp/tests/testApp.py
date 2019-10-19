import os
from unittest import TestCase

from flask import json

from Models.Image import Images
from app import app


class TestApp(TestCase):
    def setUp(self) -> None:
        app_path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1])
        self.image_get_response = {'images': Images(main_dir=app_path).get_images_list()}
        self.image_other_response = {'images': 'Only GET method is supported here...'}

        self.image_response = {'image': Images(main_dir=app_path).get_images_list()[0]}
        self.image_others_response = {'image': 'Only GET and DELETE methods are supported here...'}

    def tearDown(self) -> None:
        pass

    def testImagesGet(self):
        response = app.test_client().get('/api/images')

        code = response.status_code
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(code, 200)
        self.assertEqual(data, self.image_get_response)

    def testImageOthers(self):
        post_response = app.test_client().post('/api/images')
        post_code = post_response.status_code
        post_data = json.loads(post_response.get_data(as_text=True))

        put_response = app.test_client().put('/api/images')
        put_code = put_response.status_code
        put_data = json.loads(put_response.get_data(as_text=True))

        del_response = app.test_client().delete('/api/images')
        del_code = del_response.status_code
        del_data = json.loads(del_response.get_data(as_text=True))

        self.assertEqual(post_code, 200)
        self.assertEqual(post_data, self.image_other_response)

        self.assertEqual(put_code, 200)
        self.assertEqual(put_data, self.image_other_response)

        self.assertEqual(del_code, 200)
        self.assertEqual(del_data, self.image_other_response)

    def testImageGet(self):
        response = app.test_client().get('/api/images/0')

        code = response.status_code
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(code, 200)
        self.assertEqual(data, self.image_response)

    def testImageOther(self):
        post_response = app.test_client().post('/api/images/100')
        post_code = post_response.status_code
        post_data = json.loads(post_response.get_data(as_text=True))

        put_response = app.test_client().put('/api/images/100')
        put_code = put_response.status_code
        put_data = json.loads(put_response.get_data(as_text=True))

        del_response = app.test_client().delete('/api/images/100')
        del_code = del_response.status_code

        self.assertEqual(post_code, 200)
        self.assertEqual(post_data, self.image_others_response)

        self.assertEqual(put_code, 200)
        self.assertEqual(put_data, self.image_others_response)

        self.assertEqual(del_code, 404)
