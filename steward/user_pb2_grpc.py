# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from steward import user_pb2 as steward_dot_user__pb2


class UserStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetUser = channel.unary_unary(
        '/maintcal.User/GetUser',
        request_serializer=steward_dot_user__pb2.UserRequest.SerializeToString,
        response_deserializer=steward_dot_user__pb2.UserResponse.FromString,
        )
    self.GetUsers = channel.unary_stream(
        '/maintcal.User/GetUsers',
        request_serializer=steward_dot_user__pb2.UsersRequest.SerializeToString,
        response_deserializer=steward_dot_user__pb2.UserResponse.FromString,
        )


class UserServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUsers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetUser': grpc.unary_unary_rpc_method_handler(
          servicer.GetUser,
          request_deserializer=steward_dot_user__pb2.UserRequest.FromString,
          response_serializer=steward_dot_user__pb2.UserResponse.SerializeToString,
      ),
      'GetUsers': grpc.unary_stream_rpc_method_handler(
          servicer.GetUsers,
          request_deserializer=steward_dot_user__pb2.UsersRequest.FromString,
          response_serializer=steward_dot_user__pb2.UserResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'maintcal.User', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
