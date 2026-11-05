import csv
import json
import os

OUTPUT_DIR = "/Users/agiliteach/Documents/antigravity/LDC/PharmaNova"
CSV_DIR = os.path.join(OUTPUT_DIR, "CSV_Data")
os.makedirs(CSV_DIR, exist_ok=True)

# ==============================================================================
# 1. PHARMANOVA CORPORATE PROFILE
# ==============================================================================
COMPANY_INFO = {
    "name": "PharmaNova SA",
    "legal_status": "Société Anonyme à Directoire et Conseil de Surveillance",
    "capital": "42 500 000 €",
    "founded_year": 1998,
    "headquarters": "14, Avenue Tony Garnier, Biopôle de Gerland, 69007 Lyon, France",
    "r_and_d_center": "Centre d'Innovation Thérapeutique Marcel Mérieux, 69007 Lyon",
    "manufacturing_sites": [
        {
            "site_id": "SITE-CHALON",
            "name": "Site Industriel de Chalon-sur-Saône",
            "address": "Zone Industrielle Nord, 71100 Chalon-sur-Saône, France",
            "capabilities": "Formes sèches (comprimés, gélules), formes liquides et poudres pour inhalation. Lignes de conditionnement automatisées blister/flacon.",
            "certifications": "ANSM GMP, FDA cGMP (2022), ISO 9001:2015, ISO 14001:2015",
            "head": "M. Pierre-Yves Bernard (Directeur de Site Industriel)"
        },
        {
            "site_id": "SITE-MARBURG",
            "name": "PharmaNova Biologics & Injectables GmbH",
            "address": "Emil-von-Behring-Straße 76, 35041 Marburg, Allemagne",
            "capabilities": "Biotechnologie (fermentation bioréacteurs, chromatographie, filtration stérilisante), remplissage aseptique de seringues préremplies et stylos.",
            "certifications": "BfArM / Regierungspräsidium Gießen GMP, EMA Certified, ISO 13485:2016",
            "head": "Dr. Klaus Reinhardt (Geschäftsführer Standort Marburg)"
        }
    ],
    "distribution_hubs": [
        {
            "site_id": "HUB-ST-QUENTIN",
            "name": "Hub Logistique Européen PharmaNova Saint-Quentin-Fallavier",
            "address": "Parc d'Activités de Chesnes, 38070 Saint-Quentin-Fallavier, France",
            "capabilities": "Entrepôt central sous température dirigée (15-25°C, chambre froide 2-8°C, zone cryo -20°C/-80°C), distribution GDP.",
            "certifications": "Certificat GDP ANSM N° 2023-GDP-FR-0412"
        },
        {
            "site_id": "HUB-MECHELEN",
            "name": "Benelux & Northern Europe Logistics Center",
            "address": "Industriepark Noord, 2800 Mechelen, Belgique",
            "capabilities": "Plateforme logistique cross-docking et expédition Benelux, UK et Scandinavie.",
            "certifications": "Certificat GDP AFMPS/FAGG N° BE-GDP-2022-881"
        }
    ],
    "commercial_subsidiaries": [
        {"name": "PharmaNova France SAS", "city": "Lyon & Paris, France"},
        {"name": "PharmaNova GmbH", "city": "Francfort-sur-le-Main, Allemagne"},
        {"name": "PharmaNova Iberia SL", "city": "Madrid, Espagne"},
        {"name": "PharmaNova Italia Srl", "city": "Milan, Italie"},
        {"name": "PharmaNova UK Ltd", "city": "Guildford, Surrey, Royaume-Uni"}
    ],
    "financials_2023": {
        "revenue_eur": "684 500 000 €",
        "ebitda_eur": "142 800 000 €",
        "r_and_d_investment": "98 500 000 € (14.4% du CA)",
        "total_employees": 1420
    }
}

