import json


def read(filename):
    '''
    Gets the current configuration from a given file

    Parameters
    ----------
    filename : str
        path to JSON file

    Returns
    -------
    dict
        config variables mapped to their values
    '''
    with open(filename, 'r') as config_file:
        config = json.load(config_file)
    return config


def write(filename, config_dict):
    '''
    Overwrites parameters to given configuration file

    Parameters
    ----------
    filename : str
        path to JSON file
    config_dict : dict
        config variables to write
    '''
    with open(filename, 'w') as config_file:
        json.dump(config_dict, config_file)


def append(filename, config_dict):
    '''
    Adds parameters to the given configuration file

    Parameters
    ----------
    filename : str
        path to JSON file
    config_dict : dict
        config variables to write
    '''
    cfg = read(filename)
    cfg.update(config_dict)
    with open(filename, 'w') as config_file:
        json.dump(config_dict, config_file)
