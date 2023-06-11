# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mafia.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmafia.proto\x12\x05mafia\"4\n\rFollowRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\x12\x11\n\tSessionId\x18\x02 \x01(\x05\"\x88\x01\n\x06Update\x12\x0f\n\x07Message\x18\x01 \x01(\t\x12\x1f\n\x05\x45vent\x18\x02 \x01(\x0e\x32\x10.mafia.GameEvent\x12\x14\n\x0cKilledPlayer\x18\x03 \x01(\t\x12\x11\n\tIsGameEnd\x18\x04 \x01(\x08\x12\x10\n\x08MafiaWin\x18\x05 \x01(\x08\x12\x11\n\tSessionId\x18\x06 \x01(\x05\"\x1f\n\x0bJoinRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\"4\n\rEndDayRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\x12\x11\n\tSessionId\x18\x02 \x01(\x05\"\x1f\n\x0e\x45ndDayResponse\x12\r\n\x05\x45rror\x18\x01 \x01(\t\"&\n\x11GetPlayersRequest\x12\x11\n\tSessionId\x18\x01 \x01(\r\"6\n\x12GetPlayersResponse\x12\x11\n\tUsernames\x18\x01 \x03(\t\x12\r\n\x05Roles\x18\x02 \x03(\t\"0\n\x0cJoinResponse\x12\r\n\x05\x45rror\x18\x01 \x01(\t\x12\x11\n\tSessionId\x18\x02 \x01(\x05\"I\n\x0fVoteKillRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\x12\x11\n\tWhoToKill\x18\x02 \x01(\t\x12\x11\n\tSessionId\x18\x03 \x01(\x05\"!\n\x10VoteKillResponse\x12\r\n\x05\x45rror\x18\x01 \x01(\t\"J\n\x10MafiaKillRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\x12\x11\n\tWhoToKill\x18\x02 \x01(\t\x12\x11\n\tSessionId\x18\x03 \x01(\x05\"\"\n\x11MafiaKillResponse\x12\r\n\x05\x45rror\x18\x01 \x01(\t\"P\n\x15\x44\x65tectiveCheckRequest\x12\x10\n\x08Username\x18\x01 \x01(\t\x12\x12\n\nWhoToCheck\x18\x02 \x01(\t\x12\x11\n\tSessionId\x18\x03 \x01(\x05\"8\n\x16\x44\x65tectiveCheckResponse\x12\x0f\n\x07Message\x18\x01 \x01(\t\x12\r\n\x05\x45rror\x18\x02 \x01(\t\"O\n\x0cVotingResult\x12\x1a\n\x12IsSomebodyExecuted\x18\x01 \x01(\x08\x12\r\n\x05\x45rror\x18\x02 \x01(\t\x12\x14\n\x0cWhoWasKilled\x18\x03 \x01(\t*i\n\tGameEvent\x12\x0e\n\nGameStarts\x10\x00\x12\x0c\n\x08\x45ndOfDay\x10\x01\x12\r\n\tVotedKill\x10\x02\x12\x0f\n\x0bVotedNoKill\x10\x03\x12\x0e\n\nEndOfNight\x10\x04\x12\x0e\n\nPlayerJoin\x10\x05*8\n\tMafiaRole\x12\t\n\x05Mafia\x10\x00\x12\x07\n\x03Red\x10\x01\x12\r\n\tDetective\x10\x02\x12\x08\n\x04\x44\x65\x61\x64\x10\x03\x32\xb6\x03\n\tMafiaGame\x12/\n\x04Join\x12\x12.mafia.JoinRequest\x1a\x13.mafia.JoinResponse\x12;\n\x08VoteKill\x12\x16.mafia.VoteKillRequest\x1a\x17.mafia.VoteKillResponse\x12\x38\n\tEndTheDay\x12\x14.mafia.EndDayRequest\x1a\x15.mafia.EndDayResponse\x12>\n\tMafiaKill\x12\x17.mafia.MafiaKillRequest\x1a\x18.mafia.MafiaKillResponse\x12M\n\x0e\x44\x65tectiveCheck\x12\x1c.mafia.DetectiveCheckRequest\x1a\x1d.mafia.DetectiveCheckResponse\x12/\n\x06\x46ollow\x12\x14.mafia.FollowRequest\x1a\r.mafia.Update0\x01\x12\x41\n\nGetPlayers\x12\x18.mafia.GetPlayersRequest\x1a\x19.mafia.GetPlayersResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mafia_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GAMEEVENT._serialized_start=924
  _GAMEEVENT._serialized_end=1029
  _MAFIAROLE._serialized_start=1031
  _MAFIAROLE._serialized_end=1087
  _FOLLOWREQUEST._serialized_start=22
  _FOLLOWREQUEST._serialized_end=74
  _UPDATE._serialized_start=77
  _UPDATE._serialized_end=213
  _JOINREQUEST._serialized_start=215
  _JOINREQUEST._serialized_end=246
  _ENDDAYREQUEST._serialized_start=248
  _ENDDAYREQUEST._serialized_end=300
  _ENDDAYRESPONSE._serialized_start=302
  _ENDDAYRESPONSE._serialized_end=333
  _GETPLAYERSREQUEST._serialized_start=335
  _GETPLAYERSREQUEST._serialized_end=373
  _GETPLAYERSRESPONSE._serialized_start=375
  _GETPLAYERSRESPONSE._serialized_end=429
  _JOINRESPONSE._serialized_start=431
  _JOINRESPONSE._serialized_end=479
  _VOTEKILLREQUEST._serialized_start=481
  _VOTEKILLREQUEST._serialized_end=554
  _VOTEKILLRESPONSE._serialized_start=556
  _VOTEKILLRESPONSE._serialized_end=589
  _MAFIAKILLREQUEST._serialized_start=591
  _MAFIAKILLREQUEST._serialized_end=665
  _MAFIAKILLRESPONSE._serialized_start=667
  _MAFIAKILLRESPONSE._serialized_end=701
  _DETECTIVECHECKREQUEST._serialized_start=703
  _DETECTIVECHECKREQUEST._serialized_end=783
  _DETECTIVECHECKRESPONSE._serialized_start=785
  _DETECTIVECHECKRESPONSE._serialized_end=841
  _VOTINGRESULT._serialized_start=843
  _VOTINGRESULT._serialized_end=922
  _MAFIAGAME._serialized_start=1090
  _MAFIAGAME._serialized_end=1528
# @@protoc_insertion_point(module_scope)
