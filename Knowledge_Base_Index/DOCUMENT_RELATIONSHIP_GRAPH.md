# Cartographie Relationnelle et Graphe des Données - PharmaNova

Ce document formalise les interconnexions logiques et relationnelles entre l'ensemble des entités du corpus documentaire PharmaNova SA (432 fichiers PDF et 26 tables CSV relationnelles).

```
                            ┌─────────────────────────────────┐
                            │          PharmaNova SA          │
                            │ (Corporate Profile & Manuel MQ) │
                            └────────────────┬────────────────┘
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      ▼                                      ▼                                      ▼
┌──────────────────┐               ┌──────────────────┐                   ┌──────────────────┐
│  15 Médicaments  │◄──────────────┤ 120 Collaborateurs│                  │   40 SOPs GxP    │
│  (produits.csv)  │               │(collaborateurs.csv               │    (sop.csv)     │
└─────────┬────────┘               └────────┬─────────┘                   └────────┬─────────┘
          │                                 │                                      │
          ├────────────────────────┬────────┴───────────────┬──────────────────────┤
          ▼                        ▼                        ▼                      ▼
┌──────────────────┐      ┌──────────────────┐    ┌──────────────────┐   ┌──────────────────┐
│  30 Déviations   ├─────►│     25 CAPA      │◄───┤ 35 Audits Int/Sup│   │ 20 Investigations│
│ (deviations.csv) │      │    (capa.csv)    │    │   (audits.csv)   │   │  (investig.csv)  │
└─────────┬────────┘      └──────────────────┘    └──────────────────┘   └──────────────────┘
          │
          ├────────────────────────────────┬───────────────────────────────────────┐
          ▼                                ▼                                       ▼
┌──────────────────┐             ┌──────────────────┐                    ┌──────────────────┐
│ 30 Réclamations  │             │  40 Soumissions  │                    │ 12 Fiches AMM &  │
│(product_comp.csv)│             │(reg_submiss.csv) │                    │ 15 Dossiers CTD  │
└──────────────────┘             └────────┬─────────┘                    └──────────────────┘
                                          │
          ┌───────────────────────────────┴───────────────────────────────┐
          ▼                                                               ▼
┌──────────────────┐             ┌──────────────────┐                    ┌──────────────────┐
│    150 ICSRs     │────────────►│    30 Signaux    │───────────────────►│   10 Rapports    │
│(adverse_events)  │             │(signaux_securite)│                    │  PSUR / PBRER    │
└─────────┬────────┘             └────────┬─────────┘                    └──────────────────┘
          │                               │
          ▼                               ▼
┌──────────────────┐             ┌──────────────────┐
│    20 Suivis     │             │  20 Évaluations  │
│(rapports_suivi)  │             │  (eval_securite) │
└──────────────────┘             └──────────────────┘
```

## Référentiel des 26 Tables Structurées CSV (`PharmaNova/CSV_Data/`)

| Nom du Fichier CSV | Nb Lignes | Clé Primaire | Clés Étrangères Principales | Domaine Métier |
| :--- | :---: | :--- | :--- | :--- |
| `produits.csv` | 15 | `prod_id` | `ra_manager` -> `collaborateurs.emp_id` | Portefeuille Produits |
| `collaborateurs.csv` | 120 | `emp_id` | `manager_id` -> `collaborateurs.emp_id` | Ressources Humaines |
| `organigramme.csv` | 15 | `unit_id` | `head_emp_id` -> `collaborateurs.emp_id` | Gouvernance & Structure |
| `procedures_internes.csv` | 10 | `policy_id` | `document_owner` -> `collaborateurs.name` | Politiques & Chartes |
| `glossaire_pharmaceutique.csv` | 154 | `terme` | N/A | Dictionnaire GxP |
| `referentiel_documentaire.csv` | 8 | `doc_id` | `owner` -> `collaborateurs.name` | GED Niveau 1 |
| `sop.csv` | 40 | `sop_id` | `author` -> `collaborateurs.name` | Procédures Opératoires |
| `deviations.csv` | 30 | `deviation_id` | `product_name` -> `produits.brand_name`, `capa_reference` -> `capa.capa_id` | Assurance Qualité |
| `capa.csv` | 25 | `capa_id` | `origin_id` -> `deviations` ou `audits` | ICH Q10 CAPA |
| `audits.csv` | 35 | `audit_id` | `lead_auditor` -> `collaborateurs.name` | Auto-inspections & Fournisseurs |
| `product_complaints.csv` | 30 | `complaint_id` | `product_name` -> `produits.brand_name` | Réclamations Clients |
| `investigations_qualite.csv` | 20 | `investigation_id` | `product_name` -> `produits.brand_name`, `capa_triggered` -> `capa.capa_id` | OOS / OOT Labo & Procédé |
| `regulatory_submissions.csv` | 40 | `submission_id` | `product_name` -> `produits.brand_name` | Variations, Plans, Renouvellements |
| `checklists_reglementaires.csv` | 10 | `checklist_id` | `product_name` -> `produits.brand_name` | Conformité Réglementaire |
| `fiches_amm.csv` | 12 | `amm_id` | `product_name` -> `produits.brand_name` | Décisions Officielles d'AMM |
| `dossiers_produits_ctd.csv` | 15 | `ctd_id` | `product_name` -> `produits.brand_name` | Modules CTD 1 & 2 |
| `adverse_events.csv` | 150 | `case_id` | `suspect_drug` -> `produits.brand_name` | Base Safety E2B(R3) |
| `signaux_securite.csv` | 30 | `signal_id` | `product_name` -> `produits.brand_name` | Détection de Signaux PV |
| `evaluations_securite.csv` | 20 | `eval_id` | `signal_reference` -> `signaux_securite.signal_id` | Rapports Bénéfice/Risque |
| `rapports_periodiques_psur.csv` | 10 | `psur_id` | `product_name` -> `produits.brand_name` | Rapports PBRER / PSUR |
| `rapports_suivi_icsr.csv` | 20 | `followup_id` | `icsr_case_id` -> `adverse_events.case_id` | Suivi Clinique ICH E2B |
| `medical_faq.csv` | 200 | `faq_id` | `product_name` -> `produits.brand_name` | Information Médicale Officielle |
| `faq_scientifiques.csv` | 50 | `faq_id` | `product_name` -> `produits.brand_name` | FAQ Scientifiques Expertes |
| `notes_medicales.csv` | 30 | `note_id` | `product_name` -> `produits.brand_name` | Notes Médicales de Synthèse |
| `syntheses_bibliographiques.csv` | 25 | `biblio_id` | `product_name` -> `produits.brand_name` | Revues Systématiques |
| `training_catalog.csv` | 8 | `training_id` | N/A | Catalogue de Formations |
| `competences_matrix.csv` | 8 | `matrix_id` | `required_modules` -> `training_catalog.training_id` | Matrice des Compétences GxP |

