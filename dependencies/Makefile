#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

uco_srcdir := $(top_srcdir)/dependencies/CDO-Shapes-Time/dependencies/UCO

all: \
  catalog-v001.xml

catalog-v001.xml: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/etc/domain_directories.tsv \
  $(top_srcdir)/etc/dependency_files.tsv \
  $(uco_srcdir)/src/create-catalog-v001.xml.py \
  imports-transitive.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    imports-transitive.ttl
	mv _$@ $@

check: \
  catalog-v001.xml

clean:
	@rm -f \
	  catalog-v001.xml \
	  imports-transitive.ttl

# This recipe intentionally does not incorporate CDO ontologies (UCO,
# CASE, etc.), to avoid redundant imports between multiple profiles.
imports-transitive.ttl: \
  $(top_srcdir)/dependencies/CDO-Shapes-Time/dependencies/imports-transitive.ttl
	cp $< _$@
	mv _$@ $@
