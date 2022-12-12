from rest_framework.response import Response
from rest_framework.decorators import api_view
from neo4j import GraphDatabase
from typing import Dict
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
    print (uri)
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
    logger = setup_custom_logger('create_journal')
    load_dotenv()
    uri=str(os.getenv("uri"))
    user=str(os.getenv("user"))
    pwd=str(os.getenv("pwd"))
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    session=driver.session()
    data=request.data
    keys=list(data.keys())
    print(keys)
    simple_keys=[]
    for key in keys:
    #print(type(data[key]))
        if isinstance(data[key],Dict) or isinstance(data[key],str):
            simple_keys.append(key)

    for simple_key in simple_keys: 
            print(simple_key)       
            if simple_key == "JournalReference":
                rJournalReference=data[simple_key]
                referenceDOI=rJournalReference['doi']
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

    # qFunding="""merge(h:Funding {name:$rFunding.name}) 
    # on create 
    # set h=$rFunding,h.fundingID=apoc.create.uuid()
    # return h.fundingID"""
    # print (qFunding)
    # Dict_funding={"rFunding":rFunding}
    # fundingResult=session.run(qFunding,Dict_funding)
    # fundingValue  = fundingResult.value(0)
    # rFundinID = fundingValue[0]

    # print (rFundinID)

    # create(a)<-[:FUNDED]-(h)
    # set a.fundingID=h.fundingID
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
    create(a)-[:USED]->(j)
    create(d)-[:USED]->(j)
    create(d)-[:USED]->(i)
    create(a)<-[:FUNDED]-(h)
    """
    Dict_all={"rJournalReference":rJournalReference,"rYear":rYear,"rJournalPublication":rJournalPublication,"rPublisher":rPublisher,"rFunding":rFunding,"rData":rData,"rMethod":rMethod}

    #Dict_all={"rJournalReference":rJournalReference,"rYear":rYear,"rConceptual":rConceptual,"rJournalPublication":rJournalPublication,"rPublisher":rPublisher,"rEmpirical":rEmpirical,"rKeyword":rKeyword,"rFunding":rFunding,"rData":rData,"rMethod":rMethod}
    logger.info('Creation of nodes set 1')
    session.run(qall,Dict_all)
    # (JournalReference if isEmpirical =true)-[:HAS_TYPE]->(Empirical) 
    # (JournalReference if  isConceptual =true )-[:HAS_TYPE]->(Conceptual)
    # keyword match with doi to JournalReference [:HAS]
    # match JournalReference authorScopusID with author [AUTHORED_BY]
    # match Affiliation authorScopusID with author [WITH]

    complex_keys=[]
    for key in keys:
        if isinstance(data[key],list) and len(data[key])!=0:
            complex_keys.append(key)
    print(complex_keys)
    logger.info('Creation of nodes set 2')
    for complex_key in complex_keys:
            print(complex_key)
            if complex_key=="Author":
                print("here")
                authors=data[complex_key]
                print(authors)
                for author in authors:
                    rAuthor=author
                    qauthor="""
                    create(a:Author) set a=$rAuthor
                    """
                    try:
                        Dict={"rAuthor":rAuthor}
                        session.run(qauthor,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="BibliographicReference":
                bibliographicReferences=data[complex_key]
                for bibliographicReference in bibliographicReferences:
                    rBibliographicReference=bibliographicReference
                    qbib="""
                    create(a:BibliographicReference) set a=$rBibliographicReference
                    """
                    try:
                        Dict={"rBibliographicReference":rBibliographicReference}
                        session.run(qbib,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="Hypothesis":
                hypothesiss=data[complex_key]
                for hypothesis in hypothesiss:
                    rHypothesis=hypothesis
                    qhyp="""
                    create(a:Hypothesis) set a=$rHypothesis
                    """
                    try:
                        Dict={"rHypothesis":rHypothesis}
                        session.run(qhyp,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="Proposition":
                propositions=data[complex_key]
                for proposition in propositions:
                    rProposition=proposition
                    qprop="""
                    create(a:Proposition) set a=$rProposition
                    """
                    try:
                        Dict={"rProposition":rProposition}
                        session.run(qprop,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="Affiliation":
                Affiliations=data[complex_key]
                for Affiliation in Affiliations:
                    rAffiliation=Affiliation
                    qbib="""
                    create(a:Affiliation) set a=$rAffiliation
                    """
                    try:
                        Dict={"rAffiliation":rAffiliation}
                        session.run(qbib,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="Keyword":
                Keywords=data[complex_key]
                for Keyword in Keywords:
                    rKeyword=Keyword
                    qbib="""
                    create(a:Keyword) set a=$rKeyword
                    """
                    try:
                        Dict={"rKeyword":rKeyword}
                        session.run(qbib,Dict)
                    except Exception as e:
                        print(str(e))
            elif complex_key=="Construct":
                Constructs=data[complex_key]
                for Construct in Constructs:
                    rConstruct=Construct
                    qbib="""
                    create(a:Construct) set a=$rConstruct
                    """
                    try:
                        Dict={"rConstruct":rConstruct}
                        session.run(qbib,Dict)
                    except Exception as e:
                        print(str(e))
            else:
                print(complex_key)
                print("invalid data")
                sys.exit()

    Dict={"referenceDOI":referenceDOI,"authorScopusID":authorScopusID,"vPublisherName":vPublisherName}    

    q="""MERGE (iv:`Construct Role`:`Independent Variable`)
    MERGE (dv:`Construct Role`:`Dependent Variable`)
    MERGE (mv1:`Construct Role`:`Moderator Variable`)
    MERGE (mv2:`Construct Role`:`Mediator Variable`)"""

    session.run (q,Dict)
    logger.info('Creation of relationships start')
    q="""CALL apoc.cypher.runMany('match(j:JournalReference)-[:USED]->(d:Data),(j)-[:APPEARED_IN]->(jp:JournalPublication),(jp)-[:PUBLISHED_BY]->(p:Publisher),(j)<-[:FUNDED]-(f:Funding),(a:Author),(b:BibliographicReference),(j)-[:USED]->(m:Method)
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
    MERGE (jp)-[:STUDIED]->(h);
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    match (pr:Proposition)
    where j.doi=pr.doi 
    merge (jp)-[:STUDIED]->(pr)
    merge (a)-[:STUDIED]->(pr)
    merge (j)-[:STUDIED]->(pr);
    match(j:JournalReference)-[:AUTHORED_BY]->(a:Author)
    where j.doi=$referenceDOI 
    match (k:Keyword)
    where  k.doi=j.doi 
    merge (j)-[:HAS]->(k)
    MERGE (jp)-[:HAS]->(k)
    MERGE (a)-[:HAS]->(k)
    MERGE (p)-[:HAS]->(k);
    MATCH (c:Construct)<-[:STUDIED]-(j:JournalReference), (j:JournalReference)-[:STUDIED]->(h:Hypothesis)
    where j.doi=$referenceDOI and c.hypothesisID=h.hypothesisID
    MERGE (h)-[:STUDIED]->(c);
    MATCH (c:Construct)<-[:STUDIED]-(j:JournalReference), (j:JournalReference)-[:STUDIED]->(p:Proposition)
    where j.doi=$referenceDOI and c.propositionID=p.propositionID
    MERGE (p)-[:STUDIED]->(c);
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
    MERGE (c)-[:AS]->(mv);', {referenceDOI:$referenceDOI},{statistics: false});"""

    session.run (q,Dict)
    logger.info('Creation of relationships ended')
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