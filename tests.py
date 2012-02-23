# -*- coding: utf-8 -*-
from unittest import TestCase
from mcfly_machine import Machine as m
from datetime import datetime, timedelta
import machine_utils


class DatesAssertsMixin(TestCase):
    def assert_equals_dates(self, date1, date2, msg):
        date1 = machine_utils.get_date_withot_ms(date1)
        date2 = machine_utils.get_date_withot_ms(date2)
        self.assertEquals(date1, date2, msg=msg)


class TestMcflyMachineBehavior(DatesAssertsMixin, TestCase):
    """Behavior tests for Machine class"""
    def test_experiments(self):
        now = datetime.now
        utcnow = datetime.utcnow
        from_ = datetime(2012, 10, 11) - timedelta(days=10)

        # lambdas is for dates accuracy
        experiments = [
            {
                'machine':  lambda: m(5).days.ago(),
                'expected': lambda: now() - timedelta(days=5),
            },
            {
                'machine':  lambda: m(5).days.later(),
                'expected': lambda: now() + timedelta(days=5),
            },
            {
                'machine':  lambda: m(5).days.ago(in_utc=True),
                'expected': lambda: utcnow() - timedelta(days=5),
                'msg':      'date should be in utc'
            },
            {
                'machine':  lambda: m(5).days.later(in_utc=True),
                'expected': lambda: utcnow() + timedelta(days=5),
                'msg':      'date should be in utc'
            },
            {
                'machine':  lambda: m(5).days.ago(from_=from_),
                'expected': lambda: from_ - timedelta(days=5),
                'msg':      'calculation from "from_" date is wrong'
            },
            {
                'machine':  lambda: m(5).days.and_(10).minutes.ago(),
                'expected': lambda: m(10).minutes.ago(from_=m(5).days.ago()),
                'msg':      'calculation with "and" chain is wrong'
            },
            {
                'machine':  lambda: m(9).days.and_(8).hours.and_(7).seconds.later(),
                'expected': lambda: now() + timedelta(days=9, hours=8, seconds=7),
                'msg':      'calculation with long chain is wrong'
            }          
        ]
        
        for exp in experiments:
            response = exp['machine']()
            self.assert_equals_dates(response, exp['expected'](), msg=exp.get('msg'))

    def test_singular_date_component(self):
        experiments = ['day', 'hour', 'minute', 'second', 'microsecond']

        for exp in experiments:
            from_ = datetime(2012, 10, 11)
            kwargs = {exp + 's': 1}
            expected = from_ - timedelta(**kwargs)
            msg_error = 'singular form for "%s" does not supported' % exp
            self.assertEquals(getattr(m(1), exp).ago(from_=from_), expected, msg_error)


class TestUtils(TestCase):
    def test_get_date_withot_ms(self):
        date =     datetime(year=2012, month=2, day=23, hour=20, minute=39, second=54, microsecond=3)
        expected = datetime(year=2012, month=2, day=23, hour=20, minute=39, second=54)
        self.assertEquals(machine_utils.get_date_withot_ms(date), expected)
