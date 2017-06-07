|Build Status| |Coveralls Status| |Requirements Status|

scrapy-sqs-exporter
===================

This is an extension to Scrapy_ to allow exporting of scraped items to an Amazon SQS instance.

Setup
=====

After installing the package, the two classes defined in the library need to be added to the relevant
sections of the settings file::

  FEED_EXPORTERS = {
    'sqs': 'sqsfeedexport.SQSExporter'
  }

  FEED_STORAGES = {
    'sqs': 'sqsfeedexport.SQSFeedStorage'
  }

The ``FEED_STORAGES`` section uses a URL prefixed with ``sqs`` to differentiate it from other URI based storage
options.

In the environment we also need to define some keys::

  AWS_DEFAULT_REGION=eu-central-1
  AWS_ACCESS_KEY_ID=...
  AWS_SECRET_ACCESS_KEY=...
  FEED_URI=sqs://foo
  FEED_FORMAT=sqs

The ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` are the AWS credentials to be used, and ``AWS_DEFAULT_REGION``
is the region to default to for the SQS instance. ``FEED_URI`` is the name of the AWS SQS instance in the
``AWS_DEFAULT_REGION`` region for example::

  AWS_DEFAULT_REGION=us-east-1
  FEED_URI=sqs://bar
  FEED_FORMAT=sqs

would refer to a queue name ``bar`` in the ``us-east-1`` region.

Finally, the ``FEED_FORMAT`` option makes the Scrapy spiders use the SQSExporter class.

.. _Scrapy: https://github.com/scrapy/scrapy/
.. |Build Status| image:: https://travis-ci.org/multiplechoice/scrapy-sqs-exporter.svg?branch=master
  :target: https://travis-ci.org/multiplechoice/scrapy-sqs-exporter
.. |Coveralls Status| image:: https://coveralls.io/repos/github/multiplechoice/scrapy-sqs-exporter/badge.svg?branch=master
  :target: https://coveralls.io/github/multiplechoice/scrapy-sqs-exporter?branch=master
.. |Requirements Status| image:: https://requires.io/github/multiplechoice/scrapy-sqs-exporter/requirements.svg?branch=master
  :target: https://requires.io/github/multiplechoice/scrapy-sqs-exporter/requirements/?branch=master
  :alt: Requirements Status
