# meteor-ejson

[![Build Status](https://travis-ci.org/lyschoening/meteor-ejson-python.svg?branch=master)](https://travis-ci.org/lyschoening/meteor-ejson-python)
[![PyPI version](https://badge.fury.io/py/meteor-ejson.svg)](http://badge.fury.io/py/meteor-ejson)

A Python implementation of Extended JSON (EJSON) as used in Meteor and DDP.


## Installation

    pip install meteor-ejson

Supports Python 2.7, Python 3.x, and PyPy

The `meteor-ejson` Python package is open source under the MIT license.


## Usage


This implementation piggybacks on the native `json` package by providing a `EJSONEncoder` and a `EJSONDecoder` class. Use either the `ejson.dumps(o)` and `ejson.loads(s)` shortcuts or the built-ins.

	>>> import ejson
	>>> import datetime
	>>> ejson.dumps({"createdAt": datetime.date(2010, 10, 10)})
	'{"createdAt": {"$date": 1286668800000}}'
	>>>
	>>> ejson.loads('{"createdAt": {"$date": 1286668800000}}')
	{'createdAt': datetime.datetime(2010, 10, 10)}

Use with built-in JSON functions:

    import json
    import ejson

    print(json.loads('{"$binary": "SGVsbG8gd29ybGQh"}', cls=ejson.EJSONDecoder))

### EJSON <-> Python types

| EJSON type    | Python type     |
| ------------- | --------------- |
| $date         | `datetime.datetime` (and `datetime.date` when encoding) |
| $binary       | `str` (Python 2.x; decoding only), `bytes` (Python 3.x) |
| $type/$value  | *user-specified* |

### Advanced Usage

The EJSON format allows for user-specified types:

	{"$type": TYPENAME, "$value": VALUE}

These can be handled with the `custom_type_hooks` keyword. The encoder expects these hooks as a list of 3-tuples in the format `(cls, type_name, encoder_callback)` and the decoder expects a dict or a list of 2-tuples in the format `(type_name, decoder_callback)`. For example:
	
	>>> v = ejson.dumps(set(['a', 'b', 'c']), custom_type_hooks=[(set, 'set', list)])
	>>> v
	'{"$value": ["a", "c", "b"], "$type": "set"}'
	>>> ejson.loads(v, custom_type_hooks=[('set', set)])
	{'a', 'c', 'b'}
	
If the decoder encounters a user-specified type it cannot handle, it raises an `ejson.UnknownTypeError(ValueError)`.


## See also

- [Meteor](https://www.meteor.com)
- [EJSON - Meteor Documentation](http://docs.meteor.com/#/full/ejson)
- [meteor-ejson NPM package](https://www.npmjs.com/package/meteor-ejson)