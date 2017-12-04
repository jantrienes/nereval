import os
import pytest
from muceval import (
    correct_text, correct_type, count_correct, has_overlap, Entity, precision, recall, evaluate,
    _parse_json, evaluate_json
)

def test_has_overlap():
    a = Entity('CILINDRISCHE PLUG', 'Productname', 0)
    b = Entity('PLUG', 'Productname', 13)
    assert has_overlap(a, b) is True
    assert has_overlap(b, a) is True

    b = Entity('PLUG', 'Productname', 18)
    assert has_overlap(a, b) is False

def test_has_overlap_open_interval():
    a = Entity('PLUG', 'Productname', 0)
    b = Entity('AB', 'Productname', 4)
    assert has_overlap(a, b) is False
    assert has_overlap(b, a) is False

def test_entity():
    e = Entity('CILINDRISCHE PLUG', 'Productname', 0)
    assert e.text == 'CILINDRISCHE PLUG'
    assert e.type == 'Productname'
    assert e.start == 0

def test_correct_text_symmetry():
    true = Entity("CILINDRISCHE PLUG", "Productname", 0)
    pred = Entity("CILINDRISCHE", "Productname", 0)
    assert correct_text(true, pred) is False
    assert correct_text(pred, true) is False
    assert correct_text(true, true) is True
    assert correct_text(pred, pred) is True

def test_correct_text_without_overlap():
    true = Entity("CILINDRISCHE PLUG", "Productname", 0)
    pred = Entity("CILINDRISCHE PLUG", "Productname", 11)
    assert correct_text(true, pred) is False

def test_correct_text_type_mismatch():
    true = Entity("a", "Productname", 0)
    pred = Entity("a", "Material", 0)
    assert correct_text(true, pred) is True

def test_correct_type_symmetry():
    true = Entity("CILINDRISCHE PLUG", "Productname", 0)
    pred = Entity("PLUG", "Productname", 13)
    assert correct_type(true, pred) is True
    assert correct_type(pred, true) is True
    assert correct_type(true, true) is True
    assert correct_type(pred, pred) is True

def test_correct_type_with_overlap():
    true = Entity('CILINDRISCHE', 'Productname', 0)
    pred = Entity('CILINDRISCHE PLUG', 'Productname', 0)
    assert correct_type(true, pred) is True

def test_correct_type_without_overlap():
    true = Entity("PLUG", "Productname", 0)
    pred = Entity("CILINDRISCHE PLUG", "Productname", 21)
    assert correct_type(true, pred) is False

def test_correct_type_with_mismatch():
    true = Entity("PLUG", "Productname", 0)
    pred = Entity("PLUG", "Material", 0)
    assert correct_type(true, pred) is False

def test_count_correct():
    # CILINDRISCHE PLUG     DIN908  M10X1   foo
    # B_PROD       I_PROD   B_PROD  B_DIM   O
    x = [
        Entity("CILINDRISCHE PLUG", "Productname", 0),
        Entity("DIN908", "Productname", 18),
        Entity("M10X1", "Dimension", 25)
    ]

    # CILINDRISCHE PLUG     DIN908  M10X1   foo
    # B_PROD       B_PROD   B_PROD  B_PROD  B_PROD
    y = [
        # correct type, wrong text
        Entity("CILINDRISCHE", "Productname", 0),
        # correct type, wrong text
        Entity('PLUG', 'Productname', 13),
        # correct type, correct text
        Entity("DIN908", "Productname", 18),
        # wrong type, correct text
        Entity("M10X1", "Productname", 25),
        # wrong type, wrong text (no entity)
        Entity('foo', 'Productname', 35)
    ]

    count_correct_text, count_correct_type = count_correct(x, y)
    assert count_correct_text == 2
    assert count_correct_type == 2

    # is not necessarily symmetric!
    count_correct_text, count_correct_type = count_correct(y, x)
    assert count_correct_text == 2
    assert count_correct_type == 3

    count_correct_text, count_correct_type = count_correct([], [])
    assert count_correct_text == 0
    assert count_correct_type == 0

def test_precision():
    assert precision(0, 10) == 0
    assert precision(0, 0) == 0
    assert precision(10, 10) == 1
    assert precision(5, 10) == 0.5

def test_recall():
    assert recall(0, 0) == 0
    assert recall(0, 10) == 0
    assert recall(10, 10) == 1
    assert precision(5, 10) == 0.5


def test_evaluate():
    # CILINDRISCHE PLUG     DIN908  M10X1   foo
    # B_PROD       I_PROD   B_PROD  B_DIM   O
    x = [
        Entity("CILINDRISCHE PLUG", "Productname", 0),
        Entity("DIN908", "Productname", 18),
        Entity("M10X1", "Dimension", 25)
    ]

    # CILINDRISCHE PLUG     DIN908  M10X1   foo
    # B_PROD       B_PROD   B_PROD  B_PROD  B_PROD
    y = [
        # correct type, wrong text
        Entity("CILINDRISCHE", "Productname", 0),
        # correct type, wrong text
        Entity('PLUG', 'Productname', 13),
        # correct type, correct text
        Entity("DIN908", "Productname", 18),
        # wrong type, correct text
        Entity("M10X1", "Productname", 25),
        # wrong type, wrong text (no entity)
        Entity('foo', 'Productname', 35)
    ]

    # dataset containing a single description
    assert evaluate([x], [y]) == 0.5
    assert evaluate([y], [x]) == 0.625
    # multiple descriptions
    assert evaluate([x, y], [x, y]) == 1
    assert evaluate([x, y], [y, x]) == 0.5625
    # edge cases
    assert evaluate([x], [[]]) == 0
    assert evaluate([[]], [x]) == 0

def test_evaluate_different_shapes():
    x = [[], []]
    y = [[], [], []]

    with pytest.raises(ValueError):
        evaluate(x, y)

def test_parse_json():
    file_name = os.path.join(os.path.dirname(__file__), 'input.json')
    predictions = _parse_json(file_name)
    assert len(predictions) == 1
    instance = predictions[0]
    assert instance['text'] == 'a b'
    assert instance['true'][0] == Entity('a', 'NAME', 0)
    assert instance['predicted'][0] == Entity('a', 'LOCATION', 0)

def test_evaluate_json():
    file_name = os.path.join(os.path.dirname(__file__), 'input.json')
    assert isinstance(evaluate_json(file_name), float)
