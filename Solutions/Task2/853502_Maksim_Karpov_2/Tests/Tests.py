from external_sort import ExternalSort
from JSON_task import JSON, Company
from vector import Vector
from cashed import cached
from SingleTone import MetaSingleton, Check
import unittest
import json



class SortUnitTest(unittest.TestCase):

    def setUp(self):
        self.UniSort = ExternalSort(5, 4000, "unittest_file.txt", "unittest_sorted.txt")

    def test_is_sorted(self):

        test_string = []
        test_string2 = []
        with open('unittest_sorted.txt', 'r') as test_file:
            test_string = test_file.read().splitlines()
            test_string = [int(item) for item in test_string]
        with open(self.UniSort.file, 'r') as test_file_2:
            test_string2 = test_file_2.read().splitlines()
            test_string2 = [int(item) for item in test_string2]
            test_string2.sort()

        self.assertEqual(test_string, test_string2)


class UnitTestJSON(unittest.TestCase):

    def setUp(self):
        self.json = JSON(Company("Karpov", "Maksim", "Konstantinovich"))
        self.valid_json_string = '{"EployeeInfo": {"First_name": "Maksim", "Second_name": "Karpov", "Patronymic_name": "Konstantinovich", "Married": true, "Kids": false, "Kids_Name": null, "Company_Name": "Zhodinsky_milkdairy_plant", "Company_Phone": [(375, 29), 228, 14, 88]}}'
        self.obj = Company("Karpov", "Maksim", "Konstantinovich")

    def test_valid(self):
        self.assertEqual(self.valid_json_string, self.json.to_json())

    def test_reverse(self):
        temp_string = self.valid_json_string
        self.json.obj = self.json.from_json(temp_string)
        temp_string = self.json.to_json()
        self.assertEqual(temp_string, self.valid_json_string)

    def test_dump(self):
        self.obj.EployeeInfo.popitem()
        self.test_json = JSON(self.obj.get_company_info())
        print(json.dumps(self.obj.get_company_info()))
        print(self.test_json.to_json())
        self.assertEqual(json.dumps(self.obj.get_company_info()), self.test_json.to_json())

    def test_load(self):
        self.valid_json_string = '{"EployeeInfo": {"First_name": "Maksim", "Second_name": "Karpov", "Patronymic_name": "Konstantinovich", "Married": true, "Kids": false, "Kids_Name": null, "Company_Name": "Zhodinsky_milkdairy_plant", "Company_Phone": [375, 29, 228, 14, 88]}}'
        self.assertEqual(self.json.from_json(self.valid_json_string), json.loads(self.valid_json_string))


class TestVector(unittest.TestCase):

    def setUp(self):
        self.vector = Vector(10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def test_equal(self):
        self.assertEqual(self.vector, Vector(10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    def test_inequality_with_vector_by_values(self):
        self.assertNotEqual(self.vector, Vector(10, 2))

    def test_inequality_with_vector_by_dimension(self):
        self.assertNotEqual(self.vector, Vector(7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    def test_inequality_with_not_vector(self):
        self.assertNotEqual(self.vector, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_negation(self):
        self.assertEqual(-self.vector, Vector(10, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10))

    def test_vector_add(self):
        vector2 = Vector(10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        result_vector = Vector(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.assertEqual(self.vector + vector2, result_vector)

    def test_scalar_add(self):
        a = 5
        result_vector = Vector(10, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.assertEqual(self.vector + a, result_vector)

    def test_scalar_iadd(self):
        self.vector += 5
        result_vector = Vector(10, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.assertEqual(self.vector, result_vector)

    def test_vector_sub(self):
        vector2 = Vector(10, 2, 2, 3, 3, 4, 4, 5, 5, 10, 20)
        result_vector = Vector(10, -1, 0, 0, 1, 1, 2, 2, 3, -1, -10)
        self.assertEqual(self.vector - vector2, result_vector)

    def test_scalar_rsub(self):
        a = 1
        result_vector = Vector(10, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9)
        self.assertEqual(a - self.vector, result_vector)

    def test_vector_isub(self):
        self.vector -= Vector(10, 2, 2, 3, 3, 4, 4, 5, 5, 10, 20)
        result_vector = Vector(10, -1, 0, 0, 1, 1, 2, 2, 3, -1, -10)
        self.assertEqual(self.vector, result_vector)

    def test_scalar_product(self):
        vector2 = Vector(10, 2, 2, 2, 2, 2, 5, 5, 5, 0, 0)
        self.assertEqual(self.vector * vector2, 135)

    def test_scalar_rmul(self):
        a = 2
        result_vector = Vector(10, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
        self.assertEqual(a * self.vector, result_vector)

    def test_index_access(self):
        self.assertEqual(1, self.vector[0])

    def test_length(self):
        self.assertEqual(10, len(self.vector))

    def test_to_str(self):
        self.assertEqual('<1, 2, 3, 4, 5, 6, 7, 8, 9, 10>', str(self.vector))

    def test_str_repr(self):
        self.assertEqual('[1, <1, 2, 3, 4, 5, 6, 7, 8, 9, 10>]', str([1, self.vector]))

    def test_different_lengths_for_sum(self):
        with self.assertRaises(ValueError):
            self.vector + Vector(5)

    def test_different_lengths_for_sub(self):
        with self.assertRaises(ValueError):
            self.vector - Vector(3, *[5, 15, 91])

    def test_wrong_type_for_mul(self):
        with self.assertRaises(ValueError):
            a = self.vector * [1, 2, 3]

    def test_wrong_type_for_add(self):
        with self.assertRaises(ValueError):
            a = self.vector + [1, 2, 3]

    def test_wrong_type_init(self):
        with self.assertRaises(ValueError):
            vector = Vector(3, 'qwe', 3, 5.3)

    def test_modification_with_wrong_value(self):
        with self.assertRaises(ValueError):
            self.vector[0] = Vector(1)

    def test_index_error(self):
        with self.assertRaises(IndexError):
            a = self.vector[100]


class TestSingleTone(unittest.TestCase):

    def setUp(self):
        self.data_1 = Check()
        self.data_2 = Check()

    def test_singleton(self):

        self.assertEqual(self.data_1, self.data_2)


class CashedTests(unittest.TestCase):
    @cached
    def mul_func(self, a, b):
        return a * b

    def test_cached_decorator(self):
        self.assertTrue(5 == self.mul_func(5, 1))
        self.mul_func(5, 1)
        self.assertTrue(5 == self.mul_func(5, 1))
        self.assertFalse(5 == self.mul_func(2, 6))

    def test_cached_error(self):
        self.assertRaises(Exception, self.mul_func('123', 4))
