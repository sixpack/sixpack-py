Sixpack
=======

Python client library for SeatGeak's Sixpack_ ab testing framework.

.. _Sixpack: http://github.com/seatgeek/sixpack

Installation
------------

First install in your virtual environment::

    $ pip install sixpack-client

Usage
-----

Basic example::


    from sixpack.sixpack import Session

    session = Session()

    # Participate in a test (creates the test if necessary)
    session.participate("new-test", ["alternative-1", "alternative-2"])

    # Convert
    session.convert("new-test")

Each session has a `client_id` associated with it that must be preserved across requests. Here's what the first request might look like::

    session = Session()
    resp = session.participate("new-test", ["alternative-1", "alternative-2"])
    set_cookie_in_your_web_framework("sixpack-id", session.client_id)


You can then make decisions in your application based on resp['alternative']['name']::

    session = Session()
    resp = session.participate("new-test", ["alt-1", "alt-2"])
    if resp["alternative"]["name"] == "alt-1":
        set_variable_in_view("new-test-alternative", "alt-1")

For future requests, create the `Session` using the `client_id` stored in the cookie::

    client_id = get_cookie_from_web_framework("sixpack-id")
    session = Session(client_id=client_id)
    session.convert("new-test")

Sessions can take an optional `options` dictionary that takes `host` and `timeout` as keys. This allows you to customize Sixpack's location.::

    options = {'host': 'http://mysixpacklocation.com'}
    session = Session(client_id="123", options=options)

If Sixpack is unreachable or other errors occur, sixpack-py will provide the control alternative.


Contributing
------------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
