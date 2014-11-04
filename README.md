This file is part of Docky.

Copyright 2014 [Camille MOUGEY](mailto:commial@gmail.com)

Docky
=====

A lightweight client, multi-registries aware, for [Docker](https://docker.io).

Why Docky ?
===========

The *Docker* client provided by *Docker* authors is full of feature and works
pretty well. But currently, we found it boring while working with several
registries. That's why we made *Docky*.

*Docky* **does not aim to clone official** *Docker* client features.

*Docky* focus on boring and / or repetitive tasks while working with *Docker*.

Features
========

TODO

Configuration
=============

The configuration is located in the file `docky.conf`.

In the `General` section:
* `server`: URI of the *Docker* daemon
* `timeout`: Timeout for connexion
* `enabled`: Enabled registries, separated by a comma

For each registry, there is a section with:

* `index`: URL of the registry's index
* `registry`: URL of the registry's registry

For instance, a configuration file with a local registry listenning on port
`5000` and the official one:

```Config
[General]
server = unix://var/run/docker.sock
timeout = 10
enabled = Local,Docker.io

[Local]
index = 127.0.0.1:5000
registry = %(index)s

[Docker.io]
index = index.docker.io:80
registry = registry.docker.io:80
```

Install
=======

*Docky* depends on the [docker-py](https://github.com/docker/docker-py) module
 (ver >= 0.5.1-dev). See `requirements.txt`.

Contribute
==========

For now, *Docky* provides just a few actions. Feel free to contribute !

Adding an action
----------------

Actions are *Docky* features. There are located in `action` directory.

Typically, an action inherits from `Action` class, located in
`action/action.py`.

Attributes and methods to override are:

* `_name_`: the action name
* `_desc_`: the action description, displayed in the help
* `_args_` (optional): a list of *(list, dictionnary)* which handle argument
  parsing. `ArgumentParser.add_argument` will be called with each list element
* `run()`: the method called when the action is invoked.

Parsed arguments are saved in the attribute `args`.

To allow your action to be called from *Docky* client, add a reference to the
action class in `ACTIONS`, located in `action/__init__.py`.