# Key Executives and Department Leads
PERSONNEL = [
    {"emp_id": "EMP-001", "name": "Dr. Jean-Marc Delacroix", "title": "Président du Directoire (CEO)", "dept": "Direction Générale", "email": "jm.delacroix@pharmanova.eu", "phone": "+33 4 78 50 10 01", "location": "Lyon HQ", "manager_id": None},
    {"emp_id": "EMP-002", "name": "Dr. Éléonore Vance", "title": "Directrice Médicale Globale & VP Affaires Médicales (CMO)", "dept": "Affaires Médicales", "email": "e.vance@pharmanova.eu", "phone": "+33 4 78 50 10 02", "location": "Lyon HQ", "manager_id": "EMP-001"},
    {"emp_id": "EMP-003", "name": "Mme Christine Baudry", "title": "Directrice Globale des Affaires Réglementaires (VP RA)", "dept": "Affaires Réglementaires", "email": "c.baudry@pharmanova.eu", "phone": "+33 4 78 50 10 03", "location": "Lyon HQ", "manager_id": "EMP-001"},
    {"emp_id": "EMP-004", "name": "M. François Mercier", "title": "Directeur Qualité Groupe & Pharmacien Responsable (VP QA / QP)", "dept": "Assurance Qualité", "email": "f.mercier@pharmanova.eu", "phone": "+33 4 78 50 10 04", "location": "Lyon HQ", "manager_id": "EMP-001"},
    {"emp_id": "EMP-005", "name": "Dr. Marc-Antoine Leroy", "title": "Directeur Global de la Pharmacovigilance & EU QPPV", "dept": "Pharmacovigilance", "email": "ma.leroy@pharmanova.eu", "phone": "+33 4 78 50 10 05", "location": "Lyon HQ", "manager_id": "EMP-002"},
    {"emp_id": "EMP-006", "name": "Mme Valérie Roche", "title": "Pharmacien Délégué Libération des Lots (QP Delegated)", "dept": "Assurance Qualité", "email": "v.roche@pharmanova.eu", "phone": "+33 4 78 50 10 06", "location": "Site Chalon", "manager_id": "EMP-004"},
    {"emp_id": "EMP-007", "name": "Dr. Philippe Gauthier", "title": "Directeur du Contrôle Qualité & Laboratoires Analytiques", "dept": "Contrôle Qualité", "email": "p.gauthier@pharmanova.eu", "phone": "+33 4 78 50 10 07", "location": "Site Chalon", "manager_id": "EMP-004"},
    {"emp_id": "EMP-008", "name": "Mme Nathalie Benhamou", "title": "Responsable Assurance Qualité Opérationnelle & Système CAPA", "dept": "Assurance Qualité", "email": "n.benhamou@pharmanova.eu", "phone": "+33 4 78 50 10 08", "location": "Site Chalon", "manager_id": "EMP-004"},
    {"emp_id": "EMP-009", "name": "M. Thomas Vasseur", "title": "Responsable des Audits Internes & Qualification Fournisseurs GxP", "dept": "Assurance Qualité", "email": "t.vasseur@pharmanova.eu", "phone": "+33 4 78 50 10 09", "location": "Lyon HQ", "manager_id": "EMP-004"},
    {"emp_id": "EMP-010", "name": "Dr. Claire Dupuis", "title": "Responsable de l'Information Médicale & Transparence", "dept": "Affaires Médicales", "email": "c.dupuis@pharmanova.eu", "phone": "+33 4 78 50 10 10", "location": "Lyon HQ", "manager_id": "EMP-002"},
    {"emp_id": "EMP-011", "name": "M. Laurent Garnier", "title": "Directeur de la Supply Chain Globale & Distribution GDP", "dept": "Supply Chain", "email": "l.garnier@pharmanova.eu", "phone": "+33 4 78 50 10 11", "location": "St-Quentin-Fallavier", "manager_id": "EMP-001"},
    {"emp_id": "EMP-012", "name": "Dr. Sarah Lindner", "title": "Deputy EU QPPV & Directrice PV Région DACH", "dept": "Pharmacovigilance", "email": "s.lindner@pharmanova.de", "phone": "+49 69 95 40 20", "location": "Francfort", "manager_id": "EMP-005"},
    {"emp_id": "EMP-013", "name": "Dr. Sophie Maréchal", "title": "Directrice Médicale Domaine Cardiovasculaire & Métabolisme", "dept": "Affaires Médicales", "email": "s.marechal@pharmanova.eu", "phone": "+33 4 78 50 10 13", "location": "Lyon HQ", "manager_id": "EMP-002"},
    {"emp_id": "EMP-014", "name": "Dr. Antoine Bertrand", "title": "Directeur Médical Domaine Oncologie & Hématologie", "dept": "Affaires Médicales", "email": "a.bertrand@pharmanova.eu", "phone": "+33 4 78 50 10 14", "location": "Lyon HQ", "manager_id": "EMP-002"},
    {"emp_id": "EMP-015", "name": "Dr. Hélène Fournier", "title": "Directrice Médicale Neurologie & Respiratoire", "dept": "Affaires Médicales", "email": "h.fournier@pharmanova.eu", "phone": "+33 4 78 50 10 15", "location": "Lyon HQ", "manager_id": "EMP-002"},
    {"emp_id": "EMP-016", "name": "M. Julien Tavernier", "title": "Manager Affaires Réglementaires Europe (Procédures Centralisées)", "dept": "Affaires Réglementaires", "email": "j.tavernier@pharmanova.eu", "phone": "+33 4 78 50 10 16", "location": "Lyon HQ", "manager_id": "EMP-003"},
    {"emp_id": "EMP-017", "name": "Mme Sophie Bernard", "title": "Manager Affaires Réglementaires France & MRP/DCP", "dept": "Affaires Réglementaires", "email": "s.bernard@pharmanova.eu", "phone": "+33 4 78 50 10 17", "location": "Lyon HQ", "manager_id": "EMP-003"},
    {"emp_id": "EMP-018", "name": "Dr. Karim Belkacem", "title": "Médecin Évaluateur Pharmacovigilance & Gestion des Signaux", "dept": "Pharmacovigilance", "email": "k.belkacem@pharmanova.eu", "phone": "+33 4 78 50 10 18", "location": "Lyon HQ", "manager_id": "EMP-005"},
    {"emp_id": "EMP-019", "name": "Mme Camille Roussel", "title": "Pharmacien Spécialiste ICSR & Déclarations EudraVigilance", "dept": "Pharmacovigilance", "email": "c.roussel@pharmanova.eu", "phone": "+33 4 78 50 10 19", "location": "Lyon HQ", "manager_id": "EMP-005"},
    {"emp_id": "EMP-020", "name": "M. David Leroy", "title": "Responsable Conformité eCTD & Variations Réglementaires", "dept": "Affaires Réglementaires", "email": "d.leroy@pharmanova.eu", "phone": "+33 4 78 50 10 20", "location": "Lyon HQ", "manager_id": "EMP-003"}
]

