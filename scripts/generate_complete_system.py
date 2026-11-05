import os
import sys
import csv
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PHARMANOVA_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_DIR = os.path.join(PHARMANOVA_ROOT, "CSV_Data")
CORP_DIR = os.path.join(PHARMANOVA_ROOT, "Corporate")
QA_DIR = os.path.join(PHARMANOVA_ROOT, "Quality")
PV_DIR = os.path.join(PHARMANOVA_ROOT, "Pharmacovigilance")
MED_DIR = os.path.join(PHARMANOVA_ROOT, "Medical_Information")
REG_DIR = os.path.join(PHARMANOVA_ROOT, "Regulatory_Affairs")
TRN_DIR = os.path.join(PHARMANOVA_ROOT, "Training")
KB_DIR = os.path.join(PHARMANOVA_ROOT, "Knowledge_Base_Index")

sys.path.append(SCRIPT_DIR)

from data_models import PRODUCTS, PERSONNEL, COMPANY_INFO
from glossary_data import GLOSSARY_154
from pdf_helper import create_pharma_doc, get_pharma_styles, build_approval_block, build_metadata_box
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
from reportlab.lib import colors

styles = get_pharma_styles()

author_qa = [p for p in PERSONNEL if p["emp_id"] == "EMP-008"][0]
reviewer_qa = [p for p in PERSONNEL if p["emp_id"] == "EMP-006"][0]
approver_pr = [p for p in PERSONNEL if p["emp_id"] == "EMP-004"][0]

author_pv = [p for p in PERSONNEL if p["emp_id"] == "EMP-005"][0]
reviewer_pv = [p for p in PERSONNEL if p["emp_id"] == "EMP-018"][0]
approver_cmo = [p for p in PERSONNEL if p["emp_id"] == "EMP-002"][0]

author_med = [p for p in PERSONNEL if p["emp_id"] == "EMP-010"][0]
approver_ceo = [p for p in PERSONNEL if p["emp_id"] == "EMP-001"][0]

# ==============================================================================
# 1. GENERATE AUTHENTIC GLOSSARY CSV & MULTI-PAGE PDF
# ==============================================================================
def build_glossary():
    print("Building Glossary (CSV + multi-page PDF with 154 authentic terms)...")
    csv_path = os.path.join(CSV_DIR, "glossaire_pharmaceutique.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["terme", "definition"])
        writer.writeheader()
        for t, d in GLOSSARY_154:
            writer.writerow({"terme": t, "definition": d})

    pdf_path = os.path.join(CORP_DIR, "GLOSSAIRE_PHARMACEUTIQUE_REGLEMENTAIRE_GXP.pdf")
    doc, custom_canvas = create_pharma_doc(pdf_path, doc_ref="CORP-GLO-2024", doc_title="Glossaire Pharmaceutique GxP")
    story = [
        Paragraph("RÉFÉRENTIEL TERMINOLOGIQUE ET VOCABULAIRE RÉGLEMENTAIRE GxP", styles['PharmaDocSubtitle']),
        Paragraph("<b>GLOSSAIRE PHARMACEUTIQUE, RÉGLEMENTAIRE & GxP PHARMANOVA (154 TERMES)</b>", styles['PharmaDocTitle']),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10),
        Paragraph("Ce dictionnaire terminologique officiel répertorie et explicite les 154 termes, acronymes et concepts fondamentaux régissant les activités d'assurance qualité, de pharmacovigilance, d'affaires réglementaires et de production de PharmaNova SA, conformément aux référentiels EMA, ANSM, ICH, EudraLex et FDA.", styles['PharmaBody']),
        Spacer(1, 8)
    ]
    t_data = [[
        Paragraph("<b>Terme / Acronyme</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Définition & Référence Réglementaire</b>", styles['PharmaTableHeader'])
    ]]
    for t, d in GLOSSARY_154:
        t_data.append([
            Paragraph(f"<b>{t}</b>", styles['PharmaTableCell']),
            Paragraph(d, styles['PharmaTableCell'])
        ])
    t_glo = Table(t_data, colWidths=[130, 395], repeatRows=1)
    t_glo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2942")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_glo)
    story.append(Spacer(1, 14))
    story.append(build_approval_block(styles, approver_pr, approver_cmo, approver_ceo, "CORP-GLO-2024", "15/01/2024"))
    doc.build(story, canvasmaker=custom_canvas)
    print("Glossary built successfully.")

# ==============================================================================
# 2. GENERATE FULL MULTI-PAGE ANNUAIRE COLLABORATEURS PDF (120 EMPLOYEES)
# ==============================================================================
def build_annuaire_pdf():
    print("Building Annuaire Collaborateurs PDF (all 120 employees)...")
    pdf_path = os.path.join(CORP_DIR, "ANNUAIRE_COLLABORATEURS_PHARMANOVA.pdf")
    doc, custom_canvas = create_pharma_doc(pdf_path, doc_ref="CORP-DIR-2024", doc_title="Annuaire Général du Personnel")
    story = [
        Paragraph("DIRECTION DES RESSOURCES HUMAINES ET DU LEADERSHIP", styles['PharmaDocSubtitle']),
        Paragraph("<b>ANNUAIRE OFFICIEL DU PERSONNEL PHARMANOVA SA (120 COLLABORATEURS CLÉS)</b>", styles['PharmaDocTitle']),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10),
        Paragraph("Cet annuaire répertorie l'intégralité des 120 collaborateurs nominatifs, responsables de directions, cadres scientifiques, pharmaciens délégués, ingénieurs qualité et experts opérationnels de PharmaNova SA sur les sites de Lyon, Chalon-sur-Saône, Marburg et Saint-Quentin-Fallavier.", styles['PharmaBody']),
        Spacer(1, 8)
    ]
    t_data = [[
        Paragraph("<b>Matricule</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Nom & Prénom</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Fonction / Titre</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Département</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Site</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Email</b>", styles['PharmaTableHeader'])
    ]]
    for emp in PERSONNEL:
        t_data.append([
            Paragraph(emp["emp_id"], styles['PharmaTableCell']),
            Paragraph(f"<b>{emp['name']}</b>", styles['PharmaTableCell']),
            Paragraph(emp["title"][:28], styles['PharmaTableCell']),
            Paragraph(emp["dept"][:20], styles['PharmaTableCell']),
            Paragraph(emp["location"], styles['PharmaTableCell']),
            Paragraph(emp["email"], styles['PharmaSmall'])
        ])
    t_dir = Table(t_data, colWidths=[55, 95, 130, 95, 65, 85], repeatRows=1)
    t_dir.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2942")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_dir)
    story.append(Spacer(1, 14))
    story.append(build_approval_block(styles, approver_pr, approver_cmo, approver_ceo, "CORP-DIR-2024", "15/01/2024"))
    doc.build(story, canvasmaker=custom_canvas)
    print("Annuaire PDF built successfully.")

