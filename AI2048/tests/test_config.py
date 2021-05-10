import json
import os

import AI2048.config as config


def test_config():
    # normal behavior
    test_dict = {'t1': 0, 't2': [1, 2, 3], 't3': {'t4': 1}}
    config.write('test.json', test_dict)
    cfg = config.read('test.json')
    key_diff = test_dict.keys() - cfg.keys()
    assert(len(key_diff) == 0)
    key_diff = cfg.keys() - test_dict.keys()
    assert(len(key_diff) == 0)
    assert(cfg['t1'] == 0)
    assert(cfg['t2'] == [1, 2, 3])
    assert(cfg['t3'] == {'t4': 1})
    add_dict = {'t5': 2}
    config.append('test.json', add_dict)
    cfg = config.read('test.json')
    assert('t5' in cfg.keys())
    assert(cfg['t5'] == 2)
    os.remove('test.json')

