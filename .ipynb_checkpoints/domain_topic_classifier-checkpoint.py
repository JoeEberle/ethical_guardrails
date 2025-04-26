import re

# Define keyword lists
DOMAIN_KEYWORDS = {
    "healthcare": {
        "cancer", "diabetes", "glucose", "A1C", "surgery", "blood", "screening", "lungs", "bone", "colonoscopy",
        "obesity", "arthritis", "osteoporosis", "chronic pain",  # General & chronic
        "myocardial", "heart attack", "stroke", "hypertension", "blood pressure", "cholesterol",  # Cardiovascular
        "covid", "flu", "hepatitis", "hiv", "aids", "tuberculosis", "malaria",  # Infectious
        "asthma", "copd", "bronchitis",  # Respiratory
        "alzheimers", "parkinsons", "depression", "anxiety", "autism", "epilepsy",  # Neurological / mental
        "lupus", "celiac", "crohn", "multiple sclerosis", "psoriasis", "sickle cell",  # Autoimmune & genetic
        "tissue", "procedure", "doctor", "heart", "disease", "diagnosis", "population", "patient", "hospital",
        "condition", "sick", "ill", "visit", "clinic", "nurse", "smoking", "dr", "practice", "diet", "drug",
        "treat", "treatment", "walking", "weight", "obese", "health", "pnuemonia", "fever", "rash", "infarction",
        "medication", "ozempic", "wegovy", "aspirin", "viagra", "opioid", "statin", "antidepressant", "antibiotics", "acetaminophen", "ibuprofen",
        "metformin", "lisinopril", "amoxicillin", "atorvastatin", "simvastatin", "omeprazole", "pantoprazole", "levothyroxine",
        "albuterol", "insulin", "gabapentin", "hydrochlorothiazide", "amlodipine", "losartan", "clopidogrel", "xarelto",
        "eliquis", "warfarin", "glipizide", "tramadol", "morphine", "fentanyl", "naltrexone", "suboxone", "naloxone", "prednisone",
        "fluoxetine", "sertraline", "citalopram", "bupropion", "duloxetine", "venlafaxine", "lorazepam", "clonazepam", "insulin",
        "neuropathy", "sepsis", "wellness", "knee", "arm", "hip", "EKG", "leg", "shoulder", "mouth", "eye",
        "teeth", "biopsy", "lab", "epidemic", "pandemic", "abuse", "overweight", "prevalance", "diabetic", "at risk",
        "viagra", "ozempic", "warfarin", "wagovi", "prozac", "opiod", "addiction", "medical", "prescription", "tumor",
        "comorbid", "cough", "congestion", "xray", "scan", "medication", "prescribe", "medicine", "skin"
    },
    "innapropriatelanguage": {
        "shit", "fuck", "crap", "sucks", "bitch", "asshole", "pussy", "dick", "cunt", "bullshit", "rage", "furious",
        "angry", "curse", "abuse", "harass", "insult", "threat", "violence", "retaliate"
    },
    "hostility": {
        "bomb", "kill", "shoot", "invade", "weapon", "gun", "hate", "bully", "attack", "murder", "slaughter",
        "massacre", "stab", "assault", "execute", "terror", "ambush", "raid", "rage", "scum", "vermin",
        "exterminate", "genocide", "racist", "bigot", "lynch", "burn", "destroy", "war", "battle", "conflict",
        "combat", "uprising", "rebellion", "hostile", "oppress", "occupation"
    },
    "racism": {
        "black people", "white people", "jews", "muslims", "asians", "latinos", "immigrants", "illegals",
        "nigger", "kike", "chink", "cracker", "spic", "gook", "coon", "ape", "savage", "mulatto", "redskin", "whitey",
        "great replacement", "white genocide", "globalist", "they control the media", "take back our country",
        "their all criminals", "their lazy", "they do not belong here", "send them back", "master race", "inferior race"
    },
    "titanic": {
        "passenger", "ticket class", "survived", "died", "titanic", "iceberg", "lifeboat", "drown", "ship", "deck",
        "age", "sex", "fare", "embarked", "cabin", "port", "crew", "captain", "steerage", "first class", "second class",
        "third class", "sibling", "spouse", "parent", "child", "pclass", "name", "embarkation", "rescue", "disaster",
        "collision", "women", "children", "men", "elderly", "victim", "survivor", "SOS", "North Atlantic", "April 1912",
        "White Star Line", "RMS", "British", "New York", "Southampton", "Cherbourg", "Queenstown", "lifebelt"
    },
    "penguin": {
        "flipper", "beak", "gentoo", "penguins", "feathers", "colony", "antarctica", "huddle", "adelie", "chinstrap",
        "island", "bill length", "bill depth", "flipper length", "body mass", "sex", "species", "diet", "krill", "fish",
        "diving", "swimming", "incubation", "nesting", "mate", "egg", "parenting", "molting", "rookery", "cold", "snow",
        "ice", "climate", "Biscoe", "Dream", "Torgersen", "habitat", "marine", "flightless", "birds", "antarctic"
    }
}

