#!/usr/bin/env python3
"""Copy the legacy srcV2 sources into the standard morphology layout."""

from pathlib import Path
import re
import shutil


MORPHOLOGY = Path(__file__).resolve().parent
SRCV2 = MORPHOLOGY / "orig" / "srcV2"

STEM_LEXICONS = {
    "Exceptions": "exceptions.lexc",
    "NonYupikBase": "non-yupik.lexc",
    "Particle": "particles.lexc",
    "Ignorative": "ignorative.lexc",
    "ProperNoun": "propernouns.lexc",
    "NounBase": "nouns.lexc",
    "VerbBase": "verbs.lexc",
    "DimensionalRoot": "dimensional.lexc",
    "EmotionalRoot": "emotional.lexc",
    "PosturalRoot": "postural.lexc",
    "PersonalPronoun": "pronouns.lexc",
    "QuantQual": "quantqual.lexc",
    "Demonstrative": "demonstratives.lexc",
    "Positional": "positionals.lexc",
    "Numeral": "numerals.lexc",
}

COPIED_SOURCES = {
    "esu.ana.twol": "remove-boundaries.twolc",
    "esu.seg.twol": "collapse-boundaries.twolc",
    "esu.stress.twol": "assign-stress.twolc",
    "esu.twol": "phonology.twolc",
    "esu.lexc.xfst": "lexicon.cleanup.xfscript",
    "esu.lexc.permissive.xfst": "lexicon.cleanup.permissive.xfscript",
    "esu.twol.xfst": "extra-phonology.xfscript",
    "esu.twol.permissive.xfst": "extra-phonology.permissive.xfscript",
}


def split_lexc() -> None:
    source = (SRCV2 / "esu.lexc").read_text(encoding="utf-8")
    sections = list(re.finditer(r"(?m)^LEXICON[ \t]+([^\s!]+).*?(?:\n|$)", source))
    if not sections or sections[0].group(1) != "Root":
        raise ValueError("srcV2/esu.lexc must start with the Root lexicon")

    root_end = sections[1].start() if len(sections) > 1 else len(source)
    (MORPHOLOGY / "root.lexc").write_text(source[:root_end], encoding="utf-8")

    stems: dict[str, list[str]] = {}
    affixes: list[str] = []
    for index, section in enumerate(sections[1:], start=1):
        end = sections[index + 1].start() if index + 1 < len(sections) else len(source)
        name = section.group(1)
        content = source[section.start():end]
        stem_file = STEM_LEXICONS.get(name)
        if stem_file:
            stems.setdefault(stem_file, []).append(content)
        else:
            affixes.append(content)

    stems_dir = MORPHOLOGY / "stems"
    affixes_dir = MORPHOLOGY / "affixes"
    stems_dir.mkdir(parents=True, exist_ok=True)
    affixes_dir.mkdir(parents=True, exist_ok=True)
    for filename, contents in stems.items():
        (stems_dir / filename).write_text("".join(contents), encoding="utf-8")
    (affixes_dir / "affixes.lexc").write_text("".join(affixes), encoding="utf-8")


def main() -> None:
    split_lexc()
    for source, destination in COPIED_SOURCES.items():
        shutil.copyfile(SRCV2 / source, MORPHOLOGY / destination)


if __name__ == "__main__":
    main()