# ==============================================================================
# 3. BUILD CORPORATE ORGANIGRAMME & PROCEDURES INTERNES CSV
# ==============================================================================
def build_corporate_csvs():
    print("Building organigramme.csv and procedures_internes.csv...")
    
    # organigramme.csv
    org_rows = [
        {"unit_id": "ORG-EXEC-01", "unit_name": "Directoire & Direction Générale", "parent_unit": "Conseil de Surveillance", "division": "Direction Générale", "head_name": "Dr. Jean-Marc Delacroix", "head_emp_id": "EMP-001", "head_title": "Président du Directoire & Directeur Général", "gxp_criticality": "Critique", "responsibilities": "Orientation stratégique globale, allocation des ressources et engagement qualité directoire."},
        {"unit_id": "ORG-MED-01", "unit_name": "Direction Médicale Globale", "parent_unit": "ORG-EXEC-01", "division": "Affaires Médicales", "head_name": "Dr. Éléonore Vance", "head_emp_id": "EMP-002", "head_title": "Directrice Médicale (CMO)", "gxp_criticality": "Critique", "responsibilities": "Gouvernance médicale, évaluation bénéfice/risque, essais cliniques et information médicale."},
        {"unit_id": "ORG-RA-01", "unit_name": "Direction des Affaires Réglementaires", "parent_unit": "ORG-EXEC-01", "division": "Affaires Réglementaires", "head_name": "Mme Christine Baudry", "head_emp_id": "EMP-003", "head_title": "Vice-Présidente Affaires Réglementaires", "gxp_criticality": "Critique", "responsibilities": "Stratégie de soumission eCTD, obtention et maintenance des AMM, conformité EudraLex."},
        {"unit_id": "ORG-QA-01", "unit_name": "Direction de l'Assurance Qualité & Pharmacien Responsable", "parent_unit": "ORG-EXEC-01", "division": "Qualité Pharmaceutique", "head_name": "M. François Mercier", "head_emp_id": "EMP-004", "head_title": "Pharmacien Responsable & VP Global Quality", "gxp_criticality": "Critique", "responsibilities": "Respect du Code de la Santé Publique, politique PQS ICH Q10, libération des lots et tutelle GxP."},
        {"unit_id": "ORG-PV-01", "unit_name": "Département de Pharmacovigilance & QPPV", "parent_unit": "ORG-MED-01", "division": "Pharmacovigilance", "head_name": "Dr. Marc-Antoine Leroy", "head_emp_id": "EMP-005", "head_title": "Qualified Person for Pharmacovigilance (QPPV)", "gxp_criticality": "Critique", "responsibilities": "Surveillance continue du profil de tolérance, gestion EudraVigilance, détection de signaux et PSMF."},
        {"unit_id": "ORG-QP-01", "unit_name": "Pôle Libération des Lots (Qualified Persons)", "parent_unit": "ORG-QA-01", "division": "Qualité Pharmaceutique", "head_name": "Mme Valérie Roche", "head_emp_id": "EMP-006", "head_title": "Pharmacien Délégué QP - Libération des Lots", "gxp_criticality": "Critique", "responsibilities": "Certification officielle des lots selon l'Annexe 16 BPF, gestion des dérogations et réclamations."},
        {"unit_id": "ORG-OPS-01", "unit_name": "Direction Industrielle & Sites de Fabrication", "parent_unit": "ORG-EXEC-01", "division": "Opérations Industrielles", "head_name": "M. Pierre-Yves Bernard", "head_emp_id": "EMP-007", "head_title": "Directeur des Opérations Industrielles", "gxp_criticality": "Critique", "responsibilities": "Pilotage des usines de Chalon-sur-Saône (formes sèches) et Marburg (biotechnologies)."},
        {"unit_id": "ORG-CAPA-01", "unit_name": "Service Déviations, CAPA & Systèmes Qualité", "parent_unit": "ORG-QA-01", "division": "Qualité Pharmaceutique", "head_name": "Mme Nathalie Benhamou", "head_emp_id": "EMP-008", "head_title": "Responsable Assurance Qualité Opérationnelle", "gxp_criticality": "Majeure", "responsibilities": "Investigation des écarts de fabrication, coordination des plans CAPA et Change Control."},
        {"unit_id": "ORG-AUD-01", "unit_name": "Département Audits Qualité & Conformité Fournisseurs", "parent_unit": "ORG-QA-01", "division": "Qualité Pharmaceutique", "head_name": "M. Thomas Vasseur", "head_emp_id": "EMP-009", "head_title": "Responsable des Audits Qualité & Fournisseurs", "gxp_criticality": "Majeure", "responsibilities": "Programme d'auto-inspections internes et audits sur site des sous-traitants/fournisseurs API."},
        {"unit_id": "ORG-MEDINFO-01", "unit_name": "Département Information Médicale & Scientifique", "parent_unit": "ORG-MED-01", "division": "Affaires Médicales", "head_name": "Dr. Claire Dupuis", "head_emp_id": "EMP-010", "head_title": "Responsable de l'Information Médicale", "gxp_criticality": "Majeure", "responsibilities": "Réponses documentées aux professionnels de santé, validation du matériel promotionnel."},
        {"unit_id": "ORG-SCM-01", "unit_name": "Direction Supply Chain & Distribution GDP", "parent_unit": "ORG-OPS-01", "division": "Supply Chain", "head_name": "M. Laurent Garnier", "head_emp_id": "EMP-011", "head_title": "Directeur Supply Chain & Logistique Globale", "gxp_criticality": "Majeure", "responsibilities": "Distribution sous température dirigée, respect des GDP, traçabilité sérialisation FMD."},
        {"unit_id": "ORG-QC-01", "unit_name": "Direction du Contrôle Qualité Analytique", "parent_unit": "ORG-QA-01", "division": "Qualité Pharmaceutique", "head_name": "Dr. Philippe Gauthier", "head_emp_id": "EMP-012", "head_title": "Directeur Contrôle Qualité & Laboratoires", "gxp_criticality": "Critique", "responsibilities": "Analyses physico-chimiques, microbiologiques, stabilités ICH et traitement des OOS/OOT."},
        {"unit_id": "ORG-BIO-01", "unit_name": "Direction du Site Biopharmaceutique de Marburg", "parent_unit": "ORG-OPS-01", "division": "Bioproduction", "head_name": "Dr. Klaus Reinhardt", "head_emp_id": "EMP-013", "head_title": "Geschäftsführer Standort Marburg Biologics", "gxp_criticality": "Critique", "responsibilities": "Fermentation en bioréacteurs, purification chromatographique et remplissage aseptique."},
        {"unit_id": "ORG-REG-EU-01", "unit_name": "Pôle Soumissions Européennes & Procédures Centralisées", "parent_unit": "ORG-RA-01", "division": "Affaires Réglementaires", "head_name": "M. Julien Tavernier", "head_emp_id": "EMP-014", "head_title": "Responsable Affaires Réglementaires Europe", "gxp_criticality": "Majeure", "responsibilities": "Interface directe EMA/CHMP, gestion des variations de Type IA, IB et II en format eCTD."},
        {"unit_id": "ORG-REG-FR-01", "unit_name": "Pôle Enregistrements Nationaux France & Procédures DCP", "parent_unit": "ORG-RA-01", "division": "Affaires Réglementaires", "head_name": "Mme Sophie Bernard", "head_emp_id": "EMP-015", "head_title": "Responsable Réglementaire France & DCP", "gxp_criticality": "Majeure", "responsibilities": "Interactions ANSM, renouvellements quinquennaux, mentions légales et notices patients."}
    ]
    with open(os.path.join(CSV_DIR, "organigramme.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "unit_id", "unit_name", "parent_unit", "division", "head_name",
            "head_emp_id", "head_title", "gxp_criticality", "responsibilities"
        ])
        writer.writeheader()
        for r in org_rows:
            writer.writerow(r)

    # procedures_internes.csv
    proc_rows = [
        {"policy_id": "POL-CORP-001", "title": "Manuel Qualité Pharmaceutique et Politique Générale GxP", "category": "Politique Qualité", "scope": "Groupe PharmaNova (Tous sites)", "document_owner": "M. François Mercier (Pharmacien Responsable)", "version": "8.0", "effective_date": "2024-01-01", "next_review_date": "2026-01-01", "status": "Effectif"},
        {"policy_id": "POL-CORP-002", "title": "Charte d'Intégrité des Données et Principes ALCOA+ en Environnement GxP", "category": "Intégrité des Données", "scope": "Tous départements opérationnels", "document_owner": "Mme Nathalie Benhamou", "version": "4.0", "effective_date": "2024-01-15", "next_review_date": "2025-01-15", "status": "Effectif"},
        {"policy_id": "POL-CORP-003", "title": "Code de Déontologie Pharmaceutique et Conformité Éthique", "category": "Conformité & Éthique", "scope": "Tous collaborateurs PharmaNova", "document_owner": "Dr. Jean-Marc Delacroix (CEO)", "version": "5.0", "effective_date": "2024-01-01", "next_review_date": "2027-01-01", "status": "Effectif"},
        {"policy_id": "POL-CORP-004", "title": "Politique Globale de Pharmacovigilance et Continuité du Signalement 24/7", "category": "Pharmacovigilance", "scope": "Direction Médicale & PV", "document_owner": "Dr. Marc-Antoine Leroy (QPPV)", "version": "6.0", "effective_date": "2024-02-01", "next_review_date": "2025-02-01", "status": "Effectif"},
        {"policy_id": "POL-CORP-005", "title": "Procédure d'Alerte Sanitaire Rapide et Retrait de Marché (Recall)", "category": "Sécurité Sanitaire", "scope": "Direction Générale & QP", "document_owner": "M. François Mercier (Pharmacien Responsable)", "version": "7.0", "effective_date": "2024-01-10", "next_review_date": "2025-01-10", "status": "Effectif"},
        {"policy_id": "POL-CORP-006", "title": "Politique de Validation des Systèmes Informatisés (CSV) selon GAMP 5", "category": "Informatique GxP", "scope": "Systèmes informatisés GxP", "document_owner": "M. Thomas Vasseur", "version": "4.1", "effective_date": "2024-03-01", "next_review_date": "2026-03-01", "status": "Effectif"},
        {"policy_id": "POL-CORP-007", "title": "Plan Directeur de Formation Continue et Habilitations GxP du Personnel", "category": "Ressources Humaines", "scope": "Ensemble du personnel", "document_owner": "Mme Nathalie Benhamou", "version": "5.0", "effective_date": "2024-01-05", "next_review_date": "2025-01-05", "status": "Effectif"},
        {"policy_id": "POL-CORP-008", "title": "Politique de Maîtrise des Risques Qualité (QRM) selon ICH Q9(R1)", "category": "Assurance Qualité", "scope": "Développement, Production & QC", "document_owner": "M. François Mercier", "version": "3.0", "effective_date": "2024-02-15", "next_review_date": "2026-02-15", "status": "Effectif"},
        {"policy_id": "POL-CORP-009", "title": "Plan de Continuité d'Activité et Gestion des Crises d'Approvisionnement", "category": "Supply Chain", "scope": "Production & Distribution", "document_owner": "M. Laurent Garnier", "version": "3.2", "effective_date": "2024-01-20", "next_review_date": "2025-01-20", "status": "Effectif"},
        {"policy_id": "POL-CORP-010", "title": "Charte de Transparence et Relations avec les Professionnels de Santé", "category": "Affaires Médicales", "scope": "Information Médicale & Ventes", "document_owner": "Dr. Éléonore Vance (CMO)", "version": "4.0", "effective_date": "2024-01-15", "next_review_date": "2026-01-15", "status": "Effectif"}
    ]
    with open(os.path.join(CSV_DIR, "procedures_internes.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "policy_id", "title", "category", "scope", "document_owner",
            "version", "effective_date", "next_review_date", "status"
        ])
        writer.writeheader()
        for r in proc_rows:
            writer.writerow(r)
    print("Corporate CSVs built successfully.")

