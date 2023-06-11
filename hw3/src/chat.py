import pika
import grpc
import mafia_pb2
import mafia_pb2_grpc
from threading import Thread

class ChatServer:
    stub = None
    
    def __init__(self):
        self.grpc_channel = grpc.insecure_channel('localhost:50051')
        ChatServer.stub = mafia_pb2_grpc.MafiaGameStub(self.grpc_channel)
        self.connections = []
        self.consume_threads = []
    
    def callback(ch, method, properties, body):
        msg = body.decode('utf-8').split()
        ChatServer.stub.PublishMessage(mafia_pb2.PublishMessageRequest(Username = msg[1], Message = ' '.join(msg[2:]), SessionId = int(msg[0])))

    def init_new_chat(self, session_id):
        self.connections.append(pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', port=5672)))
        channel = self.connections[-1].channel()
        q_name = f'mafia_chat_{session_id}'
        channel.queue_declare(queue=q_name)
        channel.basic_consume(queue=q_name, on_message_callback=ChatServer.callback, auto_ack=True)
        self.consume_threads.append(Thread(target=channel.start_consuming))
        self.consume_threads[-1].start()

    def close(self):
        self.grpc_channel.close()
        self.connection.close()
    
class ChatClient:
    def __init__(self, session_id):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', port=5672))
        self.channel = self.connection.channel()
        self.q_name = f'mafia_chat_{session_id}'
        self.channel.queue_declare(queue=self.q_name)

    def send_message(self, sender, message, session_id):
        self.channel.basic_publish(exchange='', routing_key=self.q_name, body=f'{session_id} {sender} {message}')