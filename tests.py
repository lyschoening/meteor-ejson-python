import datetime
import six
import ejson

import unittest


class EJSONTestCase(unittest.TestCase):
    def test_escape_encode(self):
        s = ejson.dumps({
                            "foo": "bar",
                            "bat": {
                                "$escape": {
                                    "baz": "bazam"
                                }
                            }
                        }, sort_keys=True)

        self.assertEqual('{"bat": {"$escape": {"$escape": {"baz": "bazam"}}}, "foo": "bar"}', s)

    def test_escape_decode(self):
        self.assertEqual({
                             "foo": "bar",
                             "bat": {
                                 "$escape": {
                                     "baz": "bazam"
                                 }
                             }
                         }, ejson.loads('{"bat": {"$escape": {"$escape": {"baz": "bazam"}}}, "foo": "bar"}'))

    def test_escape_escape(self):
        self.assertEqual({
                             "$date": datetime.datetime(1970, 1, 1, 0, 0, 32, tzinfo=ejson.timezone.utc)
                         }, ejson.loads('{"$escape": {"$date": {"$date": 32000}}}'))

    def test_date(self):
        s1 = ejson.dumps(datetime.date(2015, 1, 25))
        self.assertEqual('{"$date": 1422144000000}', s1)
        self.assertEqual(datetime.datetime(2015, 1, 25, tzinfo=ejson.timezone.utc), ejson.loads(s1))
        s2 = ejson.dumps(datetime.datetime(2015, 1, 25, 10, 30, 1, tzinfo=ejson.timezone.utc))
        self.assertEqual('{"$date": 1422181801000}', s2)
        self.assertEqual(datetime.datetime(2015, 1, 25, 10, 30, 1, tzinfo=ejson.timezone.utc), ejson.loads(s2))

    def test_binary(self):
        if six.PY3:
            s = ejson.dumps([six.binary_type('foo', 'ascii'), 'foo'])
            self.assertEqual('[{"$binary": "Zm9v"}, "foo"]', s)
            self.assertEqual([six.binary_type('foo', 'ascii'), 'foo'], ejson.loads(s))
        else:
            s = ejson.dumps(['foo', six.text_type('foo')])
            self.assertEqual('["foo", "foo"]', s)
            self.assertEqual(['foo', 'foo'], ejson.loads('[{"$binary": "Zm9v"}, "foo"]'))

    def test_custom_type_encode(self):
        encoder = ejson.EJSONEncoder(custom_type_hooks=[
            (set, 'set', sorted)
        ], sort_keys=True)

        self.assertEqual('{"foo": {"$type": "set", "$value": [1, 2, 3]}}', encoder.encode({
            "foo": {1, 2, 3}
        }))

    def test_unknown_type_decode(self):
        with self.assertRaises(ejson.UnknownTypeError):
            ejson.loads('{"foo": {"$type": "pow", "$value": 5}}')

            # TODO better error message for UnknownTypeError

    def test_custom_type_decode(self):
        decoder = ejson.EJSONDecoder(custom_type_hooks=[
            ('pow', lambda v: v ** 2),
            ('set', set)
        ])

        self.assertEqual({
                             'foo': [25, 1.23],
                             'things': {1, 2, 4}
                         }, decoder.decode('{"foo": [{"$type": "pow", "$value": 5}, 1.23],'
                                           ' "things": {"$type": "set", "$value": [1, 1, 2, 4]}}'))


if __name__ == '__main__':
    unittest.main()
