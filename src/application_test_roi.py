import unittest

from application_roi import *
from application_commands import *


"""
صف لاختبار بعض مكونات البرنامج, غير مستخدم حاليا و ليس له وظيفة غير أداء بعض الاختبارات على عمل بعض الاجرائيات بشكل صحيح
"""
class MyTestCase(unittest.TestCase):
    """
    Class for unit testing part of the code developed for this project
    TODO: add more tests for all parts of the project
    """
    def test_roi(self):
        r1 = RoiBounds(0, 0, 10, 10)
        r2 = RoiBounds(20, 20, 30, 30)

        r3 = RoiBounds(5, 5, 15, 15)
        r4 = RoiBounds(5, 50, 15, 55)

        self.assertTrue(r1.is_top_left_to(r2))
        self.assertTrue(r1.is_left_to(r2))
        self.assertTrue(r1.is_upper_than(r2))

        self.assertTrue(r2.is_lower_right_to(r1))
        self.assertTrue(r2.is_right_to(r1))
        self.assertTrue(r2.is_lower_than(r1))

        self.assertTrue(r1.is_same_level_v(r3))
        self.assertTrue(r1.is_same_level_h(r3))
        self.assertFalse(r1.is_same_level_h(r4))
        self.assertTrue(r1.is_same_level_v(r4))

        print "done"

    def test_command(self):
        ref = RoiBounds(20, 20, 25, 25)
        left = RoiBounds(0, 0, 10, 10)
        right = RoiBounds(40, 0, 50, 10)
        smile = RoiBounds(10, 50, 20, 55)

        self.assertTrue(left.is_top_left_to(ref))
        self.assertTrue(right.is_top_right_to(ref))
        self.assertTrue(RoiBounds.command_is_forward(left, right, smile, ref))

    def test_command_queue(self):
        cmd = CommandQueue(7, 3, CMD.STOP)
        self.assertEqual(cmd.add_and_get(CMD.BACKWARD), 'S')
        self.assertEqual(cmd.add_and_get(CMD.BACKWARD), 'S')
        self.assertEqual(cmd.add_and_get(CMD.BACKWARD), 'S')
        self.assertEqual(cmd.add_and_get(CMD.FORWARD), 'S')
        self.assertEqual(cmd.add_and_get(CMD.FORWARD), 'B')
        self.assertEqual(cmd.add_and_get(CMD.FORWARD), 'B')