# ==============================================================================
# 4. FIX QUALITÉ RELATIONAL LOGIC (DEVIATIONS, CAPAs, AUDITS, INVESTIGATIONS)
# ==============================================================================
def build_quality_data_and_pdfs():
    print("Rebuilding Quality CSVs and PDFs with airtight relational mapping...")
    
    # 30 Deviations
    # Critical: DEV-2024-005, 012, 022 (3)
    # Major: DEV-2024-002, 004, 006, 008, 010, 014, 016, 018, 020, 024, 026 (11)
    # Minor: remaining 16 deviations -> NO mandatory CAPA (empty/non-requis)
    
    critical_indices = [5, 12, 22]
    major_indices = [2, 4, 6, 8, 10, 14, 16, 18, 20, 24, 26]
    
    # Map each deviation requiring CAPA to a unique CAPA-2024-001 to CAPA-2024-014
    capa_map = {}
    capa_counter = 1
    for i in sorted(critical_indices + major_indices):
        capa_map[i] = f"CAPA-2024-{capa_counter:03d}"
        capa_counter += 1
    
    deviations_data = []
    for i in range(1, 31):
        dev_id = f"DEV-2024-{i:03d}"
        prod = PRODUCTS[(i - 1) % len(PRODUCTS)]
        
        if i in critical_indices:
            crit = "Critique"
        elif i in major_indices:
            crit = "Majeure"
        else:
            crit = "Mineure"
            
        batch = f"LOT-{prod['code']}-240{10 + i}"
        capa_ref = capa_map.get(i, "NON_REQUIS")
        
        desc = (
            f"Écart critique constaté lors du procédé de fabrication de {prod['brand_name']} : contamination particulaire ou rupture de stérilité."
            if crit == "Critique" else
            (f"Écart majeur survenu en production de {prod['brand_name']} : excursion thermique prolongée ou dérive de paramètre critique CPP."
             if crit == "Majeure" else
             f"Écart mineur constaté lors du conditionnement de {prod['brand_name']} : défaut mineur d'étiquetage ou bourrage machine ponctuel.")
        )
        status = "Clôturée" if i < 26 else "Sous investigation QA"
        
        # Re-render DEVIATION PDF with aligned metadata
        dev_file = os.path.join(QA_DIR, f"DEVIATION_{dev_id}.pdf")
        doc, custom_canvas = create_pharma_doc(dev_file, doc_ref=f"QA-DEV-{dev_id}", doc_title=f"Rapport de Déviation {dev_id}")
        story = [
            Paragraph(f"RAPPORT DE DÉVIATION QUALITÉ GxP ({crit.upper()})", styles['PharmaDocSubtitle']),
            Paragraph(f"<b>DÉVIATION {dev_id} - {prod['brand_name'].upper()}</b>", styles['PharmaDocTitle']),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10)
        ]
        meta = [
            ("Réf Déviation", dev_id),
            ("Criticité", crit),
            ("Produit Affecté", prod["brand_name"]),
            ("Numéro de Lot", batch),
            ("Date de Constat", f"2024-{(i%9)+1:02d}-14"),
            ("Statut Déviation", status),
            ("Réf CAPA liée", capa_ref),
            ("Décision QP", "Lot Conforme après analyse" if crit != "Critique" else "Rejet partiel / Lot quarantaine")
        ]
        story.append(build_metadata_box(styles, meta))
        story.append(Spacer(1, 12))
        story.append(Paragraph("1. DESCRIPTION FACTUELLE DE L'ÉVÉNEMENT", styles['PharmaH1']))
        story.append(Paragraph(desc, styles['PharmaBody']))
        story.append(Paragraph("<b>Mesures conservatoires immédiates :</b> Mise en quarantaine informatique et physique immédiate du lot sous scellés QA. Arrêt de la ligne et notification au Responsable Assurance Qualité Opérationnelle.", styles['PharmaBody']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("2. ANALYSE DES CAUSES RACINES (5 POURQUOI & ISHIKAWA)", styles['PharmaH1']))
        story.append(Paragraph("L'investigation technique a identifié l'origine de l'anomalie. Aucune contamination microbiologique ni impact sur la stérilité ou la teneur du produit fini n'ont été relevés sur les prélèvements représentatifs.", styles['PharmaBody']))
        story.append(Spacer(1, 14))
        story.append(build_approval_block(styles, author_qa, reviewer_qa, approver_pr, dev_id, f"2024-{(i%9)+1:02d}-14"))
        doc.build(story, canvasmaker=custom_canvas)

        deviations_data.append({
            "deviation_id": dev_id,
            "product_name": prod["brand_name"],
            "batch_number": batch,
            "classification": crit,
            "occurrence_date": f"2024-{(i%9)+1:02d}-14",
            "department": "Production Chalon" if i % 2 == 0 else "Laboratoire QC",
            "status": status,
            "capa_reference": capa_ref,
            "summary": desc
        })

    # Export deviations.csv
    with open(os.path.join(CSV_DIR, "deviations.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "deviation_id", "product_name", "batch_number", "classification",
            "occurrence_date", "department", "status", "capa_reference", "summary"
        ])
        writer.writeheader()
        for d in deviations_data:
            writer.writerow(d)

    # 35 Audits
    # Internal: AUD-INT-2024-001 to 020
    # Supplier: AUD-SUP-2024-001 to 015
    # Audits triggering CAPAs 015 to 025:
    # AUD-INT-2024-004, 008, 012, 016, 020 (5)
    # AUD-SUP-2024-002, 004, 007, 009, 011, 014 (6)
    
    capa_audit_map = {
        "AUD-INT-2024-004": "CAPA-2024-015",
        "AUD-INT-2024-008": "CAPA-2024-016",
        "AUD-INT-2024-012": "CAPA-2024-017",
        "AUD-INT-2024-016": "CAPA-2024-018",
        "AUD-INT-2024-020": "CAPA-2024-019",
        "AUD-SUP-2024-002": "CAPA-2024-020",
        "AUD-SUP-2024-004": "CAPA-2024-021",
        "AUD-SUP-2024-007": "CAPA-2024-022",
        "AUD-SUP-2024-009": "CAPA-2024-023",
        "AUD-SUP-2024-011": "CAPA-2024-024",
        "AUD-SUP-2024-014": "CAPA-2024-025",
    }
    
    # Build 25 CAPAs
    capa_data = []
    # CAPAs 001 to 014 from Deviations
    for dev_idx in sorted(critical_indices + major_indices):
        c_id = capa_map[dev_idx]
        d_id = f"DEV-2024-{dev_idx:03d}"
        dev_item = [d for d in deviations_data if d["deviation_id"] == d_id][0]
        
        capa_data.append({
            "capa_id": c_id,
            "origin_type": "DEVIATION",
            "origin_id": d_id,
            "origin_source": f"Déviation {d_id} ({dev_item['classification']} - {dev_item['product_name']})",
            "responsible_lead": "Mme Nathalie Benhamou",
            "opening_date": dev_item["occurrence_date"],
            "target_due_date": f"2024-{(int(dev_item['occurrence_date'].split('-')[1]) + 2):02d}-28",
            "status": "Clôturée avec VoE satisfaisante" if int(c_id.split("-")[-1]) <= 10 else "En cours de vérification d'efficacité (VoE)",
            "description": f"Plan CAPA visant à éradiquer la cause racine identifiée lors de l'investigation de {d_id} ({dev_item['product_name']})."
        })

    # CAPAs 015 to 025 from Audits
    for aud_id, c_id in sorted(capa_audit_map.items(), key=lambda x: x[1]):
        is_int = "INT" in aud_id
        o_type = "AUDIT_INTERNE" if is_int else "AUDIT_FOURNISSEUR"
        num = int(aud_id.split("-")[-1])
        aud_date = f"2024-{(num%8)+2:02d}-10"
        
        capa_data.append({
            "capa_id": c_id,
            "origin_type": o_type,
            "origin_id": aud_id,
            "origin_source": f"Audit {o_type.replace('_', ' ').title()} {aud_id}",
            "responsible_lead": "Mme Nathalie Benhamou",
            "opening_date": aud_date,
            "target_due_date": f"2024-{(int(aud_date.split('-')[1]) + 2):02d}-28",
            "status": "Clôturée avec VoE satisfaisante" if int(c_id.split("-")[-1]) <= 20 else "En cours de vérification d'efficacité (VoE)",
            "description": f"Plan d'actions correctives et préventives issu des constats majeurs relevés lors de l'audit {aud_id}."
        })

    # Re-render 25 CAPA PDFs with aligned metadata
    for c in capa_data:
        capa_id = c["capa_id"]
        capa_file = os.path.join(QA_DIR, f"CAPA_{capa_id}.pdf")
        doc, custom_canvas = create_pharma_doc(capa_file, doc_ref=f"QA-CAPA-{capa_id}", doc_title=f"Plan CAPA {capa_id}")
        story = [
            Paragraph("SYSTÈME CORRECTIF ET PRÉVENTIF GxP (ICH Q10)", styles['PharmaDocSubtitle']),
            Paragraph(f"<b>FICHE D'ACTION CAPA {capa_id}</b>", styles['PharmaDocTitle']),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10)
        ]
        meta = [
            ("Réf CAPA", capa_id),
            ("Source d'Origine", c["origin_source"]),
            ("Responsable CAPA", c["responsible_lead"]),
            ("Date d'Ouverture", c["opening_date"]),
            ("Échéance de Réalisation", c["target_due_date"]),
            ("Statut CAPA", c["status"]),
            ("VoE (Efficacité)", "Contrôlée à 90 jours sans récurrence"),
            ("Validation QA", "Approuvée par le Pharmacien Responsable (M. François Mercier)")
        ]
        story.append(build_metadata_box(styles, meta))
        story.append(Spacer(1, 12))
        story.append(Paragraph("1. PLAN D'ACTIONS CORRECTIVES ET PRÉVENTIVES", styles['PharmaH1']))
        story.append(Paragraph("<b>Action Corrective Immédiate (AC) :</b> Révision immédiate des paramètres de consigne et remplacement préventif des pièces d'usure incriminées.<br/><b>Action Préventive Structurelle (AP) :</b> Mise à jour de la SOP correspondante, recalibration complète des capteurs critiques et formation obligatoire de 100% des opérateurs de zone avant remise en service.", styles['PharmaBody']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("2. VÉRIFICATION DE L'EFFICACITÉ (VERIFICATION OF EFFECTIVENESS - VoE)", styles['PharmaH1']))
        story.append(Paragraph("Un suivi renforcé sur une durée de 3 mois et sur 10 lots consécutifs a confirmé une stabilité parfaite des procédés sans réapparition de l'écart. L'efficacité de la CAPA est validée formellement par l'Assurance Qualité.", styles['PharmaBody']))
        story.append(Spacer(1, 14))
        story.append(build_approval_block(styles, author_qa, reviewer_qa, approver_pr, capa_id, c["opening_date"]))
        doc.build(story, canvasmaker=custom_canvas)

    # Export capa.csv
    with open(os.path.join(CSV_DIR, "capa.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "capa_id", "origin_type", "origin_id", "origin_source",
            "responsible_lead", "opening_date", "target_due_date", "status", "description"
        ])
        writer.writeheader()
        for c in capa_data:
            writer.writerow(c)

    # 20 Investigations Qualité OOS/OOT
    inv_data = []
    for i in range(1, 21):
        inv_id = f"INV-2024-{i:03d}"
        prod = PRODUCTS[(i - 1) % len(PRODUCTS)]
        batch = f"LOT-{prod['code']}-240{30 + i}"
        test_type = "Teneur HPLC hors spécifications (OOS)" if i % 2 == 0 else "Vitesse de dissolution in vitro ralentie (OOT)"
        capa_trig = capa_map.get(i if i in capa_map else None, "NON_REQUIS")
        
        inv_data.append({
            "investigation_id": inv_id,
            "product_name": prod["brand_name"],
            "batch_number": batch,
            "type_of_outlier": test_type,
            "phase_1_lab_result": "Erreur analytique de dilution en laboratoire confirmée" if i % 2 == 0 else "Aucune erreur de laboratoire décelée",
            "phase_2_manufacturing_result": "Sans objet (cause laboratoire)" if i % 2 == 0 else "Variation thermique au séchoir lit d'air fluidisé identifiée",
            "root_cause_category": "Laboratoire QC" if i % 2 == 0 else "Procédé de Fabrication",
            "capa_triggered": capa_trig,
            "final_disposition": "Lot Conforme libéré après ré-analyse conforme" if i % 2 == 0 else "Lot mis en quarantaine / Retraitement autorisé",
            "lead_investigator": "Dr. Philippe Gauthier",
            "closed_date": f"2024-{(i%8)+1:02d}-25"
        })

    with open(os.path.join(CSV_DIR, "investigations_qualite.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "investigation_id", "product_name", "batch_number", "type_of_outlier",
            "phase_1_lab_result", "phase_2_manufacturing_result", "root_cause_category",
            "capa_triggered", "final_disposition", "lead_investigator", "closed_date"
        ])
        writer.writeheader()
        for iv in inv_data:
            writer.writerow(iv)

    print("Quality CSVs successfully aligned.")

# ==============================================================================
# 5. BUILD REGULATORY CSVs (AMM, CTD, CHECKLISTS)
# ==============================================================================
def build_regulatory_csvs():
    print("Building Regulatory Affairs CSVs (checklists, fiches AMM, dossiers CTD)...")
    
    # 1. checklists_reglementaires.csv (10 Checklists)
    chk_topics = [
        ("CHK-REG-001", "Cardiolux", "Conformité eCTD v4.0 et Validation Technique du Dossier d'AMM", "Dossier eCTD", 45, 45, "100%", "Conforme"),
        ("CHK-REG-002", "Glucorite", "Audit de Lisibilité Notice Patient (User Consultation / Readability Testing)", "Notice Patient", 30, 29, "96.7%", "Conforme avec remarques mineures"),
        ("CHK-REG-003", "Immunolin", "Évaluation de Conformité de la Sunset Clause (Commercialisation UE)", "Maintien AMM", 20, 20, "100%", "Conforme"),
        ("CHK-REG-004", "Oncovance", "Vérification des Engagements Post-AMM et Études PASS / PAES", "Post-AMM", 25, 25, "100%", "Conforme"),
        ("CHK-REG-005", "Neurotix", "Validation Réglementaire du Plan d'Investigation Pédiatrique (PIP)", "Pédiatrie", 35, 33, "94.3%", "Conforme sous réserve d'avenant"),
        ("CHK-REG-006", "Respispray", "Conformité du Conditionnement et Traçabilité Sérialisation FMD", "Emballage & FMD", 40, 40, "100%", "Conforme"),
        ("CHK-REG-007", "Vascopril", "Harmonisation Européenne du Résumé des Caractéristiques du Produit (SmPC)", "Information Produit", 50, 49, "98.0%", "Conforme"),
        ("CHK-REG-008", "Insulip", "Conformité du Dispositif Médical Associé (Règlement MDR 2017/745)", "Dispositif Médical", 35, 35, "100%", "Conforme"),
        ("CHK-REG-009", "Tremopan", "Audit de Renouvellement Quinquennal et Analyse Bénéfice/Risque", "Renouvellement", 40, 40, "100%", "Conforme"),
        ("CHK-REG-010", "Cognifère", "Conformité du Plan de Gestion des Risques (RMP Module V)", "Pharmacovigilance", 30, 30, "100%", "Conforme")
    ]
    with open(os.path.join(CSV_DIR, "checklists_reglementaires.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "checklist_id", "product_name", "topic", "regulatory_scope",
            "items_checked", "compliant_items", "compliance_rate", "status"
        ])
        writer.writeheader()
        for chk in chk_topics:
            writer.writerow({
                "checklist_id": chk[0], "product_name": chk[1], "topic": chk[2],
                "regulatory_scope": chk[3], "items_checked": chk[4], "compliant_items": chk[5],
                "compliance_rate": chk[6], "status": chk[7]
            })

    # 2. fiches_amm.csv (12 AMMs)
    amm_list = [
        {"amm_id": "AMM-CARDIOLUX", "product_name": "Cardiolux", "inn_dci": "Ziltorvastatine / Amlodipine bésylate", "ma_number": "EU/1/20/1482/001-004", "eu_number": "EMEA/H/C/004821", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 10 ter Directive 2001/83 (Association fixe)", "competent_authority": "EMA", "grant_date": "2020-04-15", "renewal_date": "2025-04-15", "prescription_status": "Liste I (Prescription médicale obligatoire)", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-VASCOPRIL", "product_name": "Vascopril", "inn_dci": "Candésartan cilexétil / Indapamide", "ma_number": "FR/H/2019/0421/001", "eu_number": "FR/H/0421/001", "procedure_type": "Procédure Décentralisée (DCP)", "legal_basis": "Article 10 ter Directive 2001/83", "competent_authority": "ANSM", "grant_date": "2019-06-20", "renewal_date": "Illimitée", "prescription_status": "Liste I", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-CORANID", "product_name": "Coranid", "inn_dci": "Ivabradine chlorhydrate / Métoprolol succinate", "ma_number": "FR/H/2018/0112/001", "eu_number": "FR/H/0112/001", "procedure_type": "Procédure Décentralisée (DCP)", "legal_basis": "Article 10 ter Directive 2001/83", "competent_authority": "ANSM", "grant_date": "2018-09-12", "renewal_date": "Illimitée", "prescription_status": "Liste I", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-NEUROTIX", "product_name": "Neurotix", "inn_dci": "Brivastérol", "ma_number": "EU/1/21/1590/001-003", "eu_number": "EMEA/H/C/005112", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83 (Dossier complet)", "competent_authority": "EMA", "grant_date": "2021-02-18", "renewal_date": "2026-02-18", "prescription_status": "Liste I - Surveillance particulière", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-COGNIFERE", "product_name": "Cognifère", "inn_dci": "Donepézil chlorhydrate / Mémantine chlorhydrate", "ma_number": "DE/H/2104/001/DC", "eu_number": "DE/H/2104/001", "procedure_type": "Procédure Décentralisée (DCP)", "legal_basis": "Article 10 ter Directive 2001/83", "competent_authority": "BfArM / ANSM", "grant_date": "2020-01-10", "renewal_date": "2025-01-10", "prescription_status": "Liste I - Prescription réservée aux neurologues et gériatres", "reimbursement_rate": "Non remboursé (SMR insuffisant)"},
        {"amm_id": "AMM-TREMOPAN", "product_name": "Tremopan", "inn_dci": "Safinamide mésylate / Lévodopa retard", "ma_number": "EU/1/19/1375/001", "eu_number": "EMEA/H/C/004390", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 10 ter Directive 2001/83", "competent_authority": "EMA", "grant_date": "2019-11-22", "renewal_date": "Illimitée", "prescription_status": "Liste I", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-GLUCORITE", "product_name": "Glucorite", "inn_dci": "Dagliflozine / Sitagliptine phosphate", "ma_number": "EU/1/21/1602/001-002", "eu_number": "EMEA/H/C/005230", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 10 ter Directive 2001/83", "competent_authority": "EMA", "grant_date": "2021-07-14", "renewal_date": "2026-07-14", "prescription_status": "Liste I", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-INSULIP", "product_name": "Insulip", "inn_dci": "Églifénotide", "ma_number": "EU/1/22/1688/001", "eu_number": "EMEA/H/C/005741", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83 (Dossier complet)", "competent_authority": "EMA", "grant_date": "2022-10-05", "renewal_date": "2027-10-05", "prescription_status": "Liste I - Médicament d'exception", "reimbursement_rate": "65%"},
        {"amm_id": "AMM-ONCOVANCE", "product_name": "Oncovance", "inn_dci": "Zanitatinib citrate", "ma_number": "EU/1/22/1650/001", "eu_number": "EMEA/H/C/005510", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83 (Désignation orpheline)", "competent_authority": "EMA", "grant_date": "2022-05-19", "renewal_date": "2027-05-19", "prescription_status": "Liste I - Prescription hospitalière réservée aux oncologues", "reimbursement_rate": "100%"},
        {"amm_id": "AMM-LINFABLOC", "product_name": "Linfabloc", "inn_dci": "Tébricitinib", "ma_number": "EU/1/23/1720/001", "eu_number": "EMEA/H/C/005882", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83", "competent_authority": "EMA", "grant_date": "2023-03-30", "renewal_date": "2028-03-30", "prescription_status": "Liste I - Prescription hospitalière spécialisée", "reimbursement_rate": "100%"},
        {"amm_id": "AMM-MELANOR", "product_name": "Mélanor", "inn_dci": "Encorafénil", "ma_number": "EU/1/23/1745/001", "eu_number": "EMEA/H/C/005934", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83", "competent_authority": "EMA", "grant_date": "2023-08-16", "renewal_date": "2028-08-16", "prescription_status": "Liste I - Prescription restreinte oncologie/dermatologie", "reimbursement_rate": "100%"},
        {"amm_id": "AMM-IMMUNOLIN", "product_name": "Immunolin", "inn_dci": "Secukirumab", "ma_number": "EU/1/19/1401/001-002", "eu_number": "EMEA/H/C/004618", "procedure_type": "Procédure Centralisée (CP)", "legal_basis": "Article 8.3 Directive 2001/83 (Biomédicament)", "competent_authority": "EMA", "grant_date": "2019-12-08", "renewal_date": "Illimitée", "prescription_status": "Liste I - Médicament à prescription initiale hospitalière", "reimbursement_rate": "65%"}
    ]
    with open(os.path.join(CSV_DIR, "fiches_amm.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "amm_id", "product_name", "inn_dci", "ma_number", "eu_number",
            "procedure_type", "legal_basis", "competent_authority",
            "grant_date", "renewal_date", "prescription_status", "reimbursement_rate"
        ])
        writer.writeheader()
        for a in amm_list:
            writer.writerow(a)

    # 3. dossiers_produits_ctd.csv (15 Products)
    ctd_list = []
    for p in PRODUCTS:
        ctd_list.append({
            "ctd_id": f"CTD-{p['code']}",
            "product_name": p["brand_name"],
            "inn_dci": p["inn_dci"],
            "therapeutic_area": p["therapeutic_area"],
            "galenic_form": p["galenic_form"],
            "module_1_admin": "Conforme (Formulaires administratifs, RCP, Étiquetage, PIL)",
            "module_2_qso": "Conforme (Quality Overall Summary 2.3, Nonclinical/Clinical Overviews 2.4-2.5)",
            "module_3_quality": f"Conforme (3.2.S Substance Active, 3.2.P Produit Fini - {p['storage_condition']})",
            "module_4_nonclinical": "Conforme (Pharmacologie de sécurité, Pharmacocinétique, Toxicologie BPL)",
            "module_5_clinical": "Conforme (Essais cliniques pivots Phase I-III BPC ICH E6)",
            "lead_ra_manager": p["ra_manager"],
            "overall_status": "Approuvé et Maintenu eCTD v4.0"
        })
    with open(os.path.join(CSV_DIR, "dossiers_produits_ctd.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ctd_id", "product_name", "inn_dci", "therapeutic_area", "galenic_form",
            "module_1_admin", "module_2_qso", "module_3_quality", "module_4_nonclinical",
            "module_5_clinical", "lead_ra_manager", "overall_status"
        ])
        writer.writeheader()
        for c in ctd_list:
            writer.writerow(c)
            
    print("Regulatory CSVs built successfully.")

# ==============================================================================
# 6. BUILD PHARMACOVIGILANCE CSVs & COMPLETE MULTI-PAGE ICSR PDF (150 CAS)
# ==============================================================================
def build_pv_data_and_pdfs():
    print("Building Pharmacovigilance CSVs (signaux, évaluations, PSUR, suivis) and full ICSR Registry PDF...")
    
    # Load 150 ICSRs
    icsr_path = os.path.join(CSV_DIR, "adverse_events.csv")
    with open(icsr_path, encoding="utf-8") as f:
        icsr_records = list(csv.DictReader(f))

    # Re-render REGISTRE_GLOBAL_ICSR_PHARMACOVIGILANCE.pdf with ALL 150 ICSRs
    reg_pdf = os.path.join(PV_DIR, "REGISTRE_GLOBAL_ICSR_PHARMACOVIGILANCE.pdf")
    doc, custom_canvas = create_pharma_doc(reg_pdf, doc_ref="REG-PV-ICSR-2024", doc_title="Registre Annuel Pharmacovigilance ICSR")
    story = [
        Paragraph("DIRECTION DE LA PHARMACOVIGILANCE GLOBALE - BASE SAFETY", styles['PharmaDocSubtitle']),
        Paragraph("<b>REGISTRE CONSOLIDÉ DES CAS INDIVIDUELS D'EFFETS INDÉSIRABLES (150 ICSR)</b>", styles['PharmaDocTitle']),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10),
        Paragraph("Conformément au Module VI des Bonnes Pratiques de Pharmacovigilance (GVP Module VI) et aux standards ICH E2B(R3), ce registre récapitule l'intégralité des 150 notifications individuelles de cas de sécurité enregistrées, évaluées et transmises sur la passerelle européenne EudraVigilance au cours de l'exercice 2024.", styles['PharmaBody']),
        Spacer(1, 8)
    ]
    t_data = [[
        Paragraph("<b>ID Cas</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Produit</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Patient</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Événement (MedDRA PT)</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Gravité</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Causalité</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Issue</b>", styles['PharmaTableHeader'])
    ]]
    for r in icsr_records:
        t_data.append([
            Paragraph(r["case_id"], styles['PharmaTableCell']),
            Paragraph(f"<b>{r['suspect_drug']}</b>", styles['PharmaTableCell']),
            Paragraph(f"{r['patient_age']} a / {r['patient_gender']}", styles['PharmaTableCell']),
            Paragraph(r["adverse_event_pt"][:28], styles['PharmaTableCell']),
            Paragraph(r["seriousness"][:18], styles['PharmaTableCell']),
            Paragraph(r["causality"], styles['PharmaTableCell']),
            Paragraph(r["outcome"], styles['PharmaTableCell'])
        ])
    t_icsr = Table(t_data, colWidths=[95, 65, 55, 135, 75, 50, 50], repeatRows=1)
    t_icsr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2942")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_icsr)
    story.append(Spacer(1, 14))
    story.append(build_approval_block(styles, author_pv, reviewer_pv, approver_cmo, "REG-PV-ICSR-2024", "31/12/2024"))
    doc.build(story, canvasmaker=custom_canvas)
    print("Master ICSR PDF rebuilt with 150 cases.")

    # 1. signaux_securite.csv (30 Signals)
    sig_rows = []
    signals_def = [
        ("Cardiolux", "Rhabdomyolyse aiguë en association aux fibrates", "Troubles musculo-squelettiques", "Disproportion PRR EVDAS", "PRR=3.85 [2.4-5.9]", "Validé PRAC", "Ajout contre-indication RCP Section 4.3"),
        ("Glucorite", "Acidocétose euglycémique lors d'interventions chirurgicales", "Troubles du métabolisme", "Algorithme ROR Safety Database", "ROR=4.12 [2.8-6.1]", "Validé PRAC", "DHPC envoyée aux chirurgiens et anesthésistes"),
        ("Oncovance", "Pneumopathie interstitielle diffuse toxique", "Affections respiratoires", "Signal PRAC européen", "PRR=5.20 [3.1-8.7]", "Sous surveillance renforcée", "Suivi mensuel et exploration scanner obligatoire"),
        ("Immunolin", "Réactivation virale d'hépatite B occulte", "Infections et infestations", "Notification spontanée E2B", "ROR=2.90 [1.7-4.8]", "Validé PRAC", "Dépistage sérologique obligatoire pré-thérapeutique"),
        ("Respispray", "Bronchospasme paradoxal immédiat post-inhalation", "Affections respiratoires", "Surveillance disproportion ROR", "ROR=3.15 [1.9-5.1]", "Clôturé", "Information d'emploi renforcée dans la notice"),
        ("Cognifère", "Bradycardie syncopale chez le sujet âgé polymédiqué", "Affections cardiaques", "Analyse disproportion PRR", "PRR=2.70 [1.5-4.2]", "Validé PRAC", "ECG de contrôle annuel recommandé au RCP")
    ]
    for i in range(1, 31):
        sig_id = f"SIG-2024-{i:03d}"
        s_item = signals_def[(i - 1) % len(signals_def)]
        sig_rows.append({
            "signal_id": sig_id,
            "product_name": s_item[0],
            "inn_dci": [p["inn_dci"] for p in PRODUCTS if p["brand_name"] == s_item[0]][0],
            "meddra_pt": s_item[1],
            "meddra_soc": s_item[2],
            "detection_method": s_item[3],
            "disproportion_metric": s_item[4],
            "detection_date": f"2024-{(i%10)+1:02d}-08",
            "validation_date": f"2024-{(i%10)+1:02d}-22",
            "assigned_physician": "Dr. Marc-Antoine Leroy (QPPV)",
            "status": s_item[5],
            "regulatory_action": s_item[6]
        })
    with open(os.path.join(CSV_DIR, "signaux_securite.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "signal_id", "product_name", "inn_dci", "meddra_pt", "meddra_soc",
            "detection_method", "disproportion_metric", "detection_date",
            "validation_date", "assigned_physician", "status", "regulatory_action"
        ])
        writer.writeheader()
        for s in sig_rows:
            writer.writerow(s)

    # 2. evaluations_securite.csv (20 Evaluations)
    eval_rows = []
    for i in range(1, 21):
        eval_id = f"EVAL-2024-{i:03d}"
        s_ref = f"SIG-2024-{i:03d}"
        s_item = sig_rows[i - 1]
        eval_rows.append({
            "eval_id": eval_id,
            "product_name": s_item["product_name"],
            "inn_dci": s_item["inn_dci"],
            "signal_reference": s_ref,
            "topic": f"Évaluation clinique du lien causal entre {s_item['product_name']} et {s_item['meddra_pt']}",
            "data_sources": "Base Safety PharmaNova, EudraVigilance, Registre d'essais pivots, Littérature PubMed",
            "lead_evaluator": "Dr. Éléonore Vance (CMO) / Dr. Marc-Antoine Leroy (QPPV)",
            "completion_date": f"2024-{(i%9)+2:02d}-15",
            "benefit_risk_impact": "Rapport Bénéfice/Risque favorable maintenu sous réserve de mesures de minimisation",
            "recommended_actions": s_item["regulatory_action"],
            "smpc_update_required": "OUI (Sections 4.3, 4.4 ou 4.8)" if i % 2 == 0 else "NON (Maintien surveillance de routine)"
        })
    with open(os.path.join(CSV_DIR, "evaluations_securite.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "eval_id", "product_name", "inn_dci", "signal_reference", "topic",
            "data_sources", "lead_evaluator", "completion_date",
            "benefit_risk_impact", "recommended_actions", "smpc_update_required"
        ])
        writer.writeheader()
        for ev in eval_rows:
            writer.writerow(ev)

    # 3. rapports_periodiques_psur.csv (10 PSUR/PBRER)
    psur_prods = ["Cardiolux", "Vascopril", "Coranid", "Neurotix", "Cognifère", "Tremopan", "Glucorite", "Insulip", "Oncovance", "Linfabloc"]
    psur_rows = []
    for i, p_name in enumerate(psur_prods, start=1):
        p_obj = [p for p in PRODUCTS if p["brand_name"] == p_name][0]
        psur_rows.append({
            "psur_id": f"PSUR-2024-{i:03d}",
            "product_name": p_name,
            "inn_dci": p_obj["inn_dci"],
            "dlp_date": f"2024-{(i%6)+6:02d}-30",
            "submission_deadline": f"2024-{(i%6)+7:02d}-30",
            "reporting_interval": "1 an (Période post-autorisation triennale)",
            "cumulative_exposure_patients": f"{p_obj['annual_volume_packs'] * 3:,} patients-années".replace(",", " "),
            "interval_icsr_count": 10 + i * 2,
            "benefit_risk_conclusion": "Rapport Bénéfice/Risque hautement favorable confirmé. Aucune modification majeure du profil de sécurité.",
            "qppv_sign_off_date": f"2024-{(i%6)+7:02d}-20",
            "status": "Transmis au Répertoire Européen des PSUR (EMA)"
        })
    with open(os.path.join(CSV_DIR, "rapports_periodiques_psur.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "psur_id", "product_name", "inn_dci", "dlp_date", "submission_deadline",
            "reporting_interval", "cumulative_exposure_patients", "interval_icsr_count",
            "benefit_risk_conclusion", "qppv_sign_off_date", "status"
        ])
        writer.writeheader()
        for ps in psur_rows:
            writer.writerow(ps)

    # 4. rapports_suivi_icsr.csv (20 Follow-up reports linked to serious cases)
    fu_rows = []
    serious_cases = [r for r in icsr_records if "Grave" in r["seriousness"]][:20]
    for i, sc in enumerate(serious_cases, start=1):
        fu_id = f"FU-2024-{i:03d}"
        fu_rows.append({
            "followup_id": fu_id,
            "icsr_case_id": sc["case_id"],
            "product_name": sc["suspect_drug"],
            "followup_number": 1 if i <= 15 else 2,
            "receipt_date": f"2024-{(i%8)+3:02d}-12",
            "reporting_source": sc["reporter_type"],
            "new_clinical_information": f"Obtention du compte-rendu d'hospitalisation complet et bilans biologiques confirmant l'évolution favorable sous traitement symptomatique.",
            "final_outcome": sc["outcome"],
            "reassessed_causality": sc["causality"],
            "pv_officer": "Dr. Marc-Antoine Leroy (QPPV)"
        })
    with open(os.path.join(CSV_DIR, "rapports_suivi_icsr.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "followup_id", "icsr_case_id", "product_name", "followup_number",
            "receipt_date", "reporting_source", "new_clinical_information",
            "final_outcome", "reassessed_causality", "pv_officer"
        ])
        writer.writeheader()
        for fu in fu_rows:
            writer.writerow(fu)

    print("Pharmacovigilance suite complete.")

# ==============================================================================
# 7. BUILD INFORMATION MÉDICALE CSVs & REBUILD 200 Q&A & 50 FAQ PDFs
# ==============================================================================
def build_medinfo_data_and_pdfs():
    print("Rebuilding Medical Information CSVs and PDFs (200 Q&A full PDF + 50 distinct Expert FAQs)...")
    
    # Load 200 Q&As
    med_faq_csv = os.path.join(CSV_DIR, "medical_faq.csv")
    with open(med_faq_csv, encoding="utf-8") as f:
        med_faq_records = list(csv.DictReader(f))

    # Re-render RECUEIL_OFFICIEL_200_REPONSES_INFORMATION_MEDICALE.pdf with ALL 200 Q&As
    master_pdf = os.path.join(MED_DIR, "RECUEIL_OFFICIEL_200_REPONSES_INFORMATION_MEDICALE.pdf")
    doc, custom_canvas = create_pharma_doc(master_pdf, doc_ref="MED-INFO-200-QA", doc_title="Recueil Officiel Information Médicale")
    story = [
        Paragraph("DIRECTION DES AFFAIRES MÉDICALES - INFORMATION MÉDICALE SCIENTIFIQUE", styles['PharmaDocSubtitle']),
        Paragraph("<b>RECUEIL OFFICIEL DE 200 QUESTIONS / RÉPONSES MÉDICALES DE RÉFÉRENCE</b>", styles['PharmaDocTitle']),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10),
        Paragraph("Ce document officiel rassemble l'intégralité des 200 questions et réponses standardisées et scientifiquement validées destinées aux professionnels de santé (médecins spécialistes, pharmaciens hospitaliers et d'officine) pour le bon usage et la sécurité des 15 médicaments du portefeuille PharmaNova SA.", styles['PharmaBody']),
        Spacer(1, 8)
    ]
    t_data = [[
        Paragraph("<b>ID / Spécialité</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Demandeur</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Question Médicale</b>", styles['PharmaTableHeader']),
        Paragraph("<b>Réponse Scientifique Fondée sur les Preuves</b>", styles['PharmaTableHeader'])
    ]]
    for r in med_faq_records:
        t_data.append([
            Paragraph(f"<b>{r['faq_id']}</b><br/>{r['product_name']}", styles['PharmaTableCell']),
            Paragraph(r["requester_profile"][:22], styles['PharmaTableCell']),
            Paragraph(r["question"], styles['PharmaTableCell']),
            Paragraph(r["evidence_based_answer"], styles['PharmaTableCell'])
        ])
    t_qa = Table(t_data, colWidths=[80, 75, 175, 195], repeatRows=1)
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2942")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_qa)
    story.append(Spacer(1, 14))
    story.append(build_approval_block(styles, author_med, approver_cmo, approver_ceo, "MED-INFO-200-QA", "15/03/2024"))
    doc.build(story, canvasmaker=custom_canvas)
    print("Master 200 Q&A PDF successfully rebuilt with all 200 Q&As.")

    # 50 DISTINCT Scientific Expert FAQs
    faq_domains = [
        "Pharmacocinétique & Métabolisme CYP450",
        "Insuffisance Rénale & Adaptation Posologique",
        "Insuffisance Hépatique & Liaison Protéique",
        "Switch Thérapeutique & Modalités de Relai",
        "Interactions Médicamenteuses Spécifiques",
        "Populations Spéciales : Sujets Âgés & Fragilité",
        "Tolérance Cardiovasculaire & Allongement Intervalle QT",
        "Pharmacogénétique & Variabilité de Réponse",
        "Administration Entérale & Écrasement Galénique",
        "Grossesse, Allaitement & Données Registres"
    ]
    
    faq_records_50 = []
    for i in range(1, 51):
        faq_id = f"FAQ-EXP-{i:03d}"
        prod = PRODUCTS[(i - 1) % len(PRODUCTS)]
        domain = faq_domains[(i - 1) % len(faq_domains)]
        
        q_text = f"[{prod['brand_name']} - {domain}] Quelles sont les recommandations cliniques et données pharmacologiques relatives à {domain.lower()} pour {prod['brand_name']} ({prod['inn_dci']}) ?"
        
        ans_text = (
            f"Les données cliniques pivots et pharmacologiques de {prod['brand_name']} ({prod['inn_dci']}) démontrent : "
            f"1) Pour {domain.lower()}, le profil cinétique montre une biodisponibilité de {65 + (i%25)}% et une demi-vie d'élimination de {8 + (i%16)} heures. "
            f"2) Dans les essais pivots de Phase III, aucun ajustement de dose initial n'est requis sous réserve d'une clairance adaptée (> 30 mL/min). "
            f"3) La surveillance recommandée inclut un contrôle biologique régulier et une vigilance sur les inhibiteurs enzymatiques concomitants selon la section 4.5 du SmPC."
        )
        ref_text = f"SmPC {prod['brand_name']} (Section 4.2 & 5.2) ; Étude pivot PharmaNova PN-{prod['code']}-301 ; Directives EMA/CHMP 2024."
        
        faq_records_50.append({
            "faq_id": faq_id,
            "product_name": prod["brand_name"],
            "inn_dci": prod["inn_dci"],
            "domain": domain,
            "scientific_question": q_text,
            "evidence_based_response": ans_text,
            "primary_literature_source": ref_text,
            "review_date": "2024-04-01",
            "expert_reviewer": "Dr. Claire Dupuis (Head MedInfo) / Dr. Éléonore Vance (CMO)"
        })

    # Export faq_scientifiques.csv
    with open(os.path.join(CSV_DIR, "faq_scientifiques.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "faq_id", "product_name", "inn_dci", "domain",
            "scientific_question", "evidence_based_response",
            "primary_literature_source", "review_date", "expert_reviewer"
        ])
        writer.writeheader()
        for f50 in faq_records_50:
            writer.writerow(f50)

    # Re-render FAQ_SCIENTIFIQUES_EXPERTES_PHARMANOVA.pdf with ALL 50 FAQs
    faq_pdf = os.path.join(MED_DIR, "FAQ_SCIENTIFIQUES_EXPERTES_PHARMANOVA.pdf")
    doc, custom_canvas = create_pharma_doc(faq_pdf, doc_ref="MED-FAQ-EXP-50", doc_title="50 FAQ Scientifiques Expertes")
    story = [
        Paragraph("AFFAIRES MÉDICALES - EXPERTISE THÉRAPEUTIQUE APPROFONDIE", styles['PharmaDocSubtitle']),
        Paragraph("<b>RECUEIL DES 50 FAQ SCIENTIFIQUES EXPERTES DE HAUT NIVEAU</b>", styles['PharmaDocTitle']),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f2942"), spaceAfter=10),
        Paragraph("Ce corpus d'excellence aborde l'intégralité des 50 interrogations cliniques complexes, surspécialités, mécanismes pharmacocinétiques et conduites thérapeutiques pour les 15 spécialités du portefeuille PharmaNova SA.", styles['PharmaBody']),
        Spacer(1, 8)
    ]
    for item in faq_records_50:
        story.append(Paragraph(f"<b>{item['faq_id']} [{item['product_name']}] - {item['domain']}</b>", styles['PharmaH2']))
        story.append(Paragraph(f"<b>Question clinique d'expert :</b> {item['scientific_question']}", styles['PharmaBody']))
        story.append(Paragraph(f"<b>Réponse scientifique fondée sur les preuves :</b> {item['evidence_based_response']}", styles['PharmaBody']))
        story.append(Paragraph(f"<i>Source réglementaire : {item['primary_literature_source']}</i>", styles['PharmaSmall']))
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 14))
    story.append(build_approval_block(styles, author_med, approver_cmo, approver_ceo, "MED-FAQ-EXP-50", "01/04/2024"))
    doc.build(story, canvasmaker=custom_canvas)
    print("50 Expert FAQ PDF rebuilt successfully.")

    # 3. notes_medicales.csv (30 Notes)
    notes_rows = []
    for i in range(1, 31):
        n_id = f"MED-NOTE-2024-{i:03d}"
        prod = PRODUCTS[(i - 1) % len(PRODUCTS)]
        notes_rows.append({
            "note_id": n_id,
            "product_name": prod["brand_name"],
            "inn_dci": prod["inn_dci"],
            "title": f"Note Médicale {n_id} : Synthèse d'évaluation clinique et positionnement thérapeutique de {prod['brand_name']}",
            "target_specialty": prod["therapeutic_area"],
            "author": "Dr. Claire Dupuis (Head MedInfo)",
            "creation_date": f"2024-{(i%9)+1:02d}-18",
            "clinical_objective": f"Mise au point sur les données d'efficacité clinique et le profil de tolérance de {prod['brand_name']} dans sa population cible.",
            "key_takeaways": "Bénéfice clinique démontré avec réduction significative des événements indésirables d'intérêt vs comparateur historique."
        })
    with open(os.path.join(CSV_DIR, "notes_medicales.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "note_id", "product_name", "inn_dci", "title", "target_specialty",
            "author", "creation_date", "clinical_objective", "key_takeaways"
        ])
        writer.writeheader()
        for nr in notes_rows:
            writer.writerow(nr)

    # 4. syntheses_bibliographiques.csv (25 Literature Syntheses)
    bib_rows = []
    for i in range(1, 26):
        b_id = f"BIB-REV-2024-{i:03d}"
        prod = PRODUCTS[(i - 1) % len(PRODUCTS)]
        bib_rows.append({
            "biblio_id": b_id,
            "product_name": prod["brand_name"],
            "inn_dci": prod["inn_dci"],
            "search_scope": f"Revue systématique de la littérature internationale relative à {prod['inn_dci']} en vie réelle",
            "databases_searched": "PubMed, EMBASE, Cochrane Library, ClinicalTrials.gov",
            "date_range": "2018 - 2024",
            "articles_identified": 120 + i * 5,
            "articles_included": 14 + (i % 8),
            "lead_researcher": "Dr. Éléonore Vance (CMO) & Équipe Documentation Médicale",
            "clinical_conclusion": f"Confirmation de la consistance des données de tolérance et d'efficacité de {prod['brand_name']} en conditions réelles d'utilisation clinique."
        })
    with open(os.path.join(CSV_DIR, "syntheses_bibliographiques.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "biblio_id", "product_name", "inn_dci", "search_scope",
            "databases_searched", "date_range", "articles_identified",
            "articles_included", "lead_researcher", "clinical_conclusion"
        ])
        writer.writeheader()
        for br in bib_rows:
            writer.writerow(br)

    print("Medical Information suite complete.")

# ==============================================================================
# 8. BUILD TRAINING COMPETENCES MATRIX CSV
# ==============================================================================
def build_training_csvs():
    print("Building Training competences_matrix.csv...")
    matrix_rows = [
        {"matrix_id": "MAT-001", "department": "Assurance Qualité", "role_title": "Ingénieur Assurance Qualité / Auditeur", "required_modules": "MOD-TRN-001, MOD-TRN-002, MOD-TRN-004, MOD-TRN-005, MOD-TRN-008", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "Mme Nathalie Benhamou", "evaluation_method": "QCM en ligne (seuil 85%) + audit pratique"},
        {"matrix_id": "MAT-002", "department": "Contrôle Qualité", "role_title": "Technicien / Analyste QC", "required_modules": "MOD-TRN-001, MOD-TRN-002, MOD-TRN-004, MOD-TRN-005", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "Dr. Philippe Gauthier", "evaluation_method": "QCM théorique + qualification double aveugle"},
        {"matrix_id": "MAT-003", "department": "Production & Salles Blanches", "role_title": "Opérateur de Fabrication / Miragiste", "required_modules": "MOD-TRN-001, MOD-TRN-002, MOD-TRN-004, MOD-TRN-006", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "M. Pierre-Yves Bernard", "evaluation_method": "Habilitation d'habillage ZAC Grade A/B + test pratique"},
        {"matrix_id": "MAT-004", "department": "Supply Chain & Logistique", "role_title": "Gestionnaire Magasin / Transport GDP", "required_modules": "MOD-TRN-002, MOD-TRN-003, MOD-TRN-004, MOD-TRN-008", "retraining_frequency": "Annuelle", "target_compliance_rate": "98%", "responsible_trainer": "M. Laurent Garnier", "evaluation_method": "QCM en ligne + validation procédures transport froid"},
        {"matrix_id": "MAT-005", "department": "Pharmacovigilance", "role_title": "Spécialiste ICSR / Évaluateur Safety", "required_modules": "MOD-TRN-002, MOD-TRN-004, MOD-TRN-007", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "Dr. Marc-Antoine Leroy", "evaluation_method": "Cas test de saisie E2B + QCM GVP"},
        {"matrix_id": "MAT-006", "department": "Affaires Réglementaires", "role_title": "Chargé d'Affaires Réglementaires", "required_modules": "MOD-TRN-001, MOD-TRN-002, MOD-TRN-004, MOD-TRN-007", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "Mme Christine Baudry", "evaluation_method": "QCM eCTD + cas pratique de variation"},
        {"matrix_id": "MAT-007", "department": "Affaires Médicales (MSL)", "role_title": "Medical Science Liaison (MSL)", "required_modules": "MOD-TRN-002, MOD-TRN-004, MOD-TRN-007", "retraining_frequency": "Annuelle", "target_compliance_rate": "100%", "responsible_trainer": "Dr. Éléonore Vance", "evaluation_method": "Certification annuelle de connaissances scientifiques"},
        {"matrix_id": "MAT-008", "department": "Direction Générale & Fonctions Support", "role_title": "Tous Collaborateurs PharmaNova", "required_modules": "MOD-TRN-002", "retraining_frequency": "Annuelle obligatoire", "target_compliance_rate": "100%", "responsible_trainer": "Dr. Marc-Antoine Leroy", "evaluation_method": "Attestation individuelle de formation PV"}
    ]
    with open(os.path.join(CSV_DIR, "competences_matrix.csv"), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "matrix_id", "department", "role_title", "required_modules",
            "retraining_frequency", "target_compliance_rate", "responsible_trainer", "evaluation_method"
        ])
        writer.writeheader()
        for mr in matrix_rows:
            writer.writerow(mr)
    print("Training matrix CSV built successfully.")

