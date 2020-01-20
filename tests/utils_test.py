import json

import pytest

from swaggerf.core import utils
from swaggerf.core.utils import immutable


def test_merge_simple_dicts_without_precedence():
    a = {'a': 'value'}
    b = {'b': 'other value'}
    assert utils.merge(a, b) == {'a': 'value', 'b': 'other value'}

def test_merge_simple_dicts_with_precedence():
    a = {'a': 'value', 'ab': 'overwritten'}
    b = {'b': 'other value', 'ab': 'keep'}
    assert utils.merge(a, b) == {'a': 'value', 'b': 'other value', 'ab': 'keep'}

def test_recursions():
    a = {
        'a': 'value',
        'ab': 'overwritten',
        'nested_a': {
            'a': 'nested'
        },
        'nested_a_b': {
            'a': 'a only',
            'ab': 'overwritten'
        }
    }
    b = {
        'b': 'other value',
        'ab': 'keep',
        'nested_b': {
            'b': 'nested'
        },
        'nested_a_b': {
            'b': 'b only',
            'ab': 'keep'
        }
    }
    assert utils.merge(a, b) == {
        'a': 'value',
        'b': 'other value',
        'ab': 'keep',
        'nested_a': {
            'a': 'nested'
        },
        'nested_b': {
            'b': 'nested'
        },
        'nested_a_b': {
            'a': 'a only',
            'b': 'b only',
            'ab': 'keep'
        }
    }

def test_recursions_with_empty():
    a = {}
    b = {
        'b': 'other value',
        'ab': 'keep',
        'nested_b': {
            'b': 'nested'
        },
        'nested_a_b': {
            'b': 'b only',
            'ab': 'keep'
        }
    }
    assert utils.merge(a, b) == b


def test_no_transform():
    assert utils.camel_to_dash('test') == 'test'

@pytest.mark.parametrize('value,expected', [
    ('aValue', 'a_value'),
    ('aLongValue', 'a_long_value'),
    ('Upper', 'upper'),
    ('UpperCase', 'upper_case'),
])

def test_transform(value, expected):
    assert utils.camel_to_dash(value) == expected


def test_single_value():
    data, code, headers = utils.unpack('test')
    assert data == 'test'
    assert code == 200
    assert headers == {}

def test_single_value_with_default_code():
    data, code, headers = utils.unpack('test', 500)
    assert data == 'test'
    assert code == 500
    assert headers == {}

def test_value_code():
    data, code, headers = utils.unpack(('test', 201))
    assert data == 'test'
    assert code == 201
    assert headers == {}

def test_value_code_headers():
    data, code, headers = utils.unpack(('test', 201, {'Header': 'value'}))
    assert data == 'test'
    assert code == 201
    assert headers == {'Header': 'value'}

def test_value_headers_default_code():
    data, code, headers = utils.unpack(('test', None, {'Header': 'value'}))
    assert data == 'test'
    assert code == 200
    assert headers == {'Header': 'value'}

def test_too_many_values():
    with pytest.raises(ValueError):
        utils.unpack((None, None, None, None))

def test_immutable_raises_when_set():
    obj = immutable(x=2, y=23)

    with pytest.raises(TypeError):
        obj['x'] = 5

    with pytest.raises(TypeError):
        obj.x = 5

    with pytest.raises(TypeError):
        del obj['x']

    with pytest.raises(TypeError):
        del obj.x

def test_immutable_none_comparison():
    obj = immutable(x=2, y=23)
    isEqual = obj == None
    assert isEqual is not True

def test_immutable_repr_dumps_json():
    obj = immutable(x=2, y=23)
    r = repr(obj)
    json.loads(r)

def test_immutable_str_dumps_json():
    obj = immutable(x=2, y=23)
    s = str(obj)
    json.loads(s)
