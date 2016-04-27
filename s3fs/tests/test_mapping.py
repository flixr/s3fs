from s3fs.tests.test_s3fs import s3, test_bucket_name
from s3fs import S3Map, S3FileSystem

root = test_bucket_name+'/mapping'


def test_simple(s3):
    d = S3Map(root, s3)
    assert not d

    assert list(d) == list(d.keys()) == []
    assert list(d.values()) == []
    assert list(d.items()) == []


def test_default_s3filesystem(s3):
    d = S3Map(root)
    assert d.s3 is s3


def test_with_data(s3):
    d = S3Map(root, s3)
    d['x'] = b'123'
    assert list(d) == list(d.keys()) == ['x']
    assert list(d.values()) == [b'123']
    assert list(d.items()) == [('x', b'123')]
    assert d['x'] == b'123'
    assert bool(d)

    assert s3.walk(root) == [test_bucket_name+'/mapping/x']
    d['x'] = b'000'
    assert d['x'] == b'000'

    d['y'] = b'456'
    assert d['y'] == b'456'
    assert set(d) == {'x', 'y'}

    d.clear()
    assert list(d) == []


def test_complex_keys(s3):
    d = S3Map(root, s3)
    d[1] = b'hello'
    assert d[1] == b'hello'
    del d[1]

    d[1, 2] = b'world'
    assert d[1, 2] == b'world'
    del d[1, 2]

    d['x', 1, 2] = b'hello world'
    assert d['x', 1, 2] == b'hello world'
    print(list(d))

    assert ('x', 1, 2) in d


def test_pickle(s3):
    d = S3Map(root, s3)
    d['x'] = b'1'

    import pickle
    d2 = pickle.loads(pickle.dumps(d))

    assert d2['x'] == b'1'
