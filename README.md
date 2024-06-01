Named Entity Recognition for PII and PHI Data
This project provides a robust solution for Named Entity Recognition (NER) of Personally Identifiable Information (PII) and Protected Health Information (PHI) data. It leverages the capabilities of Microsoft's Presidio tool, SpaCy Transformer models, and GLiNER to identify and anonymize sensitive information in text. The project also exposes its functionality via a FastAPI interface for easy integration and use.

Features
Multi-Model NER: Combines GLiNER and SpaCy transformer-based models for enhanced entity recognition.
Flexible Anonymization: Supports multiple anonymization approaches including redaction, replacement, masking, hashing, and encryption.
Customizable: Users can specify custom entities to recognize and anonymize, in addition to the default set of supported entities.
FastAPI Integration: Provides a RESTful API for easy interaction with the NER and anonymization functionalities.
Installation
Clone the Repository

bash
Copy code
git clone https://github.com/avisaini0501/Name-Entity-Recognizer.git
cd Name-Entity-Recognizer
Create a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Download SpaCy Model

bash
Copy code
python -m spacy download en_core_web_trf
Usage
Running the FastAPI Server
Start the Server

bash
Copy code
uvicorn endpoint:app --reload
Access the API Documentation

Open your web browser and navigate to http://127.0.0.1:8000/docs to access the interactive API documentation provided by Swagger UI.

API Endpoints
POST /deidentify_unstructured_data
De-identify unstructured text by recognizing and anonymizing PII and PHI entities.

Parameters:

text (str): The input text to process.
approach (str): The anonymization approach. Options: "redact", "replace", "mask", "hash", "encrypt".
Add_supported_entities (Optional[List[str]]): List of additional entities to recognize.
mask_char (str): Character to use for masking (applicable only for 'mask' approach).
num_chars_to_mask (int): Number of characters to mask (applicable only for 'mask' approach).
encrypt_key (str): Encryption key of length 16 (applicable only for 'encrypt' approach).
entities_to_anonamize (Optional[List[str]]): List of entities to recognize and anonymize instead of the default entities.
Response:

JSON object containing the anonymized text.
Example Request
json
Copy code
POST /deidentify_unstructured_data
{
  "text": "John Doe's social security number is 123-45-6789.",
  "approach": "replace",
  "entities_to_anonamize": ["PERSON", "US_SSN"]
}
Example Response
json
Copy code
{
  "Anonamized_text": "<PERSON>'s social security number is <US_SSN>."
}
Project Structure
endpoint.py: Contains the FastAPI application and endpoint definitions.
gliner_recognizer.py: Defines the GLiNER recognizer class.
spacy_trf_model.py: Contains the integration code for the SpaCy transformer model.
helper.py: Provides utility functions for text processing and entity management.
main.py: Entry point for core processing functions.
requirements.txt: Lists the project dependencies.
Customization
Adding Custom Entities
To add custom entities, specify them in the Add_supported_entities parameter when making a request to the API. The entities should be in uppercase and separated by commas.

Adjusting Confidence Threshold
The entities_with_threshold function filters entities based on a confidence score threshold. You can adjust the threshold value in this function to control the sensitivity of entity recognition.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the existing style and conventions.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or inquiries, please open an issue on GitHub or contact the project maintainer at your.email@example.com.

