from collections import deque
from itertools import izip_longest
from uuid import uuid4

from scrapy.exporters import BaseItemExporter
from scrapy.extensions.feedexport import BlockingFeedStorage
from six.moves.urllib.parse import urlparse


class SQSExporter(BaseItemExporter):
    """
    Simple class for accumulating yielded items from the spiders.

    Rather than serialising the yielded items to a file or emitting the one after the other
    we store them so that the SQSFeedStorage class can emit them in batches. Rather than
    returning a file like object as the other exporter classes do, this class returns a
    `collections.deque` instance, which means than this class is only intended to be used
    in conjunction with SQSFeedStorage.
    """

    def __init__(self, deck, *args, **kwargs):
        self.deck = deck

    def export_item(self, item):
        self.deck.append(translate_item_to_message(item))


class SQSFeedStorage(BlockingFeedStorage):
    def __init__(self, uri):
        from scrapy.conf import settings
        u = urlparse(uri)
        self.queue_name = u.netloc
        self.region_name = settings['AWS_DEFAULT_REGION']
        self.access_key = settings['AWS_ACCESS_KEY_ID']
        self.secret_key = settings['AWS_SECRET_ACCESS_KEY']
        self.deck = deque()

    def open(self, *args, **kwargs):
        return self.deck

    def _store_in_thread(self, *args, **kwargs):
        import boto3
        self.sqs = boto3.resource(
            'sqs',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )
        self.queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)

        for batch in grouper(self.deck, 10):
            items = filter(lambda x: x is not None, batch)
            self.queue.send_messages(Entries=items)


def translate_item_to_message(item):
    """
    Loop through the items as they are emitted from the Scrapy spider
    Args:
        item (dict): Scrapy item dict

    Returns:
        dict: reformatted item valid for use in the `send_messages`_ function.
        See also the AWS `documentation`_.

    .. _send_messages:
        https://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_messages
    .. _documentation:
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessageBatchRequestEntry.html

    """
    message = {'Id': str(uuid4()), 'MessageBody': 'ScrapyItem', 'MessageAttributes': {}}
    for key, value in item.iteritems():
        if value is None:
            continue
        message['MessageAttributes'][key] = {'StringValue': value, 'DataType': 'String'}

    if not message['MessageAttributes']:
        del message['MessageAttributes']
    return message


# https://docs.python.org/2/library/itertools.html#recipes
def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
