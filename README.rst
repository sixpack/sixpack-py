Sixpack
=======

Python client library for SeatGeak's Sixpack ab testing framework.

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

    session = Session
    session.participate("new-test", ["alternative-1", "alternative-2"])
    set_cookie_in_your_web_framework("sixpack-id", session.client_id)

For future requests, create the `Session` using the `client_id` stored in the cookie::

    client_id = get_cookie_from_web_framework("sixpack-id")
    session = Session(client_id=client_id)
    session.convert("new-test")

If you already have a client_id (you can generate one using `sixpack.generate_client_id()`) you can use the `participate()` and `convert()` methods to avoid instantiating a `Session` yourself. This can help to clean up your logic a bit::

    from sixpack.sixpack import participate, convert

    partipate("new-test", ["alternative-1", "alternative-2"], client_id)

    convert("new-test", client_id)


Contributing
------------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