SUB_DOMAIN_KEYWORDS = {
    "disease": {"cancer", "diabetes", "obesity", "myocardial", "asthma", "cholesterol", "blood pressure", "influenza", "flu", "covid", "illness", "pnuemonia"},
    "disease chronic": {"cancer", "diabetes", "obesity", "arthritis", "osteoporosis", "chronic pain"},
    "disease cardiovascular": {"myocardial", "heart attack", "stroke", "hypertension", "blood pressure", "cholesterol"},
    "disease Infectious": {"covid", "flu", "hepatitis", "hiv", "aids", "tuberculosis", "malaria"},
    "disease Respiratory": {"asthma", "copd", "bronchitis"},
    "disease Neurological": {"alzheimers", "parkinsons", "depression", "anxiety", "autism", "epilepsy"},
    "condition": {"pregnancy", "smoking"},
    "weight": {"obese", "fat", "skinny", "diet", "weight loss", "overweight"},
    "medication": {"ozempic", "wegovy", "aspirin", "viagra", "opioid", "statin", "antidepressant", "antibiotics", "acetaminophen", "ibuprofen",
    "metformin", "lisinopril", "amoxicillin", "atorvastatin", "simvastatin", "omeprazole", "pantoprazole", "levothyroxine",
    "albuterol", "insulin", "gabapentin", "hydrochlorothiazide", "amlodipine", "losartan", "clopidogrel", "xarelto",
    "eliquis", "warfarin", "glipizide", "tramadol", "morphine", "fentanyl", "naltrexone", "suboxone", "naloxone", "prednisone",
    "fluoxetine", "sertraline", "citalopram", "bupropion", "duloxetine", "venlafaxine", "lorazepam", "clonazepam", "diazepam",
    "aripiprazole", "risperidone", "quetiapine", "methotrexate", "adalimumab", "montelukast"},
    "lab result": {"screening", "test", "panel", "ekg", "mri", "xray", "biopsy", "colonoscopy"},
    "anatomy": { "heart", "lungs", "brain", "liver", "kidney", "stomach", "intestine", "colon", "pancreas", "spleen",
    "bladder", "esophagus", "trachea", "bronchi", "diaphragm", "skin", "bone", "muscle", "joint", "spine",
    "rib", "skull", "pelvis", "femur", "tibia", "fibula", "humerus", "ulna", "radius", "knee", "hip", "shoulder",
    "arm", "leg", "hand", "foot", "eye", "ear", "nose", "mouth", "tongue", "teeth", "throat", "neck",
    "thyroid", "prostate", "uterus", "ovary", "testicle", "vein", "artery", "nerve", "lymph node"},
    "behavioral": {
    "depression", "anxiety", "addiction", "suicide", "abuse", "substance abuse", "therapy", "therapist",
    "mental health", "self-harm", "panic attacks", "bipolar", "schizophrenia", "ocd", "ptsd", "eating disorder",
    "anorexia", "bulimia", "insomnia", "mood swings", "psychosis", "trauma", "grief", "loss", "loneliness",
    "stress", "burnout", "counseling", "psychologist", "psychiatrist", "cbt", "meditation", "mindfulness",
    "anger management", "support group"},
    "medical": {"doctor", "physician", "nurse", "practitioner", "appointment", "visit", "checkup", "referral", "triage",
    "admission", "discharge", "hospitalization", "clinic", "hospital", "inpatient", "outpatient",
    "emergency department", "urgent care", "primary care", "specialist", "chart", "medical record", "ehr",
    "prescription", "medication", "iv", "infusion", "anesthesia", "procedure", "surgery", "labs", "vitals",
    "diagnosis", "insurance", "copay", "authorization"},
    "procedure": {"surgery", "operation", "excision", "ablation", "knee replacement", "hip replacement", "appendectomy",
    "colonoscopy", "endoscopy", "biopsy", "cataract surgery", "bypass surgery", "angioplasty", "stent placement",
    "mastectomy", "lumpectomy", "cesarean section", "hysterectomy", "cholecystectomy", "dialysis",
    "laparoscopy", "mri", "ct scan", "xray", "ultrasound", "mammogram", "vaccination", "injection",
    "blood transfusion", "intubation", "ventilation", "physical therapy"},
    "racist": {"black people", "nigger", "jew", "jewish", "jews", "white people"},
    "racism": {"black people", "white people", "jew", "jewish", "jews", "nigger", "kike", "chink", "spic", "gook",
    "coon", "cracker", "wetback", "raghead", "sand nigger", "porch monkey", "slant eye", "ape", "savage", 
    "subhuman", "master race", "inferior race", "deport them all", "they do not belong here", 
    "go back to your country", "they're all criminals", "build the wall", "invaders", "white genocide", 
    "great replacement", "race war", "ethnic cleansing"},     
    "antisemitic": {
    "jew", "jewish", "jews", "zionist", "globalist", "they control the media", "rothschild", 
    "holocaust hoax", "dirty jew", "kike", "heeb", "hook-nosed", "new world order", "protocols of the elders of zion",
    "jewish conspiracy", "kill the jews", "jews are evil", "jews run everything", "anti-zionist not antisemitic", 
    "gas the jews"},    
    "violent": {"attack", "murder", "slaughter", "massacre", "kill", "stab", "assault", "execute", "terror", "ambush", "raid"},
    "aggressive": {"rage", "furious", "angry", "curse", "abuse", "harass", "insult", "threat", "violence", "retaliate"},
    "military": {"war", "battle", "conflict", "combat", "uprising", "rebellion", "hostile", "oppress", "occupation"},
    "dehumanizing": {"scum", "vermin", "exterminate", "genocide", "racist", "bigot", "lynch", "burn", "destroy"},
    "racial group": {"black people", "white people", "jews", "muslims", "asians", "latinos", "immigrants", "illegals"},
    "racial slur": {"nigger", "kike", "chink", "cracker", "spic", "gook", "coon", "ape", "savage", "mulatto", "redskin", "whitey"},
    "racial genocide": {"great replacement", "white genocide", "globalist", "they control the media", "take back our country"},
    "racial stereotype": {"their all criminals", "their lazy", "they do not belong here", "send them back", "master race", "inferior race"},
    "penguin": {"flipper", "beak", "gentoo", "penguins", "feathers", "colony", "antarctica", "huddle"},
    "titanic": {"passenger", "ticket class", "survived", "died", "titanic", "iceberg", "lifeboat", "drown", "ship", "deck"}   
}


