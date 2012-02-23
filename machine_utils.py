# -*- coding: utf-8 -*-
import datetime


def get_date_withot_ms(date):
    """Removes microseconds from date

    @type date: datetime.datetime
    @rtype: datetime.datetime

    """
    return datetime.datetime(*tuple(date.timetuple())[:6])