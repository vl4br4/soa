# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import mafia_pb2 as mafia__pb2


class MafiaGameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Join = channel.unary_unary(
                '/mafia.MafiaGame/Join',
                request_serializer=mafia__pb2.JoinRequest.SerializeToString,
                response_deserializer=mafia__pb2.JoinResponse.FromString,
                )
        self.VoteKill = channel.unary_unary(
                '/mafia.MafiaGame/VoteKill',
                request_serializer=mafia__pb2.VoteKillRequest.SerializeToString,
                response_deserializer=mafia__pb2.VoteKillResponse.FromString,
                )
        self.EndTheDay = channel.unary_unary(
                '/mafia.MafiaGame/EndTheDay',
                request_serializer=mafia__pb2.EndDayRequest.SerializeToString,
                response_deserializer=mafia__pb2.EndDayResponse.FromString,
                )
        self.MafiaKill = channel.unary_unary(
                '/mafia.MafiaGame/MafiaKill',
                request_serializer=mafia__pb2.MafiaKillRequest.SerializeToString,
                response_deserializer=mafia__pb2.MafiaKillResponse.FromString,
                )
        self.DetectiveCheck = channel.unary_unary(
                '/mafia.MafiaGame/DetectiveCheck',
                request_serializer=mafia__pb2.DetectiveCheckRequest.SerializeToString,
                response_deserializer=mafia__pb2.DetectiveCheckResponse.FromString,
                )
        self.Follow = channel.unary_stream(
                '/mafia.MafiaGame/Follow',
                request_serializer=mafia__pb2.FollowRequest.SerializeToString,
                response_deserializer=mafia__pb2.Update.FromString,
                )
        self.GetPlayers = channel.unary_unary(
                '/mafia.MafiaGame/GetPlayers',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=mafia__pb2.GetPlayersResponse.FromString,
                )


class MafiaGameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Join(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VoteKill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndTheDay(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MafiaKill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DetectiveCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Follow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlayers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MafiaGameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Join': grpc.unary_unary_rpc_method_handler(
                    servicer.Join,
                    request_deserializer=mafia__pb2.JoinRequest.FromString,
                    response_serializer=mafia__pb2.JoinResponse.SerializeToString,
            ),
            'VoteKill': grpc.unary_unary_rpc_method_handler(
                    servicer.VoteKill,
                    request_deserializer=mafia__pb2.VoteKillRequest.FromString,
                    response_serializer=mafia__pb2.VoteKillResponse.SerializeToString,
            ),
            'EndTheDay': grpc.unary_unary_rpc_method_handler(
                    servicer.EndTheDay,
                    request_deserializer=mafia__pb2.EndDayRequest.FromString,
                    response_serializer=mafia__pb2.EndDayResponse.SerializeToString,
            ),
            'MafiaKill': grpc.unary_unary_rpc_method_handler(
                    servicer.MafiaKill,
                    request_deserializer=mafia__pb2.MafiaKillRequest.FromString,
                    response_serializer=mafia__pb2.MafiaKillResponse.SerializeToString,
            ),
            'DetectiveCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.DetectiveCheck,
                    request_deserializer=mafia__pb2.DetectiveCheckRequest.FromString,
                    response_serializer=mafia__pb2.DetectiveCheckResponse.SerializeToString,
            ),
            'Follow': grpc.unary_stream_rpc_method_handler(
                    servicer.Follow,
                    request_deserializer=mafia__pb2.FollowRequest.FromString,
                    response_serializer=mafia__pb2.Update.SerializeToString,
            ),
            'GetPlayers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlayers,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=mafia__pb2.GetPlayersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mafia.MafiaGame', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MafiaGame(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Join(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/Join',
            mafia__pb2.JoinRequest.SerializeToString,
            mafia__pb2.JoinResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VoteKill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/VoteKill',
            mafia__pb2.VoteKillRequest.SerializeToString,
            mafia__pb2.VoteKillResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EndTheDay(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/EndTheDay',
            mafia__pb2.EndDayRequest.SerializeToString,
            mafia__pb2.EndDayResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MafiaKill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/MafiaKill',
            mafia__pb2.MafiaKillRequest.SerializeToString,
            mafia__pb2.MafiaKillResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DetectiveCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/DetectiveCheck',
            mafia__pb2.DetectiveCheckRequest.SerializeToString,
            mafia__pb2.DetectiveCheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Follow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mafia.MafiaGame/Follow',
            mafia__pb2.FollowRequest.SerializeToString,
            mafia__pb2.Update.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPlayers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaGame/GetPlayers',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            mafia__pb2.GetPlayersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)