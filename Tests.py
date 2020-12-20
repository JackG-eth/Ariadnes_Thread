import unittest
from unittest import TestCase

from Logic import get_Officers_Companies, get_company_info , getCompanyScore,get_associated_companies_info_by_company


class AssociationsTestCase(unittest.TestCase):

    # Testing that associated companies for a particular officer are returned
    """
    def test_associations(self):
        dict= get_associated_companies_info_by_company('09784535', depth=1)
        i = 1
        outputA = []
        for key, values in dict.items():
            for keys, value in values.items():
                if(len(value) == 8):
                    outputA.append(value)

        self.assertListEqual(
            sorted(outputA),
            sorted(['08000943', '07315558']))

    # Testing IWOCA
    """
    """
    def test_associations(self):
        dict= get_associated_companies_info_by_company('07798925', depth=1)
        i = 1
        outputA = []
        for key, values in dict.items():
            for keys, value in values.items():
                if(len(value) == 8):
                    outputA.append(value)
        print(outputA)
        self.assertListEqual(
            sorted(outputA),
            sorted(['10056048', '12896673', '08971917', '07782371', '07546735', '09099356', '07714634', '10366510',
            '09701947', '11194408', '11194622', '10624955', '11118262', 'OC355777', '06573695', '12437336',
            '12437351', '12206687', '10470734', '06924164', '12240506', '09959642', '10443871', '11509161',
            '11510263', '09510201', '10247619', '04712266', '07513834', '11899125', '11896188', 'OC424211',
            '11262180', '10704648', '07182042', '09857705', '09546159', '05518629', '07311752', '08054586',
            '07726567', '07512990', '09639436', '06893077', '09669260', 'C3UK LTD', '08973931', '08562035',
            '08460938', '07564428', '08267810', '09481404', '08339609', '04712266', '09900830', '03287157',
            '04631147', '04481406', '05468033', 'SE000007']))
    """
    def test_associations(self):
        self.assertRaisesRegex(ValueError,  "Company Does Not Exist!")

    def test_associations(self):
        try:
          dict= get_company_info('')
          self.assertFail()
        except Exception as inst:
          self.assertEqual(inst.message, "Company Does Not Exist!")


    def test_associations(self):
        storedInfo = get_company_info('07798925')
        expected = {'Company Name: ': 'IWOCA LTD', 'has_been_liquidated: ': 0, 'has_insolvency_history: ': 0, 'registered_office_is_in_dispute: ': 0}
        self.assertListEqual(sorted(storedInfo),sorted(expected))


    """
    Write a few score test_something
    Think of a few others
    Try to get 10
    Check all comments
    See if you can format it nicely
    look for any extra error handlimng you could padding
    README
    """
if __name__ == '__main__':
    unittest.main()
