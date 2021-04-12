import unittest
from rules import fpe, mask, mask_ssn, us_zipcode

class TestMasking(unittest.TestCase):
    def test_mask(self):
        self.assertEqual(mask('078051120', 4), 'XXXXX1120')
        self.assertEqual(mask('078051120', 1, '*'), '********0')
        self.assertEqual(mask('078051120', 9, '*'), '078051120')

    def test_mask_ssn(self):
        self.assertEqual(mask_ssn('078-05-1120'), 'XXX-XX-1120')
        self.assertEqual(mask_ssn('078-05-1120', '*'), '***-**-1120')

class TestRules(unittest.TestCase):

    def test_zip_code(self):
        self.assertEqual(us_zipcode('05900'), '00000')
        self.assertEqual(us_zipcode('07739'), '07700')
        self.assertEqual(us_zipcode('07739-1234'), '07700')
        self.assertRaises(ValueError, us_zipcode, '077')

class TestGeneralizeDate(unittest.TestCase):

    def test_year1(self):
        #a = GeneralizeDate(5).apply(date(1970,12,31))
        #self.assertEqual(a, date(1970,1,1))
        pass

    def test_year2(self):
        #a = GeneralizeDate(5).apply(date(2020,1,1))
        #self.assertEqual(a, date(2020,1,1))
        pass

    def test_decrypt_all(self):
        pass

if __name__ == '__main__':
        unittest.main()
