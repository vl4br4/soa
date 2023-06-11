import mafia_pb2 as mafia_pb2
import mafia_pb2_grpc as mafia_pb2_grpc
import grpc
import argparse
from threading import Thread
from threading import Lock
import time


class MafiaClient:
    def __init__(self, channel) -> None:
        self.username = None
        self.stub = mafia_pb2_grpc.MafiaGameStub(channel)
        self.commands = ['join-game --username <username>',
                          'vote-kill --username <username>',
                          'end-day', 'mafia-kill --username <username>',
                          'reveal --username <username>',
                          'commands?',
                          'players'
                          'exit']
        self.parsers = dict()
        self.role = mafia_pb2.MafiaRole
        self.did_mafia_killed = False
        self.did_detective = False
        self.initialize_parsers()
        self.is_game_started = False
        self.is_night_phase = False
        self.follow_thread = None
        self.is_game_end = False
        self.lock = Lock()
        self.enter_msg = '\nPlease, enter command(to see available commands type "commands?"):\n> '
        self.role_to_str = {mafia_pb2.MafiaRole.Red: "Red", mafia_pb2.MafiaRole.Detective: "Detective", mafia_pb2.MafiaRole.Mafia: "Mafia"}
        self.channel = grpc.insecure_channel('localhost:50051')

    def initialize_parsers(self):
        self.parsers['join-game'] = argparse.ArgumentParser(description='Join the game')
        self.parsers['join-game'].add_argument('--username', type=str)
        self.parsers['vote-kill'] = argparse.ArgumentParser(description='Vote to kill player')
        self.parsers['vote-kill'].add_argument('--username', type=str)
        self.parsers['end-day'] = argparse.ArgumentParser(description='End a game day')
        self.parsers['mafia-kill'] = argparse.ArgumentParser(description='Make mafia kill')
        self.parsers['mafia-kill'].add_argument('--username', type=str)
        self.parsers['reveal'] = argparse.ArgumentParser(description='Reveal player when playing Detective')
        self.parsers['reveal'].add_argument('--username', type=str)
        self.parsers['commands?'] = argparse.ArgumentParser(description='Check avaiable commands')
        self.parsers['exit'] = argparse.ArgumentParser(description='Exit the game')
        self.parsers['players'] = argparse.ArgumentParser(description='Get players list')

    def wait_and_parse_updates(self):
        try:
            stub = mafia_pb2_grpc.MafiaGameStub(self.channel)
            for update in stub.Follow(mafia_pb2.FollowRequest(Username = self.username)):
                time.sleep(1)
                with self.lock:
                    self.correct_inp_output()
                    print('\n')
                    if update.Event == mafia_pb2.GameEvent.GameStarts:
                        str_to_role = {"Red": mafia_pb2.MafiaRole.Red, "Mafia": mafia_pb2.MafiaRole.Mafia, "Detective": mafia_pb2.MafiaRole.Detective}
                        self.role = str_to_role[update.Message]
                        print('Now all the players have joined. Let\'s start the game! You\'re on ' + update.Message + 's')
                        print('The day starts. Remember, you can\'t vote during the first day')
                        self.is_game_started = True
                    elif update.Event == mafia_pb2.GameEvent.VotedNoKill:
                        print('Players couldn\'t get to an agreement after voting. Nobody killed. Please end the day if you are ready')
                    elif update.Event == mafia_pb2.GameEvent.VotedKill:
                        print('Players made their votes.', "\"" + update.Message + "\"", 'was killed. Please end the day if you are ready')
                        if update.IsGameEnd:
                            print('End of the game. Mafia lost!')
                            self.is_game_end = True
                            continue
                    elif update.Event == mafia_pb2.GameEvent.EndOfDay:
                        print('The city falls asleep. The Mafia wakes up')
                        self.is_night_phase = True
                    elif update.Event == mafia_pb2.GameEvent.EndOfNight:
                        print(update.Message)
                        if update.KilledPlayer == self.username:
                            self.role = mafia_pb2.MafiaRole.Dead
                            print('Now you became dead. You can watch the game progress still')
                        if update.IsGameEnd:
                            print('End of the game. Mafia wins!')
                            self.is_game_end = True
                            continue
                        print('Day phase starts. Speak and vote')
                        self.is_night_phase = False
                    elif update.Event == mafia_pb2.GameEvent.PlayerJoin:
                        self.chat_msg('lobby', 'Player ' + '\"' + update.Message + "\"" + ' joined the game')
                    print(self.enter_msg, end='')
        except:
            pass
        self.channel.close()

    def chat_msg(self, who, msg):
        print('[' + who + ']:', msg)

    def follow_for_updates(self):
        self.follow_thread = Thread(target=self.wait_and_parse_updates)
        self.follow_thread.start()

    def join_game(self, username):
        if self.username is not None:
            print('You are already registered, your nickname is', self.username)
            return
        response = self.stub.Join(mafia_pb2.JoinRequest(Username = username))
        if response.Error != "":
            self.print_error(response.Error)
        else:
            self.username = username
            print('You have succussfully joined the game!')
            self.follow_for_updates()

    def vote_kill(self, who_to_kill):
        if not self.check_possibility():
            return
        response = self.stub.VoteKill(mafia_pb2.VoteKillRequest(Username = self.username, WhoToKill = who_to_kill))
        if response.Error != "":
            self.print_error(response.Error)

    def end_the_day(self):
        if not self.check_possibility():
            return
        response = self.stub.EndTheDay(mafia_pb2.EndDayRequest(Username = self.username))
        if response.Error != "":
            self.print_error(response.Error)

    def mafia_kill(self, who_to_kill):
        if not self.check_possibility():
            return
        if self.role != mafia_pb2.MafiaRole.Mafia:
            print('You are not Mafia')
            return
        if not self.is_night_phase:
            print('Wait until night to kill someone')
            return
        response = self.stub.MafiaKill(mafia_pb2.MafiaKillRequest(Username = self.username, WhoToKill = who_to_kill))
        if response.Error != "":
            self.print_error(response.Error)

    def detective_check(self, who_to_check):
        if not self.check_possibility():
            return
        if self.role != mafia_pb2.MafiaRole.Detective:
            print('You are not Detective')
            return
        if not self.is_night_phase:
            print('Wait until night to check someone')
            return
        response = self.stub.DetectiveCheck(mafia_pb2.DetectiveCheckRequest(Username = self.username, WhoToCheck = who_to_check))
        if response.Error != "":
            self.print_error(response.Error)
        else:
            print(response.Message)

    def get_players(self):
        if self.is_night_phase and not self.role == mafia_pb2.MafiaRole.Dead:
            print('Wait until morning')
            return
        if not self.check_possibility():
            return
        response = self.stub.GetPlayers(mafia_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
        print('Players:')
        for i in range(len(response.Usernames)):
            print('Player:', response.Usernames[i], ', Status:', response.Roles[i])
    
    def correct_inp_output(self):
        print('\033[2A', ' ' * len(self.enter_msg), '\n', ' ' * 70, '\033[3A', end='')

    def check_possibility(self):
        if self.username is None:
            print('You must join the game first')
            return False
        elif not self.is_game_started:
            print('Game has not yet started')
            return False
        elif self.role == mafia_pb2.MafiaRole.Red and self.is_night_phase:
            print('It is night phase and you are Civilian. Wait until morning')
            return False
        return True
        
    def print_error(self, error):
        print('Error occured:', error)
    
    def print_available_commands(self):
        print('\n'.join(self.commands))

    def start(self):
        while True:
            try:
                command = input(self.enter_msg).split()
                if self.is_game_end:
                    print('Game ended. Bye!')
                    self.follow_thread.join()
                    return
                args = self.parsers[command[0]].parse_args(command[1:])
                print('\"' + command[0] + '\"', 'command submited\n')
                if command[0] == 'join-game':
                    self.join_game(args.username)
                elif command[0] == 'vote-kill':
                    self.vote_kill(args.username)
                elif command[0] == 'end-day':
                    self.end_the_day()
                elif command[0] == 'mafia-kill':
                    self.mafia_kill(args.username)
                elif command[0] == 'reveal':
                    self.detective_check(args.username)
                elif command[0] == 'commands?':
                    self.print_available_commands()
                elif command[0] == 'players':
                    self.get_players()
                elif command[0] == 'exit':
                    self.channel.close()
                    return
                else:
                    print('Unknown command(to see available commands type "commands?")')
            except Exception as e:
                print('Error occured, try again', e)
            except:
                print('Bad input')


def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        client = MafiaClient(channel=channel)
        client.start()
        client.follow_thread.join()

main()
