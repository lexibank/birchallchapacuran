# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.misc import slug

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset


class Dataset(BaseDataset):
    dir = Path(__file__).parent

    def cmd_download(self, **kw):
        self.raw.xls2csv('chapacuran.xlsx')

    def cmd_install(self, **kw):
        concept_map = {
            x.english: x.concepticon_id for x in self.conceptlist.concepts.values()}

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            for lang in self.languages:
                ds.add_language(
                    ID=lang['NAME'],
                    glottocode=lang['GLOTTOCODE'],
                    iso=lang['ISO'],
                    name=lang['NAME'])
            for r in self.read_csv('chapacuran.Sheet1.csv'):
                csid = concept_map.get(r['Meaning'], None)
                assert csid, 'Missing concept %s' % r['Meaning']
                ds.add_concept(ID=csid, gloss=r['Meaning'], conceptset=csid)

                for lang in self.languages:
                    if lang['NAME'] in r:  # ignore missing/empty entries
                        cogid = '%s-%s' % (slug(r['Meaning']), r['Set'])
                        for row in ds.add_lexemes(
                            Language_ID=lang['NAME'],
                            Parameter_ID=csid,
                            Value=r[lang['NAME']],
                            Cognacy=cogid,
                            Source=lang['SOURCES'].split(';'),
                        ):
                            ds.add_cognate(lexeme=row, Cognateset_ID=cogid)

    def read_csv(self, filename):
        """Lightweight wrapper to read data records, and tidy them gently"""
        for record in self.raw.read_csv(filename, dicts=True):
            yield {k.strip(): v.strip() for k, v in record.items()
                   if v.strip() not in ['?', '', '-', '?-']}