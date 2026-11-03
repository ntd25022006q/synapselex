"""
SynapseLex: Vietnamese Civil Law Ontology (VCLO) Builder
Formal OWL 2 DL TBox & ABox Schema for Civil Legal Adjudication

Target Statutes:
- Bộ luật Dân sự 2015 (Civil Code 2015 - Law No. 91/2015/QH13)
- Luật Đất đai 2024 (Land Law 2024 - Law No. 31/2024/QH15)
- Nghị quyết số 02/2004/NQ-HĐTP của Hội đồng Thẩm phán TANDTC về tranh chấp hợp đồng đặt cọc

Authors: Nguyễn Tiến Đạt (datbazuka2502) & Antigravity Research Agent
Standard: OWL 2 DL Description Logics (SROIQ)
"""

import os
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD, URIRef
from rdflib.collection import Collection

def build_vclo_ontology(output_dir: str = "."):
    os.makedirs(output_dir, exist_ok=True)
    g = Graph()
    
    # Namespaces
    VCLO = Namespace("http://synapselex.org/ontology/vclo#")
    g.bind("vclo", VCLO)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    
    ontology_uri = URIRef("http://synapselex.org/ontology/vclo")
    g.add((ontology_uri, RDF.type, OWL.Ontology))
    g.add((ontology_uri, RDFS.label, Literal("Vietnamese Civil Law Ontology (VCLO Core)", lang="en")))
    g.add((ontology_uri, RDFS.label, Literal("Bản thể học Pháp luật Dân sự Việt Nam (VCLO)", lang="vi")))
    g.add((ontology_uri, RDFS.comment, Literal("Formal OWL 2 DL ontology for Vietnamese Civil Adjudication on real estate and deposit disputes under Civil Code 2015 and Land Law 2024.", lang="en")))
    g.add((ontology_uri, OWL.versionInfo, Literal("1.0.0 (Axiomatic Release)")))

    # -------------------------------------------------------------
    # 1. CORE CLASSES (TBox Concepts)
    # -------------------------------------------------------------
    classes = {
        # Root concepts
        "LegalEntity": ("Thực thể Pháp lý", "Base class for all legal persons, organizations and judicial organs."),
        "NaturalPerson": ("Cá nhân / Thể nhân", "A human being possessing legal capacity and civil act capacity."),
        "JuridicalPerson": ("Pháp nhân / Tổ chức", "An organization established lawfully with independent assets."),
        "JudicialOrgan": ("Cơ quan Tố tụng", "Courts and procuracies adjudicating civil disputes."),
        "CourtInstance": ("Cấp Tòa án Xét xử", "First instance or appellate judicial court."),
        
        # Procedural Roles (Bộ luật Tố tụng Dân sự 2015)
        "ProceduralRole": ("Vai trò Tố tụng", "Procedural legal status in civil proceedings."),
        "Plaintiff": ("Nguyên đơn", "The party initiating lawsuit alleging infringed civil rights."),
        "Defendant": ("Bị đơn", "The party against whom civil claims are filed."),
        "Intervener": ("Người có quyền lợi nghĩa vụ liên quan", "Third party having independent claims or related obligations."),
        
        # Legal Acts & Contracts
        "LegalAct": ("Hành vi Pháp lý", "Lawful or unlawful act creating, modifying, or terminating civil relations."),
        "CivilTransaction": ("Giao dịch Dân sự", "Contracts or unilateral legal acts under Article 116 BLDS 2015."),
        "Contract": ("Hợp đồng Dân sự", "Agreement between parties under Article 385 BLDS 2015."),
        "DepositContract": ("Hợp đồng Đặt cọc", "Measure to secure obligation under Article 328 BLDS 2015."),
        "LandUseRightTransferContract": ("Hợp đồng Chuyển nhượng QSDĐ", "Real estate transfer contract under Land Law & BLDS."),
        "BreachOfContract": ("Hành vi Vi phạm Hợp đồng", "Failure to perform or improper performance of contractual obligations."),
        "LawsuitFiling": ("Hành vi Khởi kiện", "Formal submission of civil petition to court."),
        
        # Legal States (Non-monotonic Adjudication)
        "LegalState": ("Trạng thái Hiệu lực Pháp lý", "Validity state of contracts and claims."),
        "ValidState": ("Trạng thái Có hiệu lực", "Contract fulfills all statutory validity conditions (Article 117)."),
        "VoidableState": ("Trạng thái Vô hiệu Tương đối", "Contract may be declared void upon petition (mistake, deception)."),
        "VoidAbInitioState": ("Trạng thái Vô hiệu Tuyệt đối", "Contract void from inception due to statutory prohibition (Article 123)."),
        "ExtinguishedState": ("Trạng thái Hết hiệu lực / Hết thời hiệu", "Claim extinguished due to statute of limitations lapse."),
        
        # Normative Hierarchy & Statutes
        "StatutoryRegime": ("Hệ thống Quy phạm Pháp luật", "Hierarchical body of legal norms."),
        "Statute": ("Văn bản Quy phạm Pháp luật", "Legal document enacted by competent state bodies."),
        "Constitution": ("Hiến pháp", "Supreme law of Vietnam (Rank 1)."),
        "CivilCode": ("Bộ luật Dân sự", "General primary civil statute (Rank 2)."),
        "SpecializedLaw": ("Luật Chuyên ngành", "Specialized statutory acts overriding general law (Rank 2.5)."),
        "SubLawDecree": ("Nghị định / Thông tư", "Executive subordinate regulatory decrees (Rank 3)."),
        "JudicialPrecedent": ("Án lệ / Nghị quyết HĐTP", "Binding Supreme People's Court interpretations."),
        
        # Temporal Concept
        "TemporalInterval": ("Khoảng Thời gian Pháp lý", "Interval with definite start and end dates."),
        "StatuteOfLimitations": ("Thời hiệu Khởi kiện", "Statutory time window to request judicial remedy (Article 429)."),
        
        # Judicial Verdicts
        "CourtVerdict": ("Phán quyết của Tòa án", "Binding judicial resolution of the civil dispute."),
        "AcceptDepositForfeiture": ("Chấp nhận Phạt cọc", "Ruling ordering forfeiture of deposit to innocent party."),
        "AcceptDoubleDepositRefund": ("Chấp nhận Phạt cọc Gấp đôi", "Ruling requiring breaching deposit-taker to return deposit + equal penalty."),
        "DismissDueToLapsedLimitation": ("Đình chỉ / Bác đơn do Hết thời hiệu", "Ruling dismissing claims because statute of limitations expired."),
        "DeclareContractVoid": ("Tuyên bố Hợp đồng Vô hiệu", "Ruling declaring contract void and ordering restitution of original status."),
    }

    for cls_name, (label_vi, comment_en) in classes.items():
        uri = VCLO[cls_name]
        g.add((uri, RDF.type, OWL.Class))
        g.add((uri, RDFS.label, Literal(label_vi, lang="vi")))
        g.add((uri, RDFS.comment, Literal(comment_en, lang="en")))

    # Subclass hierarchies
    hierarchies = [
        ("NaturalPerson", "LegalEntity"),
        ("JuridicalPerson", "LegalEntity"),
        ("JudicialOrgan", "LegalEntity"),
        ("CourtInstance", "JudicialOrgan"),
        
        ("Plaintiff", "ProceduralRole"),
        ("Defendant", "ProceduralRole"),
        ("Intervener", "ProceduralRole"),
        
        ("CivilTransaction", "LegalAct"),
        ("Contract", "CivilTransaction"),
        ("DepositContract", "Contract"),
        ("LandUseRightTransferContract", "Contract"),
        ("BreachOfContract", "LegalAct"),
        ("LawsuitFiling", "LegalAct"),
        
        ("ValidState", "LegalState"),
        ("VoidableState", "LegalState"),
        ("VoidAbInitioState", "LegalState"),
        ("ExtinguishedState", "LegalState"),
        
        ("Constitution", "Statute"),
        ("CivilCode", "Statute"),
        ("SpecializedLaw", "Statute"),
        ("SubLawDecree", "Statute"),
        ("JudicialPrecedent", "Statute"),
        
        ("AcceptDepositForfeiture", "CourtVerdict"),
        ("AcceptDoubleDepositRefund", "CourtVerdict"),
        ("DismissDueToLapsedLimitation", "CourtVerdict"),
        ("DeclareContractVoid", "CourtVerdict"),
    ]

    for sub_cls, super_cls in hierarchies:
        g.add((VCLO[sub_cls], RDFS.subClassOf, VCLO[super_cls]))

    # Disjointness Axioms (Ensure mutual exclusivity)
    disjoint_groups = [
        ["ValidState", "VoidAbInitioState", "ExtinguishedState"],
        ["Plaintiff", "Defendant", "Intervener"],
        ["DepositContract", "LandUseRightTransferContract"],
        ["Constitution", "CivilCode", "SpecializedLaw", "SubLawDecree"],
    ]
    for grp in disjoint_groups:
        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                g.add((VCLO[grp[i]], OWL.disjointWith, VCLO[grp[j]]))

    # -------------------------------------------------------------
    # 2. OBJECT PROPERTIES (TBox Predicates)
    # -------------------------------------------------------------
    object_properties = {
        "hasProceduralRole": ("has procedural role", "LegalEntity", "ProceduralRole"),
        "isPartyToContract": ("is party to contract", "LegalEntity", "Contract"),
        "securesObligation": ("secures obligation for", "DepositContract", "LandUseRightTransferContract"),
        "governedByStatute": ("governed by statutory act", "LegalAct", "Statute"),
        "hasValidityState": ("has current validity state", "Contract", "LegalState"),
        "hasTemporalInterval": ("has active temporal interval", "LegalAct", "TemporalInterval"),
        "triggersStateTransition": ("triggers state transition to", "LegalAct", "LegalState"),
        "violatesStatutoryArticle": ("violates statutory article", "LegalAct", "Statute"),
        "initiatesCivilDispute": ("initiates civil dispute", "LawsuitFiling", "Contract"),
        "adjudicatesVerdict": ("adjudicates final verdict", "CourtInstance", "CourtVerdict"),
        "resolvesContract": ("resolves disputed contract", "CourtVerdict", "Contract"),
    }

    for prop_name, (label, domain, range_cls) in object_properties.items():
        uri = VCLO[prop_name]
        g.add((uri, RDF.type, OWL.ObjectProperty))
        g.add((uri, RDFS.label, Literal(label, lang="en")))
        g.add((uri, RDFS.domain, VCLO[domain]))
        g.add((uri, RDFS.range, VCLO[range_cls]))

    # -------------------------------------------------------------
    # 3. DATATYPE PROPERTIES (TBox Literals)
    # -------------------------------------------------------------
    datatype_properties = {
        "caseIdentificationNumber": ("case number ID", "CourtVerdict", XSD.string),
        "adjudicationDate": ("date verdict was rendered", "CourtVerdict", XSD.dateTime),
        "depositAmountVND": ("monetary deposit value in VND", "DepositContract", XSD.decimal),
        "agreedTransferPriceVND": ("total agreed real estate price", "LandUseRightTransferContract", XSD.decimal),
        "isNotarizedByNotaryPublic": ("has official public notarization", "Contract", XSD.boolean),
        "hasLandUseRightCertificate": ("land possesses Red/Pink Book Certificate", "LandUseRightTransferContract", XSD.boolean),
        "statuteOfLimitationsDays": ("statutory limitation days (1095 days for CC 2015 Art. 429)", "StatuteOfLimitations", XSD.integer),
        "elapsedDaysSinceInfringement": ("elapsed calendar days from breach to filing", "LawsuitFiling", XSD.integer),
        "normativeRank": ("hierarchical statutory rank (1 supreme, 4 subordinate)", "Statute", XSD.integer),
    }

    for prop_name, (label, domain, datatype) in datatype_properties.items():
        uri = VCLO[prop_name]
        g.add((uri, RDF.type, OWL.DatatypeProperty))
        g.add((uri, RDFS.label, Literal(label, lang="en")))
        g.add((uri, RDFS.domain, VCLO[domain]))
        g.add((uri, RDFS.range, datatype))

    # -------------------------------------------------------------
    # 4. FORMAL AXIOMS (Description Logics SROIQ representation)
    # -------------------------------------------------------------
    # Axiom 1: DepositContract must secure some Contract
    some_restriction = g.resource(URIRef("http://synapselex.org/ontology/vclo#DepositSecuresRestriction"))
    g.add((some_restriction.identifier, RDF.type, OWL.Restriction))
    g.add((some_restriction.identifier, OWL.onProperty, VCLO.securesObligation))
    g.add((some_restriction.identifier, OWL.someValuesFrom, VCLO.Contract))
    g.add((VCLO.DepositContract, RDFS.subClassOf, some_restriction.identifier))

    # Export formats
    owl_path = os.path.join(output_dir, "vclo_core.owl")
    ttl_path = os.path.join(output_dir, "vclo_core.ttl")
    
    g.serialize(destination=owl_path, format="xml")
    g.serialize(destination=ttl_path, format="turtle")
    
    print(f"[GROUND TRUTH / FACT] VCLO Ontology successfully built:")
    print(f"  • OWL/XML: {owl_path} ({os.path.getsize(owl_path)} bytes)")
    print(f"  • Turtle:  {ttl_path} ({os.path.getsize(ttl_path)} bytes)")
    print(f"  • Total Triples: {len(g)}")
    return g

if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    build_vclo_ontology(out_dir)
