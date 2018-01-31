# pylint: disable=C0103
from __future__ import division
import argparse
import collections
import json

Entity = collections.namedtuple('Entity', ['text', 'type', 'start'])

def has_overlap(x, y):
    """
    Determines whether the text of two entities overlap. This function is symmetric.

    Returns
    -------
    bool
        True iff text overlaps.
    """
    end_x = x.start + len(x.text)
    end_y = y.start + len(y.text)
    return x.start < end_y and y.start < end_x

def correct_text(x, y):
    """
    Assert entity boundaries are correct regardless of entity type.
    """
    return x.text == y.text and x.start == y.start

def correct_type(x, y):
    """
    Assert entity types match and that there is an overlap in the text of the two entities.
    """
    return x.type == y.type and has_overlap(x, y)

def count_correct(true, pred):
    """
    Computes the count of correctly predicted entities on two axes: type and text.

    Parameters
    ----------
    true: list of Entity
        The list of ground truth entities.
    pred: list of Entity
        The list of predicted entities.

    Returns
    -------
    count_text: int
        The number of entities predicted where the text matches exactly.
    count_type: int
        The number of entities where the type is correctly predicted and the text overlaps.
    """
    count_text, count_type = 0, 0

    for x in true:
        for y in pred:
            text_match = correct_text(x, y)
            type_match = correct_type(x, y)

            if text_match:
                count_text += 1

            if type_match:
                count_type += 1

            if type_match or text_match:
                # Stop as soon as an entity has been recognized by the system
                break

    return count_text, count_type

def precision(correct, actual):
    if actual == 0:
        return 0

    return correct / actual

def recall(correct, possible):
    if possible == 0:
        return 0

    return correct / possible

def f1(p, r):
    if p + r == 0:
        return 0

    return 2 * (p * r) / (p + r)

def evaluate(y_true, y_pred):
    """
    Evaluate classification results for a whole dataset. Each row corresponds to one text in the
    dataset.

    Parameters
    ----------
    y_true: list of list
        For each text in the dataset, a list of ground-truth entities.
    y_pred: list of list
        For each text in the dataset, a list of predicted entities.

    Returns
    -------
    float:
        Micro-averaged F1 score of precision and recall.

    Example
    -------
    >>> from nereval import Entity, evaluate
    >>> y_true = [
    ...     [Entity('a', 'b', 0), Entity('b', 'b', 2)]
    ... ]
    >>> y_pred = [
    ...     [Entity('b', 'b', 2)]
    ... ]
    >>> evaluate(y_true, y_pred)
    0.6666666666666666
    """
    if len(y_true) != len(y_pred):
        raise ValueError('Bad input shape: y_true and y_pred should have the same length.')

    correct, actual, possible = 0, 0, 0

    for x, y in zip(y_true, y_pred):
        correct += sum(count_correct(x, y))
        # multiply by two to account for both type and text
        possible += len(x) * 2
        actual += len(y) * 2

    return f1(precision(correct, actual), recall(correct, possible))

def sign_test(truth, model_a, model_b):
    better = 0
    worse = 0

    for true, a, b in zip(truth, model_a, model_b):
        score_a = evaluate([true], [a])
        score_b = evaluate([true], [b])

        if score_a - score_b > 0:
            worse += 1
        elif score_a - score_b < 0:
            better += 1

    return better, worse

def _parse_json(file_name):
    data = None

    with open(file_name) as json_file:
        data = json.load(json_file)

        dict_to_entity = lambda e: Entity(e['text'], e['type'], e['start'])
        for instance in data:
            instance['true'] = [dict_to_entity(e) for e in instance['true']]
            instance['predicted'] = [dict_to_entity(e) for e in instance['predicted']]

    return data

def evaluate_json(file_name):
    """
    Evaluate according to results in JSON file format.
    """
    y_true = []
    y_pred = []

    for instance in _parse_json(file_name):
        y_true.append(instance['true'])
        y_pred.append(instance['predicted'])

    return evaluate(y_true, y_pred)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute F1 score for predictions in JSON file.')
    parser.add_argument('file_name', help='The JSON containing classification results')
    args = parser.parse_args()

    print('F1-score: %.2f' % evaluate_json(args.file_name))
