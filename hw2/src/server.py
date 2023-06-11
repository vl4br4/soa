import grpc
import mafia_pb2
import mafia_pb2_grpc
from concurrent import futures
from collections import defaultdict
from enum import Enum
import random
from threading import Lock
import time
import queue


class MafiaServer(mafia_pb2_grpc.MafiaGameServicer):
    class Round:
        def __init__(self) -> None:
            self.vote_table = defaultdict(int)
            self.mafia_turn_done = False
            self.detective_turn_done = False
            self.is_first_round = False
            self.end_day_requests = set()
            self.vote_kill_requests = set()
            self.nightly_killed_player = ""
            self.killed_role = None

    class GameSession:
        def __init__(self) -> None:
            self.players = set()
            self.player_to_role = dict()
            self.round = MafiaServer.Round()
            self.round.is_first_round = True
            self.is_game_started = False
            self.players_to_start = 4
            self.roles_to_assign = [mafia_pb2.MafiaRole.Red, mafia_pb2.MafiaRole.Red, mafia_pb2.MafiaRole.Detective, mafia_pb2.MafiaRole.Mafia]
            self.alive_roles = set(self.roles_to_assign)
            self.is_first_round = True
            self.alive_players = set()
            self.killed_player = None
            self.lock = Lock()
            self.events_queues = dict()
            self.role_to_str = {mafia_pb2.MafiaRole.Red: "Red", mafia_pb2.MafiaRole.Detective: "Detective", mafia_pb2.MafiaRole.Mafia: "Mafia", mafia_pb2.MafiaRole.Dead: "Dead"}

    def __init__(self) -> None:
        self.players = set()
        self.player_to_role = dict()
        self.round = MafiaServer.Round()
        self.round.is_first_round = True
        self.is_game_started = False
        self.players_to_start = 4
        self.roles_to_assign = [mafia_pb2.MafiaRole.Red, mafia_pb2.MafiaRole.Red, mafia_pb2.MafiaRole.Detective, mafia_pb2.MafiaRole.Mafia]
        self.alive_roles = set(self.roles_to_assign)
        self.is_first_round = True
        self.alive_players = set()
        self.killed_player = None
        self.lock = Lock()
        self.events_queues = dict()
        self.role_to_str = {mafia_pb2.MafiaRole.Red: "Red", mafia_pb2.MafiaRole.Detective: "Detective", mafia_pb2.MafiaRole.Mafia: "Mafia", mafia_pb2.MafiaRole.Dead: "Dead"}

    def Join(self, request, context):
        with self.lock:
            if self.is_game_started:
                return mafia_pb2.JoinResponse(Error = 'Game has already started')
            if request.Username in self.players:
                return mafia_pb2.JoinResponse(Error = 'This name is already taken. Please, choose another')
            self.players.add(request.Username)
            self.alive_players.add(request.Username)
            self.events_queues[request.Username] = queue.Queue()
            self.notify_players(update = mafia_pb2.Update(Message = request.Username, Event = mafia_pb2.GameEvent.PlayerJoin))
            if len(self.players) == self.players_to_start:
                for q in self.events_queues:
                    self.events_queues[q].put(mafia_pb2.Update(Event = mafia_pb2.GameEvent.GameStarts, Message = self.assign_role(q)))
            return mafia_pb2.JoinResponse()
        
    def VoteKill(self, request, context):
        err = self.check_possibility(request.Username)
        if err != "":
            return mafia_pb2.VoteKillResponse(err)
        with self.lock:
            if request.WhoToKill not in self.alive_players:
                return mafia_pb2.VoteKillResponse(Error = 'No alive player with such name')
            self.round.vote_kill_requests.add(request.Username)
            self.round.vote_table[request.WhoToKill] += 1
            if len(self.round.vote_kill_requests) == len(self.alive_players):
                killee = self.kill_most_voted()
                if killee == "":
                    self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.VotedNoKill))
                else:
                    is_game_end = self.player_to_role[killee] == mafia_pb2.MafiaRole.Mafia or len(self.alive_players) <= 2
                    self.notify_players(update = mafia_pb2.Update(Message = killee, Event = mafia_pb2.GameEvent.VotedKill, IsGameEnd = is_game_end))
            return mafia_pb2.VoteKillResponse()
        
    def EndTheDay(self, request, context):
        with self.lock:
            err = self.check_possibility(request.Username)
            if err != "":
                return mafia_pb2.EndDayResponse(Error = err)
            if not self.round.is_first_round and request.Username not in self.round.vote_kill_requests:
                return mafia_pb2.EndDayResponse(Error = 'You must make your vote before ending the day')
            self.round.end_day_requests.add(request.Username)
            if len(self.round.end_day_requests) == len(self.alive_players):
                self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.EndOfDay))
            return mafia_pb2.EndDayResponse()
        
    def MafiaKill(self, request, context):
        with self.lock:
            err = self.check_possibility(request.Username)
            if err != "":
                return mafia_pb2.MafiaKillResponse(Error = err)
            if request.WhoToKill not in self.alive_players:
                return mafia_pb2.MafiaKillResponse(Error = 'No such player alive')
            if self.round.mafia_turn_done:
                return mafia_pb2.MafiaKillResponse(Error = 'Your have already killed a player')
            can_switch = self.player_to_role[request.WhoToKill] != mafia_pb2.MafiaRole.Detective or self.round.detective_turn_done
            self.kill_player(request.WhoToKill)
            self.round.nightly_killed_player = request.WhoToKill
            self.round.mafia_turn_done = True
            if (self.round.detective_turn_done or mafia_pb2.MafiaRole.Detective not in self.alive_roles) and can_switch:
                self.swith_round()
        return mafia_pb2.MafiaKillResponse()
    
    def DetectiveCheck(self, request, context):
        with self.lock:
            err = self.check_possibility(request.Username)
            if err != "":
                return mafia_pb2.DetectiveCheckResponse(Error = err)
            if request.WhoToCheck not in self.alive_players:
                return mafia_pb2.DetectiveCheckResponse(Error = 'No such player alive')
            if self.round.detective_turn_done:
                return mafia_pb2.DetectiveCheckResponse(Error = 'Your have already revealed a player')
            self.round.detective_turn_done = True
            if self.round.mafia_turn_done:
                self.swith_round()
            return mafia_pb2.DetectiveCheckResponse(Message = 'You revealed player ' + request.WhoToCheck + '. His role is ' + self.role_to_str[self.player_to_role[request.WhoToCheck]])
            

    def Follow(self, request, context):
        while True:
            update = self.events_queues[request.Username].get(block=True)
            yield update
            with self.lock:
                if update.IsGameEnd:
                    return
                
    def GetPlayers(self, request, context):
        response = mafia_pb2.GetPlayersResponse()
        response.Usernames[:] = list(self.player_to_role.keys())
        response.Roles[:] = ["Dead" if self.player_to_role[player] == mafia_pb2.MafiaRole.Dead else "Alive" for player in self.player_to_role.keys()]
        return response

    def swith_round(self):
        msg = 'This night player ' + self.round.nightly_killed_player + ' was killed. '
        is_game_end = len(self.alive_players) <= 2
        self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.EndOfNight, Message = msg, KilledPlayer = self.round.nightly_killed_player, IsGameEnd = is_game_end))
        self.round = MafiaServer.Round()

    def assign_role(self, player):
        role = random.choice(self.roles_to_assign)
        self.roles_to_assign.remove(role)
        self.player_to_role[player] = role
        return self.role_to_str[role]

    def notify_players(self, update):
        for q_num in self.events_queues:
            self.events_queues[q_num].put(update)

    def check_possibility(self, username):
        if username not in self.players:
            return 'You must join the game first'
        if username not in self.alive_players and not self.round.killed_role == mafia_pb2.MafiaRole.Detective:
            return 'You can\'t use this command because you\'re dead'
        return ""
    
    def kill_most_voted(self):
        killee = ""
        max_votes = 0
        no_agreement = False
        for player in self.round.vote_table:
            if self.round.vote_table[player] > max_votes:
                max_votes = self.round.vote_table[player]
                killee = player
                no_agreement = False
            elif self.round.vote_table[player] == max_votes:
                no_agreement = True
        if no_agreement:
            return ""
        else:
            self.kill_player(killee)
            return killee
    
    def kill_player(self, player):
        self.alive_players.remove(player)
        self.round.killed_role = self.player_to_role[player] 
        self.alive_roles.remove(self.player_to_role[player])
        self.player_to_role[player] = mafia_pb2.MafiaRole.Dead
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mafia_pb2_grpc.add_MafiaGameServicer_to_server(MafiaServer(), server)
    server.add_insecure_port("localhost:50051")
    print('Running...')
    server.start()
    server.wait_for_termination()


def main():
    serve()


main()