import os
import time
import random
import pickle
import copy

import pandas as pd
import numpy as np
import itertools
import ipdb
import datetime
from pprint import pprint
import logging

# what if there aren't enough players to fit in all courts?
# Players will sit in the pool until there's 8 players
# can manually set_court each time

class Session(object):
    """
    A session has a 'pool' (list of players), 'queue' (list of lists of 4
    players), and 'courts'.

    Players sit in the pool. New players are added to the back of the pool.
    When the pool is bigger than 8 players,
    a recalculation is triggered, randomly pairing the first 8 players into
    2 groups of 4, and adding them to the queue.

    When a game finishes on a 'court', the players on that court are moved to the
    back of the 'pool', and the first group in the 'queue' is popped and assigned
    to the free court.
    """

    def __init__(self):
        # can change this to an input if necessary
        self.courts = 2 # for testing
        self.member_df = pd.read_excel('member_list.xlsx')
        self.init_player_list = []
        for index, row in self.member_df.iterrows():
            curr_name = row['name']
            curr_skill_level = row['skill_level']
            new_player = Player(curr_name, skill_level=curr_skill_level)
            self.init_player_list.append(new_player)
        self.court_list = [Court(i) for i in range(1, self.courts + 1)]
        self.pool = self.init_player_list # for testing, in prod 'pool' will start empty
        # need to copy it, otherwise 'pool' and 'full_player_list' will reference the same object
        self.full_player_list = self.init_player_list.copy() # for testing, in prod 'pool' will start empty
        self.current_player_list = self.init_player_list.copy()
        self.queue = []
        self.finished_games_list = []
        # self.running = True # implement a while loop
        self.info()

    def add_player(self, name, skill_level=None):
        new_player = Player(name, skill_level=skill_level)
        self.full_player_list.append(new_player)
        self.current_player_list.append(new_player)
        self.pool.append(new_player)
        logging.info(f'Player {name} added with skill level {skill_level}.')

        pool_length = len(self.pool)
        if pool_length >= 8:
            logging.info(f'Pool has {pool_length} players, recalculating.')
            self.recalc_pool()
        else:
            logging.info(f'Pool has {pool_length} players, not recalculating.')
            return

    def set_court(self, p1_id, p2_id, p3_id, p4_id, court_id):
        # sets four players from the pool into a court.
        court = self.get_court(court_id) # might be None
        if court is None:
            logging.warning('That court does not exist.')
            return

        if court.player_list != []:
            logging.warning('There are players still on the court!')
            return

        for player_id in [p1_id, p2_id, p3_id, p4_id]:
            self.add_player_to_court(player_id, court_id)

    def add_player_to_court(self, player_id, court_id):
        player = self.get_current_player(player_id)
        if player is None:
            logging.warning(f'Player with id {player_id} not currently playing.')
            return

        player_ids_on_court = [player.id for court in self.court_list for player in court.player_list]
        if player_id in player_ids_on_court:
            logging.warning(f'Player with id {player_id} is already on a court!')
            return



        # ssss

        # remove player from pool+queue if they're in there
        # should it also remove players from the queue?
        # if so, should call self.fill_gaps()


        raise NotImplementedError

    def get_current_player(self, player_id):
        return next((x for x in self.current_player_list if x.id == player_id), None)

    def get_player(self, player_id):
        return next((x for x in self.full_player_list if x.id == player_id), None)

    def get_court(self, court_id):
        return next((x for x in self.court_list if x.id == court_id), None)

    def get_game(self, game_id):
        # Search finished_games_list first, then all available courts for the game_id.
        # else log warning and return
        raise NotImplementedError

    def delete_player(self, player_id):
        # remove a Player from the full_player_list, pool, queue, and all courts.

        # does NOT remove them from self.full_player_list
        # removes them from self.current_player_list

        # automatically call fill_courts if a person was deleted from a court?
        # The person using the program needs to be notified.
        raise NotImplementedError

    def remove_player_from_court(self, player_id, court_id):
        ''' Move a player from a court back into the pool. '''
        court = self.get_court(court_id)
        if court is None:
            logging.warning(f'Court with id {court_id} not found!')
            return

        flag = 0
        for index, player in enumerate(court.player_list):
            if player.id == player_id:
                flag = 1
                self.pool.append(player)
                del court.player_list[index]
                logging.info(f'Player {player.name} moved from court {court_id} to pool.')

        if flag == 0:
            logging.warning(f'Player with id {player_id} not found on court {court_id}!')

    def remove_player_from_list(self, curr_list, player_id):
        for index, element in enumerate(curr_list):
            if isinstance(element, Player) and elemend.id == player_id:
                del curr_list[index]

    def recalc_pool(self):
        logging.info('Recalculating pool.')
        if len(self.pool) < 8:
            logging.critical(f'There are only {len(self.pool)} players in the pool!')
            return
        # if there are over 8 players in the pool, make 2 new groups and add to queue
        first_eight = self.pool[:8]
        random.shuffle(first_eight)
        self.pool = self.pool[8:]

        self.queue.append(first_eight[:4])
        self.queue.append(first_eight[4:])

        # the critical log above isn't triggered if at least one recalc_pool() occurs
        if len(self.pool) >= 8:
            self.recalc_pool()

        # can initially comment this out for the demo
        if any(court.player_list == [] for court in self.court_list):
            logging.info('An empty court has been detected, triggering court recalculation.')
            self.recalc_courts()

        # once groups are implemented, logic will need to be added here. What if first_eight are groups of (3, 3, 2)?
        # Will need to add them to queue, then call self.fill_gaps()
        # maybe: if no groups in first_eight, do as normal. Else, add two groups to the pool and call fill_gaps?
        # Will need to check if there's enough people in the pool to fill the gaps.

    def fill_gaps(self):
        logging.info('Filling gaps.')
        raise NotImplementedError
        # if any court is missing players (from 'remove_player'), fill in the
        # gaps with the first players in 'pool'

        # Also fill in gaps in the queue.
        pass

    def recalc_courts(self):
        logging.info('Recalculating courts.')
        # for any courts which are empty,
        for court in self.court_list:
            if court.player_list == []:
                try:
                    court.player_list = self.queue.pop(0)
                    court.game = Game(court.player_list.copy(), court.id)
                    logging.info(f'Court {court.id} recalculated.')
                except IndexError as e:
                    logging.warning('There is a free court, but the queue is empty!')
                    return

    def end_court(self, court):
        court.game.end_datetime = datetime.datetime.now()
        court.game.game_length = str(court.game.end_datetime - court.game.start_datetime)
        # deepcopy is not necessary in this case, as court.game will point to None,
        # and wont have a chance to modify court.game, but it's a nice to have.
        self.finished_games_list.append(copy.deepcopy(court.game))
        court.game = None

        for player in court.player_list:
            self.pool.append(player)
        court.player_list = []

    def finish_court(self, court_id):
        logging.info(f'Finishing Court Number {court_id}.')
        # "finish" the game on Court(court_id).

        # append the players to the pool, and move the players in the
        # first group in the queue onto the court. (call recalc_courts)
        # There may be less than 4 players in the game, as players might get removed.
        court = next((x for x in self.court_list if x.id == court_id), None)
        if court is None:
            logging.critical(f'Court with id {court_id} not found!')
            return

        if court.game is None:
            logging.critical(f'No game on court {court_id}!')
            return

        self.end_court(court)

        self.recalc_courts()

        if len(self.pool) >= 8:
            logging.info('Automatic pool recalucation triggered.')
            self.recalc_pool()

    def finish_session(self):
        # finish all courts, not recalculating.
        for court in self.court_list:
            self.end_court(court)

        # self.save_file()

        # write summary of session to csv
        player_df = self.get_player_info()
        # ssss



    def save_file(self):
        filename = time.strftime('%Y%m%d%H%M%S') + '.p'
        fobj = open(os.path.join('pickle_states', filename), 'wb')
        pickle.dump(self, fobj)
        fobj.close()

    def player_info(self):
        print(self.get_player_info())

    def get_player_info(self):
        player_names = [player.name for player in self.full_player_list]
        player_ids = [player.id for player in self.full_player_list]
        player_skill_levels = [player.skill_level for player in self.full_player_list]
        player_df = pd.DataFrame({
            'player_name': player_names,
            'player_id': player_ids,
            'player_skill_level': player_skill_levels
        })
        return player_df

    def info(self):
        # display an overview of the session.
        # print pool, queue, and courts
        print('=' * 32)
        print('Pool:')
        pprint(self.pool)
        print('Queue:')
        pprint(self.queue)
        print('Courts:')
        for court in self.court_list:
            print(str(court) + ':')
            print(str(court.game))
            print(court.player_list)
        print('=' * 32)





