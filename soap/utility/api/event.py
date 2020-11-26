from datetime import datetime
import logging
import uuid

from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials

logger = logging.getLogger(__name__)


class EventGridHook:
    def __init__(self, topic_uri, topic_key):
        if not topic_uri or not topic_key:
            raise Exception("Topic credentials missing")
        self.topic_uri = topic_uri
        self.topic_key = topic_key
        self.client = None

    def __get_connection(self):
        if not self.client:
            credentials = TopicCredentials(self.topic_key)
            self.client = EventGridClient(credentials)
        return self.client

    def publish_event(self, subject, event_type, data):
        self.__get_connection().publish_events(
            topic_hostname=self.topic_uri,
            events=[{
                "id": uuid.uuid4(),
                "subject": subject,
                "data": data,
                "event_type": event_type,
                "event_time": datetime.utcnow(),
                "data_version": 1
            }]
        )