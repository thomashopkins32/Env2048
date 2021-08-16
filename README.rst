======
2048AI
======

Collection of intelligent algorithms that attempt to beat the game 2048.

* Free software: 3-clause BSD license

Features
--------

* Any size game board
* Play manually from the keyboard
* Interactive GUI for selecting different agents

Installation
------------

To try it out yourself:

.. code-block:: bash

    $ git clone https://github.com/thomashopkins32/2048AI.git
    $ cd 2048AI/AI2048
    $ python gui.py
    
For manual play, select ``ManualTextAgent`` or ``KeyboardAgent`` from the drop-down menu and hit ``Start``.

Choose other agents for AI solutions to the game.

Configure various game, learning, and other parameters by editing the ``config/{Agent}.yml`` file.