# Generate realistic collaborators up to 120
FIRST_NAMES = ["Alexandre", "Béatrice", "Cédric", "Delphine", "Éric", "Florence", "Guillaume", "Hélène", "Isabelle", "Jérôme", "Karine", "Ludovic", "Mathieu", "Nathalie", "Olivier", "Patricia", "Quentin", "Régis", "Sandrine", "Thierry", "Virginie", "Xavier", "Yves", "Zoé", "Marc", "Sylvie", "Benoît", "Anne", "Christophe", "Julie"]
LAST_NAMES = ["Moreau", "Lefebvre", "Dubois", "Roux", "Fournier", "Gerard", "Bonnet", "Dupont", "Lambert", "Fontaine", "Rousseau", "Vincent", "Muller", "Guerin", "Boyer", "Garnier", "Chevalier", "Francois", "Legrand", "Gauthier", "Garcia", "Perrin", "Robin", "Clement", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu", "Gautier"]
DEPTS = [
    ("Assurance Qualité", "Site Chalon", "EMP-008", ["Ingénieur QA Validation", "Spécialiste CAPA", "Auditeur Qualité Interne", "Technicien Revue de Dossier de Lot"]),
    ("Contrôle Qualité", "Site Chalon", "EMP-007", ["Technicien HPLC/GC", "Microbiologiste QC", "Analyste Stabilité", "Responsable Salle Blanche"]),
    ("Production", "Site Chalon", "EMP-006", ["Superviseur Ligne Conditionnement", "Opérateur Granulation", "Pilote Compression", "Chef d'Équipe Pelliculage"]),
    ("Bioproduction", "Site Marburg", "EMP-004", ["Bioprocédé Fermentation", "Ingénieur Purification Downstream", "Technicien Remplissage Aseptique", "Spécialiste Formulation Biologique"]),
    ("Supply Chain & GDP", "St-Quentin-Fallavier", "EMP-011", ["Coordinateur Chaîne du Froid", "Gestionnaire Entrepôt GDP", "Responsable Transport Qualifié", "Planificateur Logistique"]),
    ("Pharmacovigilance", "Lyon HQ", "EMP-005", ["Gestionnaire de Données ICSR", "Pharmacien Évaluateur Tolérance", "Coordinateur PSUR/PBRER", "Spécialiste Base Safety"]),
    ("Affaires Réglementaires", "Lyon HQ", "EMP-003", ["Chargé d'Enregistrement", "Spécialiste Étiquetage & Notices", "Coordinateur Renouvellements", "Gestionnaire eCTD"]),
    ("Information Médicale", "Lyon HQ", "EMP-010", ["Pharmacien Info Médicale", "Rédacteur Médical Scientifique", "Gestionnaire FAQ Médicales", "Attaché de Documentation Clinique"]),
    ("Affaires Médicales (MSL)", "Territoire National", "EMP-013", ["MSL Cardiologie", "MSL Oncologie", "MSL Neurologie", "MSL Immunologie", "MSL Pneumologie"]),
    ("Systèmes d'Information GxP", "Lyon HQ", "EMP-004", ["Administrateur GED Qualité Veeva", "Ingénieur Validation Informatique CSV", "Responsable Intégrité des Données ALCOA+"])
]

idx = 21
for dept, loc, mgr, roles in DEPTS:
    for role in roles:
        fn = FIRST_NAMES[(idx * 7) % len(FIRST_NAMES)]
        ln = LAST_NAMES[(idx * 11) % len(LAST_NAMES)]
        PERSONNEL.append({
            "emp_id": f"EMP-{idx:03d}",
            "name": f"{fn} {ln}",
            "title": role,
            "dept": dept,
            "email": f"{fn[0].lower()}.{ln.lower()}@pharmanova.eu",
            "phone": f"+33 4 78 50 {1000 + idx}",
            "location": loc,
            "manager_id": mgr
        })
        idx += 1
        if idx > 120:
            break
    if idx > 120:
        break

# Complete the rest up to 120
while len(PERSONNEL) < 120:
    fn = FIRST_NAMES[(idx * 3) % len(FIRST_NAMES)]
    ln = LAST_NAMES[(idx * 5) % len(LAST_NAMES)]
    PERSONNEL.append({
        "emp_id": f"EMP-{idx:03d}",
        "name": f"{fn} {ln}",
        "title": "Analyste Qualité Opérationnelle",
        "dept": "Assurance Qualité",
        "email": f"{fn[0].lower()}.{ln.lower()}@pharmanova.eu",
        "phone": f"+33 4 78 50 {1000 + idx}",
        "location": "Site Chalon",
        "manager_id": "EMP-008"
    })
    idx += 1

# ==============================================================================
# 2. PRODUCT PORTFOLIO (15 MEDICINES)
# ==============================================================================
PRODUCTS = [
    {
        "prod_id": "PRD-001",
        "code": "CARDIO",
        "brand_name": "Cardiolux",
        "inn_dci": "Ziltorvastatine / Amlodipine bésylate",
        "therapeutic_area": "Cardiovasculaire",
        "atc_code": "C10BX03",
        "indication": "Traitement de l'hypertension artérielle essentielle associée à une hypercholestérolémie primaire chez l'adulte à haut risque cardiovasculaire.",
        "galenic_form": "Comprimé pelliculé bi-couche (20 mg / 5 mg)",
        "dosage_regimen": "1 comprimé par jour par voie orale, le matin de préférence, au cours ou en dehors des repas.",
        "contraindications": "Insuffisance hépatique sévère, choc cardiogénique, sténose aortique serrée, angor instable, grossesse et allaitement, hypersensibilité aux dihydropyridines ou aux statines.",
        "common_adverse_events": "Œdèmes des membres inférieurs (8.4%), céphalées (5.1%), myalgies bénignes (3.8%), sensations vertigineuses (3.2%), nausées (2.5%).",
        "serious_risks": "Rhabdomyolyse aiguë (rare < 1/10 000), hépatotoxicité cytolytique, hypotension orthostatique sévère.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/16/1089/001",
        "initial_ma_date": "2016-04-18",
        "renewal_date": "2021-04-20 (Illimitée)",
        "commercial_status": "Commercialisé dans 14 pays de l'UE",
        "packaging": "Boîte de 30 comprimés sous plaquettes thermoformées (Alu/Alu)",
        "storage_condition": "À conserver à une température ne dépassant pas 25°C, à l'abri de l'humidité.",
        "shelf_life_months": 36,
        "price_eur": "18.45 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 1250000,
        "annual_sales_eur": "23 062 500 €",
        "lead_physician": "Dr. Sophie Maréchal",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-002",
        "code": "VASCO",
        "brand_name": "Vascopril",
        "inn_dci": "Candésartan cilexétil / Indapamide",
        "therapeutic_area": "Cardiovasculaire",
        "atc_code": "C09DA06",
        "indication": "Hypertension artérielle essentielle non contrôlée par une monothérapie chez l'adulte.",
        "galenic_form": "Comprimé pelliculé sécable (16 mg / 1.5 mg LP)",
        "dosage_regimen": "1 comprimé par jour, à prendre le matin avec un verre d'eau.",
        "contraindications": "Insuffisance rénale sévère (ClCr < 30 mL/min), encéphalopathie hépatique, hypokaliémie réfractaire, 2e et 3e trimestres de grossesse.",
        "common_adverse_events": "Hypotension, vertiges, hypokaliémie modérée (2.8%), asthénie, éruption cutanée.",
        "serious_risks": "Insuffisance rénale aiguë chez les sujets déshydratés, angio-œdème de Quincke, torsades de pointes sur hypokaliémie profonde.",
        "regulatory_status": "Autorisé (Procédure Décentralisée FR/H/0452/001)",
        "ma_number": "FR/H/0452/001",
        "initial_ma_date": "2018-09-12",
        "renewal_date": "2023-09-15 (Illimitée)",
        "commercial_status": "Commercialisé en France, Allemagne, Espagne, Italie",
        "packaging": "Boîte de 28 comprimés sous blister PVC/PVDC/Alu",
        "storage_condition": "À conserver à une température inférieure à 30°C.",
        "shelf_life_months": 36,
        "price_eur": "14.20 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 980000,
        "annual_sales_eur": "13 916 000 €",
        "lead_physician": "Dr. Sophie Maréchal",
        "ra_manager": "Mme Sophie Bernard",
        "pv_officer": "Mme Camille Roussel"
    },
    {
        "prod_id": "PRD-003",
        "code": "CORAN",
        "brand_name": "Coranid",
        "inn_dci": "Ivabradine chlorhydrate / Métoprolol succinate",
        "therapeutic_area": "Cardiovasculaire",
        "atc_code": "C01EB22",
        "indication": "Angor stable chronique et insuffisance cardiaque chronique classe II-IV NYHA avec fraction d'éjection réduite chez l'adulte en rythme sinusal et FC ≥ 70 bpm.",
        "galenic_form": "Gélule à libération modifiée (7.5 mg / 50 mg)",
        "dosage_regimen": "1 gélule deux fois par jour (matin et soir) pendant les repas.",
        "contraindications": "Fréquence cardiaque au repos < 60 bpm avant traitement, choc cardiogénique, infarctus du myocarde récent, bloc sino-auriculaire, BAV du 2e et 3e degré.",
        "common_adverse_events": "Phénomènes lumineux visuels (phosphènes 11.2%), bradycardie sinusale (6.4%), céphalées, vertiges.",
        "serious_risks": "Fibrillation auriculaire paroxystique, bradycardie sévère (< 45 bpm), décompensation cardiaque aiguë.",
        "regulatory_status": "Autorisé (Procédure Reconnaissance Mutuelle NL/H/1820/001)",
        "ma_number": "NL/H/1820/001",
        "initial_ma_date": "2019-06-25",
        "renewal_date": "2024-06-30 (En cours de renouvellement)",
        "commercial_status": "Commercialisé dans 8 pays européens",
        "packaging": "Boîte de 56 gélules sous plaquettes thermoformées",
        "storage_condition": "Conserver dans l'emballage d'origine, à l'abri de la lumière et de l'humidité.",
        "shelf_life_months": 24,
        "price_eur": "34.80 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 620000,
        "annual_sales_eur": "21 576 000 €",
        "lead_physician": "Dr. Sophie Maréchal",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-004",
        "code": "NEURO",
        "brand_name": "Neurotix",
        "inn_dci": "Brivastérol",
        "therapeutic_area": "Neurologie",
        "atc_code": "N03AX24",
        "indication": "Traitement adjuvant des crises d'épilepsie focale avec ou sans généralisation secondaire chez l'adulte et l'adolescent à partir de 16 ans.",
        "galenic_form": "Comprimé pelliculé (50 mg et 100 mg) & Solution injectable IV (10 mg/mL)",
        "dosage_regimen": "Dose initiale de 50 mg deux fois par jour, pouvant être augmentée à 100 mg deux fois par jour en fonction de la réponse clinique.",
        "contraindications": "Hypersensibilité aux dérivés pyrrolidone, antécédents de troubles psychotiques aigus sous racétams.",
        "common_adverse_events": "Somnolence (14.2%), étourdissements (11.0%), irritabilité (4.5%), fatigue (7.3%), nausées.",
        "serious_risks": "Idéations suicidaires, dépression majeure aiguë, bronchospasme réactionnel.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/18/1254/001",
        "initial_ma_date": "2018-03-22",
        "renewal_date": "2023-04-10 (Illimitée)",
        "commercial_status": "Commercialisé dans l'UE et au Royaume-Uni",
        "packaging": "Boîte de 56 comprimés pelliculés (plaquettes Alu/Alu)",
        "storage_condition": "Pas de précautions particulières de conservation.",
        "shelf_life_months": 48,
        "price_eur": "62.50 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 750000,
        "annual_sales_eur": "46 875 000 €",
        "lead_physician": "Dr. Hélène Fournier",
        "ra_manager": "M. David Leroy",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-005",
        "code": "COGNI",
        "brand_name": "Cognifère",
        "inn_dci": "Donepézil chlorhydrate / Mémantine chlorhydrate",
        "therapeutic_area": "Neurologie",
        "atc_code": "N06DX30",
        "indication": "Traitement symptomatique de la maladie d'Alzheimer au stade modéré à sévère chez le patient adulte stabilisé sous cette association.",
        "galenic_form": "Comprimé orodispersible (10 mg / 20 mg)",
        "dosage_regimen": "1 comprimé orodispersible par jour, à déposer sur la langue le soir au coucher.",
        "contraindications": "Insuffisance hépatique sévère, antécédents d'ulcère gastro-duodénal actif, épilepsie non contrôlée.",
        "common_adverse_events": "Diarrhée (8.1%), crampes musculaires, insomnie, vertiges, hallucinations visuelles transitoires.",
        "serious_risks": "Syncope vagale avec bradycardie sévère, syndrome malin des neuroleptiques, hépatite aiguë toxique.",
        "regulatory_status": "Autorisé (Procédure Décentralisée DE/H/2104/001)",
        "ma_number": "DE/H/2104/001",
        "initial_ma_date": "2020-01-15",
        "renewal_date": "2025-01-15 (Dossier préparé)",
        "commercial_status": "Commercialisé en Allemagne, France, Espagne, Benelux",
        "packaging": "Boîte de 28 comprimés orodispersibles en strips prédécoupés",
        "storage_condition": "À conserver à l'abri de l'humidité et à température < 25°C.",
        "shelf_life_months": 36,
        "price_eur": "48.20 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 410000,
        "annual_sales_eur": "19 762 000 €",
        "lead_physician": "Dr. Hélène Fournier",
        "ra_manager": "Mme Sophie Bernard",
        "pv_officer": "Mme Camille Roussel"
    },
    {
        "prod_id": "PRD-006",
        "code": "TREMO",
        "brand_name": "Tremopan",
        "inn_dci": "Safinamide mésylate / Lévodopa retard",
        "therapeutic_area": "Neurologie",
        "atc_code": "N04BA05",
        "indication": "Traitement de la maladie de Parkinson idiopathique chez les patients fluctuants sous lévodopa seule ou associée.",
        "galenic_form": "Gélule à libération prolongée (100 mg / 200 mg)",
        "dosage_regimen": "1 gélule une fois par jour le matin, avalée entière sans être croquée.",
        "contraindications": "Traitement concomitant par IMAO non sélectifs ou péthidine, rétinopathie pigmentaire ou antécédents de décollement de rétine, insuffisance hépatique sévère.",
        "common_adverse_events": "Dyskinésies (12.5%), somnolence diurne brutale, nausées, hypotension orthostatique, insomnie.",
        "serious_risks": "Syndrome de dysrégulation dopaminergique (troubles du contrôle des impulsions : jeu pathologique, hypersexualité), syndrome sérotoninergique.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/20/1445/001",
        "initial_ma_date": "2020-11-19",
        "renewal_date": "2025-11-20 (Dossier en cours)",
        "commercial_status": "Commercialisé dans 10 pays de l'UE",
        "packaging": "Flacon PEHD de 30 gélules avec bouchon sécurité enfant et dessiccant",
        "storage_condition": "À conserver à une température ne dépassant pas 30°C.",
        "shelf_life_months": 36,
        "price_eur": "78.00 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 380000,
        "annual_sales_eur": "29 640 000 €",
        "lead_physician": "Dr. Hélène Fournier",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-007",
        "code": "GLUCO",
        "brand_name": "Glucorite",
        "inn_dci": "Dagliflozine / Sitagliptine phosphate",
        "therapeutic_area": "Diabète",
        "atc_code": "A10BD22",
        "indication": "Traitement du diabète de type 2 chez l'adulte en complément du régime alimentaire et de l'exercice physique lorsque la metformine est insuffisante ou non tolérée.",
        "galenic_form": "Comprimé pelliculé (10 mg / 100 mg)",
        "dosage_regimen": "1 comprimé par jour par voie orale, à n'importe quel moment de la journée, avec ou sans aliments.",
        "contraindications": "Acidocétose diabétique, insuffisance rénale terminale (DFG < 20 mL/min/1.73m²), antécédents de pancréatite aiguë sévère sous gliptine.",
        "common_adverse_events": "Infections urinaires et mycoses génitales (9.8%), polyurie, rhinopharyngite, constipation légère.",
        "serious_risks": "Acidocétose diabétique euglycémique, fasciite nécrosante du périnée (gangrène de Fournier), pancréatite aiguë nécrosante.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/19/1376/001",
        "initial_ma_date": "2019-10-14",
        "renewal_date": "2024-10-15 (Renouvelé)",
        "commercial_status": "Blockbuster commercialisé dans 18 pays européens",
        "packaging": "Boîte de 30 et 90 comprimés pelliculés (plaquettes Alu/Alu thermoformées)",
        "storage_condition": "Conserver à température ambiante (15-25°C).",
        "shelf_life_months": 36,
        "price_eur": "42.10 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 1850000,
        "annual_sales_eur": "77 885 000 €",
        "lead_physician": "Dr. Sophie Maréchal",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-008",
        "code": "INSUL",
        "brand_name": "Insulip",
        "inn_dci": "Églifénotide",
        "therapeutic_area": "Diabète & Obésité",
        "atc_code": "A10BJ07",
        "indication": "Contrôle glycémique du diabète de type 2 et réduction pondérale chez les patients avec IMC ≥ 30 kg/m² ou ≥ 27 kg/m² avec comorbidité métabolique.",
        "galenic_form": "Solution injectable en stylo prérempli SC hebdomadaire (2 mg / 0.5 mL)",
        "dosage_regimen": "Injection sous-cutanée une fois par semaine (abdomen, cuisse ou bras) débutée à 0.5 mg puis titrée à 2 mg.",
        "contraindications": "Antécédents personnels ou familiaux de cancer médullaire de la thyroïde, syndrome de néoplasie endocrinienne multiple de type 2 (NEM 2).",
        "common_adverse_events": "Nausées transitoires (22.4%), diarrhée (14.2%), vomissements (8.6%), dyspepsie, perte d'appétit marquée.",
        "serious_risks": "Pancréatite aiguë, iléus paralytique / gastroparésie sévère, hypoglycémie en cas d'association aux sulfamides ou insulines.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/22/1620/001",
        "initial_ma_date": "2022-05-18",
        "renewal_date": "2027-05-20 (Prochain renouvellement)",
        "commercial_status": "Commercialisation en pleine expansion européenne",
        "packaging": "Boîte de 4 stylos préremplis jetables avec 4 aiguilles stériles",
        "storage_condition": "À conserver au réfrigérateur (2°C - 8°C). Ne pas congeler. Après première utilisation, stable 28 jours < 30°C.",
        "shelf_life_months": 24,
        "price_eur": "129.50 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 820000,
        "annual_sales_eur": "106 190 000 €",
        "lead_physician": "Dr. Sophie Maréchal",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Mme Camille Roussel"
    },
    {
        "prod_id": "PRD-009",
        "code": "ONCOV",
        "brand_name": "Oncovance",
        "inn_dci": "Zanitatinib citrate",
        "therapeutic_area": "Oncologie",
        "atc_code": "L01EB08",
        "indication": "Traitement de première ligne du cancer bronchique non à petites cellules (CBNPC) localement avancé ou métastatique avec mutations activatrices de l'EGFR (exon 19 del ou L858R).",
        "galenic_form": "Gélules orales (150 mg)",
        "dosage_regimen": "150 mg une fois par jour par voie orale, à jeun (au moins 1 heure avant ou 2 heures après un repas).",
        "contraindications": "Grossesse, pneumopathie interstitielle médicamenteuse active, insuffisance rénale terminale sous dialyse.",
        "common_adverse_events": "Éruption cutanée acnéiforme (48.0%), diarrhée (36.5%), paronychie (22.1%), sécheresse cutanée (19.4%), stomatite.",
        "serious_risks": "Pneumopathie interstitielle diffuse (PID fatale dans 1.2% des cas), allongement de l'intervalle QTc, perforation gastro-intestinale.",
        "regulatory_status": "Autorisé (AMM Centralisée - Médicament d'exception)",
        "ma_number": "EU/1/17/1190/001",
        "initial_ma_date": "2017-08-29",
        "renewal_date": "2022-09-01 (Illimitée)",
        "commercial_status": "Prescription hospitalière réservée aux oncologues dans toute l'UE",
        "packaging": "Boîte de 30 gélules sous plaquettes thermoformées aluminium renforcé",
        "storage_condition": "À conserver dans l'emballage d'origine à l'abri de l'humidité et à T < 25°C.",
        "shelf_life_months": 36,
        "price_eur": "2450.00 €",
        "reimbursement_rate": "100%",
        "annual_volume_packs": 32000,
        "annual_sales_eur": "78 400 000 €",
        "lead_physician": "Dr. Antoine Bertrand",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-010",
        "code": "LINFA",
        "brand_name": "Linfabloc",
        "inn_dci": "Tébricitinib",
        "therapeutic_area": "Oncologie / Hématologie",
        "atc_code": "L01EL04",
        "indication": "Traitement des adultes atteints de leucémie lymphoïde chronique (LLC) ou de lymphome à cellules du manteau (LCM) en rechute ou réfractaire.",
        "galenic_form": "Comprimé pelliculé (400 mg)",
        "dosage_regimen": "400 mg par jour en une prise unique orale continue jusqu'à progression de la maladie ou toxicité inacceptable.",
        "contraindications": "Hémorragie active majeure, association avec des anticoagulants oraux à dose curative sans surveillance hématologique étroite.",
        "common_adverse_events": "Neutropénie (28.4%), infections respiratoires hautes (21.0%), thrombocytopénie, arthralgies, contusions spontanées.",
        "serious_risks": "Hémorragie majeure cérébrale ou digestive, fibrillation auriculaire, neutropénie fébrile sévère, syndrome de lyse tumorale.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/21/1532/001",
        "initial_ma_date": "2021-02-14",
        "renewal_date": "2026-02-15 (En préparation)",
        "commercial_status": "Médicament de réserve hospitalière",
        "packaging": "Boîte de 30 comprimés pelliculés sous blister unitaire",
        "storage_condition": "Conserver à température ne dépassant pas 25°C.",
        "shelf_life_months": 36,
        "price_eur": "3850.00 €",
        "reimbursement_rate": "100%",
        "annual_volume_packs": 14500,
        "annual_sales_eur": "55 825 000 €",
        "lead_physician": "Dr. Antoine Bertrand",
        "ra_manager": "M. David Leroy",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-011",
        "code": "MELAN",
        "brand_name": "Mélanor",
        "inn_dci": "Encorafénil",
        "therapeutic_area": "Oncologie",
        "atc_code": "L01EC04",
        "indication": "Traitement du mélanome non résecable ou métastatique porteur de la mutation BRAF V600E ou V600K, en association avec un inhibiteur de MEK.",
        "galenic_form": "Gélule (75 mg)",
        "dosage_regimen": "450 mg (soit six gélules de 75 mg) une fois par jour par voie orale, au cours ou en dehors d'un repas.",
        "contraindications": "Mélanome sans mutation BRAF documentée, insuffisance cardiaque sévère, allaitement.",
        "common_adverse_events": "Fatigue (41.2%), arthralgie, éruption cutanée, alopécie réversible, nausées, vomissements.",
        "serious_risks": "Développement de nouveaux carcinomes épidermoïdes cutanés primaires, hémorragies sévères, allongement de l'intervalle QT.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/23/1705/001",
        "initial_ma_date": "2023-01-26",
        "renewal_date": "2028-01-26",
        "commercial_status": "Médicament innovant en phase de lancement européen",
        "packaging": "Boîte de 42 gélules sous plaquettes aluminium/PVDC",
        "storage_condition": "À conserver dans l'emballage extérieur d'origine à température < 30°C.",
        "shelf_life_months": 24,
        "price_eur": "2980.00 €",
        "reimbursement_rate": "100%",
        "annual_volume_packs": 9500,
        "annual_sales_eur": "28 310 000 €",
        "lead_physician": "Dr. Antoine Bertrand",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-012",
        "code": "IMMUN",
        "brand_name": "Immunolin",
        "inn_dci": "Secukirumab",
        "therapeutic_area": "Immunologie",
        "atc_code": "L04AC16",
        "indication": "Psoriasis en plaques modéré à sévère chez l'adulte éligible à un traitement systémique ; Rhumatisme psoriasique actif.",
        "galenic_form": "Solution injectable en seringue préremplie avec protège-aiguille (150 mg / 1.0 mL)",
        "dosage_regimen": "300 mg en injection sous-cutanée (2 injections de 150 mg) aux semaines 0, 1, 2, 3 et 4, puis dose d'entretien mensuelle.",
        "contraindications": "Infections actives graves (tuberculose évolutive, sepsis fongique, herpès disséminé), hypersensibilité au latex du capuchon de seringue.",
        "common_adverse_events": "Rhinopharyngite (12.3%), candidose cutanéo-muqueuse (4.5%), céphalées, prurit au site d'injection.",
        "serious_risks": "Exacerbation sévère de maladie inflammatoire chronique de l'intestin (Crohn/RCH), choc anaphylactique systémique.",
        "regulatory_status": "Autorisé (AMM Centralisée - Biomédicament)",
        "ma_number": "EU/1/19/1402/001",
        "initial_ma_date": "2019-11-20",
        "renewal_date": "2024-11-22 (Renouvelé)",
        "commercial_status": "Commercialisé dans 15 pays européens",
        "packaging": "Boîte de 2 seringues préremplies sécurisées (système automatique de retrait d'aiguille)",
        "storage_condition": "Conserver au réfrigérateur (entre 2°C et 8°C). Ne pas congeler. Conserver dans l'emballage à l'abri de la lumière.",
        "shelf_life_months": 24,
        "price_eur": "745.00 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 85000,
        "annual_sales_eur": "63 325 000 €",
        "lead_physician": "Dr. Antoine Bertrand",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Mme Camille Roussel"
    },
    {
        "prod_id": "PRD-013",
        "code": "COLIT",
        "brand_name": "Colitane",
        "inn_dci": "Ozanimod chlorhydrate",
        "therapeutic_area": "Gastro-entérologie / Immunologie",
        "atc_code": "L04AA38",
        "indication": "Traitement de la rectocolite hémorragique (RCH) active modérée à sévère chez les patients adultes en cas de réponse insuffisante ou d'intolérance aux biothérapies conventionnelles.",
        "galenic_form": "Gélule (0.92 mg)",
        "dosage_regimen": "Schéma d'escalade posologique sur 7 jours (0.23 mg J1-J4, 0.46 mg J5-J7) puis dose d'entretien de 0.92 mg une fois par jour.",
        "contraindications": "Infarctus du myocarde, angor instable ou AVC au cours des 6 derniers mois ; BAV 2e ou 3e degré sans stimulateur cardiaque ; insuffisance hépatique sévère.",
        "common_adverse_events": "Nasopharyngite, élévation asymptomatique des ALAT/ASAT (6.5%), céphalées, bradycardie transitoire à l'initiation.",
        "serious_risks": "Leuconeurodystrophie multifocale progressive (LEMP), œdème maculaire rétinien, réactivation du virus varicelle-zona (VZV).",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/21/1580/001",
        "initial_ma_date": "2021-11-18",
        "renewal_date": "2026-11-20 (En cours de suivi)",
        "commercial_status": "Prescription initiale hospitalière annuelle réservée aux gastro-entérologues",
        "packaging": "Plaquette thermoformée de 28 gélules (et kit d'initiation 7 gélules)",
        "storage_condition": "À conserver à une température ne dépassant pas 25°C.",
        "shelf_life_months": 36,
        "price_eur": "920.00 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 48000,
        "annual_sales_eur": "44 160 000 €",
        "lead_physician": "Dr. Antoine Bertrand",
        "ra_manager": "Mme Sophie Bernard",
        "pv_officer": "Dr. Karim Belkacem"
    },
    {
        "prod_id": "PRD-014",
        "code": "RESPI",
        "brand_name": "Respispray",
        "inn_dci": "Fluticasone furoate / Vilantérol trifénatate / Uméclidinium bromure",
        "therapeutic_area": "Pneumologie / Respiratoire",
        "atc_code": "R03AL08",
        "indication": "Traitement continu de fond de l'asthme persistant sévère non contrôlé par une bithérapie CSI/LABA, et traitement d'entretien de la BPCO sévère avec antécédents d'exacerbations.",
        "galenic_form": "Poudre pour inhalation en récipient unidose (inhalateur multidose à poudre sèche - DPI) 92 µg / 22 µg / 55 µg",
        "dosage_regimen": "1 inhalation une fois par jour, à heure fixe (matin ou soir). Rinçage de bouche à l'eau sans avaler après inhalation.",
        "contraindications": "Hypersensibilité sévère aux protéines du lait (lactose monohydraté excipient), traitement d'urgence de la crise d'asthme aiguë.",
        "common_adverse_events": "Candidose oropharyngée (muguet 5.8%), dysphonie (enrouement 4.2%), céphalées, toux d'irritation.",
        "serious_risks": "Pneumonie chez les patients atteints de BPCO, bronchospasme paradoxal immédiat, glaucome à angle fermé.",
        "regulatory_status": "Autorisé (AMM Centralisée)",
        "ma_number": "EU/1/20/1478/001",
        "initial_ma_date": "2020-07-23",
        "renewal_date": "2025-07-25 (Dossier préparé)",
        "commercial_status": "Commercialisé dans 16 pays d'Europe",
        "packaging": "Inhalateur pré-chargé de 30 doses avec compteur mécanique dégressif",
        "storage_condition": "Conserver à température < 30°C dans l'emballage en barquette scellée jusqu'à première utilisation (conservation 6 semaines après ouverture).",
        "shelf_life_months": 24,
        "price_eur": "52.40 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 1420000,
        "annual_sales_eur": "74 408 000 €",
        "lead_physician": "Dr. Hélène Fournier",
        "ra_manager": "M. Julien Tavernier",
        "pv_officer": "Mme Camille Roussel"
    },
    {
        "prod_id": "PRD-015",
        "code": "BRONC",
        "brand_name": "Bronchoclar",
        "inn_dci": "Roflumilast micronisé",
        "therapeutic_area": "Pneumologie / Respiratoire",
        "atc_code": "R03DX07",
        "indication": "Traitement d'entretien de la bronchopneumopathie chronique obstructive (BPCO) sévère associée à une bronchite chronique chez l'adulte avec exacerbations fréquentes, en complément des bronchodilatateurs.",
        "galenic_form": "Comprimé pelliculé (500 µg)",
        "dosage_regimen": "1 comprimé de 500 µg une fois par jour avec un verre d'eau, débuté éventuellement par une dose d'initiation à 250 µg pendant 28 jours.",
        "contraindications": "Insuffisance hépatique modérée à sévère (Child-Pugh B ou C), antécédents d'épisodes dépressifs sévères avec comportement suicidaire.",
        "common_adverse_events": "Perte de poids involontaire (8.2%), diarrhée motrice transitoire (7.5%), diminution de l'appétit, insomnie.",
        "serious_risks": "Idées et comportements suicidaires, amaigrissement morbide, troubles psychiatriques sévères.",
        "regulatory_status": "Autorisé (Procédure Reconnaissance Mutuelle FR/H/0890/001)",
        "ma_number": "FR/H/0890/001",
        "initial_ma_date": "2021-04-12",
        "renewal_date": "2026-04-15 (En cours)",
        "commercial_status": "Commercialisé en France, Allemagne, Espagne, Belgique",
        "packaging": "Boîte de 30 et 90 comprimés sous blister PVC/Alu",
        "storage_condition": "Pas de précautions particulières de conservation.",
        "shelf_life_months": 36,
        "price_eur": "38.90 €",
        "reimbursement_rate": "65%",
        "annual_volume_packs": 540000,
        "annual_sales_eur": "21 006 000 €",
        "lead_physician": "Dr. Hélène Fournier",
        "ra_manager": "Mme Sophie Bernard",
        "pv_officer": "Dr. Karim Belkacem"
    }
]

# Export CSVs for core entities
def export_core_csvs():
    # 1. produits.csv
    prod_path = os.path.join(CSV_DIR, "produits.csv")
    with open(prod_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "prod_id", "code", "brand_name", "inn_dci", "therapeutic_area", "atc_code",
            "indication", "galenic_form", "dosage_regimen", "contraindications",
            "common_adverse_events", "serious_risks", "regulatory_status", "ma_number",
            "initial_ma_date", "renewal_date", "commercial_status", "packaging",
            "storage_condition", "shelf_life_months", "price_eur", "reimbursement_rate",
            "annual_volume_packs", "annual_sales_eur", "lead_physician", "ra_manager", "pv_officer"
        ])
        writer.writeheader()
        for p in PRODUCTS:
            writer.writerow(p)

    # 2. collaborateurs.csv
    collab_path = os.path.join(CSV_DIR, "collaborateurs.csv")
    with open(collab_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "emp_id", "name", "title", "dept", "email", "phone", "location", "manager_id"
        ])
        writer.writeheader()
        for c in PERSONNEL:
            writer.writerow(c)

    print(f"Exported produits.csv ({len(PRODUCTS)} records) and collaborateurs.csv ({len(PERSONNEL)} records)")

if __name__ == "__main__":
    export_core_csvs()
