SPECIALTY_MESH: dict[str, list[str]] = {
    "cardiology": [
        "Heart Diseases[MeSH]",
        "Cardiovascular Diseases[MeSH]",
        "Coronary Artery Disease[MeSH]",
        "Heart Failure[MeSH]",
        "Arrhythmias, Cardiac[MeSH]",
        "Hypertension[MeSH]",
    ],
    "internal medicine": [
        "Internal Medicine[MeSH]",
        "Chronic Disease[MeSH]",
        "Diabetes Mellitus[MeSH]",
        "Hypertension[MeSH]",
        "Kidney Diseases[MeSH]",
        "Liver Diseases[MeSH]",
    ],
    "oncology": [
        "Neoplasms[MeSH]",
        "Antineoplastic Agents[MeSH]",
        "Cancer[TIAB]",
        "Tumor Microenvironment[MeSH]",
        "Immunotherapy[MeSH]",
        "Precision Medicine[MeSH]",
    ],
    "neurology": [
        "Nervous System Diseases[MeSH]",
        "Stroke[MeSH]",
        "Neurodegenerative Diseases[MeSH]",
        "Epilepsy[MeSH]",
        "Multiple Sclerosis[MeSH]",
        "Parkinson Disease[MeSH]",
        "Alzheimer Disease[MeSH]",
    ],
    "psychiatry": [
        "Mental Disorders[MeSH]",
        "Depression[MeSH]",
        "Anxiety Disorders[MeSH]",
        "Schizophrenia[MeSH]",
        "Bipolar Disorder[MeSH]",
        "Suicide[MeSH]",
        "Psychopharmacology[MeSH]",
    ],
    "pediatrics": [
        "Child[MeSH]",
        "Infant[MeSH]",
        "Pediatrics[MeSH]",
        "Child Development[MeSH]",
        "Vaccination[MeSH]",
        "Congenital Abnormalities[MeSH]",
    ],
    "surgery": [
        "Surgical Procedures, Operative[MeSH]",
        "Postoperative Complications[MeSH]",
        "Minimally Invasive Surgical Procedures[MeSH]",
        "Laparoscopy[MeSH]",
        "Robotic Surgical Procedures[MeSH]",
    ],
    "emergency medicine": [
        "Emergencies[MeSH]",
        "Emergency Medicine[MeSH]",
        "Critical Care[MeSH]",
        "Shock[MeSH]",
        "Trauma Centers[MeSH]",
        "Triage[MeSH]",
    ],
    # Subspecialties
    "heart failure": [
        "Heart Failure[MeSH]",
        "Cardiomyopathies[MeSH]",
        "Ventricular Dysfunction[MeSH]",
    ],
    "electrophysiology": [
        "Arrhythmias, Cardiac[MeSH]",
        "Atrial Fibrillation[MeSH]",
        "Catheter Ablation[MeSH]",
        "Cardiac Pacing, Artificial[MeSH]",
    ],
    "interventional cardiology": [
        "Percutaneous Coronary Intervention[MeSH]",
        "Stents[MeSH]",
        "Cardiac Catheterization[MeSH]",
        "Angioplasty, Balloon, Coronary[MeSH]",
    ],
    "neuro-oncology": [
        "Brain Neoplasms[MeSH]",
        "Glioblastoma[MeSH]",
        "Central Nervous System Neoplasms[MeSH]",
        "Meningeal Neoplasms[MeSH]",
    ],
    "child psychiatry": [
        "Child Psychiatry[MeSH]",
        "Attention Deficit Disorder with Hyperactivity[MeSH]",
        "Autism Spectrum Disorder[MeSH]",
        "Child Behavior Disorders[MeSH]",
    ],
    "neonatology": [
        "Infant, Newborn[MeSH]",
        "Intensive Care, Neonatal[MeSH]",
        "Premature Birth[MeSH]",
        "Infant, Premature, Diseases[MeSH]",
    ],
    "infectious disease": [
        "Communicable Diseases[MeSH]",
        "Anti-Bacterial Agents[MeSH]",
        "Antiviral Agents[MeSH]",
        "Sepsis[MeSH]",
        "Drug Resistance, Microbial[MeSH]",
    ],
    "rheumatology": [
        "Rheumatic Diseases[MeSH]",
        "Arthritis, Rheumatoid[MeSH]",
        "Lupus Erythematosus, Systemic[MeSH]",
        "Spondylarthritis[MeSH]",
    ],
    "endocrinology": [
        "Endocrine System Diseases[MeSH]",
        "Diabetes Mellitus, Type 2[MeSH]",
        "Thyroid Diseases[MeSH]",
        "Obesity[MeSH]",
        "Adrenal Gland Diseases[MeSH]",
    ],
    "gastroenterology": [
        "Gastrointestinal Diseases[MeSH]",
        "Inflammatory Bowel Diseases[MeSH]",
        "Colorectal Neoplasms[MeSH]",
        "Liver Cirrhosis[MeSH]",
        "Helicobacter pylori[MeSH]",
    ],
    "pulmonology": [
        "Lung Diseases[MeSH]",
        "Asthma[MeSH]",
        "Pulmonary Disease, Chronic Obstructive[MeSH]",
        "Respiratory Insufficiency[MeSH]",
        "Pulmonary Fibrosis[MeSH]",
    ],
    "nephrology": [
        "Kidney Diseases[MeSH]",
        "Renal Insufficiency, Chronic[MeSH]",
        "Dialysis[MeSH]",
        "Kidney Transplantation[MeSH]",
        "Glomerulonephritis[MeSH]",
    ],
    "hematology": [
        "Hematologic Diseases[MeSH]",
        "Leukemia[MeSH]",
        "Anemia[MeSH]",
        "Blood Coagulation Disorders[MeSH]",
        "Lymphoma[MeSH]",
    ],
    "dermatology": [
        "Skin Diseases[MeSH]",
        "Melanoma[MeSH]",
        "Psoriasis[MeSH]",
        "Dermatitis, Atopic[MeSH]",
        "Skin Neoplasms[MeSH]",
    ],
    "ophthalmology": [
        "Eye Diseases[MeSH]",
        "Glaucoma[MeSH]",
        "Macular Degeneration[MeSH]",
        "Diabetic Retinopathy[MeSH]",
        "Cataract[MeSH]",
    ],
    "orthopedics": [
        "Musculoskeletal Diseases[MeSH]",
        "Fractures, Bone[MeSH]",
        "Arthroplasty, Replacement[MeSH]",
        "Spine[MeSH]",
        "Osteoarthritis[MeSH]",
    ],
    "geriatrics": [
        "Geriatrics[MeSH]",
        "Aged[MeSH]",
        "Frailty[MeSH]",
        "Dementia[MeSH]",
        "Polypharmacy[MeSH]",
    ],
    "obstetrics": [
        "Obstetrics[MeSH]",
        "Pregnancy Complications[MeSH]",
        "Labor, Obstetric[MeSH]",
        "Preeclampsia[MeSH]",
        "Maternal Mortality[MeSH]",
    ],
    "gynecology": [
        "Gynecology[MeSH]",
        "Uterine Neoplasms[MeSH]",
        "Ovarian Neoplasms[MeSH]",
        "Endometriosis[MeSH]",
        "Polycystic Ovary Syndrome[MeSH]",
    ],
    "urology": [
        "Urologic Diseases[MeSH]",
        "Prostatic Neoplasms[MeSH]",
        "Urinary Incontinence[MeSH]",
        "Kidney Calculi[MeSH]",
        "Bladder Neoplasms[MeSH]",
    ],
    "radiology": [
        "Radiology[MeSH]",
        "Magnetic Resonance Imaging[MeSH]",
        "Tomography, X-Ray Computed[MeSH]",
        "Ultrasonography[MeSH]",
        "Interventional Radiology[MeSH]",
    ],
    "anesthesiology": [
        "Anesthesiology[MeSH]",
        "Anesthesia[MeSH]",
        "Pain Management[MeSH]",
        "Perioperative Care[MeSH]",
        "Intensive Care Units[MeSH]",
    ],
}