# ==============================================================================
# 9. REBUILD MASTER_DOCUMENT_INDEX (CSV + MD) WITH 100% UNIQUE IDENTIFIERS
# ==============================================================================
def extract_unique_identifier(filename, rel_path):
    fn = filename.upper()
    base, ext = os.path.splitext(filename)
    
    # CSV files
    if ext.lower() == ".csv":
        return f"CSV-{base.upper().replace('_', '-')}"

    # Specific patterns
    # Quality
    if "DEVIATION_" in fn:
        m = re.search(r"DEV-2024-\d+", fn)
        if m: return m.group(0)
    if "CAPA_" in fn:
        m = re.search(r"CAPA-2024-\d+", fn)
        if m: return m.group(0)
    if "AUDIT_INTERNE_" in fn:
        m = re.search(r"AUD-INT-2024-\d+", fn)
        if m: return m.group(0)
    if "AUDIT_FOURNISSEUR_" in fn:
        m = re.search(r"AUD-SUP-2024-\d+", fn)
        if m: return m.group(0)
    if "INVESTIGATION_QUALITE_" in fn:
        m = re.search(r"INV-2024-\d+", fn)
        if m: return m.group(0)
    if "RECLAMATION_" in fn:
        m = re.search(r"PQC-2024-\d+", fn)
        if m: return m.group(0)
    if fn.startswith("SOP-"):
        m = re.search(r"SOP-[A-Z]+-\d+", fn)
        if m: return m.group(0)

    # Regulatory
    if "CHECKLIST_REGLEMENTAIRE_" in fn:
        m = re.search(r"CHK-REG-\d+", fn)
        if m: return m.group(0)
    if "FICHE_AMM_" in fn:
        prod = fn.replace("FICHE_AMM_", "").replace(".PDF", "")
        return f"AMM-{prod}"
    if "CTD_SYNTHESE_" in fn:
        prod = fn.replace("CTD_SYNTHESE_", "").replace(".PDF", "")
        return f"CTD-{prod}"
    if "FICHE_VARIATION_" in fn:
        m = re.search(r"VAR-2024-\d+", fn)
        if m: return m.group(0)
    if "PLAN_SOUMISSION_" in fn:
        m = re.search(r"SUB-PLN-\d+", fn)
        if m: return m.group(0)
    if "RAPPORT_RENOUVELLEMENT_" in fn:
        m = re.search(r"REN-REP-\d+", fn)
        if m: return m.group(0)

    # Pharmacovigilance
    if "SIGNAL_SECURITE_" in fn:
        m = re.search(r"SIG-2024-\d+", fn)
        if m: return m.group(0)
    if "EVALUATION_SECURITE_" in fn:
        m = re.search(r"EVAL-2024-\d+", fn)
        if m: return m.group(0)
    if "PSUR_PBRER_" in fn:
        prod = fn.replace("PSUR_PBRER_", "").replace("_2024.PDF", "").replace(".PDF", "")
        return f"PSUR-{prod}"
    if "SUIVI_CAS_" in fn:
        m = re.search(r"FU-2024-\d+", fn)
        if m: return m.group(0)
    if "REGISTRE_GLOBAL_ICSR" in fn:
        return "REG-PV-ICSR-2024"

    # Medical Info
    if "NOTE_MEDICALE_" in fn:
        m = re.search(r"MED-NOTE-2024-\d+", fn)
        if m: return m.group(0)
    if "SYNTHESE_BIBLIO_" in fn:
        m = re.search(r"BIB-REV-2024-\d+", fn)
        if m: return m.group(0)
    if "RECUEIL_OFFICIEL_200" in fn:
        return "MED-INFO-200-QA"
    if "FAQ_SCIENTIFIQUES_EXPERTES" in fn:
        return "MED-FAQ-EXP-50"

    # Training
    if "GUIDE_INTEGRATION_" in fn:
        m = re.search(r"ONB-\d+", fn)
        if m: return m.group(0)
    if "MODULE_FORMATION_" in fn:
        m = re.search(r"MOD-TRN-\d+", fn)
        if m: return m.group(0)
    if "MATRICE_COMPETENCES" in fn:
        return "TRN-MAT-2024"
    if "PROGRAMME_FORMATION_QUALITE" in fn:
        return "TRN-PRG-QA-2024"
    if "PROGRAMME_FORMATION_PHARMACOVIGILANCE" in fn:
        return "TRN-PRG-PV-2024"

    # Product Portfolio
    if "DOSSIER_PRODUIT_" in fn:
        prod = fn.replace("DOSSIER_PRODUIT_", "").replace(".PDF", "")
        return f"DOS-{prod}"

    # Corporate
    if "ANNUAIRE_COLLABORATEURS" in fn:
        return "DIR-001"
    if "CATALOGUE_MAITRE" in fn:
        return "CAT-001"
    if "GLOSSAIRE_PHARMACEUTIQUE" in fn:
        return "GLO-001"
    if "MANUEL_QUALITE" in fn:
        return "MQ-001"
    if "ORGANIGRAMME_ET_GOUVERNANCE" in fn:
        return "ORG-001"
    if "REFERENTIEL_DOCUMENTAIRE" in fn:
        return "REF-001"

    return base.replace("_", "-")

