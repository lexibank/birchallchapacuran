from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class Language(pylexibank.Language):
    Source = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "birchallchapacuran"
    language_class = Language

    form_spec = pylexibank.FormSpec(missing_data=("?", "-", "", "?-"))

    def cmd_download(self, args):
        self.raw_dir.xls2csv("chapacuran.xlsx")

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        sources = {s["ID"]: s["Source"].split(";") for s in self.languages}

        languages = args.writer.add_languages(lookup_factory=lambda l: l["Name"])

        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )

        for row in self.raw_dir.read_csv("chapacuran.Sheet1.csv", dicts=True):
            # remove trailing spaces in all cells
            row = {r.strip(): k.strip() for (r, k) in row.items()}
            concept = concepts[row["Meaning"]]
            cogid = "%s-%s" % (concept, row["Set"])
            for lang in languages:
                lex = args.writer.add_forms_from_value(
                    Language_ID=languages[lang],
                    Parameter_ID=concept,
                    Value=row.get(lang),
                    Source=sources[languages[lang]],
                    Cognacy=cogid,
                )
                for l in lex:
                    args.writer.add_cognate(lexeme=l, Cognateset_ID=cogid)
