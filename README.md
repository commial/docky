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

Available options :
```ShellSession
$> python docky.py 
Minimalist Docker client.

Actions:
  clean                   Cleanning actions               
  images                List available images             
   pull     Pull an image or a repository from a registry 
  search                 Search for an image              
 transfer   Transfer an image from a registry to another
```

To select an action, use `python docky.py [ACTION] [ACTION ARGUMENTS]`. *Docky* automatically completes the command line: `python docky.py c` is equivalent to `python docky.py clean`.

Clean
-----

```Org
$ python docky.py clean
7 images unammed ('<none>:<none>') founds.
Remove them (N)? y
Removing 915e79a73c...
Removing 95d070bc92...
Removing 1d9496e2b5...
Removing 97e5b30b1c...
Removing 1762a60e76...
Removing facad4c7eb...
Removing 50f90cae2a...
3 containers exited founds.
       NAME       |           IMAGE           | COMMAND               
--------------------------------------------------------
    high_morse    |      imatest:latest       | /bin/sh 
 focused_poincare | 192.168.20.20/test:v0.321 | /bin/sh
 pensive_lumiere  | 192.168.20.20/test:v0.322 | /bin/sh
Remove some of them (N)? y
        Remove high_morse (N)? n
        Remove focused_poincare (N)? n
        Remove pensive_lumiere (N)? y
1 identities founds: 
        - user1@127.0.0.1:5000
        - usertest@192.168.20.20
Remove some of them (N)? y
        Remove user1@127.0.0.1:5000 (N)? y
        Remove usertest@192.168.20.20 (N)? n
```

Images
------

Registries name are translated according to the configuration:

```Org
$ python docky.py images
   REGISTRY    |  REPOSITORY   |  TAG   |  IMAGE ID  |       CREATED       | VIRTUAL SIZE 
------------------------------------------------------------------------------------------
     Local     | commial/sibyl | latest | 2f3ee6fef3 | 21/10/2014 16:51:18 |   429.4 MB   
   Docker.io   | commial/sibyl | latest | 2f3ee6fef3 | 21/10/2014 16:51:18 |   429.4 MB   
   Docker.io   | miasm/tested  | latest | dfce8fc63a | 21/10/2014 08:59:30 |   429.3 MB   
     Local     |     miasm     |  base  | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
   Docker.io   |  miasm/base   | latest | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
     Local     |  miasm/base   | latest | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
   Docker.io   |    debian     | jessie | ff478fc127 | 23/09/2014 22:38:34 |   115.0 MB   
   Docker.io   |    ubuntu     | latest | 826544226f | 04/09/2014 18:41:55 |   194.2 MB   
   Docker.io   |   registry    | latest | e42d15ec84 | 27/08/2014 02:38:29 |   455.0 MB   
   Docker.io   |    debian     | latest | c1eec48018 | 12/08/2014 03:54:58 |   85.2 MB 
```

To sort images:
```Org
$ python docky.py images -s REGISTRY
   REGISTRY    |  REPOSITORY   |  TAG   |  IMAGE ID  |       CREATED       | VIRTUAL SIZE 
------------------------------------------------------------------------------------------
   Docker.io   | commial/sibyl | latest | 2f3ee6fef3 | 21/10/2014 16:51:18 |   429.4 MB   
   Docker.io   | miasm/tested  | latest | dfce8fc63a | 21/10/2014 08:59:30 |   429.3 MB   
   Docker.io   |  miasm/base   | latest | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
   Docker.io   |    debian     | jessie | ff478fc127 | 23/09/2014 22:38:34 |   115.0 MB   
   Docker.io   |    ubuntu     | latest | 826544226f | 04/09/2014 18:41:55 |   194.2 MB   
   Docker.io   |   registry    | latest | e42d15ec84 | 27/08/2014 02:38:29 |   455.0 MB   
   Docker.io   |    debian     | latest | c1eec48018 | 12/08/2014 03:54:58 |   85.2 MB    
     Local     | commial/sibyl | latest | 2f3ee6fef3 | 21/10/2014 16:51:18 |   429.4 MB   
     Local     |     miasm     |  base  | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
     Local     |  miasm/base   | latest | 35cf8a7cf4 | 29/09/2014 15:43:00 |   440.0 MB   
```

*Docky* automatically completes command line: `docky.py images -s C` is equivalent to `docky.py images -s CREATED`.

Pull
----

Optional arguments are:
```ShellSession
  -r REGISTRY, --registry REGISTRY
                        Source registry (default is Docker.io)
  -w, --with-creds      Include credential while pulling (default is not)
```

Names, instead of URL, can be used for registry argument:
```ShellSession
$ python docky.py pull -r Local miasm
Pulling 127.0.0.1:5000/miasm...
Download complete layers
```

Search
------

```ShellSession
$ python docky.py search miasm
Local
=====

     NAME      | DESCRIPTION | AUTO-BUILD | OFFICIAL | STARS 
-------------------------------------------------------------
  miasm/base   |             |            |          |       
 library/miasm |             |            |          |       
Docker.io
=========

     NAME     | DESCRIPTION | AUTO-BUILD | OFFICIAL | STARS 
------------------------------------------------------------
  miasm/base  |             |     OK     |          |       
 miasm/tested |             |     OK     |          |       

```

Transfer
--------

Optional arguments are:
```ShellSession
  -f FROM, --from FROM  Source registry (default is Docker.io)
  -t TO, --to TO        Destination registry (default is Docker.io)
```

Transferring official `debian:jessie` image to linux on the `Local` registry:
```ShellSession
$ python docky.py transfer debian:jessie -t Local linux
Transfer debian:jessie -> 127.0.0.1:5000/linux:latest (Y)? 
'debian:jessie' is locally available (ff478fc127), use it
Pushing...
Pushing tag for rev [ff478fc12717] on {http://127.0.0.1:5000/v1/repositories/linux/tags/latest}
Transfer complete !
```

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
