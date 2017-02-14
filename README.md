# rcdat
A simple utility for controlling Mini-Circuits RCDAT programmable attenuator

This interactive terminal application is written in Python. It can be used to
control certain Mini-Circuits programmable attenuators over HTTP. It has only
been tested with the following model numbers:

RCDAT-4000-120

Instructions
--------

If known, the user can directly specify the IP address of the device, e.g.:

    $ python rcdat.py 192.168.1.2

If no argument is provided, the application will attempt to discover the
device's address using a UDP broadcast message on port 4950:

    # python rcdat.py

The end user should change the `DISCOVERY_IP` variable to reflect her local
network broadcast address. Depending on the user's system, it may be necessary
to modify firewall settings or to run the application with elevated privileges.

Submitting changes
--------

If you have any useful additions or changes, please submit them through GitHub:

https://github.com/nowls/rcdat
