============
Installation
============

Install `numpy` dependencies::

  sudo apt-get update
  sudo apt-get install -y build-essential python-dev


At the command line::

  pip install pylocating


To install from source code::

  git clone https://github.com/hachreak/pylocating.git
  cd pylocating
  pip install -e .


If you use `python2`, you need to install more dependencies::

  pip install -e .[py2]
