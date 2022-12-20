import time
from rest_framework.response import Response
from rest_framework.decorators import api_view
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import sys
import logging

@api_view(["GET"])
def get(request):
    logger = setup_custom_logger('create_journal')
    load_dotenv()
    uri=str(os.getenv("uri"))
    user=str(os.getenv("user"))
    pwd=str(os.getenv("pwd"))
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    session=driver.session()
    q1="""
    Match(n) return count(n) as count
    """
    results=session.run(q1)
    li=[r["count"] for r in results]
    result={"count":li}
    return Response(result)

@api_view(["POST"])
def create_journal(request):
    from typing import Dict
    import json
    logger = setup_custom_logger('create_journal')
    load_dotenv()
    uri=str(os.getenv("uri"))
    user=str(os.getenv("user"))
    pwd=str(os.getenv("pwd"))
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    session=driver.session()
    data=request.data #.decode('utf-8')
    # data= json.load(codecs.decode(request.data,'utf-8-sig'))
    keys=list(data.keys())
    simple_keys=[]
    for key in keys:
        if isinstance(data[key],Dict) or isinstance(data[key],str):
            simple_keys.append(key)

    for simple_key in simple_keys:     
            if simple_key == "JournalReference":
                rJournalReference=data[simple_key]
                referenceDOI=rJournalReference['doi']
                referenceTitle=rJournalReference['title']
                referenceDOIURL=rJournalReference['doiURL']
                authorScopusID=rJournalReference['authorScopusID']
            elif simple_key=="Affiliation":
                rAffiliation=data[simple_key]
            elif simple_key=="Year":
                rYear=data[simple_key]
            elif simple_key=="Conceptual":
                rConceptual=data[simple_key]
            elif simple_key=="JournalPublication":
                rJournalPublication=data[simple_key]
            elif simple_key=="Publisher":
                rPublisher=data[simple_key]
                vPublisherName=rPublisher['name']
            elif simple_key=="Empirical":
                rEmpirical=data[simple_key]
            elif simple_key=="Keyword":
                rKeyword=data[simple_key]
                if rKeyword=="":
                    rKeyword={}
            elif simple_key=="Funding":
                rFunding=data[simple_key]
            elif simple_key=="Data":
                rData=data[simple_key]
            elif simple_key=="Method":
                rMethod=data[simple_key]
            else:
                print(simple_key)
                print("invalid data")
                sys.exit()

    qall="""
    merge (a:JournalReference {doi:$rJournalReference.doi}) 
    on create 
    set a=$rJournalReference
    merge(b:Year {name:$rYear.name}) 
    on create 
    set b=$rYear
    create(d:JournalPublication) set d=$rJournalPublication
    create(e:Publisher) set e=$rPublisher
    create(h:Funding) set e=$rFunding
    create(i:Data) set i=$rData
    create(j:Method) set j=$rMethod
    create(a)-[:USED]->(i)
    create(a)-[:IN]->(b)
    create(a)-[:APPEARED_IN]->(d)
    create(d)-[:PUBLISHED_BY]->(e)
    create(a)-[r1:USED]->(j)
    set r1.referenceTitle=$referenceTitle, r1.referenceDOIURL=$referenceDOIURL
    create(d)-[:USED]->(j)
    create(d)-[r2:USED]->(i)
    set r2.referenceTitle=$referenceTitle, r2.referenceDOIURL=$referenceDOIURL
    create(a)<-[:FUNDED]-(h)
    """
    Dict_all={"rJournalReference":rJournalReference,"rYear":rYear,"rJournalPublication":rJournalPublication,
    "rPublisher":rPublisher,"rFunding":rFunding,"rData":rData,"rMethod":rMethod,
    "referenceTitle":referenceTitle,
    "referenceDOIURL":referenceDOIURL}

    complex_keys=[]
    for key in keys:
        if isinstance(data[key],list) and len(data[key])!=0:
            complex_keys.append(key)
    qauthor=""
    authors=[]
    qbib=""
    bibliographicReferences=[]
    qhyp=""
    hypothesiss=[]
    qprop=""
    propositions=[]
    qafiliation=""
    affiliations=[]
    qkey=""
    keywords=[]
    qcons=""
    constructs=[]

    for complex_key in complex_keys:
            if complex_key=="Author":
                authors=data[complex_key]
                qauthor="""
                UNWIND $authors as row
                create(a:Author) set a+=row;
                """
            elif complex_key=="BibliographicReference":
                bibliographicReferences=data[complex_key]           
                qbib="""
                UNWIND $bibliographicReferences AS row
                CREATE (b:BibliographicReference)
                SET b += row ;
                """
            elif complex_key=="Hypothesis":
                hypothesiss=data[complex_key]
                qhyp="""
                UNWIND $hypothesiss AS row
                create(h:Hypothesis) set h +=row;
                """

            elif complex_key=="Proposition":
                propositions=data[complex_key]
                qprop="""
                UNWIND $propositions AS row
                create(p:Proposition) set p+=row;
                """
            elif complex_key=="Affiliation":
                Affiliations=data[complex_key]
                qafiliation="""
                unwind $affiliations as row
                create(af:Affiliation) set af+=row;
                """
            elif complex_key=="Keyword":
                keywords=data[complex_key]
                qkey="""
                unwind $keywords as row
                create(k:Keyword) set k+=row;
                """
            elif complex_key=="Construct":
                constructs=data[complex_key]
                qcons="""
                unwind $constructs as row
                create(c:Construct) set c+=row;
                """
            else:
                print(complex_key)
                print("invalid data")
                sys.exit()
    dict_complex={"authors":authors,
    "bibliographicReferences":bibliographicReferences,
    "hypothesiss":hypothesiss,
    "propositions":propositions,
    "affiliations":affiliations,
    "keywords":keywords,
    "constructs":constructs}
    query_all="""CALL apoc.cypher.runMany('""" + qauthor+ qbib + qhyp + qprop + qafiliation + qkey + qcons +"""',{authors:$authors,bibliographicReferences:$bibliographicReferences,hypothesiss:$hypothesiss,propositions:$propositions,affiliations:$affiliations,keywords:$keywords,constructs:$constructs},{statistics: false});"""


    Dict={"referenceDOI":referenceDOI,
    "authorScopusID":authorScopusID,
    "vPublisherName":vPublisherName,
    "referenceTitle":referenceTitle,
    "referenceDOIURL":referenceDOIURL}    


    q="""MERGE (iv:`Construct Role`:`Independent Variable`)
    MERGE (dv:`Construct Role`:`Dependent Variable`)
    MERGE (mv1:`Construct Role`:`Moderator Variable`)
    MERGE (mv2:`Construct Role`:`Mediator Variable`)"""

    session.run (q,Dict)

    q="""CALL apoc.cypher.runMany('match(j:JournalReference)-[:USED]->(d:Data),
    (j)-[:APPEARED_IN]->(jp:JournalPublication),(jp)-[:PUBLISHED_BY]->(p:Publisher),
    (j)<-[:FUNDED]-(f:Funding),(a:Author),(b:BibliographicReference),(j)-[:USED]->(m:Method)
    where b.citingDOI = j.doi and (a.scopusID in j.authorScopusID ) and j.doi=$referenceDOI 
    merge (j)-[:AUTHORED_BY]->(a)
    merge (j)-[:CITED]->(b)
    MERGE (a)-[:CONTRIBUTED_TO]->(jp)
    MERGE (a)-[:CONTRIBUTED_TO]->(p)
    MERGE (a)-[:FUNDED_BY]->(f)
    MERGE (d)<-[:USED]-(a)
    MERGE (m)<-[:USED]-(a);
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where  j.doi=$referenceDOI 
    match  (af:Affiliation), (c:Construct)
    where  a.scopusID in af.authorScopusID and j.doi=c.doi 
    merge (j)-[:STUDIED]->(c)
    MERGE (jp)-[:STUDIED]->(c)
    merge (af)-[:PRODUCED]->(j);
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    match (h:Hypothesis)
    where j.doi=h.doi 
    merge (j)-[:STUDIED]->(h)
    MERGE (jp)-[:STUDIED]->(h)
    MERGE (a)-[r:STUDIED]->(h)
    set r.referenceTitle=$referenceTitle, r.referenceDOIURL=$referenceDOIURL;
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    match (pr:Proposition)
    where j.doi=pr.doi 
    merge (jp)-[:STUDIED]->(pr)
    merge (a)-[r:STUDIED]->(pr)
    set r.referenceTitle=$referenceTitle, r.referenceDOIURL=$referenceDOIURL
    merge (j)-[:STUDIED]->(pr);
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    match (k:Keyword)
    where  k.doi=j.doi 
    merge (j)-[:HAS]->(k)
    MERGE (jp)-[:HAS]->(k)
    MERGE (a)-[r1:HAS]->(k)
    set r1.referenceTitle=$referenceTitle, r1.referenceDOIURL=$referenceDOIURL
    MERGE (p)-[:HAS]->(k)
    MERGE (a)-[r2:USED]->(k:Keyword)
    set r2.referenceTitle=$referenceTitle, r2.referenceDOIURL=$referenceDOIURL;
    MATCH (c:Construct)<-[:STUDIED]-(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    MERGE (a)-[r:STUDIED]->(c)
    set r.referenceTitle=$referenceTitle, r.referenceDOIURL=$referenceDOIURL;
    MATCH (c:Construct)<-[:STUDIED]-(j:JournalReference), (j:JournalReference)-[:STUDIED]->(h:Hypothesis)
    where j.doi=$referenceDOI and c.hypothesisID=h.hypothesisID
    MERGE (h)-[r:STUDIED]->(c)
    set r.referenceTitle=$referenceTitle, r.referenceDOIURL=$referenceDOIURL;
    MATCH (c:Construct)<-[:STUDIED]-(j:JournalReference), (j:JournalReference)-[:STUDIED]->(p:Proposition)
    where j.doi=$referenceDOI and c.propositionID=p.propositionID
    MERGE (p)-[r:STUDIED]->(c)
    set r.referenceTitle=$referenceTitle, r.referenceDOIURL=$referenceDOIURL;
    MATCH (c:Construct), (iv:`Construct Role`:`Independent Variable`)
    WHERE c.ConstructRole = "IndependentVariable" and c.doi=$referenceDOI
    MERGE (c)-[:AS]->(iv);
    MATCH (c:Construct), (dv:`Construct Role`:`Dependent Variable`)
    WHERE c.ConstructRole = "DependentVariable" and c.doi=$referenceDOI
    MERGE (c)-[:AS]->(dv);
    MATCH (c:Construct), (mv:`Construct Role`:`Mediator Variable`)
    WHERE c.ConstructRole = "MediatorVariable" and c.doi=$referenceDOI
    MERGE (c)-[:AS]->(mv);
    MATCH (c:Construct), (mv:`Construct Role`:`Moderator Variable`)
    WHERE c.ConstructRole = "ModeratorVariable" and c.doi=$referenceDOI
    MERGE (c)-[:AS]->(mv);', {referenceDOI:$referenceDOI, referenceTitle:$referenceTitle,
    referenceDOIURL:$referenceDOIURL},{statistics: false});"""
    startTime = time.perf_counter()
    try:       
        session.run(qall,Dict_all)
        session.run(query_all,dict_complex)
        session.run (q,Dict)
    except Exception as e:
        print(str(e))
    request_time = time.perf_counter() - startTime
    logger.info("Request completed in {0:.0f}ms".format(request_time))
    return Response({"status":"ok"})

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger