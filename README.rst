=======
Env2048
=======

OpenAI Gym environment for the game 2048!

- Free software: 3-clause BSD license

Features
--------

- Any size game board!

- Rendering support with PyGame!

    You can also get an array of pixels with :code:`mode='rgb_array'` for training image-based agents.
    
- Different reward types! Set the :code:`reward_type` parameter on initialization.

    :code:`'score'` uses the normal score update from the game.
    
        This is the sum of all tiles created by merging that occurred after an action.
        
        So if two 8 tiles are merged after an action, then the reward is +16.
        
    :code:`'survival'` gives a reward of +1.0 on every timestep unless:
    
        The action did not produce a change in state; reward is -0.1.
        
        The game is over; reward is 0.0.
        
    :code:`'milestone'` gives a reward of +10.0 every time a new tile is reached.

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
        observation, reward, done, info = env.step(action)
        env.render()
