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
import chat


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
        self.session_cnt = 0
        self.sessions = dict()
        self.sessions[self.session_cnt] = MafiaServer.GameSession()
        self.chat_server = chat.ChatServer()
        self.chat_server.init_new_chat(self.session_cnt)

    def Join(self, request, context):
        session = self.sessions[self.session_cnt]
        with session.lock:
            if session.is_game_started:
                return mafia_pb2.JoinResponse(Error = 'Game has already started')
            if request.Username in session.players:
                return mafia_pb2.JoinResponse(Error = 'This name is already taken. Please, choose another')
            session.players.add(request.Username)
            session.alive_players.add(request.Username)
            session.events_queues[request.Username] = queue.Queue()
            self.notify_players(update = mafia_pb2.Update(Message = request.Username, Event = mafia_pb2.GameEvent.PlayerJoin), session = session)
            session_id = self.session_cnt
            if len(session.players) == session.players_to_start:
                self.session_cnt += 1
                self.sessions[self.session_cnt] = MafiaServer.GameSession()
                self.chat_server.init_new_chat(self.session_cnt)
                for q in session.events_queues:
                    session.events_queues[q].put(mafia_pb2.Update(Event = mafia_pb2.GameEvent.GameStarts, Message = self.assign_role(q, session)))
            return mafia_pb2.JoinResponse(SessionId = session_id)
        
    def VoteKill(self, request, context):
        session = self.sessions[request.SessionId]
        err = self.check_possibility(request.Username, session)
        if session.round.is_first_round:
            return mafia_pb2.VoteKillResponse(Error = 'Cant vote in first round')
        if err != "":
            return mafia_pb2.VoteKillResponse(Error = err)
        with session.lock:
            if request.WhoToKill not in session.alive_players:
                return mafia_pb2.VoteKillResponse(Error = 'No alive player with such name')
            session.round.vote_kill_requests.add(request.Username)
            session.round.vote_table[request.WhoToKill] += 1
            if len(session.round.vote_kill_requests) == len(session.alive_players):
                killee = self.kill_most_voted(session)
                if killee == "":
                    self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.VotedNoKill), session=session)
                else:
                    is_game_end = session.player_to_role[killee] == mafia_pb2.MafiaRole.Mafia or len(session.alive_players) <= 2
                    self.notify_players(update = mafia_pb2.Update(Message = killee, Event = mafia_pb2.GameEvent.VotedKill, IsGameEnd = is_game_end, MafiaWin = len(session.alive_players) <= 2), session=session)
            return mafia_pb2.VoteKillResponse()
        
    def EndTheDay(self, request, context):
        session = self.sessions[request.SessionId]
        with session.lock:
            err = self.check_possibility(request.Username, session)
            if err != "":
                return mafia_pb2.EndDayResponse(Error = err)
            if not session.round.is_first_round and request.Username not in session.round.vote_kill_requests:
                return mafia_pb2.EndDayResponse(Error = 'You must make your vote before ending the day')
            session.round.end_day_requests.add(request.Username)
            if len(session.round.end_day_requests) == len(session.alive_players):
                self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.EndOfDay), session=session)
            return mafia_pb2.EndDayResponse()
        
    def MafiaKill(self, request, context):
        session = self.sessions[request.SessionId]
        with session.lock:
            err = self.check_possibility(request.Username, session)
            if err != "":
                return mafia_pb2.MafiaKillResponse(Error = err)
            if request.WhoToKill not in session.alive_players:
                return mafia_pb2.MafiaKillResponse(Error = 'No such player alive')
            if session.round.mafia_turn_done:
                return mafia_pb2.MafiaKillResponse(Error = 'Your have already killed a player')
            can_switch = session.player_to_role[request.WhoToKill] != mafia_pb2.MafiaRole.Detective or session.round.detective_turn_done
            self.kill_player(request.WhoToKill, session)
            session.round.nightly_killed_player = request.WhoToKill
            session.round.mafia_turn_done = True
            if (session.round.detective_turn_done or mafia_pb2.MafiaRole.Detective not in session.alive_roles) and can_switch:
                self.swith_round(session)
        return mafia_pb2.MafiaKillResponse()
    
    def DetectiveCheck(self, request, context):
        session = self.sessions[request.SessionId]
        with session.lock:
            err = self.check_possibility(request.Username, session)
            if err != "":
                return mafia_pb2.DetectiveCheckResponse(Error = err)
            if request.WhoToCheck not in session.alive_players:
                return mafia_pb2.DetectiveCheckResponse(Error = 'No such player alive')
            if session.round.detective_turn_done:
                return mafia_pb2.DetectiveCheckResponse(Error = 'Your have already revealed a player')
            session.round.detective_turn_done = True
            if session.round.mafia_turn_done:
                self.swith_round(session)
            return mafia_pb2.DetectiveCheckResponse(Message = 'You revealed player ' + request.WhoToCheck + '. His role is ' + session.role_to_str[session.player_to_role[request.WhoToCheck]])
            

    def Follow(self, request, context):
        session = self.sessions[request.SessionId]
        while True:
            update = session.events_queues[request.Username].get(block=True)
            yield update
            with session.lock:
                if update.IsGameEnd:
                    self.chat_server.close()
                    return
                
    def GetPlayers(self, request, context):
        session = self.sessions[request.SessionId]
        response = mafia_pb2.GetPlayersResponse()
        response.Usernames[:] = list(session.player_to_role.keys())
        response.Roles[:] = ["Dead" if session.player_to_role[player] == mafia_pb2.MafiaRole.Dead else "Alive" for player in session.player_to_role.keys()]
        return response
    
    def PublishMessage(self, request, context):
        session = self.sessions[request.SessionId]
        update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.ChatMessage, Message = request.Message, Username = request.Username)
        for q_num in session.events_queues:
            if len(session.round.end_day_requests) == len(session.alive_players) and session.player_to_role[q_num] != mafia_pb2.MafiaRole.Mafia:
                continue
            session.events_queues[q_num].put(update)
        return mafia_pb2.PublishMessageResponse()

    def swith_round(self, session):
        msg = 'This night player ' + session.round.nightly_killed_player + ' was killed. '
        is_game_end = len(session.alive_players) <= 2
        self.notify_players(update = mafia_pb2.Update(Event = mafia_pb2.GameEvent.EndOfNight, Message = msg, KilledPlayer = session.round.nightly_killed_player, IsGameEnd = is_game_end), session=session)
        session.round = MafiaServer.Round()

    def assign_role(self, player, session):
        role = random.choice(session.roles_to_assign)
        session.roles_to_assign.remove(role)
        session.player_to_role[player] = role
        return session.role_to_str[role]

    def notify_players(self, update, session):
        for q_num in session.events_queues:
            session.events_queues[q_num].put(update)

    def check_possibility(self, username, session):
        if username not in session.players:
            return 'You must join the game first'
        if username not in session.alive_players and not session.round.killed_role == mafia_pb2.MafiaRole.Detective:
            return 'You can\'t use this command because you\'re dead'
        return ""
    
    def kill_most_voted(self, session):
        killee = ""
        max_votes = 0
        no_agreement = False
        for player in session.round.vote_table:
            if session.round.vote_table[player] > max_votes:
                max_votes = session.round.vote_table[player]
                killee = player
                no_agreement = False
            elif session.round.vote_table[player] == max_votes:
                no_agreement = True
        if no_agreement:
            return ""
        else:
            self.kill_player(killee, session)
            return killee
    
    def kill_player(self, player, session):
        session.alive_players.remove(player)
        session.round.killed_role = session.player_to_role[player] 
        session.alive_roles.remove(session.player_to_role[player])
        session.player_to_role[player] = mafia_pb2.MafiaRole.Dead
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mafia_pb2_grpc.add_MafiaGameServicer_to_server(MafiaServer(), server)
    server.add_insecure_port("[::]:50051")
    print('Running...')
    server.start()
    server.wait_for_termination()


def main():
    serve()


main()