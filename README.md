# muceval
MUC-like evaluation script for named entity recognition systems as used in the advanced research project for NLP.

## Installation
```sh
git clone https://github.com/jantrienes/twente-arp-nlp-evaluation.git
cd twente-arp-nlp-evaluation
# either install this as module via pip
pip install .

# or copy main python file into local project
cp muceval.py ~/theproject
```

## Usage
The script can either be used from within Python or from the command line when classification results have been written to a JSON file.

### Usage from Command Line
Assume we have the following classification results in `input.json`:

```json
[
  {
    "text": "a b",
    "true": [
      {
        "text": "a",
        "type": "NAME",
        "start": 0
      }
    ],
    "predicted": [
      {
        "text": "a",
        "type": "LOCATION",
        "start": 0
      }
    ]
  }
]
```

Then the script can be executed as follows:

```sh
python muceval.py input.json
F1-score: 0.50
```

### Usage from Python
Alternatively, the evaluation metric can be directly invoked from within python. Example:

```py
import muceval
from muceval import Entity

# Ground-truth:
# CILINDRISCHE PLUG
# B_PROD       I_PROD
y_true = [
    Entity('CILINDRISCHE PLUG', 'Productname', 0)
]

# Prediction:
# CILINDRISCHE PLUG
# B_PROD       B_PROD
y_pred = [
    # correct type, wrong text
    Entity('CILINDRISCHE', 'Productname', 0),
    # correct type, wrong text
    Entity('PLUG', 'Productname', 13)
]

score = muceval.evaluate([y_true], [y_pred])
print('F1-score: %.2f' % score)
F1-score: 0.33
```

## Important Note on Symmetry
The metric itself is not symmetric due to the inherent problem of word overlaps in NER. So `evaluate(y_true, y_pred) != evaluate(y_pred, y_true)`. This comes apparent if we consider the following example (tagger uses an IOB scheme):

```
# Example 1:
Input:     CILINDRISCHE PLUG     DIN908  M10X1   Foo
Truth:     B_PROD       I_PROD   B_PROD  B_DIM   O
Predicted: B_PROD       B_PROD   B_PROD  B_PROD  B_PROD

Correct Text: 2
Correct Type: 2

# Example 2 (inversed):
Input:     CILINDRISCHE PLUG     DIN908  M10X1   Foo
Truth:     B_PROD       B_PROD   B_PROD  B_PROD  B_PROD
Predicted: B_PROD       I_PROD   B_PROD  B_DIM   O

Correct Text: 2
Correct Type: 3
```
