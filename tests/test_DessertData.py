import random
import unittest
from DessertData import DessertData


class TestDessertData(unittest.TestCase):

    def setUp(self) -> None:
        """
        Define test data so that each row is [0, row_num]
        """
        self._tot_rows = 10
        data = []
        for i in range(self._tot_rows):
            data.append([0, i])
        self.test_data = DessertData(self._tot_rows, 0.0, data)
        data = [[0, i] for i in range(self._tot_rows)]
        self.multiclass_data = DessertData(self._tot_rows, 0.0, data)
        data = [[i, 0] for i in range(self._tot_rows)]
        self.one_class_data = DessertData(self._tot_rows, 0.0, data)


class TestInit(TestDessertData):

    def test_neg_rows(self):
        self.assertRaises(ValueError, DessertData, -1)

    def test_wrong_num_rows(self):
        self.assertRaises(ValueError, DessertData, 0, 0, [[1]])

    def test_num_rows(self):
        for num_rows in range(0, 20):
            with self.subTest(i=num_rows):
                self.assertEqual(len(DessertData(num_rows)._data), num_rows)

    def test_init_data(self):
        for num_rows in range(0, 20):
            with self.subTest(i=num_rows):
                data = []
                for i in range(num_rows+1):
                    data.append([0, i])
                test_data = DessertData(num_rows+1, data=data)
                self.assertEqual(test_data._data, data)

    @unittest.skip("Noise level not implemented")
    def test_noise_level(self):
        self.fail()


class TestSplit(TestDessertData):

    def test_split_objects(self):
        """
        Test that split returns DessertData objects
        """
        train_obj, test_obj = self.test_data.split(random.random())
        self.assertIsInstance(train_obj, DessertData)
        self.assertIsInstance(test_obj, DessertData)

    def test_split_one(self):
        """
        Test that splitting 100% returns all data in training and empty in test
        """
        train_set, test_set = self.test_data.split(1.0)
        self.assertEqual(train_set._data, self.test_data._data)
        self.assertFalse(test_set._data)

    def test_split_rand(self):
        """
        Test that the number of rows is correct. Cannot test actual data since it's shuffled
        before splitting.
        """
        for row_num in range(0, self._tot_rows):
            with self.subTest(i=row_num):
                percentage = row_num/self._tot_rows
                train_set, test_set = self.test_data.split(percentage)

                self.assertEqual(len(train_set._data), row_num, "Train set wrong size")
                self.assertEqual(len(test_set._data), self._tot_rows-row_num, "Test set wrong size")

    def test_split_low(self):
        percentage = 1/self._tot_rows/2
        train_set, test_set = self.test_data.split(percentage)
        self.assertEqual(len(train_set._data), 0, "Train set wrong size")
        self.assertEqual(len(test_set._data), self._tot_rows, "Test set wrong size")

    def test_split_high(self):
        percentage = 1 - 1/self._tot_rows/2
        train_set, test_set = self.test_data.split(percentage)
        self.assertEqual(len(test_set._data), 0, "Test set wrong size")
        self.assertEqual(len(train_set._data), self._tot_rows, "Train set wrong size")


class TestIsSingleClass(TestDessertData):
    """
    Test that is_single_class() method works.
    """
    def test_is_single_class(self):
        self.assertTrue(self.one_class_data.is_single_class())
        self.assertFalse(self.multiclass_data.is_single_class())
