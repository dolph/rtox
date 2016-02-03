rtox
====

This project represents an experimental development workflow with the following
considerations in mind:

- tox is an excellent tool for managing test activities in a virtualenv.

- Servers in the cloud are faster and far more powerful than my local
  development environment (laptop).

- Running huge test suites on a cloud server doesn't drain my laptop's battery
  as much as running them locally would.

- Running tests with tox is easy. Running tests with rtox on a remote machine
  against the local codebase should be just as easy.