def rebuild_kb_index():
    print("Scanning entire PharmaNova tree to rebuild Master Knowledge Base Index...")
    all_files = []
    
    for root, dirs, files in os.walk(PHARMANOVA_ROOT):
        if "Knowledge_Base_Index" in root or "scripts" in root:
            continue
        for f in files:
            if f.startswith(".") or not (f.endswith(".pdf") or f.endswith(".csv")):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, PHARMANOVA_ROOT)
            parts = rel_path.split(os.sep)
            category = parts[0]
            ext = os.path.splitext(f)[1].upper().replace(".", "")
            size = os.path.getsize(full_path)
            
            ident = extract_unique_identifier(f, rel_path)
            title = os.path.splitext(f)[0].replace("_", " ")
            
            all_files.append({
                "identifier": ident,
                "title": title,
                "category": category,
                "file_format": ext,
                "size_bytes": size,
                "relative_path": rel_path,
                "absolute_path": full_path
            })

    all_files.sort(key=lambda x: (x["category"], x["identifier"]))
    print(f"Total files indexed: {len(all_files)}")
    
    # Check uniqueness of identifiers
    idents = [f["identifier"] for f in all_files]
    duplicates = [x for x in set(idents) if idents.count(x) > 1]
    if duplicates:
        print(f"WARNING: Found duplicate identifiers: {duplicates}")
    else:
        print("ALL IDENTIFIERS ARE 100% UNIQUE!")

    # Write MASTER_DOCUMENT_INDEX.csv
    master_csv = os.path.join(KB_DIR, "MASTER_DOCUMENT_INDEX.csv")
    with open(master_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "identifier", "title", "category", "file_format", "size_bytes", "relative_path", "absolute_path"
        ])
        writer.writeheader()
        for item in all_files:
            writer.writerow(item)

    # Write MASTER_DOCUMENT_INDEX.md
    master_md = os.path.join(KB_DIR, "MASTER_DOCUMENT_INDEX.md")
    with open(master_md, mode="w", encoding="utf-8") as f:
        f.write("# Master Document Index - PharmaNova SA\n\n")
        f.write(f"Ce registre officiel recense l'intégralité des **{len(all_files)} documents** du corpus de connaissances PharmaNova SA, optimisé pour l'ingestion dans Microsoft Copilot Studio et Azure AI Search.\n\n")
        f.write("## Synthèse par Division Documentaire\n\n")
        
        cat_counts = {}
        for item in all_files:
            cat_counts[item["category"]] = cat_counts.get(item["category"], 0) + 1
        
        f.write("| Division | Nombre de Documents | Format | Responsable Réglementaire |\n")
        f.write("| :--- | :---: | :---: | :--- |\n")
        f.write(f"| `Product_Portfolio` | {cat_counts.get('Product_Portfolio', 0)} | PDF | Directrice Médicale (Dr. Éléonore Vance) |\n")
        f.write(f"| `Regulatory_Affairs` | {cat_counts.get('Regulatory_Affairs', 0)} | PDF | VP Affaires Réglementaires (Mme Christine Baudry) |\n")
        f.write(f"| `Quality` | {cat_counts.get('Quality', 0)} | PDF | Pharmacien Responsable / VP QA (M. François Mercier) |\n")
        f.write(f"| `Pharmacovigilance` | {cat_counts.get('Pharmacovigilance', 0)} | PDF | QPPV (Dr. Marc-Antoine Leroy) |\n")
        f.write(f"| `Medical_Information` | {cat_counts.get('Medical_Information', 0)} | PDF | Responsable Info Médicale (Dr. Claire Dupuis) |\n")
        f.write(f"| `Training` | {cat_counts.get('Training', 0)} | PDF | Responsable Formation GxP (Mme Nathalie Benhamou) |\n")
        f.write(f"| `Corporate` | {cat_counts.get('Corporate', 0)} | PDF | Direction Générale & Secrétariat Général |\n")
        f.write(f"| `CSV_Data` | {cat_counts.get('CSV_Data', 0)} | CSV | Administrateur Base de Données GxP |\n\n")
        
        f.write("## Inventaire Détaillé des Fichiers\n\n")
        f.write("| Identifiant Unique | Intitulé du Document | Catégorie | Format | Taille (octets) | Chemin Relatif |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :--- |\n")
        for item in all_files:
            f.write(f"| `{item['identifier']}` | {item['title']} | `{item['category']}` | {item['file_format']} | {item['size_bytes']:,} | `{item['relative_path']}` |\n")

    print("Master Document Index rebuilt successfully.")

if __name__ == "__main__":
    build_glossary()
    build_annuaire_pdf()
    build_corporate_csvs()
    build_quality_data_and_pdfs()
    build_regulatory_csvs()
    build_pv_data_and_pdfs()
    build_medinfo_data_and_pdfs()
    build_training_csvs()
    rebuild_kb_index()
    print("ALL BUILD TASKS COMPLETED SUCCESSFULLY!")
