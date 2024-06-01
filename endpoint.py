from fastapi import FastAPI, Query, HTTPException
from main import Analyze_PII_Data
from typing import List, Optional, Annotated, Union
from pydantic import BaseModel


class Entity(BaseModel):
    entity_type: str
    start: int
    end: int
    score: float

class EntitiesInput(BaseModel):
    entities: List[Entity]
    text: str
    key: str


app = FastAPI()


@app.post("/deidentify_unstructured_data")
def Deidentify_Unstructured_Data(
    text: str,
    approach: str = Query(
        default="replace",
        enum=["redact", "replace","mask", "hash", "encrypt"],
        description="""
        Select which manipulation to perform on the text after PII has been identified.
        - Redact: Completely remove the PII text.
        - Replace: Replace the PII text with a constant, e.g. <PERSON>.
        - Mask: Replaces a requested number of characters with a mask character.
        - Hash: Replaces with the hash of the PII string.
        - Encrypt: Replaces with an AES encryption of the PII string.
        """,
    ),

    Add_supported_entities: Optional[List[str]] = Query(
        None, 
        description="Enter a list of entities you want to add in default entities list.(Enter in uppercase, separated by commas, like PERSON,AGE)."
    ),

    mask_char: str = Query(
        default="*",
        description="Character to use for masking (applicable only for 'mask' approach).",
    ),
    num_chars_to_mask: int = Query(
        default=15,
        gt=0,  # Ensure positive value for number of characters
        description="Number of characters to mask (applicable only for 'mask' approach).",
    ),
    encrypt_key: str = Query(
        default="WmZq4t7w!z%C&F)J",
        description="Enter encryption key of length 16 to encrypt data (applicable only for 'encrypt' approach)"
    ),

    entities_to_anonamize: Optional[List[str]] = Query(
        None, 
        description="Enter the list of entites you want to identify and anonamize in place of default entities.(Enter in uppercase separated by commas)."
    )
):
    
    # Ensure that number of characters is greater then zero
    if approach == "mask" and num_chars_to_mask <= 0:
        raise HTTPException(status_code=400, detail="Number of characters must be greater then zero to mask the data")
    
    # Ensure that length of encryption key is sixteen
    elif approach == "encrypt" and len(encrypt_key) != 16:
        raise HTTPException(status_code=400, detail="Encryption key must be of length sixteen characters")    
    
    if Add_supported_entities and entities_to_anonamize:
        raise HTTPException(status_code=400,detail="You can either add entities to default list or replace it.")
    
    Final_Result, masked_text = Analyze_PII_Data(
        text, approach, mask_char, num_chars_to_mask, encrypt_key, Add_supported_entities, entities_to_anonamize
    )

    return {"Anonamized_text": masked_text}

































# @app.get("/masked_unstructured_data/")
# async def masked_data(text: str = Query(None, min_length=2)):
#     entity_details, anonymized_text = Masked_PII_Data(text)

#     return {"anonymized_text": anonymized_text, "entity_details": entity_details}
