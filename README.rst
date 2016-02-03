``rtox``
========

This project represents an experimental development workflow with the following
considerations in mind:

- `tox <https://tox.readthedocs.org/en/latest/>`_ is an excellent tool for
  managing test activities in a `virtualenv
  <https://virtualenv.readthedocs.org/en/latest/>`_.

- Servers in the cloud are faster and far more powerful than my local
  development environment (usually a laptop).

- Latency introduced to the command line by a remote connection, especially on
  bad WiFi, is painful.

- Running huge test suites on a cloud server doesn't drain my laptop's battery
  (or spin up my desktop's fans) like running them locally would.

- Your local development platform might not actually have the binary
  dependencies available that your project requires from your target platform
  (developing a Linux application on OS X, for example).

- Running tests with tox is easy. Running tests with ``rtox`` on a remote
  host against the local codebase should be just as easy.

This project currently makes a few assumptions that you'd have to meet for it
to be useful to you:

- You're a Python developer (that's why you're interested in tox, right?).

- You're using ``git``.

- You're working on a publicly available repository (I'd like to break this
  assumption).

Usage
-----

Configure ``rtox`` with an ``~/.rtox.cfg`` file like the following::

    [ssh]
    user = root
    hostname = localhost
    port = 22

``rtox`` simply needs to be pointed at an SSH host with ``git``, ``tox`` and
``virtualenv`` installed.

Once it's configured, just use ``rtox`` in place of ``tox``. For example::

    $ rtox -e py27 -e pep8

The state of your local codebase will be mirrored to the remote host, and tox
will be executed there.
