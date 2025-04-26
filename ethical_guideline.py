import pandas as pd
import domain_topic_classifier as dtc

brand_name = "ThriveAI"

guideline_1_action = "answering" 
guideline_2_action = "not answering - passing on"
guideline_3_action = "not answering - halting" 

guideline_1_response =  f"Question will be answered by {brand_name} "
guideline_2_response =  f"Answer to question not Found in {brand_name} the answer provided is outside of the assistant" 
guideline_3_med_response =  f"""{brand_name} cannot provide personal medical advice, diagnoses, or treatment recommendations. For any medical concerns or health related decisions, please consult a licensed healthcare provider. This platform is not authorized to replace professional medical guidance."""
guideline_3_phi_response =  f"""{brand_name} cannot provide personal or privae, diagnoses, or treatment recommendations. For any medical concerns or health related decisions, please consult a licensed healthcare provider. This platform is not authorized to replace professional medical guidance."""
guideline_3_unethical_response = f"""{brand_name} is designed to provide helpful and informative responses within ethical and responsible boundaries. Questions that are harmful, inappropriate, or unethical will not be answered. By using this platform, you agree to engage respectfully and abide by our ethical use guidelines."""
 

def get_ethical_guideline(question: str) -> dict:
    """
    Applies ethical guideline classification and confidence score to a single question.
    Returns a dictionary with guideline and confidence score.
    """
    domain_class, domain_score, domain_confidence, domain_evidence = dtc.domain_classifier(question)
    topic_class , topic_score, topic_confidence, topic_evidence = dtc.topic_classifier(question)    
    hostility_class, hostility_score, hostility_confidence, hostility_evidence = dtc.hostility_classifier(question)
    sexism_class, sexism_score, sexism_confidence, sexism_evidence = dtc.sexism_classifier(question)
    racism_class, racism_score, racism_confidence, racism_evidence = dtc.racism_classifier(question)
    il_class, il_score, il_confidence, il_evidence = dtc.innapropriate_language_classifier(question)
    pm_class,pm_score,pm_confidence,pm_evidence = dtc.practicing_medicine_classifier(question)
    phi_class,phi_score,phi_confidence,phi_evidence = dtc.phi_classifier(question)

    # if anything is unethical return and stop - Guide line #3 
    if (pm_score + il_score + hostility_score + sexism_score + racism_score + phi_score ) > 0:
        guideline_number = 3        
        if phi_score > 0:
            guidance = guideline_3_phi_response
        elif pm_score > 0: 
            guidance = guideline_3_med_response
        else:  guidance = guideline_3_unethical_response   
        return guidance,guideline_number
        
    # If in domain and topic answer the question 
    if domain_score > 0 and topic_score > 0:
        guidance = guideline_1_response
        guideline_number = 1
        return guidance,guideline_number        

    # If in domain and topic answer the question 
    if domain_score == 0 or topic_score == 0: 
        guidance = guideline_2_response
        guideline_number = 2    
        
    return guidance,guideline_number

def get_ethical_guideline_why(question: str) -> dict:
    """
    Applies ethical guideline classification and confidence score to a single question.
    Returns a dictionary with guideline and confidence score.
    """
    domain_class, domain_score, domain_confidence, domain_evidence = dtc.domain_classifier(question)
    topic_class , topic_score, topic_confidence, topic_evidence = dtc.topic_classifier(question)    
    hostility_class, hostility_score, hostility_confidence, hostility_evidence = dtc.hostility_classifier(question)
    sexism_class, sexism_score, sexism_confidence, sexism_evidence = dtc.sexism_classifier(question)
    racism_class, racism_score, racism_confidence, racism_evidence = dtc.racism_classifier(question)
    il_class, il_score, il_confidence, il_evidence = dtc.innapropriate_language_classifier(question)
    pm_class,pm_score,pm_confidence,pm_evidence = dtc.practicing_medicine_classifier(question)
    phi_class,phi_score,phi_confidence,phi_evidence = dtc.phi_classifier(question)


    ethic_score = pm_score + il_score + hostility_score + sexism_score + racism_score + phi_score
    # if anything is unethical return and stop - Guide line #3 
    if (ethic_score) > 0:
        guideline_number = 3        
        if phi_score > 0:
            guidance = guideline_3_phi_response
        elif pm_score > 0: 
            guidance = guideline_3_med_response
        else:  guidance = guideline_3_unethical_response   
        return guidance,guideline_number, domain_class, topic_class, ethic_score
        
    # If in domain and topic answer the question 
    if domain_score > 0 and topic_score > 0:
        guidance = guideline_1_response
        guideline_number = 1
        return guidance,guideline_number, domain_class, topic_class, ethic_score       

    # If in domain and topic answer the question 
    if domain_score == 0 or topic_score == 0: 
        guidance = guideline_2_response
        guideline_number = 2        

    return guidance, guideline_number, domain_class, topic_class, ethic_score
        
    



