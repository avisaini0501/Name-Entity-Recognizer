import re
from fuzzywuzzy import process

def split_text_into_sections_with_full_sentences(text, max_chars=1600):
    """
    Splits the text into sections. Each section contains complete sentences and does not exceed
    the specified maximum number of characters. If including a sentence would exceed this limit,
    the sentence is moved to the beginning of the next section.
    """
    # Split the text into sentences
    sentences = re.split('(?<=[.!?])\s+', text)
    sections = []
    section = ""

    for sentence in sentences:
        # Check if adding this sentence would exceed the max_chars limit
        if len(section) + len(sentence) > max_chars:
            # If the current section plus the new sentence is too long,
            # start a new section with the sentence
            sections.append(section.strip())
            section = sentence
        else:
            # Otherwise, add the sentence to the current section
            section += " " + sentence

    # Don't forget to add the last section if it's not empty
    if section:
        sections.append(section.strip())

    return sections



# To split the collective list of entities
def split_list(entites):
    items = []
    for entity in entites:
        items.extend(entity.split(','))
    return items


# Function to filter entities based on a confidence score threshold
def entities_with_threshold(results, threshold=0.6):
    filtered_results = [res for res in results if res.score >= threshold]
    return filtered_results


# Prepare entities to be anonymized based on the user's specified entities
def prepare_entities_to_anonamize(entities_to_mask, Combine_results): 
    entities_to_mask = split_list(entities_to_mask)   
    all_identified_entities = [result.entity_type for result in Combine_results]

    matched_entities = Fuzzy_Matching(entities_to_mask, all_identified_entities)   

    # Filter identified entities that has to be masked
    filtered_identified_entities = [
       entity for entity in Combine_results if entity.entity_type in matched_entities.values()
    ]

    return filtered_identified_entities


# Function to match user-specified entities with identified entities using fuzzy matching
def Fuzzy_Matching(user_entities, available_entities, threshold=80):
    matched_entities = {}
    for user_entity in user_entities:
        match, score = process.extractOne(user_entity, available_entities)
        if score >= threshold:
            matched_entities[user_entity] = match
    return matched_entities