PUBTYPE_BY_ROLE: dict[str, list[str]] = {
    "clinician": [
        "Clinical Trial[pt]",
        "Randomized Controlled Trial[pt]",
        "Meta-Analysis[pt]",
        "Systematic Review[pt]",
        "Practice Guideline[pt]",
        "Clinical Practice Guideline[pt]",
    ],
    "researcher": [
        "Journal Article[pt]",
        "Review[pt]",
        "Letter[pt]",
        "Comment[pt]",
        "Case Reports[pt]",
    ],
    "educator": [
        "Review[pt]",
        "Systematic Review[pt]",
        "Meta-Analysis[pt]",
        "Guideline[pt]",
        "Practice Guideline[pt]",
        "Lecture[pt]",
    ],
    "resident": [
        "Clinical Trial[pt]",
        "Case Reports[pt]",
        "Review[pt]",
        "Practice Guideline[pt]",
        "Randomized Controlled Trial[pt]",
    ],
    "fellow": [
        "Randomized Controlled Trial[pt]",
        "Meta-Analysis[pt]",
        "Systematic Review[pt]",
        "Clinical Trial[pt]",
        "Research Support[pt]",
    ],
}


def get_mesh_terms(
    specialties: list[str], subspecialties: list[str]
) -> list[tuple[str, list[str]]]:
    """
    Returns a list of (label, mesh_terms) tuples — one per specialty/subspecialty.
    Unknown terms fall back to a free-text TIAB search.
    """
    result: list[tuple[str, list[str]]] = []
    seen: set[str] = set()
    for sp in specialties + subspecialties:
        key = sp.lower().strip()
        if key in seen:
            continue
        seen.add(key)
        if key in SPECIALTY_MESH:
            result.append((sp, SPECIALTY_MESH[key]))
        else:
            result.append((sp, [f"{sp}[TIAB]"]))
    return result


def get_pubtype_filter(roles: list[str]) -> str:
    """
    Returns an OR-joined pub type filter clause for all roles combined.
    Returns empty string if roles is empty or unrecognized.
    """
    types: set[str] = set()
    for role in roles:
        types.update(PUBTYPE_BY_ROLE.get(role.lower(), []))
    if not types:
        return ""
    return "(" + " OR ".join(sorted(types)) + ")"
