import unittest
from script import parse_args
from script import main as mainfunc
import argparse 


class TestParser(unittest.TestCase):

    def test_parser_valid_info(self):
        parser = parse_args(['--period', '1h', '--tz', 'Europe/Athens', '--t1', '1', '--t2', '2'])
        self.assertEqual(parser, argparse.Namespace(endpoint='2', period='1h', startpoint='1', timezone='Europe/Athens'))

    def test_parser_invalid_timezone_exit_code(self):
        with self.assertRaises(SystemExit) as cm:
            parser = parse_args(['--period', '1h', '--tz', 'Europe/Greece', '--t1', '1', '--t2', '2'])
        self.assertEqual(cm.exception.code, 10)

    def test_parser_missing_argument_exit_code(self):
        with self.assertRaises(SystemExit) as cm:
            parser = parse_args(['--tz', 'Europe/Greece', '--t1', '1', '--t2', '2'])
        self.assertEqual(cm.exception.code, 10)

    def test_parser_wrong_period_exit_code(self):
        with self.assertRaises(SystemExit) as cm:
            parser = parse_args(['--period', '1w','--tz', 'Europe/Athens', '--t1', '1', '--t2', '2'])
        self.assertEqual(cm.exception.code, 10)

    def test_wrong_format_t1(self):
        with self.assertRaises(SystemExit) as cm:
            mainfunc(mode='unittest', test_param = ['--period', '1h','--tz', 'Europe/Athens', '--t1', '20201115T123456', '--t2', '20201115T123456Z'])
        self.assertEqual(cm.exception.code, 10)

    def test_wrong_format_t2(self):
        with self.assertRaises(SystemExit) as cm:
            mainfunc(mode='unittest', test_param = ['--period', '1h','--tz', 'Europe/Athens', '--t1', '20201115T123456Z', '--t2', '20201115T253456Z'])
        self.assertEqual(cm.exception.code, 10)

    def test_empty_ptlist_t1_after_t2(self):
        ptlist = mainfunc(mode='unittest', test_param = ['--period', '1mo', '--t1', '20210214T204603Z', '--t2', '20201115T123456Z', '--tz', 'Europe/Athens'])
        correct_output = []
        self.assertEqual(ptlist, correct_output)

    def test_period_1h(self):
        ptlist = mainfunc(mode='unittest', test_param = ['--period', '1h', '--t1', '20180214T204603Z', '--t2', '20180214T214603Z', '--tz', 'Europe/Paris'])
        correct_output = ['"20180214T190000Z"']
        self.assertEqual(ptlist, correct_output)

    def test_period_1d(self):
        ptlist = mainfunc(mode='unittest', test_param = ['--period', '1d', '--t1', '20251230T204603Z', '--t2', '20260101T214603Z', '--tz', 'Africa/Abidjan'])
        correct_output = ['"20251231T000000Z"', '"20260101T000000Z"']
        self.assertEqual(ptlist, correct_output)

    def test_period_1mo(self):
        ptlist = mainfunc(mode='unittest', test_param = ['--period', '1mo', '--t1', '20210214T204603Z', '--t2', '20211115T123456Z', '--tz', 'Europe/Athens'])
        correct_output = ['"20210228T220000Z"', '"20210331T210000Z"', '"20210430T210000Z"', '"20210531T210000Z"', '"20210630T210000Z"', '"20210731T210000Z"', '"20210831T210000Z"', '"20210930T210000Z"', '"20211031T220000Z"']
        self.assertEqual(ptlist, correct_output)

    def test_period_1y(self):
        ptlist = mainfunc(mode='unittest', test_param = ['--period', '1y', '--t1', '20180214T204603Z', '--t2', '20211115T123456Z', '--tz', 'Europe/Athens'])
        correct_output = ['"20181231T220000Z"', '"20191231T220000Z"', '"20201231T220000Z"']
        self.assertEqual(ptlist, correct_output)


if __name__ == '__main__':
    main()