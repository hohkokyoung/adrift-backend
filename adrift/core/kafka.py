from kafka import KafkaProducer, KafkaConsumer
import json 

producer = KafkaProducer(bootstrap_servers='kafka:29092', api_version=(2,8,1), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_topic(topic, message):
    producer.send(topic, message)
    producer.flush() 

def close_producer():
    producer.close()

# not thread safety
# one possible approach can be just store these abundant data in mongodb, and filter out duplicates in the transformation layer
class TopicConsumer:
    _instances = {}

    def __new__(cls, topic, *args, **kwargs):
        if topic not in cls._instances:
            instance = super(TopicConsumer, cls).__new__(cls)
            instance.consumer = KafkaConsumer(topic, 
            bootstrap_servers='kafka:29092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            # this means all consumer belong in same group
            group_id='my-group', 
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            *args, 
            **kwargs)
            cls._instances[topic] = instance
        return cls._instances[topic]

    def consume(self):
        try:
            for message in self.consumer:
                # Process message
                print(message)
        finally:
            self.consumer.close()


