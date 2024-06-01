from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer.entities import OperatorConfig
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from gliner_recognizer import GLiNERRecognizer
from spacy_trf_model import SpacyTrfAnalyze
from typing import List, Optional
from helper import split_list, split_text_into_sections_with_full_sentences, entities_with_threshold, prepare_entities_to_anonamize, Fuzzy_Matching
import spacy


# Load the spaCy transformer-based model
nlp = spacy.load("en_core_web_sm")

nlp_configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}

nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

# Initialize the AnalyzerEngine with the SpaCy NLP engine
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

# Initialize the recognizer
gliner_recognizer = GLiNERRecognizer()
analyzer.registry.recognizers = []
analyzer.registry.add_recognizer(gliner_recognizer)


#########################################################################################################################

# Analyze Pii Data
def Analyze_PII_Data(text: str,
                     operator: str,
                     mask_char: str,
                     num_char: int,
                     encrypt_key: str,
                     user_entities: Optional[List[str]] = None,
                     entities_to_mask: Optional[List[str]] = None):
    

    if entities_to_mask is not None:
        entities_to_mask = split_list(entities_to_mask)
        entities = list(set(entities_to_mask + gliner_recognizer.supported_entities))

    elif user_entities is not None:
        entity_list = split_list(user_entities)
        # Append default entities to the provided ones
        entities = list(set(entity_list + gliner_recognizer.supported_entities))
    else:
        entities = gliner_recognizer.supported_entities
    
    # Split the text into the chunks
    sections = split_text_into_sections_with_full_sentences(text)

    # Analyze the each chunk
    glinerRes = []
    SpacyTrfRes = []
    Final_Result = []
    anonamize_text=""
    for section in sections:    
        glinerRes = analyzer.analyze(text=section, language="en", entities=entities)
        SpacyTrfRes = SpacyTrfAnalyze(section)
     
        # combine results of both gliner and spacy trf model
        Combine_results = (glinerRes + SpacyTrfRes) 

        # Filter results based on the confidence score threshold
        Combine_results = entities_with_threshold(Combine_results)
        Final_Result += Combine_results

        filtered_identified_entities = None
        if entities_to_mask is not None:
            filtered_identified_entities = prepare_entities_to_anonamize(entities_to_mask, Combine_results)  
        
        anonamize_text += " " + anonamize_data(section, Combine_results, operator, mask_char, num_char, encrypt_key, filtered_identified_entities)
    
    return Final_Result, anonamize_text


#########################################################################################################################

# Function to anonymize data based on the specified operator and configurations
def anonamize_data(text: str,
                   results,
                   operator: str,
                   mask_char: str,
                   num_of_chars: int,
                   encrypt_key: str,
                   filtered_identified_entities:Optional[List[RecognizerResult]] = None):
    
    # If operator is mask then assingn the character and number of characters
    if operator == "mask":
        operator_config = {
            "type": "mask",
            "masking_char": mask_char,
            "chars_to_mask": num_of_chars,
            "from_end": False,
        }
    elif operator == "encrypt":
        operator_config = {"key": encrypt_key} 
    elif operator == "hash":
        operator_config = {"algorithm": "md5"}    
    else:
        operator_config = None    


    anonymizer_result = anonymizer.anonymize(
        text=text,
        analyzer_results = results if filtered_identified_entities is None else filtered_identified_entities,
        operators={"DEFAULT": OperatorConfig(operator, operator_config)}
    )  
    return anonymizer_result.text






