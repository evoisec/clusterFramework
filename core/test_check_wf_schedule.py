import unittest
import core.check_wf_schedule

class TestCalc(unittest.TestCase):

    def test_dates(self):
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2021-02-11"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2020-01-20"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2018-10-18"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2020-01-01"), False)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2019-09-09"), False)

        self.assertEqual(core.check_wf_schedule.isScheduledDate("2018-03-13"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2020-09-11"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2011-11-11"), True)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2021-12-04"), False)
        self.assertEqual(core.check_wf_schedule.isScheduledDate("2017-06-09"), False)

        self.assertRaises(Exception, core.check_wf_schedule.isScheduledDate, "2020/04/20")

    def test_dates_times(self):

        self.assertRaises(Exception, core.check_wf_schedule.isScheduledDate, "2015-05-20-1404")


if __name__ == "__main__":
    unittest.main()

