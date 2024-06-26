Finite State Morphological Analyzer for Central Alaskan Yup'ik
==============================================================

[![Maturity](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgiellalt%2Flang-esu%2Fgh-pages%2Fmaturity.json)](https://giellalt.github.io/MaturityClassification.html)
![Lemma count](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgiellalt%2Flang-esu%2Fgh-pages%2Flemmacount.json)
[![GitHub issues](https://img.shields.io/github/issues-raw/giellalt/lang-esu)](https://github.com/giellalt/lang-esu/issues)
[![License](https://img.shields.io/github/license/giellalt/lang-esu)](https://github.com/giellalt/lang-esu/blob/main/LICENSE)
[![Doc Build Status](https://github.com/giellalt/lang-esu/workflows/Docs/badge.svg)](https://github.com/giellalt/lang-esu/actions)
[![CI/CD Build Status](https://divvun-tc.giellalt.org/api/github/v1/repository/giellalt/lang-esu/main/badge.svg)](https://divvun-tc.giellalt.org/api/github/v1/repository/giellalt/lang-esu/main/latest)

Download nightly / CI/CD installation packages for testing (contains the core zhfst file(s)):

[![Windows](https://img.shields.io/badge/download%40latest-Windows--bhfst-brightgreen)](https://pahkat.uit.no/main/download/speller-esu?platform=windows&channel=nightly)
[![MacOS](https://img.shields.io/badge/download%40latest-macOS--bhfst-brightgreen)](https://pahkat.uit.no/main/download/speller-esu?platform=macos&channel=nightly)
[![Mobile](https://img.shields.io/badge/download%40latest-mobile--bhfst-brightgreen)](https://pahkat.uit.no/main/download/speller-esu?platform=mobile&channel=nightly)

__NB!!__ Note that the nightly / CI/CD installation packages are not tested for language quality, and might contain regressions and errors.

Central Alaskan Yup'ik (CAY) (ISO 639-3: esu) is a member of the Inuit-Yupik-Unangan (IYU) (also known as Eskimo-Aleut) language family. It is spoken in south-west Alaska among the Yukon-Kuskokwim Delta and Bristol Bay areas.

This CAY morphological analyzer/generator can **analyze** (break the word into its individual parts) and **generate** (build a word from its individual parts) Yup'ik words. The underlying form is composed of morphemes represented by the analysis of Jacobson's (1984/1995/2012) [dictionary](http://www.uaf.edu/anla/item.xml?id=CY972J2012) and grammar book. It is build using the open source [HFST tools](https://hfst.github.io). This project was developed with `hfst 3.15.2`.

Download and test speller files
-------------------------------

The speller files downloadable at the top of this page (the `*.bhfst` files) can
be used with [divvunspell](https://github.com/divvun/divvunspell), to test their
performance. These files are the exact same ones as installed on users' computers
and mobile phones. Desktop and mobile speller files differ from each other in the
error model and should be tested separately — thus also two different downloads.

Documentation
-------------

Documentation can be found at:

- [Language specific documentation](https://giellalt.github.io/lang-esu/)
- [General documentation](https://giellalt.github.io/)

FST Stack
---------
1. `lexc` - `esu.lexc` - lexicon and morphotactics
2. `xfst` - `esu.lexc.xfst` - orthography → phonemes, morphologically conditioned allomorphy
3. `twolc` - `esu.twol` - morphophonology, phonologically conditioned allomorphy
4. `twolc` - `esu.stress.twol` - prosodic stress marking on vowels used for prosodic adjustments
5. `xfst` - `esu.twol.xfst` - prosodic adjustments, phonemes → orthography

Installation
------------
1. Install dependency: [HFST tools](https://hfst.github.io). Tested with `hfst 3.15.2`. <br> Note: MacOS users may have an easier time installing HFST with this [Homebrew tap](https://github.com/UAlbertaALTLab/homebrew-hfst).

2. Run `make` to run the Makefile and compile the FST stack

Output Files
------------
* `esu.ana.hfstol`: Morphological analyser
	* Input: `calinrituq`
	* Output: `cali-–nrite[V→V][V][Intr][Ind][S_3Sg]`

* `esu.gen.hfstol`: Morphological generator
	* Input: `cali-–nrite[V→V][V][Intr][Ind][S_3Sg]`
	* Output: `calinrituq`

* `esu.seg.hfstol`: Morphological segmenter
	* Input: `calinrituq`
	* Output: `cali>nrit>uq`

Usage
-----

In the unix terminal, run this command to use the HFST lookup program:

	echo "wordToInput" | hfst-optimized-lookup hfstName

where `wordToInput` is the Yup'ik word to analyze/generate and the `hfstName` is either: `esu.ana.hfstol | esu.gen.hfstol | esu.seg.hfstol`.

License
-------

This Central Alaskan Yup'ik FST morphological analyzer/generator and the associated source code is available under the
[GNU Affero General Public License (GNU AGPL v.3)](https://www.gnu.org/licenses/agpl-3.0.en.html):

> Copyright (C) 2020 Lonny Alaskuk Strunk
> 	
> This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
> 	
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
> 	
> You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

Citing
------

<!-- Add language specific citation stuff here and to the CITATION.cff -->

If you use language data from more than one GiellaLT language, consider citing
[our LREC 2022 article on whole
infra](https://aclanthology.org/2022.lrec-1.125/):

> Linda Wiechetek, Katri Hiovain-Asikainen, Inga Lill Sigga Mikkelsen,
  Sjur Moshagen, Flammie Pirinen, Trond Trosterud, and Børre Gaup. 2022.
  *Unmasking the Myth of Effortless Big Data - Making an Open Source
  Multi-lingual Infrastructure and Building Language Resources from Scratch*.
  In Proceedings of the Thirteenth Language Resources and Evaluation Conference,
  pages 1167–1177, Marseille, France. European Language Resources Association.

If you use bibtex, following is as it is on ACL anthology:

```bibtex
@inproceedings{wiechetek-etal-2022-unmasking,
    title = "Unmasking the Myth of Effortless Big Data - Making an Open Source
    Multi-lingual Infrastructure and Building Language Resources from Scratch",
    author = "Wiechetek, Linda  and
      Hiovain-Asikainen, Katri  and
      Mikkelsen, Inga Lill Sigga  and
      Moshagen, Sjur  and
      Pirinen, Flammie  and
      Trosterud, Trond  and
      Gaup, B{\o}rre",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation
    Conference",
    month = jun,
    year = "2022",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2022.lrec-1.125",
    pages = "1167--1177"
}
```
