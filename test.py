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


# The final list of basic vocabulary includes 126 meanings (for the full data
# set, see the Supplementary Materials presented in the online Appendix).
def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 126


# A data set of 285 cognate sets of basic vocabulary was compiled using the 
# sources presented in 2 above.
def test_cognates(cldf_dataset, cldf_logger):
    cogsets = {c['Cognateset_ID'] for c in cldf_dataset['CognateTable']}
    assert len(cogsets) == 285