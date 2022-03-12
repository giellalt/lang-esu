Finite State Morphological Analyzer for Central Alaskan Yup'ik
==============================================================

[![GitHub issues](https://img.shields.io/github/issues-raw/giellalt/lang-esu)](https://github.com/giellalt/lang-esu/issues)
[![Build Status](https://divvun-tc.thetc.se/api/github/v1/repository/giellalt/lang-esu/main/badge.svg)](https://github.com/giellalt/lang-esu/actions)
[![License](https://img.shields.io/github/license/giellalt/lang-esu)](https://github.com/giellalt/lang-esu/blob/main/LICENSE)

Central Alaskan Yup'ik (CAY) (ISO 639-3: esu) is a member of the Inuit-Yupik-Unangan (IYU) (also known as Eskimo-Aleut) language family. It is spoken in south-west Alaska among the Yukon-Kuskokwim Delta and Bristol Bay areas.

This CAY morphological analyzer/generator can **analyze** (break the word into its individual parts) and **generate** (build a word from its individual parts) Yup'ik words. The underlying form is composed of morphemes represented by the analysis of Jacobson's (1984/1995/2012) [dictionary](http://www.uaf.edu/anla/item.xml?id=CY972J2012) and grammar book. It is build using the open source [HFST tools](https://hfst.github.io). This project was developed with `hfst 3.15.2`.

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
