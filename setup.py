from setuptools import setup

with open('requirements.txt') as requirements:
    setup(
        name='scrapy-sqs-exporter',
        version='1.0.4',
        py_modules=['sqsfeedexport'],
        install_requires=requirements.read().splitlines(),
        url='https://github.com/multiplechoice/scrapy-sqs-exporter',
        license='MIT',
        author='aodj',
        author_email='alexodonovanjones@gmail.com',
        description='Scrapy extension for outputting scraped items to an Amazon SQS instance',
        long_description=open('README.rst').read(),
        keywords='scrapy sqs'
    )
