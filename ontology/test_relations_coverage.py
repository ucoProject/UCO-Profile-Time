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

from rdflib import OWL, RDF, TIME, Graph, Namespace, URIRef
from rdflib.query import ResultRow

srcdir = Path(__file__).parent
top_srcdir = Path(__file__).parent.parent

NS_DRAFTING = Namespace("http://example.org/ontology/drafting/")
NS_OWL = OWL
NS_RDF = RDF
NS_TIME = TIME

# This namespace is a customized object to add concepts from the current
# Editor's Draft.
NS_TIME_ED = Namespace(str(TIME))


def test_relations_coverage() -> None:
    """
    This test lists the properties that link ``time:TemporalEntity``s to one another within OWL-Time, and checks the relative coverage of drafting-namespaced analagous properties.
    """
    # The expected-set is empty.
    # The computed set is all OWL-Time properties that do not have an analagous drafting-namespace property defined.
    expected: set[URIRef] = set()
    excused: set[URIRef] = {
        NS_TIME_ED["disjoint"],
        NS_TIME_ED["equals"],
        NS_TIME_ED["hasInside"],
        NS_TIME_ED["notDisjoint"],
    }
    computed: set[URIRef] = set()

    owl_time_graph = Graph()
    profile_graph = Graph()

    owl_time_graph.parse(
        top_srcdir / "dependencies" / "CDO-Shapes-Time" / "dependencies" / "time.ttl"
    )
    profile_graph.parse(srcdir / "uco-time.ttl")
    logging.debug("len(owl_time_graph) = %d.", len(owl_time_graph))
    logging.debug("len(profile_graph) = %d.", len(profile_graph))

    time_prefix_iri = str(NS_TIME)

    query = """\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
SELECT ?nProperty
WHERE {
  ?nTopProperty
    rdfs:domain ?nTemporalEntityClass1 ;
    rdfs:range ?nTemporalEntityClass2 ;
    .
  ?nProperty
    rdfs:subPropertyOf* ?nTopProperty ;
    .
  ?nTemporalEntityClass1
    rdfs:subClassOf* time:TemporalEntity ;
    .
  ?nTemporalEntityClass2
    rdfs:subClassOf* time:TemporalEntity ;
    .
  FILTER (isIRI(?nProperty))
}
"""
    for result in owl_time_graph.query(query):
        assert isinstance(result, ResultRow)
        assert isinstance(result[0], URIRef)
        n_time_property = result[0]
        time_property_iri = str(n_time_property)
        assert time_property_iri.startswith(time_prefix_iri)
        time_property_local_part = time_property_iri[len(time_prefix_iri) :]
        n_drafting_property = NS_DRAFTING[time_property_local_part]
        if (
            n_drafting_property,
            NS_RDF.type,
            NS_OWL.ObjectProperty,
        ) not in profile_graph:
            computed.add(n_time_property)

    assert expected == computed - excused
