#!/usr/bin/env python3

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

import logging
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.query import ResultRow

NS_DRAFTING = Namespace("http://example.org/ontology/drafting/")
NS_UCO_TIME_PROFILE = Namespace("http://example.org/ontology/uco-time/")


srcdir = Path(__file__).parent


def test_subproperty_sh_target_review() -> None:
    """
    This test confirms that subproperties are reviewed by the same shapes as their parent properties are, when those shapes use ``sh:targetSubjectsOf`` or ``sh:targetObjectsOf``.

    Note that this test leaves ``sh:path`` out of scope.
    """

    # The expected-set is empty.
    # The computed set is all node shapes that target a parent property
    # of some child property, but don't also target the child property.
    expected: set[tuple[URIRef, URIRef, URIRef, URIRef]] = set()
    computed: set[tuple[URIRef, URIRef, URIRef, URIRef]] = set()

    graph = Graph()
    filepath = srcdir / "monolithic.ttl"
    graph.parse(filepath)
    logging.debug("len(graph) = %d.", len(graph))

    prefixes_in_scope = (
        str(NS_DRAFTING),
        str(NS_UCO_TIME_PROFILE),
    )

    query = """\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?nTargetingShape ?nTargetPredicate ?nParentProperty ?nChildProperty
WHERE {
  ?nChildProperty
    rdfs:subPropertyOf+ ?nParentProperty ;
    .
  {
    ?nTargetingShape
      sh:targetSubjectsOf ?nParentProperty ;
      .
    BIND(sh:targetSubjectsOf AS ?nTargetPredicate)
  } UNION {
    ?nTargetingShape
      sh:targetObjectsOf ?nParentProperty ;
      .
    BIND(sh:targetObjectsOf AS ?nTargetPredicate)
  }
  FILTER NOT EXISTS {
    ?nTargetingShape
      ?nTargetPredicate ?nChildProperty ;
      .
  }
}
"""
    for result in graph.query(query):
        assert isinstance(result, ResultRow)
        assert isinstance(result[0], URIRef)
        assert isinstance(result[1], URIRef)
        assert isinstance(result[2], URIRef)
        assert isinstance(result[3], URIRef)

        if not str(result[2]).startswith(prefixes_in_scope) and not str(
            result[3]
        ).startswith(prefixes_in_scope):
            continue
        computed.add((result[0], result[1], result[2], result[3]))

    try:
        assert expected == computed
    except AssertionError:
        lines_to_copy_paste = "\n".join(
            sorted(
                ("<%s> <%s> <%s> ." % (x[0], x[1], x[3]) for x in (computed - expected))
            )
        )
        logging.info(
            "This can be addressed by copying the following lines into the shapes graph.  Automated format-checking should handle syntactically normalizing them.\n%s"
            % lines_to_copy_paste
        )
        raise
