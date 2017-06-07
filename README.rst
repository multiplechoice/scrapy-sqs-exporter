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
    'sqs+https': 'sqsfeedexport.SQSFeedStorage'
  }

The ``FEED_STORAGES`` section uses a URL prefixed with ``sqs+https`` so that any other storage engines that
might be using a ``https://`` URI can still function.

In the environment we also need to define four keys::

  AWS_ACCESS_KEY_ID=...
  AWS_SECRET_ACCESS_KEY=...
  FEED_URI=sqs+https://sqs.eu-central-1.amazonaws.com/1234567890/foo
  FEED_FORMAT=sqs

The ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` are the AWS credentials to be used, ``FEED_URI`` is the
address of the AWS SQS instance being used and the ``FEED_FORMAT`` option makes the Scrapy spiders use our
accumulating exporter class.

.. _Scrapy: https://github.com/scrapy/scrapy/
.. |Build Status| image:: https://travis-ci.org/multiplechoice/scrapy-sqs-exporter.svg?branch=master
  :target: https://travis-ci.org/multiplechoice/scrapy-sqs-exporter
.. |Coveralls Status| image:: https://coveralls.io/repos/github/multiplechoice/scrapy-sqs-exporter/badge.svg?branch=master
  :target: https://coveralls.io/github/multiplechoice/scrapy-sqs-exporter?branch=master
.. |Requirements Status| image:: https://requires.io/github/multiplechoice/scrapy-sqs-exporter/requirements.svg?branch=master
  :target: https://requires.io/github/multiplechoice/scrapy-sqs-exporter/requirements/?branch=master
  :alt: Requirements Status
