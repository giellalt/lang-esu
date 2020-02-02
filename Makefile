# By default produce:
#	esu.gen.hfst: Morphological generator
#	esu.ana.hfst: Morphological analyser
#	esu.seg.hfst: Morphological segmenter

all:  esu.gen.hfst   esu.ana.hfst   esu.seg.hfst   \
	  esu.gen.hfstol esu.ana.hfstol esu.seg.hfstol

# This is the lexicon file
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   cali–nrite+'(g/t)uq
esu.lexc.hfst: esu.lexc esu.lexc.xfst.hfst 
	hfst-lexc --Werror esu.lexc | hfst-compose -1 - -2 esu.lexc.xfst.hfst -o esu.lexc.hfst

# This is the lexicon xfst file, which handles cases lexc isn't suited for
# 	e.g. allomorphs for [Opt_PRS_2Sg]
esu.lexc.xfst.hfst: esu.lexc.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

# This is the phonology file, which maintains morpheme boundaries
#   cali–nrite+'(g/t)uq
#   cali>nrit0>>  >  uq
esu.twol.hfst: esu.twol
	hfst-twolc -i esu.twol -o esu.twol.hfst

# This is the phonology file, which assigns stress to vowels
#   cali>nrit0>>>uq
#   calí>nrit0>>>uq
esu.stress.hfst: esu.stress.twol
	hfst-twolc -i esu.stress.twol -o esu.stress.hfst

# This is the phonology xfst file, which handles cases twol isn't suited for
# 	e.g. tripleConsonantCluster e-insertion (CCC -> CeCC or CCec)
esu.twol.xfst.hfst: esu.twol.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

# This is the generator that still has morpheme boundaries
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   cali>nrit>>>uq
esu.gen.seg.hfst: esu.lexc.hfst esu.twol.hfst esu.stress.hfst esu.twol.xfst.hfst 
	hfst-compose-intersect -1 esu.lexc.hfst -2 esu.twol.hfst | hfst-compose-intersect -1 - -2 esu.stress.hfst | hfst-compose -1 - -2 esu.twol.xfst.hfst | hfst-minimise -o esu.gen.seg.hfst

# This is the phonology file, which removes morpheme boundaries
#   cali>nrit>>>uq
#   cali0nrit000uq
esu.ana.twol.hfst: esu.ana.twol
	hfst-twolc -i esu.ana.twol -o esu.ana.twol.hfst

# This is the generator that does not have morpheme boundaries
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   calinrituq
esu.gen.hfst: esu.gen.seg.hfst esu.ana.twol.hfst
	hfst-compose-intersect -1 esu.gen.seg.hfst -2 esu.ana.twol.hfst | hfst-minimise -o esu.gen.hfst

# This is the analyser that does not have morpheme boundaries
#   calinrituq
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
esu.ana.hfst: esu.gen.hfst
	hfst-invert esu.gen.hfst -o esu.ana.hfst

# This is the phonology file, which collapses morpheme boundaries
#   cali>nrit>>>uq
#   cali>nrit>00uq
esu.seg.twol.hfst: esu.seg.twol
	hfst-twolc -i esu.seg.twol -o esu.seg.twol.hfst

# This is a segmenter which takes surface forms and produces segmented forms
#   calinrituq
#  (cali-–nrite[V→V][V][Intr][Ind][S_3Sg])
#  (cali>nrit>>>uq)
#   cali>nrit>uq
esu.seg.hfst: esu.ana.hfst esu.gen.seg.hfst esu.seg.twol.hfst
	hfst-compose -F -1 esu.ana.hfst -2 esu.gen.seg.hfst -o tmp.hfst
	hfst-compose-intersect -1 tmp.hfst -2 esu.seg.twol.hfst -o esu.seg.hfst
	@rm tmp.hfst
#	hfst-compose -F -1 esu.ana.hfst -2 esu.gen.seg.hfst | hfst-compose-intersect -1 - -2 esu.seg.twol.hfst | hfst-minimise -o esu.seg.hfst

# These are the optimized-lookup generator, analyzer, and segmenter FSTs
esu.gen.hfstol: esu.gen.hfst
	hfst-fst2fst -w esu.gen.hfst -o esu.gen.hfstol
esu.ana.hfstol: esu.ana.hfst
	hfst-fst2fst -w esu.ana.hfst -o esu.ana.hfstol
esu.seg.hfstol: esu.seg.hfst
	hfst-fst2fst -w esu.seg.hfst -o esu.seg.hfstol


test: test-python

test-python: esu.gen.hfst esu.pairs.gold/*
	python3 runTest.py esu.gen.hfst esu.pairs.gold/*

clean:
	rm *.hfst *.hfstol
