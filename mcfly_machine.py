# -*- coding: utf-8 -*-
import datetime


class Machine(object):
    def __init__(self, number):
        self.number = number
        self.timedelta_components = {
            'days':         0,
            'hours':        0,
            'seconds':      0,
            'minutes':      0,
            'microseconds': 0,
        }

    def _clean_date_component_name(self, name):
        """Cleanes date component name

        >>> self._clean_date_component_name('day')
        days

        """
        if not name.endswith('s'):
            name += 's'
        return name

    def _update_timedelta_components(self, date_component_name):
        self.timedelta_components[date_component_name] += self.number
        return self

    def _get_current_timedelta(self):
        return datetime.timedelta(**self.timedelta_components)

    def _calculate_date(self, from_, time_direction, in_utc):
        if not from_:
            if in_utc:
                from_ = datetime.datetime.utcnow()
            else:
                from_ = datetime.datetime.now()

        if time_direction == 'past':
            return from_ - self._get_current_timedelta()
        else:
            return from_ + self._get_current_timedelta()

    def and_(self, number):
        self.number = number
        return self

    def ago(self, from_=None, in_utc=False):
        return self._calculate_date(from_=from_, time_direction='past', in_utc=in_utc)

    def later(self, from_=None, in_utc=False):
        return self._calculate_date(from_=from_, time_direction='future', in_utc=in_utc)

    def __getattr__(self, attr_name):
        cleaned_attr_name = self._clean_date_component_name(attr_name)

        if cleaned_attr_name in self.timedelta_components.keys():
            return self._update_timedelta_components(cleaned_attr_name)
        else:
            raise AttributeError(attr_name)

