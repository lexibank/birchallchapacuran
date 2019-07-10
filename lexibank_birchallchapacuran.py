# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.misc import slug
import attr

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset, Language as BaseLanguage


@attr.s
class Language(BaseLanguage):
   Sources = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'birchallchapacuran'
    language_class = Language

    def cmd_download(self, **kw):
        self.raw.xls2csv('chapacuran.xlsx')

    def cmd_install(self, **kw):
        concept_map = {
            x.english: (x.concepticon_id, x.concepticon_gloss)
            for x in self.conceptlist.concepts.values()
        }
        
        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            ds.add_languages()
            for r in self.read_csv('chapacuran.Sheet1.csv'):
                csid, csgloss = concept_map[r['Meaning']]
                ds.add_concept(ID=csid, Name=r['Meaning'], Concepticon_ID=csid, Concepticon_Gloss=csgloss)
                for lang in self.languages:
                    if lang['Name'] in r:  # ignore missing/empty entries
                        cogid = '%s-%s' % (slug(r['Meaning']), r['Set'])
                        for row in ds.add_lexemes(
                            Language_ID=lang['ID'],
                            Parameter_ID=csid,
                            Form=r[lang['Name']],
                            Value=r[lang['Name']],
                            Source=lang['Sources'].split(';'),
                            Cognacy=cogid
                        ):
                            ds.add_cognate(lexeme=row, Cognateset_ID=cogid)

    def read_csv(self, filename):
        """Lightweight wrapper to read data records, and tidy them gently"""
        for record in self.raw.read_csv(filename, dicts=True):
            yield {k.strip(): v.strip() for k, v in record.items()
                   if v.strip() not in ['?', '', '-', '?-']}
