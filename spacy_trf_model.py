from presidio_analyzer import EntityRecognizer, RecognizerResult, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpArtifacts
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer import AnalyzerEngine
import spacy

nlp = spacy.load("en_core_web_trf")
    
nlp_configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_trf"}],
}

nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

analyzer = AnalyzerEngine(
   nlp_engine=nlp_engine, 
   supported_languages=["en"]
) 


def SpacyTrfAnalyze(text):
  
    # Analyze text using spaCy model
    results = analyzer.analyze(text=text, language="en")
    

    # Convert spaCy entities to RecognizerResult objects
    recognizer_results = []
    for res in results:
        entity_type = res.entity_type
        start = res.start
        end = res.end
        score = res.score

        recognizer_results.append(RecognizerResult(
           entity_type=entity_type,
           start=start,
           end=end,
           score=score
        ))   
           
    return recognizer_results
