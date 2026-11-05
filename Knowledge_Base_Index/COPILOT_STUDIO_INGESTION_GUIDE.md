# Guide d'Ingestion et de Déploiement Microsoft Copilot Studio - PharmaNova

Ce guide opérationnel décrit pas-à-pas la méthode d'intégration du corpus documentaire **PharmaNova** dans **Microsoft Copilot Studio** pour concevoir un agent conversationnel expert en environnement pharmaceutique et formation professionnelle.

---

## 1. Préparation et Stratégie d'Indexation des Sources

L'architecture documentaire de PharmaNova a été conçue pour maximiser la précision des réponses génératives (Generative Answers) et éviter les hallucinations :

1. **Données Structurées (26 tables dans `PharmaNova/CSV_Data/`) :**
   - Importer les fichiers CSV dans Microsoft Dataverse ou directement comme tables de recherche via Power Platform Connectors (Azure SQL, SharePoint Lists ou Dataverse Virtual Tables).
   - Les CSV permettent des recherches déterministes exactes sur les numéros de lots, posologies, prix, numéros d'AMM, statuts CAPA et coordonnées des responsables :
     - **Produits & AMM :** `produits.csv`, `fiches_amm.csv`, `dossiers_produits_ctd.csv`, `regulatory_submissions.csv`, `checklists_reglementaires.csv`.
     - **Sécurité & PV :** `adverse_events.csv` (150 ICSRs), `signaux_securite.csv` (30 signaux), `evaluations_securite.csv` (20 rapports), `rapports_periodiques_psur.csv` (10 PSURs), `rapports_suivi_icsr.csv` (20 suivis).
     - **Qualité & GxP :** `sop.csv` (40 SOPs), `deviations.csv` (30 déviations), `capa.csv` (25 CAPAs), `audits.csv` (35 audits), `product_complaints.csv` (30 réclamations), `investigations_qualite.csv` (20 OOS/OOT).
     - **Médical :** `medical_faq.csv` (200 Q&A), `faq_scientifiques.csv` (50 FAQ), `notes_medicales.csv` (30 notes), `syntheses_bibliographiques.csv` (25 revues).
     - **Corporate & Formation :** `collaborateurs.csv` (120 profils), `organigramme.csv`, `procedures_internes.csv`, `glossaire_pharmaceutique.csv` (154 termes), `referentiel_documentaire.csv`, `training_catalog.csv`, `competences_matrix.csv`.

2. **Documents Textuels Non Structurés (432 fichiers dans les dossiers PDF) :**
   - Téléverser l'ensemble des répertoires PDF (`Regulatory_Affairs`, `Pharmacovigilance`, `Quality`, `Medical_Information`, `Training`, `Corporate`, `Product_Portfolio`) dans la section **Knowledge (Connaissances)** de Copilot Studio ou dans une bibliothèque SharePoint / Azure Blob connectée.
   - Activer la recherche sémantique Azure AI Search intégrée à Copilot Studio.

---

## 2. Configuration des Sujets (Topics) Recommandés

Configurer 6 Sujets personnalisés prioritaires dans Copilot Studio :

### Sujet 1 : `Recherche Produit & Données Réglementaires (AMM / RCP)`
- **Phrases de déclenchement :**
  - "Quelle est l'indication de Cardiolux ?"
  - "Quel est le numéro d'AMM de Linfabloc ?"
  - "Quelles sont les contre-indications de Respispray ?"
  - "Donne-moi la posologie d'Insulip."
  - "Quelles variations ont été déposées pour Glucorite en 2024 ?"
- **Nœud de réponse :**
  - Requête sur `produits.csv` + `fiches_amm.csv` + recherche générative dans `Product_Portfolio/` et `Regulatory_Affairs/`.

### Sujet 2 : `Procédure Qualité, Déviations & CAPA (GxP / ICH Q10)`
- **Phrases de déclenchement :**
  - "Comment déclarer une déviation de fabrication ?"
  - "Quelle est la procédure pour un résultat hors spécifications (OOS) ?"
  - "Quelles sont les étapes de la SOP-QA-002 ?"
  - "Quelle CAPA est associée à la déviation DEV-2024-002 ?"
  - "Qui est responsable de la libération des lots selon l'Annexe 16 ?"
- **Nœud de réponse :**
  - Requête sur `sop.csv`, `deviations.csv`, `capa.csv` + recherche générative dans `Quality/`.

### Sujet 3 : `Signalement et Sécurité de Pharmacovigilance (ICSR / Signaux / PSUR)`
- **Phrases de déclenchement :**
  - "Je souhaite déclarer un effet indésirable."
  - "Quels sont les signaux de sécurité identifiés pour Oncovance ?"
  - "Donne-moi les résultats du PSUR de Cardiolux."
  - "Quel est le rôle du QPPV Dr. Leroy ?"
  - "Quel est le suivi du cas grave CAS-2024-0004 ?"
