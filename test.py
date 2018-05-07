# coding: utf-8
from __future__ import unicode_literals


def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['FormTable'])) == 1037
    assert len([
        f for f in cldf_dataset['FormTable'] if f['Form'] == 'waza'
    ]) == 2


def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 10


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 13


# Birchall et al: "The final list of basic vocabulary includes 126 meanings 
# (for the full data set, see the Supplementary Materials presented in the
# online Appendix)."
def test_parameters(cldf_dataset, cldf_logger):
    # actually, there are 125 meanings, the extra is because "Mother" is entered
    # in the wordlist as "Mother" and "Mother " (note trailing space). A naive 
    # count of the different word strings (without removing whitespace) has led
    # to the incorrect count.
    assert len(list(cldf_dataset['ParameterTable'])) == 125


# Birchall et al: "A data set of 285 cognate sets of basic vocabulary was 
# compiled using the sources presented in 2 above."
def test_cognates(cldf_dataset, cldf_logger):
    cogsets = {c['Cognateset_ID'] for c in cldf_dataset['CognateTable']}
    assert len(cogsets) == 285

