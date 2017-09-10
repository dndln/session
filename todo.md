TODO:

implement add_player_to_court(), delete_player(),
fill_gaps(), get_game(), finish_session()

need to save the state of the 'session' every step, for when someone breaks it

Need to hash out skill pairing rules; how long to leave someone in the pool?
skill levels can be floats, algorithm to determine pairings

serialize the Session object to save/load state, using pickle/db - done

Will not want Session.recalc_pool() to automatically trigger on Session.add_player(),
if using the Session.set_court() workflow. Players will end up in the queue.

Currently implemented as mutating state of attributes of an instance of a Session() class.
Complex, entangling state and time. 
Could be made simple by returning a new Session() state every time an operation is called.
Refactor/rewrite so it's functional.
