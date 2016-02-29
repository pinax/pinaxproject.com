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

The ``pinaxproject.com`` documentation is currently under construction. If you would like to help us write documentation, please join our Pinax Project Slack team and let us know! The Pinax documentation is available at http://pinaxproject.com/pinax/.


Contribute
----------------

See this blog post http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/ including a video, or our How to Contribute (http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our Ways to Contribute/What We Need Help With (http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions, we would recommend for you to join our Pinax Slack team (http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We would also highly recommend for your to read our Open Source and Self-Care blog post (http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).  


Code of Conduct
-----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/. We'd like to ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


Pinax Project Blog and Twitter
-------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.