def domain_classifier(text):
    text = text.lower()
    scores = {category: 0 for category in DOMAIN_KEYWORDS}
    for category, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                scores[category] += 1
    best_match = max(scores, key=scores.get)
    return best_match if scores[best_match] > 0 else "general"


def sub_domain_classifier(text):
    text = text.lower()
    scores = {category: 0 for category in SUB_DOMAIN_KEYWORDS}
    for category, keywords in SUB_DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                scores[category] += 1
    best_match = max(scores, key=scores.get)
    return best_match if scores[best_match] > 0 else "unknown"


def test_domain_topic_classifier(sample_sentence):
    print(f"Text: {sample_sentence}")
    print(f"Domain: {domain_classifier(sample_sentence)}")
    print(f"Topic: {sub_domain_classifier(sample_sentence)}\n")

def get_sample_questions():
    sentences = [
        "The gentoo penguin has a distinctive beak and flipper movement.",
        "The Titanic had over 1,200 passengers and hit an iceberg.",
        "Early diagnosis of heart disease can save lives.",
        "I am going to kill you all.",
        "I had a cancer screening.",
        "I was diagnosed with copd.",
        "I hate jewish people.",
        "Should I take aspirin every day?",
        "I had a colonoscopy.",
        "I love tacos.",
        "The rocket launch was delayed due to weather conditions.",
        "My blood pressure is always high at the clinic.",
        "The flu hit me really hard this year.",
        "I tested positive for COVID again.",
        "Asthma runs in my family.",
        "I think I’m addicted to painkillers.",
        "He started therapy last month.",
        "They found a tumor during my MRI.",
        "I wish I didn’t have to take insulin every day.",
        "Are vaccines required for travel to Africa?",
        "Why are black people always causing problems?",
        "You’re such a stupid bitch.",
        "The war in Ukraine has caused massive displacement.",
        "They threatened to shoot everyone in the room.",
        "Do penguins live in the North Pole?",
        "My grandmother survived the Titanic disaster.",
        "I cried all night and couldn’t get out of bed.",
        "Is a stent better than bypass surgery?",
        "What are the symptoms of tuberculosis?",
        "My nephew was just diagnosed with autism."
    ]
    return sentences

def run_domain_topic_sample_test():
    sample_sentences = get_sample_questions()
    for sentence in sample_sentences:
        test_domain_topic_classifier(sentence)
    return    
