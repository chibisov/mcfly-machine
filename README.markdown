![McFly machine](http://github.com/chibisov/mcfly-machine/raw/master/machine.png "McFly machine")

#### Marty McFly machine for python

    from mcfly_machine import Machine as m
    from datetime import datetime

    print datetime.now()
    # => datetime.datetime(2012, 2, 23, 22, 11, 40, 283787)

    print m(5).days.ago()
    # => datetime.datetime(2012, 2, 18, 22, 11, 40, 283787)

For single component you can use singular form:

    print m(1).day.later()
    # => datetime.datetime(2012, 2, 24, 22, 11, 40, 283787)
    m(1).hour.ago()

Not only ints:

    m(1.5).hours.ago()

You can chain date components with 'and_' method:

    m(9).days.and_(8).hours.ago()
    m(9).days.and_(8).hours.and_(1).second.and_(10).microseconds.later()

By default timedelta calculates from datetime.now(). You can change it:

    m(9).days.ago(from_=datetime(1990, 2, 3))

Force to use datetime.utcnow():

    m(9).days.ago(in_utc=True)

