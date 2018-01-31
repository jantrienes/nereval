nereval
=======
.. image:: https://travis-ci.org/jantrienes/nereval.svg?branch=master
    :target: https://travis-ci.org/jantrienes/nereval

Evaluation script for named entity recognition (NER) systems based on entity-level F1 score.

Definition
----------
The metric as implemented here has been described by Nadeau and Sekine (2007) and was widely used as part of the Message Understanding Conferences (Grishman and Sundheim, 1996). It evaluates an NER system according to two axes: whether it is able to assign the right type to an entity, and whether it finds the exact entity boundaries. For both axes, the number of correct predictions (COR), the number of actual predictions (ACT) and the number of possible predictions (POS) are computed. From these statistics, precision and recall can be derived:

::

  precision = COR/ACT
  recall = COR/POS


The final score is the micro-averaged F1 measure of precision and recall of both type and boundary axes.

Installation
------------
.. code-block:: bash

  pip install nereval


Usage
-----
The script can either be used from within Python or from the command line when classification results have been written to a JSON file.

Usage from Command Line
~~~~~~~~~~~~~~~~~~~~~~~
Assume we have the following classification results in ``input.json``:

.. code-block:: json

  [
    {
      "text": "CILINDRISCHE PLUG",
      "true": [
        {
          "text": "CILINDRISCHE PLUG",
          "type": "Productname",
          "start": 0
        }
      ],
      "predicted": [
        {
          "text": "CILINDRISCHE",
          "type": "Productname",
          "start": 0
        },
        {
          "text": "PLUG",
          "type": "Productname",
          "start": 13
        }
      ]
    }
  ]


Then the script can be executed as follows:

.. code-block:: bash

  python nereval.py input.json
  F1-score: 0.33


Usage from Python
~~~~~~~~~~~~~~~~~
Alternatively, the evaluation metric can be directly invoked from within python. Example:

.. code-block:: python

  import nereval
  from nereval import Entity

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

  score = nereval.evaluate([y_true], [y_pred])
  print('F1-score: %.2f' % score)
  F1-score: 0.33


Note on Symmetry
----------------
The metric itself is not symmetric due to the inherent problem of word overlaps in NER. So ``evaluate(y_true, y_pred) != evaluate(y_pred, y_true)``. This comes apparent if we consider the following example (tagger uses an BIO scheme):

.. code-block:: bash

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


Notes and References
--------------------
Used in a student research project on natural language processing at `University of Twente, Netherlands <https://www.utwente.nl>`_.

**References**

* Grishman, R., & Sundheim, B. (1996). `Message understanding conference-6: A brief history <http://www.aclweb.org/anthology/C96-1079>`_. *In COLING 1996 Volume 1: The 16th International Conference on Computational Linguistics* (Vol. 1).
* Nadeau, D., & Sekine, S. (2007). `A survey of named entity recognition and classification <http://www.jbe-platform.com/content/journals/10.1075/li.30.1.03nad>`_. *Lingvisticae Investigationes*, 30(1), 3-26.
