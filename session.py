import os
import pickle
import time
import random

import datetime
import glob
import ipdb
import itertools
import logging
import numpy as np
import pandas as pd
from pprint import pprint

# session_classes is a file, not a folder
from session_classes import Session, Court, Player, Game


logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')

def load_latest_file():
    g = glob.glob(os.path.join('pickle_states', '*.p'))
    latest_filepath = sorted(g)[-1]
    session = load_file(latest_filepath)
    return session

def load_file(filepath):
    objects = []
    with (open(filepath, 'rb')) as fobj:
        while True:
            try:
                objects.append(pickle.load(fobj))
            except EOFError:
                break
    return objects[0]

def load_test():
    objects = []
    with (open('test.pickle', 'rb')) as fobj:
        while True:
            try:
                objects.append(pickle.load(fobj))
            except EOFError:
                break
    return objects[0]

def main():

    # se = Session()
    # se.info()
    # se.recalc_pool()
    # se.recalc_courts()
    # se.finish_court(1)

    # restart, and use the add/player + set_court workflow instead of recalc_pool() to kick off
    # se.add_player("bob's your uncle") x4
    # se.set_court() # NotImplementedError

    # can demo se.finished_games_list()

    # se.remove_player_from_court(player_id, court_id)
    # se.player_info()

    # se.save_file()
    # se = load_latest_file()
    ipdb.set_trace()



if __name__ == '__main__':
    main()
