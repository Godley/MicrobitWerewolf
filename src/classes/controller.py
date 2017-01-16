from enum import Enum
from transitions import Machine
import time, queue, random, copy

class States(Enum):
    REGISTER = 0
    NIGHT_WOLVES = 1
    NIGHT_DOCTOR = 2
    NIGHT_SEER = 3
    DAYTIME_ANNOUNCE = 4
    DAYTIME_VOTE = 5
    DAYTIME_KILL = 6
    END_GAME = 7



class Controller(object):
    states = ["register", "night_wolves", "night_doctor", "night_seer", "daytime_announce",
              "daytime_vote", "daytime_kill"]
    transitions = [{"trigger": "all_registered",
                "source": "register",
                "dest": "night_wolves"},
    {"trigger": "wolves_voted",
     "source": "night_wolves",
     "dest": "night_doctor"},
    {"trigger": "doctor_voted",
     "source": "night_doctor",
     "dest": "night_seer"},
    {"trigger": "seer_voted",
     "source": "night_seer",
     "dest": "daytime_announce"},
    {"trigger": "announced",
     "source": "daytime_vote",
     "dest": "daytime_kill"},
    {"trigger": "killed",
     "source": "daytime_kill",
     "dest": "night_wolves"},
        {"trigger": "win",
         "source": "*",
         "dest": "end_game"}]
    players = []
    queue = queue.Queue()

    def __init__(self):
        self.machine = Machine(model=self, transitions=self.transitions, states=self.states, initial="register")

    def await_registration(self, period=1.0, limit=60.0):
        start = time.time()
        end = time.time()
        while end - start < limit:
            try:
                player = self.get_player()
                if player not in self.players:
                    self.players.append(player)
            except:
                pass
            end = time.time()
        self.all_registered()

    def sort_players(self, players):
        orgs = {"wolves": [],
                "villagers": []}
        duplicate = copy.deepcopy(players)
        while len(duplicate) > 0:
            elem = random.choice(duplicate)
            if len(orgs["wolves"]) < 2:
                orgs["wolves"].append(elem)

            elif "seer" not in orgs:
                orgs["seer"] = elem

            elif "doctor" not in orgs:
                orgs["doctor"] = elem

            else:
                orgs["villagers"].append(elem)
            duplicate.remove(elem)

        return orgs

    def add_player(self, data):
        self.queue.put(data)

    def get_player(self):
        return self.queue.get(timeout=1.0)