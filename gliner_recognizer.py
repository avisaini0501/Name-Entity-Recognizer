from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from gliner import GLiNER



class GLiNERRecognizer(EntityRecognizer):
    def __init__(self, supported_entities=None):
        super().__init__(supported_entities=supported_entities)
        self.model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
        self.supported_entities = [
        "PERSON", "LOCATION","ORGANIZATION", "EMAIL_ADDRESS", "US_DRIVER_LICENSE", "US_PASSPORT", "US_SSN","AADHAR_NUMBER",
        "US_BANK_NUMBER", "IN_PAN", "URL", "PHONE_NUMBER", "DATE_TIME", "IP_ADDRESS", "IBAN_CODE", "CRYPTO",
        "CREDIT_CARD","US_ITIN", "VOTER_ID", "PASSPORT_NUMBER", "SSN", "HEALTH_INSURANCE_ID_NUMBER", "AMOUNT",
        "DATE_OF_BIRTH","BANK_ACCOUNT_NUMBER", "MEDICATION", "CPF", "DRIVER'S_LICENSE_NUMBER", "TAX_IDENTIFICATION_NUMBER",
        "MEDICAL_CONDITION", "IDENTITY_CARD_NUMBER","NATIONAL_ID_NUMBER", "IBAN", "CREDIT_CARD_EXPIRATION_DATE",
        "USERNAME", "HEALTH_INSURANCE_NUMBER", "REGISTRATION_NUMBER", "STUDENT_ID_NUMBER", "INSURANCE_NUMBER",
        "FLIGHT_NUMBER", "LANDLINE_PHONE_NUMBER", "BLOOD_TYPE", "CVV", "RESERVATION_NUMBER", "DIGITAL_SIGNATURE",
        "SOCIAL_MEDIA_HANDLE", "LICENSE_PLATE_NUMBER","CNPJ", "POSTAL_CODE", "SERIAL_NUMBER", "VEHICLE_REGISTRATION_NUMBER",
        "FAX_NUMBER", "VISA_NUMBER", "INSURANCE_COMPANY","IDENTITY_DOCUMENT_NUMBER","TRANSACTION_NUMBER","COST","PRICE",
        "NATIONAL_HEALTH_INSURANCE_NUMBER", "CVC", "BIRTH_CERTIFICATE_NUMBER", "TRAIN_TICKET_NUMBER", "PASSPORT_EXPIRATION_DATE"
]

    def load(self):
        # Method to load models or other data if needed
        pass

    def analyze(self, text, entities, nlp_artifacts):       
        # Use the GLiNER model to predict entities
        results = self.model.predict_entities(text, entities)
        recognizer_results = []
        for result in results:
            entity_type = result['label']
            start = result['start']
            end = result['end']
            score = result['score']  # Confidence score if available
            recognizer_results.append(RecognizerResult(
                entity_type=entity_type,
                start=start,
                end=end,
                score=score
            ))
        return recognizer_results



