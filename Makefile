# By default produce:
#	esu.mor.hfst: Morphological analyser
#	esu.gen.hfst: Morphological generator
#	esu.seg.hfst: Morphological segmenter

all: esu.mor.hfst esu.gen.hfst esu.seg.hfst \
	esu.mor.hfstol esu.seg.hfstol

# This is the lexicon 
#	evcug[V][Intr][Ind][2Pl]=llu[Encl]:evcug+'(g/t)uci=llu
esu.lexc.hfst: esu.lexc esu.lexc.xfst.hfst 
	hfst-lexc --Werror esu.lexc | hfst-compose -1 - -2 esu.lexc.xfst.hfst -o esu.lexc.hfst
#	hfst-lexc --Werror esu.lexc  -o esu.lexc.hfst

# This is the phonology file, which maintains morpheme boundaries
esu.twol.hfst: esu.twol
	hfst-twolc -i esu.twol -o esu.twol.hfst

# This is the phonology file, which removes morpheme boundaries
esu.mor.twol.hfst: esu.mor.twol
	hfst-twolc -i esu.mor.twol -o esu.mor.twol.hfst

# This is the phonology file, which collapses morpheme boundaries
esu.seg.twol.hfst: esu.seg.twol
	hfst-twolc -i esu.seg.twol -o esu.seg.twol.hfst

esu.lexc.xfst.hfst: esu.lexc.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

esu.twol.xfst.hfst: esu.twol.xfst
	hfst-xfst -p -e "source $<" -e "save stack $@" -E "hyvästi" #"exit"

# This is the generator that still has morpheme boundaries
#	<past><s_sg3><f>deyë꞉s<v><tv>:>wö>ʼön>deyë꞉s
esu.gen.seg.hfst: esu.lexc.hfst esu.twol.hfst esu.twol.xfst.hfst 
	hfst-compose-intersect -1 esu.lexc.hfst -2 esu.twol.hfst | hfst-compose -1 - -2 esu.twol.xfst.hfst | hfst-minimise -o esu.gen.seg.hfst

# This is the generator that does not have morpheme boundaries
#	<past><s_sg3><f>deyë꞉s<v><tv>:wöʼöndeyë꞉s
esu.gen.hfst: esu.gen.seg.hfst esu.mor.twol.hfst
	hfst-compose-intersect -1 esu.gen.seg.hfst -2 esu.mor.twol.hfst | hfst-minimise -o esu.gen.hfst

# This is the analyser that does not have morpheme boundaries
#	wöʼöndeyë꞉s:<past><s_sg3><f>deyë꞉s<v><tv>
esu.mor.hfst: esu.gen.hfst
	hfst-invert esu.gen.hfst -o esu.mor.hfst

# This is a segmenter which takes surface forms and produces segmented forms
#	wöʼöndeyë꞉s:>wö>ʼön>deyë꞉s
esu.seg.hfst: esu.mor.hfst esu.gen.seg.hfst esu.seg.twol.hfst
#	hfst-compose -F -1 esu.mor.hfst -2 esu.gen.seg.hfst | hfst-compose-intersect -1 - -2 esu.seg.twol.hfst | hfst-minimise -o esu.seg.hfst
	hfst-compose -F -1 esu.mor.hfst -2 esu.gen.seg.hfst -o tmp.hfst
	hfst-compose-intersect -1 tmp.hfst -2 esu.seg.twol.hfst -o esu.seg.hfst
	@rm tmp.hfst

esu.mor.hfstol: esu.mor.hfst
	hfst-fst2fst -w esu.mor.hfst -o esu.mor.hfstol

esu.seg.hfstol: esu.seg.hfst
	hfst-fst2fst -w esu.seg.hfst -o esu.seg.hfstol

clean:
	rm *.hfst *.hfstol


