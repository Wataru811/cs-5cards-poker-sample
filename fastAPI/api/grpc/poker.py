import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection

from api.pb import poker_pb2
from api.pb import poker_pb2_grpc



# gRPC サービスの実装
class PokerServicer(poker_pb2_grpc.Poker5cdServiceServicer):
    def Hello(self, request, context):
        return poker_pb2.Poker5cdResponse(message=f"Hello, {request.name}!   uid:{request.uid}")
    def HelloAgain(self, request, context):
        return poker_pb2.Poker5cdResponse(message=f"Hello Again, {request.name}!  uid:{request.uid}")




# gRPC サーバーの起動を非同期で実行
async def start_grpc_server():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    poker_pb2_grpc.add_Poker5cdServiceServicer_to_server(PokerServicer(), server)
    
    SERVICE_NAMES = (
        poker_pb2.DESCRIPTOR.services_by_name['Poker5cdService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)


    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC server started on port 50051")
    await server.wait_for_termination()