# finding instance by atribute value
# https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi
# next((x for x in test_list if x.value == value), None)
#
# for x in test_list:
#     if x.value == value:
#         print('I found it!')
#         break


class Court(object):
    def __init__(self, court_id):
        self.id = court_id
        self.player_list = []
        self.game = None # will be the current game

    def __str__(self):
        return 'Court(' + str(self.id) + ')'

    def __repr__(self):
        return self.__str__()

class Player(object):
    id_counter = itertools.count()
    def __init__(self, name, skill_level=None):
        self.name = name
        self.id = next(Player.id_counter)
        if skill_level is None:
            self.skill_level = skill_level
        else:
            self.skill_level = int(skill_level)

    def __str__(self):
        return 'Player(' + str(self.name) + ', ' + str(self.id) + ')'

    def __repr__(self):
        return self.__str__()

class Game(object):
    id_counter = itertools.count()
    # for a Game() to exist, it must have a player_list and a court_id.
    # Could add Teams, and results, but then people won't be able to choose their teams.
    # Or I'd need to add methods to swap people from their assigned teams.
    # session.finish_court() would also need to take an (optional) result.
    def __init__(self, player_list, court_id):
        self.id = next(Game.id_counter)
        self.start_datetime = datetime.datetime.now()
        self.end_datetime = None
        self.game_length = None
        self.court_id = court_id
        self.player_list = player_list

    def __str__(self):
        return 'Game(' + str(self.id) + ')'

    def __repr__(self):
        return self.__str__()
