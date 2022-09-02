# By default produce:
#	esu.gen.hfst: Morphological generator
#	esu.ana.hfst: Morphological analyzer
#	esu.seg.gen.hfst: Morphological segmenter from generator
#	esu.seg.ana.hfst: Morphological segmenter from analyzer


# all:  esu.gen.hfst   esu.ana.hfst   esu.seg.gen.hfst   esu.seg.ana.hfst   \
# 	  esu.gen.hfstol esu.ana.hfstol esu.seg.gen.hfstol esu.seg.ana.hfstol
all: esu.ana.hfstol esu.seg.gen.hfstol

### esu.seg.gen.hfstol
# esu.lexc
# esu.lexc.xfst
# esu.twol
# esu.stress.twol
# esu.twol.xfst
# esu.seg.twol

### esu.ana.hfstol
# esu.lexc
# esu.lexc.permissive.xfst
# esu.twol
# esu.stress.twol
# esu.twol.permissive.xfst
# esu.ana.twol



# This is the lexicon file
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   cali–nrite+'(g/t)uq
esu.lexc.only.hfst: srcV2/esu.lexc
	hfst-lexc --Werror srcV2/esu.lexc -o esu.lexc.only.hfst 

# This is the lexicon xfst file, which handles cases lexc isn't suited for
# 	e.g. allomorphs for [Opt_PRS_2Sg]
esu.lexc.xfst.hfst: srcV2/esu.lexc.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"
esu.lexc.permissive.xfst.hfst: srcV2/esu.lexc.permissive.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

# This is the phonology file, which maintains morpheme boundaries
#   cali–nrite+'(g/t)uq
#   cali>nrit0>>  >  uq
esu.twol.hfst: srcV2/esu.twol
	hfst-twolc -i srcV2/esu.twol -o esu.twol.hfst

# This is the phonology file, which assigns stress to vowels
#   cali>nrit0>>>uq
#   calí>nrit0>>>uq
esu.stress.hfst: srcV2/esu.stress.twol
	hfst-twolc -i srcV2/esu.stress.twol -o esu.stress.hfst

# This is the phonology xfst file, which handles cases twol isn't suited for
# 	e.g. tripleConsonantCluster e-insertion (CCC -> CeCC or CCec)
esu.twol.xfst.hfst: srcV2/esu.twol.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"
esu.twol.permissive.xfst.hfst: srcV2/esu.twol.permissive.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

# This is the phonology file, which collapses morpheme boundaries
#   cali>nrit>>>uq
#   cali0nrit>00uq
esu.seg.twol.hfst: srcV2/esu.seg.twol
	hfst-twolc -i srcV2/esu.seg.twol -o esu.seg.twol.hfst

# This is the phonology file, which removes morpheme boundaries
#   cali>nrit>>>uq
#   cali0nrit000uq
esu.ana.twol.hfst: srcV2/esu.ana.twol
	hfst-twolc -i srcV2/esu.ana.twol -o esu.ana.twol.hfst




# lexc with lext.xfst before stress
esu.lexc.hfst: esu.lexc.only.hfst esu.lexc.xfst.hfst 
	hfst-compose -1 esu.lexc.only.hfst -2 esu.lexc.xfst.hfst -o esu.lexc.hfst
esu.lexc.permissive.hfst: esu.lexc.only.hfst esu.lexc.permissive.xfst.hfst 
	hfst-compose -1 esu.lexc.only.hfst -2 esu.lexc.permissive.xfst.hfst -o esu.lexc.permissive.hfst


# This is the generator that still has morpheme boundaries
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   cali>nrit>>>uq
esu.gen.seg.hfst: esu.lexc.hfst esu.twol.hfst esu.stress.hfst esu.twol.xfst.hfst 
	hfst-compose-intersect -1 esu.lexc.hfst -2 esu.twol.hfst | hfst-compose-intersect -1 - -2 esu.stress.hfst | hfst-compose -1 - -2 esu.twol.xfst.hfst | hfst-minimise -o esu.gen.seg.hfst
esu.gen.seg.permissive.hfst: esu.lexc.permissive.hfst esu.twol.hfst esu.stress.hfst esu.twol.permissive.xfst.hfst 
	hfst-compose-intersect -1 esu.lexc.permissive.hfst -2 esu.twol.hfst | hfst-compose-intersect -1 - -2 esu.stress.hfst | hfst-compose -1 - -2 esu.twol.permissive.xfst.hfst | hfst-minimise -o esu.gen.seg.permissive.hfst


# This is the generator that does not have morpheme boundaries
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   calinrituq
esu.gen.permissive.hfst: esu.gen.seg.permissive.hfst esu.ana.twol.hfst
	hfst-compose-intersect -1 esu.gen.seg.permissive.hfst -2 esu.ana.twol.hfst | hfst-minimise -o esu.gen.permissive.hfst

# This is the analyser that does not have morpheme boundaries
#   calinrituq
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
esu.ana.hfst: esu.gen.permissive.hfst
	hfst-invert esu.gen.permissive.hfst -o esu.ana.hfst

# This is the generator that keeps morpheme boundaries
#	cali-–nrite[V→V][V][Intr][Ind][S_3Sg]
#   cali>nrit>uq
esu.seg.gen.hfst: esu.gen.seg.hfst esu.seg.twol.hfst
	hfst-compose-intersect -1 esu.gen.seg.hfst -2 esu.seg.twol.hfst | hfst-minimise -o esu.seg.gen.hfst


# This is a segmenter which takes surface forms and produces segmented forms
#   calinrituq
#  (cali-–nrite[V→V][V][Intr][Ind][S_3Sg])
#  (cali>nrit>>>uq)
#   cali>nrit>uq
# esu.seg.ana.hfst: esu.ana.hfst esu.gen.seg.hfst esu.seg.twol.hfst
# 	hfst-compose -F -1 esu.ana.hfst -2 esu.gen.seg.hfst -o tmp.hfst
# 	hfst-compose-intersect -1 tmp.hfst -2 esu.seg.twol.hfst | hfst-minimise -o esu.seg.ana.hfst
# 	@rm tmp.hfst
#	hfst-compose -F -1 esu.ana.hfst -2 esu.gen.seg.hfst | hfst-compose-intersect -1 - -2 esu.seg.twol.hfst | hfst-minimise -o esu.seg.hfst

# These are the optimized-lookup generator, analyzer, and segmenter FSTs
# esu.gen.hfstol: esu.gen.hfst
# 	hfst-fst2fst -w esu.gen.hfst -o esu.gen.hfstol
esu.ana.hfstol: esu.ana.hfst
	hfst-fst2fst -w esu.ana.hfst -o esu.ana.hfstol
esu.seg.gen.hfstol: esu.seg.gen.hfst
	hfst-fst2fst -w esu.seg.gen.hfst -o esu.seg.gen.hfstol
# esu.seg.ana.hfstol: esu.seg.ana.hfst
# 	hfst-fst2fst -w esu.seg.ana.hfst -o esu.seg.ana.hfstol

test: test-python

test-python: esu.gen.hfstol esu.ana.hfstol test/esu.pairs.gold/*
	python3 script/runTest.py -g esu.gen.hfstol -a esu.ana.hfstol test/esu.pairs.gold/*

clean:
	rm *.hfst *.hfstol
