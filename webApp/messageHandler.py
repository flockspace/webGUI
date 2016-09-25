'''
Created on 24-Sep-2016

@author: suhaheer
'''
import pika
import json

AMQ_SERVER="localhost"
EXCHANGE_NAME = "direct_queue"
EXCHANGE_TYPE = "direct"


'''
1. AMQ object should be created when an user registers. The AMQ object should 
create an unique Queue based on user-id and bind the queue to any topic.
2. The user can subscribe to any topic she is interested in after 1st login or 
any time. Whenever user subscribes, her queue should be bound to the topic.
3. The category of topic is predefined as of now.

'''

class AMQHandler:
    channel = None
    connection = None
    thisQ = None
    routingKey = ['entertainment'] #topic taken for experimental purpose,

    def __init__(self,Qname):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(AMQ_SERVER))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE_NAME,type=EXCHANGE_TYPE)
        self.useQ(Qname)
        return
    
    def closeConnection(self):
        return self.connection.close()
    
    '''Each user would be interested in different topics. Hence each user queue
    should be bound to each topic she is subscribed to.
    '''
    def bind_topic(self, topic):
        self.channel.queue_bind(exchange=EXCHANGE_NAME,
                                queue=self.thisQ,
                                routing_key=topic) #routing_key should be topic name. Multiple topic name can be assigned to single Queue
        return
        
    def useQ(self,Qname):
        self.thisQ = Qname
        self.channel.queue_declare(self.thisQ, durable=True)
        for key in self.routingKey:
            self.channel.queue_bind(exchange=EXCHANGE_NAME,
                                queue=self.thisQ,
                                routing_key=key) #routing_key should be topic name. Multiple topic name can be assigned to single Queue
        return

    def publish(self,message): #publish message based on its category
        
        routeKey = message['content_category']
        self.channel.basic_publish(exchange=EXCHANGE_NAME,
                              routing_key=routeKey,
                              body=json.dumps(message))
        self.closeConnection()
        return

    def consume(self):
        return
    