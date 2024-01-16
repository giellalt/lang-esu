## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

SUBDIRS = fst cg3

#################################################
#### Add language-specific build rules here: ####

### ESU requires extra processing after twolc intersection:
# Hfst:
generator-raw-gt-desc.hfst: generator-raw-gt-desc.tmp.hfst \
			fst/assign-stress.compose.hfst  \
			fst/extra-phonology.compose.hfst
	$(AM_V_INTRSCT)$(HFST_COMPOSE_INTERSECT) $(COMPOSE_INTERSECT_FLAG) \
		  -1 $< -2 fst/assign-stress.compose.hfst \
		| $(HFST_COMPOSE_INTERSECT) $(COMPOSE_INTERSECT_FLAG) \
		  -1 - -2 fst/extra-phonology.compose.hfst \
		| $(HFST_MINIMIZE) $(MORE_VERBOSITY) $(HFST_FLAGS) \
		-o $@

#### Xerox & FOMA:
analyser-raw-gt-desc.%: analyser-raw-gt-desc.tmp.% \
			fst/assign-stress.compose.%  \
			fst/extra-phonology.compose.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
				@\"$<\" \
			.o. @\"fst/assign-stress.compose.$*\"   \
			.o. @\"fst/extra-phonology.compose.$*\" \
			;\n\
		 save stack $@\n\
		 quit\n" | $(XFST_TOOL)

# Remove & change boundaries in the analysers:
define giella_default_analysers
analyser%.$(1): analyser%.tmp.$(1) \
			fst/remove-boundarie.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"fst/remove-boundarie.compose.$(1)\"  \
			.o. @\"$$<\" \
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)
endef
$(foreach fst,hfst xfst foma,$(eval $(call giella_default_analysers,$(fst))))

# Remove & change boundaries in the generators:
define giella_default_generators
generator-%.$(1): generator-%.tmp.$(1) \
			fst/remove-boundarie.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"fst/remove-boundarie.compose.$(1)\"  \
			.o. @\"$$<\" \
		 $$(INVERT_XFST)$$(INVERT_FOMA)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)
endef
$(foreach fst,hfst xfst foma,$(eval $(call giella_default_generators,$(fst))))

# Collaps boundaries in the morpher:
morpher-gt-desc.%: morpher-gt-desc.tmp.% \
			fst/collapse-boundaries.compose.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
				@\"fst/collapse-boundaries.compose.$*\".i  \
			.o. @\"$<\" \
			;\n\
		 $(INVERT_HFST)\
		 save stack $@\n\
		 quit\n" | $(XFST_TOOL)

##################################################################
#### END: Add local processing instructions ABOVE this line ######
##################################################################

include $(top_srcdir)/../giella-core/am-shared/src-dir-include.am
