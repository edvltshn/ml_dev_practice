import json
import pika

from model.task import Task

class Rabbit():
    def __init__(self, rabbit_url) -> None:
        
        self.rabbit_url = rabbit_url
        parameters = pika.URLParameters(rabbit_url)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def reconnect(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_url))
        self.channel = self.connection.channel()
    
    def send_task(self, task:Task):

        body = json.dumps({
            "id":task.id,
            "input_data":task.input_data,
            "predictor":task.predictor
        })

        try:
            self.channel.basic_publish('test_exchange',
                                'test_routing_key',
                                body,
                                pika.BasicProperties(content_type='text/plain',
                                                    delivery_mode=pika.DeliveryMode.Transient))
            
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed) as e:
            print(f"Ошибка: {e}")
            self.reconnect()
            self.channel.basic_publish('test_exchange',
                                'test_routing_key',
                                body,
                                pika.BasicProperties(content_type='text/plain',
                                                    delivery_mode=pika.DeliveryMode.Transient))
            
