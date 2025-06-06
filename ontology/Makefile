#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

uco_srcdir := $(top_srcdir)/dependencies/CDO-Shapes-Time/dependencies/UCO

test_pys := $(wildcard test_*.py)

ttl_basenames := $(wildcard uco-*.ttl)

all: \
  catalog-v001.xml

.pytest.done.log: \
  $(test_pys) \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/dependencies/CDO-Shapes-Time/dependencies/time.ttl \
  $(ttl_basenames)
	source $(top_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG
	touch $@

catalog-v001.xml: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/etc/domain_directories.tsv \
  $(top_srcdir)/etc/dependency_files.tsv \
  $(ttl_basenames) \
  $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
  $(uco_srcdir)/src/create-catalog-v001.xml.py
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    --catalog-xml $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    $(ttl_basenames)
	mv _$@ $@

check: \
  .pytest.done.log \
  catalog-v001.xml

clean:
	@rm -rf \
	  __pycache__
	@rm -f \
	  .*.done.log \
	  _* \
	  catalog-v001.xml
