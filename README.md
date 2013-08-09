# pyprol - Python Performance Measurement System

STATE: 2 - pre-alpha
Version: -.-.-

This hooks up to some points in various frameworks to measure several aspects
of execution of code.

In special there are injections of instrumentation code in
paster `WSGIHandlerMixin`, pylons 'WSGIControler'.

To store the optained values in a way mostly unaffecting the application, the
values are send over udp to an server.

## Configuration:

`pyprol` has a builtin configuration that takes care of needed options for a
start.

However, to change the default behaviour of `pyprol`, use the following
options:

  * `builtin_instrumentations` boolean: True
  * `instrumentations` list: None
  * `storage` string: `'sqlite://$HOME/pyprol.db`
