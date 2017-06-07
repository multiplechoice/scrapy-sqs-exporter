import sqsfeedexport

examples = [
    {
        "company": "Nings ",
        "deadline": "2017-06-13T00:00:00",
        "posted": "2017-06-06T10:15:00",
        "spider": "alfred",
        "title": "Okkur vantar sendla, ert \u00fe\u00fa r\u00e9tta manneskjan?",
        "url": "https://alfred.is/starf/11076"
    },
    {
        "company": "Tryggingami\u00f0lun \u00cdslands",
        "deadline": "2017-06-13T00:00:00",
        "posted": "2017-06-06T10:29:00",
        "spider": "alfred",
        "title": "Fr\u00e1b\u00e6rt aukastarf \u00ed bo\u00f0i",
        "url": "https://alfred.is/starf/11077"
    },
    {
        "company": "S\u00e6ta Sv\u00edni\u00f0 ",
        "deadline": "2017-11-06T00:00:00",
        "posted": "2017-06-06T10:31:00",
        "spider": "alfred",
        "title": "Leitum af uppvaskara / looking for dishwasher",
        "url": "https://alfred.is/starf/11078"
    },
    {
        "company": "Leiksk\u00f3linn M\u00falaborg",
        "deadline": "2017-06-20T00:00:00",
        "posted": "2017-06-06T10:31:00",
        "spider": "alfred",
        "title": "Deildarstj\u00f3ri/leiksk\u00f3lakennari ",
        "url": "https://alfred.is/starf/11080"
    },
    {
        "company": "Sushi Social",
        "deadline": "2017-11-06T00:00:00",
        "posted": "2017-06-06T10:32:00",
        "spider": "alfred",
        "title": "Uppvaskari/Dishwasher/ kitchen assistant ",
        "url": "https://alfred.is/starf/11079"
    },
    {
        "company": "Apotek kitchen + bar",
        "deadline": "2017-11-06T00:00:00",
        "posted": "2017-06-06T10:49:00",
        "spider": "alfred",
        "title": "Vanir \u00fej\u00f3nar \u00ed hlutastarf :)",
        "url": "https://alfred.is/starf/11081"
    }]


def test_batch_send_entry_translation(monkeypatch):
    def fake_uuid():
        return '12345-67890'

    monkeypatch.setattr('sqsfeedexport.uuid4', fake_uuid)
    message = sqsfeedexport.translate_item_to_message(examples[0])

    assert message == {
        'Id': '12345-67890',
        'MessageBody': 'ScrapyItem',
        'MessageAttributes': {
            'company': {'StringValue': 'Nings ', 'DataType': 'String'},
            'deadline': {'StringValue': '2017-06-13T00:00:00', 'DataType': 'String'},
            'posted': {'StringValue': '2017-06-06T10:15:00', 'DataType': 'String'},
            'spider': {'StringValue': 'alfred', 'DataType': 'String'},
            'title': {
                'StringValue': 'Okkur vantar sendla, ert \u00fe\u00fa r\u00e9tta manneskjan?', 'DataType': 'String'},
            'url': {'StringValue': 'https://alfred.is/starf/11076', 'DataType': 'String'}
        }
    }


def test_empty_scrapy_response(monkeypatch):
    def fake_uuid():
        return '12345-67890'

    monkeypatch.setattr('sqsfeedexport.uuid4', fake_uuid)

    assert sqsfeedexport.translate_item_to_message({}) == {
        'Id': '12345-67890',
        'MessageBody': 'ScrapyItem'
    }


def test_grouper_batching():
    batches_expected = (
        tuple(examples[:5]),  # first batch should be the first 5 entries from the examples list above
        (examples[-1], None, None, None, None)  # second batch should be the last entry in examples padded with Nones
    )
    for batch, expected in zip(sqsfeedexport.grouper(examples, 5), batches_expected):
        assert batch == expected
