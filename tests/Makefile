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

profile_ttls := $(wildcard $(top_srcdir)/ontology/uco-*.ttl)

shape_ttls := \
  $(wildcard $(top_srcdir)/dependencies/CDO-Shapes-Time/shapes/sh-*.ttl) \
  $(wildcard $(top_srcdir)/shapes/sh-*.ttl)

all: \
  monolithic.ttl

.pyshacl.done.log: \
  exemplars-expanded.ttl \
  monolithic.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --metashacl \
	    --ont-graph monolithic.ttl \
	    --shacl monolithic.ttl \
	    exemplars-expanded.ttl
	touch $@

.pytest.done.log: \
  $(test_pys) \
  exemplars.ttl \
  monolithic.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG
	touch $@

check: \
  .pytest.done.log \
  .pyshacl.done.log

clean:
	@rm -rf \
	  __pycache__
	@rm -f \
	  .*.done.log \
	  exemplars-entailment.ttl \
	  exemplars-expanded.ttl \
	  monolithic.ttl

exemplars-entailment.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/src/entail.py \
  exemplars.ttl \
  monolithic.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/entail.py \
	    _$@ \
	    exemplars.ttl \
	    monolithic.ttl
	mv _$@ $@

exemplars-expanded.ttl: \
  exemplars-entailment.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    exemplars.ttl \
	    $< \
	    > _$@
	mv _$@ $@

monolithic.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/dependencies/imports-transitive.ttl \
  $(profile_ttls) \
  $(shape_ttls)
	$(MAKE) \
	  --directory $(uco_srcdir) \
	  .venv.done.log
	$(MAKE) \
	  --directory $(uco_srcdir)/tests \
	  uco_monolithic.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(top_srcdir)/dependencies/imports-transitive.ttl \
	    $(profile_ttls) \
	    $(shape_ttls) \
	    $(uco_srcdir)/dependencies/collections-ontology/collections.owl \
	    $(uco_srcdir)/dependencies/error/docs/current/error.ttl \
	    $(uco_srcdir)/tests/uco_monolithic.ttl \
	    > _$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --shacl $(uco_srcdir)/ontology/owl/owl.ttl \
	    _$@
	mv _$@ $@
