This is a Python library that offers conventional anonymization techniques, utility metrics, and verification methods.

# Installation

You can install the package via the command line:

```bat
pip install anonymity-api
```

# Package Description

The package is divided into three different modules, as mentioned previously:
* anonymity
* utility
* verifier

## Anonymity

This module contains the functions to anonymize data.

The conventional anonymization functions available are:
* k-anonymity
* distinct l-diversity
* entropy l-diversity
* recursive (c,l)-diversity
* t-closeness

Another available function is the suggestion function that, given a dataset and its characteristics (list with quasi-identifiers and sensitive attributes), suggests an anonymization to use, returning an anonymized dataset without choosing a technique. This is helpful for users who may not know how to anonymize data or aren't familiar with it.

We also offer Workload-Aware anonymization techniques. These take the usual anonymization parameters also present in the conventional anonymization techniques but, in addition to that, the user can give a query representing to work to be done on the dataset. This ensures higher utility over the tasks to be done.

| Technique|      Query|
|----------|:-------------:|
| Simple query |  (*quasi-identifier* (operation*) *value* ) |
| Keeping correlation|    corr( *quasi-identifier*, *sensitive-attribute* )|
| Grouping | group( *quasi-identifier*, *value* ) |

*operation can be: >, >=, =, < or <=

## Utility

The utility module offers some utility techniques and a function that given an anonymized dataset, replaces the interval on the quasi-identifiers with a value comprehended in it.

The utility metrics available are:
* Discernibility Metric
* Average Equivalence Class Size Metric
* Normalized Certainty Penalty

## Verifier

This module given an anonymized dataset offers funtions for each of the conventional techniques in the Anonymization module.

These functions will say which parameter was used to anonymize the dataset. For instance, it would give the K for k-anonymity, l for distinct l-diversity, and so forth.