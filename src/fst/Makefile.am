## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# always build . last here, and tagsets have to be built after morphology
SUBDIRS = morphology filters phonetics syllabification orthography transcriptions tagsets . test

####### Automake targets: ########

# Define target variables first, before assigning to them:
GT_ANALYSERS=
GT_GENERATORS=
CUSTOM_FSTS=

#### Local modifications in *fst processing: ####
####
#### Copy the fallback targets, and rename them to the desired targets. Then:
#### Replace the 'cp' command (Xerox) / Prepend the hfst-invert command (Hfst -
#### remember to move the $<) with whatever you need to complete
#### the processing to get the final target transducer.
#### Remember to add the dependencies as well.
#### Also make sure that HFST and Xerox processing are the same.
####
#### If you add new transducers to be built, you need to add them to the
#### relevant variable, e.g.:
####
#### if CAN_HFST
#### GT_GENERATORS+=generator-oahpa-gt-norm.hfst
#### endif
####
#### NB!!!! The HFST targets should get a hyphen after 'analyser'/'generator'
#### respectively, to make the local targets minimally different from and
#### slightly more specific than the fallback targets. This is to avoid warnings
#### about duplicate targets. That is, the local targets should looke like:
####
#### analyser-%.hfst: analyser-%.tmp.hfst
#### generator-%.hfst: generator-%.tmp.hfst

##################################################################
#### BEGIN: Add local processing instructions BELOW this line ####
##################################################################

########################################################
#### Add language-specific transducer targets here: ####

#### HFST transducers
if CAN_HFST
GT_ANALYSERS+=
GT_GENERATORS+=

if WANT_CUSTOM_FSTS
CUSTOM_FSTS+=
endif # WANT_CUSTOM_FSTS

endif # CAN_HFST

#### FOMA transducers
if CAN_FOMA
GT_ANALYSERS+=
GT_GENERATORS+=

if WANT_CUSTOM_FSTS
CUSTOM_FSTS+=
endif # WANT_CUSTOM_FSTS

endif # CAN_FOMA

#################################################
#### Add language-specific build rules here: ####

### ESU adds regular output and only the permissive-only paths as Err/Orth.
.generated/generator-raw-gt-desc.tmp.hfst: \
			.generated/generator-raw-gt-desc.tmp1.hfst \
			morphology/extra-phonology.compose.hfst \
			morphology/extra-phonology.permissive.compose.hfst \
			morphology/analysis-error-tag.hfst \
			filters/reorder-semantic-tags.hfst \
			filters/reorder-subpos-tags.hfst
	$(HFST_COMPOSE) -1 $< -2 morphology/extra-phonology.compose.hfst \
		-o .generated/esu-regular.hfst
	$(HFST_COMPOSE) -1 $< -2 morphology/extra-phonology.permissive.compose.hfst \
		-o .generated/esu-permissive.hfst
	$(HFST_SUBTRACT) -1 .generated/esu-permissive.hfst \
		-2 .generated/esu-regular.hfst -o .generated/esu-permissive-only.hfst
	$(HFST_CONCATENATE) -1 .generated/esu-permissive-only.hfst \
		-2 morphology/analysis-error-tag.hfst \
		-o .generated/esu-permissive-tagged.hfst
	$(HFST_DISJUNCT) -1 .generated/esu-regular.hfst \
		-2 .generated/esu-permissive-tagged.hfst \
		-o .generated/esu-raw-unioned.hfst
	$(HFST_COMPOSE) -F -1 .generated/esu-raw-unioned.hfst \
		-2 filters/reorder-semantic-tags.hfst \
		-o .generated/esu-semantic-reordered.hfst
	$(HFST_COMPOSE) -F -1 .generated/esu-semantic-reordered.hfst \
		-2 filters/reorder-subpos-tags.hfst -o $@
	rm -f .generated/esu-regular.hfst .generated/esu-permissive.hfst \
		.generated/esu-permissive-only.hfst .generated/esu-permissive-tagged.hfst \
		.generated/esu-raw-unioned.hfst .generated/esu-semantic-reordered.hfst

#### Xerox & FOMA: keep the regular mapping, without adding stress.
.generated/analyser-raw-gt-desc.%: .generated/analyser-raw-gt-desc.tmp.% \
			morphology/extra-phonology.compose.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
				@\"$<\" \
			.o. @\"morphology/extra-phonology.compose.$*\" \
			;\n\
		 save stack $@\n\
		 quit\n" | $(XFST_TOOL)

# Remove & change boundaries in the analysers:
define giella_default_analysers
.generated/analyser%.$(1): .generated/analyser%.tmp.$(1) \
			morphology/remove-boundarie.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"morphology/remove-boundarie.compose.$(1)\"  \
			.o. @\"$$<\" \
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)
endef
$(foreach fst,hfst xfst foma,$(eval $(call giella_default_analysers,$(fst))))

# Remove & change boundaries in the generators:
define giella_default_generators
.generated/generator-%.$(1): .generated/generator-%.tmp.$(1) \
			morphology/remove-boundarie.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"morphology/remove-boundarie.compose.$(1)\"  \
			.o. @\"$$<\" \
		 $$(INVERT_XFST)$$(INVERT_FOMA)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)
endef
$(foreach fst,hfst xfst foma,$(eval $(call giella_default_generators,$(fst))))

# Collaps boundaries in the morpher:
.generated/morpher-gt-desc.%: .generated/morpher-gt-desc.tmp.% \
			morphology/collapse-boundaries.compose.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
				@\"morphology/collapse-boundaries.compose.$*\".i  \
			.o. @\"$<\" \
			;\n\
		 $(INVERT_HFST)\
		 save stack $@\n\
		 quit\n" | $(XFST_TOOL)

##################################################################
#### END: Add local processing instructions ABOVE this line ######
##################################################################

include $(top_srcdir)/../giella-core/am-shared/src-fst-dir-include.am
include $(top_srcdir)/../giella-core/am-shared/devtest-include.am
