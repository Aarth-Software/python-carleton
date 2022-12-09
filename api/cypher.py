
MATCH (a:Author)

MATCH (f:`Funding Agency`)

MATCH (jp:Reference:`Journal Paper`)

MATCH (j:Publication:Journal)

MATCH (p:Publisher)

MATCH (k:Asset:Keyword)

MATCH (c:Construct)

MERGE (a)-[:FUNDED_BY]->(f)

MERGE (a)-[:CONTRIBUTED_TO]->(p)

MERGE (a)-[:CONTRIBUTED_TO]->(j)

MERGE (a)<-[:AUTHORED_BY]-(jp)

MERGE (a)-[:HAS]->(k)

MERGE (a)-[:STUDIED]->(c)





MATCH (k:Asset:Keyword)

MATCH (m:Asset:Method)

MATCH (h:Asset:Hypothesis)

MATCH (p:Asset:Preposition)

MATCH (d:Asset:Data)

MATCH (j:Publication:Journal)

MATCH (iv:`Construct Role`:`Independent Variable`)

MATCH (dv:`Construct Role`:`Dependent Variable`)

MATCH (mv1:`Construct Role`:`Mediator Variable`)

MATCH (mv2:`Construct Role`:`Moderator Variable`)

MERGE (j)

-[:HAS]->(k)

MERGE (j)-[:USED]->(m)

MERGE (j)-[:HAS]->(iv)

MERGE (j)<-[:STUDIED]-(h)

MERGE (j)-[:HAS]->(dv)

MERGE (j)-[:HAS]->(mv1)

MERGE (j)-[:HAS]->(mv2)

MERGE (j)-[:STUDIED]->(p)

MERGE (j)-[:USED]->(d)





MATCH (c1:Construct {name: 'outsourced task entails more radical innovation'})

MATCH (c2: Construct {name: 'outsourced task with incremental innovation'})

MATCH (c3: Construct {name: 'contract that includes (a) a hybrid payment structure (T&M with a cap), (b) a more detailed description of the requirements, and (c) less emphasis on contingency planning.'})

MATCH (c4: Construct {name: 'outsourced task is more radically innovative and involvesexchange hazards'})

MATCH (c5: Construct {name: 'contract that includes (a) a T&M payment structure, (b) a less detailed description of requirements, and (c) more contingency planning compared with an outsourced radically innovative task that faces no or fewer exchange hazards.'})

MATCH (iv:`Construct Role`:`Independent Variable`)

MATCH (dv:`Construct Role`:`Dependent Variable`)

MATCH (mv1:`Construct Role`:`Mediator Variable`)

MATCH (mv2:`Construct Role`:`Moderator Variable`)

MERGE (iv)<-[:AS]-(c1)

MERGE (dv)<-[:AS]-(c2)

MERGE (mv1)<-[:AS]-(c3)

MERGE (mv1)<-[:AS]-(c4)

MERGE (mv2)<-[:AS]-(c4)

MERGE (dv)<-[:AS]-(c5)

MERGE (mv1)<-[:AS]-(c5)

MERGE (mv2)<-[:AS]-(c5)