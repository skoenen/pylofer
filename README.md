# pyprol - Python Performance Measurement System

STATE: 3 - Alpha
Version: 0.1.0

This hooks up to some points in various frameworks to measure several aspects
of execution of code.

In special there are injections of instrumentation code in
paster `WSGIHandlerMixin`, pylons 'WSGIControler'.

To store the optained values in a way mostly unaffecting the application, the
values are send over udp to an server.

## Usage:

`paster deploy`:

Add a filter to your application as following:

    ...

    [pipeline:default]
    pipeline = pyprol app

    [filter:pyprol]
    use = egg:pyprol
    pyprol.storage = `<sqlite storage location goes here>` # One can use environment variables.

    ...

## Configuration:

`pyprol` has a builtin configuration that takes care of needed options for a
start.

However, to change the default behaviour of `pyprol`, use the following
options:

  * `builtin_instrumentations` boolean: True
  * `instrumentations` list: None
  * `storage` string: `'sqlite://$HOME/pyprol.db`