- **Nœud de réponse :**
  - Requête sur `adverse_events.csv`, `signaux_securite.csv`, `rapports_suivi_icsr.csv` + recherche générative dans `Pharmacovigilance/`.

### Sujet 4 : `Information Médicale & Questions Cliniques Fondées sur les Preuves`
- **Phrases de déclenchement :**
  - "Peut-on ouvrir la gélule de Tremopan ?"
  - "Quelle conduite à tenir en cas d'oubli de prise ?"
  - "Que faire en cas d'insuffisance rénale sous Glucorite ?"
  - "Quelles sont les données de switch sous Neurotix ?"
- **Nœud de réponse :**
  - Requête sur `medical_faq.csv`, `faq_scientifiques.csv` + recherche générative dans `Medical_Information/`.

### Sujet 5 : `Annuaire, Gouvernance & Procédures Internes`
- **Phrases de déclenchement :**
  - "Qui est le Pharmacien Responsable de PharmaNova ?"
  - "Quel est le contact de la personne qualifiée pour la pharmacovigilance ?"
  - "Donne-moi l'organigramme de la direction qualité."
  - "Quelle est la charte d'intégrité des données ALCOA+ ?"
- **Nœud de réponse :**
  - Requête sur `collaborateurs.csv`, `organigramme.csv`, `procedures_internes.csv` + recherche générative dans `Corporate/`.

### Sujet 6 : `Formation Professionnelle & Habilitations GxP`
- **Phrases de déclenchement :**
  - "Quelles sont les formations obligatoires pour un technicien QC ?"
  - "Quel est le programme de formation en pharmacovigilance ?"
  - "Quels modules composent le parcours BPF MOD-TRN-001 ?"
- **Nœud de réponse :**
  - Requête sur `training_catalog.csv`, `competences_matrix.csv` + recherche générative dans `Training/`.

---

## 3. Instruction Système (Grounding System Prompt) pour l'Agent

Copier et coller ce prompt de cadrage dans les **Instructions du Copilote** :

```text
Tu es l'assistant d'entreprise officiel de PharmaNova SA, laboratoire pharmaceutique européen de référence.
Tu réponds aux collaborateurs, auditeurs qualité, inspecteurs des autorités de santé (ANSM, EMA) et professionnels de santé.

Directives absolues :
1. Fonde exclusivement tes réponses sur la documentation officielle interne de PharmaNova (SOP, dossiers d'AMM, RCP, registre de pharmacovigilance, annuaire et référentiels GxP).
2. Pour toute question relative à un médicament, cite systématiquement sa DCI, son statut d'AMM et les précautions ou contre-indications associées.
3. Pour toute question relative à la qualité ou aux déviations, mentionne la référence de la SOP applicable (ex: SOP-QA-002, SOP-QA-003, SOP-QC-026) et les responsabilités du Pharmacien Responsable (QP).
4. Pour toute question de pharmacovigilance, rappelle l'obligation légale de notification sous 24 heures des cas graves et cite le QPPV Dr. Marc-Antoine Leroy.
5. Adopte un ton professionnel, rigoureux, précis, conforme aux normes EudraLex, ICH et GVP.
6. Si une information n'existe pas dans le référentiel PharmaNova, indique clairement : "Cette information n'est pas documentée dans le référentiel officiel PharmaNova en vigueur."
```

---

## 4. Scénarios de Test et Questions d'Évaluation de l'Agent

1. **Test Posologie & Sécurité :** "Un patient sous Cardiolux présente des myalgies intenses avec élévation des CPK. Que doit faire le praticien ?"
   - *Réponse attendue :* Dosage CPK immédiat, suspicion de rhabdomyolyse rare, arrêt immédiat du produit si CPK > 10x LSN, déclaration obligatoire au département de pharmacovigilance (Dr. Marc-Antoine Leroy).
2. **Test Qualité Déviation :** "Une déviation majeure DEV-2024-002 est survenue à Chalon. Quelle CAPA lui est associée et quel est son statut ?"
   - *Réponse attendue :* Associée à la CAPA-2024-001 (plan d'actions correctives et préventives visant à éradiquer la dérive de procédé), statut clôturée avec vérification d'efficacité satisfaisante (VoE).
3. **Test Réglementaire :** "Quelle est la date de renouvellement de l'AMM de Glucorite et quel type de variation a été déposé en 2024 ?"
   - *Réponse attendue :* AMM renouvelée en juillet 2026 (EU/1/21/1602/001-002), variations Type IA (VAR-2024-002 changement d'adresse administrative) et Type IB (VAR-2024-009 prolongation de durée de validité de l'API).
4. **Test Traçabilité :** "Qui est l'auditeur principal des audits fournisseurs et quelle est la conclusion de l'audit de Lonza AG ?"
   - *Réponse attendue :* M. Thomas Vasseur (Lead Auditor IRCA/GxP), audit AUD-SUP-2024-001 concluant à un statut de fournisseur homologué / qualifié pour la fourniture d'API biologique.
