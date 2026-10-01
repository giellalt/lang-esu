## Process this file with automake to produce Makefile.in

## Copyright (C) 2011 Samediggi

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
############## BEGIN: Local modifications ###############

# List any local filter regex files here:
GIELLA_FILTER_LOCAL_REGEX_SRCS=\
					downcase_UCletters.regex\
					remove-derivation-position-tags.regex \
					remove-DNorm-tags.regex \
					remove-norm-comp-tags.regex \
					rename-POS_before_Der-tags.regex

# List any local filter xfscript files here:
GIELLA_FILTER_LOCAL_XFSCRIPT_SRCS=

# List any local filter lexc files here:
GIELLA_FILTER_LOCAL_LEXC_SRCS=

# List any locally generated regex source files here:
GIELLA_FILTER_LOCAL_GENERATED_REGEX_SRCS=

# List any locally generated xfscript source files here:
GIELLA_FILTER_LOCAL_GENERATED_XFSCRIPT_SRCS=

# List any locally generated lexc source files here:
GIELLA_FILTER_LOCAL_GENERATED_LEXC_SRCS=

# List any additional source files here, so that they are included in the dist.
# Source files that are not directly compiled to fst's but are instead used as
# part of a local build step should be listed here.
EXTRA_SRCS=

########## Add local build rules below here: ############

############### END: Local modifications ################
#########################################################

# Included build file, where the actual build instructions are:
include $(top_srcdir)/../giella-core/am-shared/src-filters-dir-include.am

# Err/Orth is added after the lexical transducer is compiled, so extract the
# existing core error-tag list from the raw generator FST instead of the lexicon.
.generated/error-tags.txt: $(top_builddir)/src/fst/.generated/generator-raw-gt-desc.hfst
	$(AM_V_GEN)$(HFST_SUMMARIZE) -v 2>/dev/null $< \
		| grep -A1 '^sigma set' \
		| grep -v '^sigma set' \
		| sed 's/, /\\\\\\/g' \
		| perl -pe 's/\\\\\\/\n/g' \
		| grep -v '^$$' \
		| egrep -v '(@_EPSILON_SYMBOL_@|@_IDENTITY_SYMBOL_@|@_UNKNOWN_SYMBOL_@)' \
		> $@.sigma.tmp
	$(AM_V_GEN)$(GTCORE)/scripts/extract-tags.sh $@.sigma.tmp $@.tmp Err/
	$(AM_V_GEN)if test -f $@; then \
		if ! diff -q $@ $@.tmp; then mv -f $@.tmp $@; else rm -f $@.tmp; fi; \
	else mv -f $@.tmp $@; fi
	rm -f $@.sigma.tmp

# vim: set ft=automake:
include $(top_srcdir)/../giella-core/am-shared/devtest-include.am
