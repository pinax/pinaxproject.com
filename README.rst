Pinaxproject.com
================

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/
   

Pinax
------

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.


pinaxproject.com
-----------------

This is the site running at pinaxproject.com http://pinaxproject.com


Setting up Documentation
-------------------------

Create a directory somewhere on your filesystem which will be the
``DOCS_ROOT``. Set the setting ``DOCS_ROOT`` to its path in your
``local_settings.py``.

To setup the documentation run the following commands::

    cd $DOCS_ROOT # fill in with yours
    virtualenv --no-site-packages env
    env/bin/pip install Sphinx==1.0.5
    git clone -b master git@github.com:pinax/pinax.git pinax-master
    git clone -b 0.7.X git@github.com:pinax/pinax.git pinax-0.7.X
    env/bin/sphinx-build -b pickle -aE pinax-0.7.X/docs/ output-0.7.X
    env/bin/sphinx-build -b pickle -aE pinax-master/docs/ output-master

This will be sufficient to run the documentation locally.

To update the docs to the latest version run::

    cd $DOCS_ROOT # fill in with yours
    (cd pinax-0.7.X ; git pull)
    (cd pinax-master ; git pull)
    env/bin/sphinx-build -b pickle -aE pinax-0.7.X/docs/ output-0.7.X
    env/bin/sphinx-build -b pickle -aE pinax-master/docs/ output-master


Documentation
--------------

The Pinax documentation is available at http://pinaxproject.com/pinax/.


Code of Conduct
-----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/.


Pinax Project Blog and Twitter
-------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.


