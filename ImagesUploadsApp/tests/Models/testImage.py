import os
from unittest import TestCase

from Models.Image import Image, Images


class TestImage(TestCase):
    def setUp(self) -> None:
        self.test_id_1 = 0
        self.test_name_1 = 'one.jpg'
        self.test_path_1 = ''

    def tearDown(self) -> None:
        pass

    def testInit(self) -> None:
        test_class = Image(index=self.test_id_1, file_name=self.test_name_1, path=self.test_path_1)
        self.assertEqual(test_class.id, self.test_id_1)
        self.assertEqual(isinstance(test_class.id, int), True)
        self.assertEqual(test_class.name, self.test_name_1)
        self.assertEqual(isinstance(test_class.name, str), True)
        self.assertEqual(test_class.path, self.test_path_1)
        self.assertEqual(isinstance(test_class.path, str), True)


class TestImages(TestCase):
    def setUp(self) -> None:
        self.test_path = f"{os.path.dirname(os.path.abspath(__file__))}\\Images"

        self.first_test_file = f"{self.test_path}\\0_testImage1.png"
        self.second_test_file = f"{self.test_path}\\1_testImage2.jpg"

        self.test_file_list = []
        self.test_file_list.append(self.first_test_file)
        self.test_file_list.append(self.second_test_file)

        self.first_test_image = Image(index=0, file_name='testImage1.png', path=self.first_test_file)
        self.second_test_image = Image(index=1, file_name='testImage2.jpg', path=self.second_test_file)

        self.test_image_list = []
        self.test_image_list.append(self.first_test_image)
        self.test_image_list.append(self.second_test_image)

        self.test_json_image_list = []
        self.test_json_image_list.append(self.first_test_image.__dict__)
        self.test_json_image_list.append(self.second_test_image.__dict__)

    def tearDown(self) -> None:
        pass

    def testGetFiles(self):
        files = Images.get_files(self.test_path)
        self.assertListEqual(files, self.test_file_list)
        self.assertEqual(isinstance(files, list), True)
        self.assertEqual(files[0], self.test_file_list[0])
        self.assertEqual(isinstance(files[0], str), True)
        self.assertEqual(files[1], self.test_file_list[1])
        self.assertEqual(isinstance(files[1], str), True)

    def testInit(self) -> None:
        test_class = Images(main_dir=os.path.dirname(os.path.abspath(__file__)))
        self.assertEqual(isinstance(test_class.images_list, list), True)
        self.assertEqual(isinstance(test_class.images_list[0], Image), True)
        self.assertEqual(isinstance(test_class.images_list[1], Image), True)
        self.assertEqual(isinstance(test_class.cur_id, int), True)
        self.assertEqual(test_class.cur_id, 1)

    def testGetImagesList(self):
        test_class = Images(main_dir=os.path.dirname(os.path.abspath(__file__)))
        test_list = test_class.get_images_list()
        self.assertEqual(isinstance(test_list, list), True)
        self.assertListEqual(test_list, self.test_json_image_list)
        self.assertEqual(isinstance(test_list[0], dict), True)
        self.assertEqual(test_list[0], self.test_json_image_list[0])
        self.assertEqual(isinstance(test_list[1], dict), True)
        self.assertEqual(test_list[1], self.test_json_image_list[1])

    def testIncreaseId(self):
        test_class = Images(main_dir=os.path.dirname(os.path.abspath(__file__)))
        test_class.increase_id()
        self.assertEqual(test_class.cur_id, 2)