## Règles de Correspondance des Clés Étrangères

| Entité Source | Clé Source | Entité Cible | Clé Cible | Type de Relation | Justification Métier & Règle d'Intégrité |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `deviations.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Tout incident de fabrication est rattaché à une spécialité pharmaceutique enregistrée. |
| `deviations.csv` | `capa_reference` | `capa.csv` | `capa_id` | 1 : 1 (ou vide) | Seules les déviations majeures ou critiques (14 cas) déclenchent une CAPA formelle obligatoire. |
| `capa.csv` | `origin_id` | `deviations.csv` | `deviation_id` | 1 : 1 | Les CAPAs 001 à 014 corrigent les déviations critiques/majeures de façon univoque. |
| `capa.csv` | `origin_id` | `audits.csv` | `audit_id` | 1 : 1 | Les CAPAs 015 à 025 traitent les constats majeurs relevés lors des audits internes ou fournisseurs. |
| `investigations_qualite.csv`| `capa_triggered` | `capa.csv` | `capa_id` | N : 1 | Les investigations concluant à une cause procédé raccordent le dossier au plan CAPA actif. |
| `adverse_events.csv` | `suspect_drug` | `produits.csv` | `brand_name` | N : 1 | Les cas de tolérance ICSR sont agrégés par médicament pour le calcul du PRR/ROR. |
| `rapports_suivi_icsr.csv` | `icsr_case_id` | `adverse_events.csv`| `case_id` | 1 : 1 | Tout rapport de suivi (Follow-up) documente l'évolution clinique d'un cas grave notifié. |
| `signaux_securite.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Les signaux de disproportion statistique émanent de la pharmacovigilance d'un produit. |
| `evaluations_securite.csv` | `signal_reference` | `signaux_securite.csv`| `signal_id`| 1 : 1 | Tout rapport d'évaluation de sécurité évalue formellement un signal validé par le PRAC. |
| `rapports_periodiques_psur.csv`| `product_name`| `produits.csv` | `brand_name` | 1 : 1 | Les rapports périodiques (ICH E2C) réévaluent le profil bénéfice/risque d'un produit sur 1 an. |
| `regulatory_submissions.csv`| `product_name` | `produits.csv` | `brand_name` | N : 1 | Les variations (Type IA, IB, II) et renouvellements modifient le dossier d'AMM du produit. |
| `fiches_amm.csv` | `product_name` | `produits.csv` | `brand_name` | 1 : 1 | Chaque décision d'AMM officielle correspond à une spécialité du catalogue commercial. |
| `dossiers_produits_ctd.csv` | `product_name` | `produits.csv` | `brand_name` | 1 : 1 | Le dossier de synthèse CTD compile les modules 1 à 5 de chaque médicament. |
| `product_complaints.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Les réclamations clients (PQC) sont rapprochées des dossiers de lots de la spécialité. |
| `medical_faq.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Les questions d'information médicale reposent sur le RCP et les essais pivots. |
| `faq_scientifiques.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Les 50 FAQ expertes répondent aux questions pharmacologiques et cliniques de pointe. |
| `notes_medicales.csv` | `product_name` | `produits.csv` | `brand_name` | N : 1 | Les notes médicales synthétisent les positionnements thérapeutiques des médicaments. |
| `syntheses_bibliographiques.csv`| `product_name`| `produits.csv`| `brand_name`| N : 1 | Les synthèses bibliographiques analysent la littérature PubMed/Cochrane du principe actif. |
| `organigramme.csv` | `head_emp_id` | `collaborateurs.csv`| `emp_id` | 1 : 1 | Les directeurs et responsables nommés sont tous identifiés dans l'annuaire général. |
| `competences_matrix.csv` | `required_modules` | `training_catalog.csv`| `training_id` | N : M | La matrice des compétences croise chaque fonction avec ses formations obligatoires GxP. |
