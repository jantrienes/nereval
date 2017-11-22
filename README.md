# muceval
MUC-like evaluation script for named entity recognition systems as used in the advanced research project for NLP.

## Installation
```sh
git clone https://github.com/jantrienes/twente-arp-nlp-evaluation.git
cd twente-arp-nlp-muceval
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
x = [
    Entity("CILINDRISCHE PLUG", "Productname", 0)
]

# Prediction:
# CILINDRISCHE PLUG
# B_PROD       B_PROD
y = [
    # correct type, wrong text
    Entity("CILINDRISCHE", "Productname", 0),
    # correct type, wrong text
    Entity('PLUG', 'Productname', 13)
]

print('F1-score: %.2f' % muceval.evaluate([x],[y]))
F1-score: 0.33
```
