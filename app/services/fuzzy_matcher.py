from typing import List, Tuple, Any
from rapidfuzz import process

def perform_fuzzy_match(source: List[Tuple[str, str]], target: List[Tuple[str, str]]) -> List[Tuple[str, str, str, str, float]]:
    target_dict = {name: id_ for id_, name in target}

    matches = []
    for src_id, src_name in source:
        best_match, score,_ = process.extractOne(
            src_name, 
            target_dict.keys()
        )
        if score >= 75:  # Set a threshold for the match percentage
            target_id = target_dict[best_match]
            matches.append((src_id, src_name, target_id, best_match, score))
        else:
            matches.append((src_id, src_name, "", "", 0.00))  # No match

    return matches


