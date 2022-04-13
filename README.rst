======
Env2048
======

OpenAI Gym environment for the game 2048!

* Free software: 3-clause BSD license

Features
--------

* Any size game board!
* `render()` support!
* Different reward types!

Installation
------------

To try it out yourself:

.. code-block:: bash

    $ git clone https://github.com/thomashopkins32/Env2048.git
    $ cd Env2048
    $ pip install .

Example Usage
-------------

Here is an example using random actions:

.. code-block:: python3

   from env2048.env import Env2048
   env = Env2048()
   observation = env.reset()
   env.render()
   done = False
   while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(a)
        env.render()
