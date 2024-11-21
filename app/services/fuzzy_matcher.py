from typing import List, Tuple, Any
from rapidfuzz import process, fuzz
#import numpy as np

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


#-------------------------------------------------------------------------------------------
def perform_fuzzy_match_with_relation(source: List[Tuple[str, str]], target: List[Tuple[str, str]],threshold_for_fields = 75,higher_threshold_for_relation = 75,lower_threshold_for_relation = 40) -> List[Tuple[str, str, str, str, float]]:
    response_matche = []
    
    #set source and target relations 
    source_relations = list(set([source[1] for source in source]))
    target_relations = list(set([target[1] for target in target]))
    #get relation matches
    relation_matches = get_relation_matches(source_relations, target_relations,higher_threshold_for_relation,lower_threshold_for_relation)
    #set source and target for field matching
    for relation_match in relation_matches: 
        source_list = [source_fields for source_fields in source if source_fields[1] == relation_match["source_relation"]]        
        target_list = []
        for target_fields in relation_match["target_relations"]:
            target_list.extend([t for t in target if t[1]==target_fields["target_relation"]])
        matches_for_current_relation = perform_fuzzy_matching_for_relations_and_fields(source_list, target_list,threshold_for_fields)
        response_matche.extend(matches_for_current_relation)
    return response_matche

def get_relation_matches(source_relations, target_relations, higher_threshold=75, lower_threshold=40):
    return_matches = []
    
    for source_relation in source_relations:
        higher_matches = []
        lower_matches = []
        
        for target_relation in target_relations:
            # Calculate fuzzy ratio
            fuzzy_ratio = fuzz.ratio(source_relation, target_relation)
            if fuzzy_ratio >= higher_threshold:
                higher_matches.append({
                    "target_relation":target_relation,
                    "score": fuzzy_ratio
                })
            elif lower_threshold < fuzzy_ratio < higher_threshold:
                lower_matches.append({
                    "target_relation":target_relation,
                    "score": fuzzy_ratio
                })
        
        # Handle higher matches
        if higher_matches:
            if len(higher_matches) == 1:  # Only one higher match
                return_matches.append({
                    "source_relation":source_relation,
                    "target_relations": higher_matches
                })
            else:
                top_higher_match = max(
                    higher_matches, 
                    key=lambda x: x["score"]
                )
                if any(keyword in top_higher_match["target_relation"].lower() for keyword in ['header', 'line', 'lines']):
                    ordered_higher_matches = sorted(
                        [
                            x for x in lower_matches                            
                            if x["target_relation"].lower().replace('header', 'line') == top_higher_match["target_relation"].lower()
                            or x["target_relation"].lower().replace('lines', 'line') == top_higher_match["target_relation"].lower()
                        ],
                        key=lambda x: x["score"],
                        reverse=True
                    )
                    if len(ordered_higher_matches) != 0:                    
                        ordered_higher_matches = ordered_higher_matches[:min(len(ordered_higher_matches),2)]
                    return_matches.append({
                        "source_relation":source_relation,
                        "target_relations": ordered_higher_matches
                    })                    
                else:                    
                    return_matches.append({
                        "source_relation":source_relation,
                        "target_relations": [top_higher_match]
                    }) 
                
                
        
        # Handle lower matches if no higher matches
        elif lower_matches:
            if len(lower_matches) == 1:  # Only one lower match
                return_matches.append({
                    "source_relation":source_relation,
                    "target_relations": lower_matches
                })
            else:
                top_lower_match = max(
                    lower_matches, 
                    key=lambda x: x["score"]
                )
                if any(keyword in top_lower_match["target_relation"].lower() for keyword in ['header', 'line', 'lines']):
                    ordered_lower_matches = sorted(
                        [
                            x for x in lower_matches                            
                            if x["target_relation"].lower().replace('header', 'line') == top_lower_match["target_relation"].lower()
                            or x["target_relation"].lower().replace('lines', 'line') == top_lower_match["target_relation"].lower()
                        ],
                        key=lambda x: x["score"],
                        reverse=True
                    )
                    if len(ordered_lower_matches) != 0:                    
                        ordered_lower_matches = ordered_lower_matches[:min(len(ordered_lower_matches),2)]
                    return_matches.append({
                        "source_relation":source_relation,
                        "target_relations": ordered_lower_matches
                    })                    
                else:                    
                    return_matches.append({
                        "source_relation":source_relation,
                        "target_relations": [top_lower_match]
                    }) 
    return return_matches
    
def perform_fuzzy_matching_for_relations_and_fields(source, target,threshold):
    target_dict = {name: id_ for id_,rel, name, *_ in target}

    matches = []
    for src_id,rel, src_name,*_ in source:
        best_match, score,_ = process.extractOne(
            src_name, 
            target_dict.keys()
        )
        if score >= threshold:  # Set a threshold for the match percentage
            target_id = target_dict[best_match]
            matches.append((src_id, src_name, target_id, best_match, score))
        else:
            matches.append((src_id, src_name, "", "", 0.00))  # No match

    return matches

#--------------------------------------------------------------------------------------------
def check_and_add_record(hash_set, record):
    if record in hash_set:
        return False
    else:
        hash_set.add(record)
        return True

def perform_fuzzy_match_with_relation_excluded_full_matches(source, target,threshold_for_fields = 75,higher_threshold_for_relation = 75,lower_threshold_for_relation = 40):
    response_matche = []
    
    #set source and target relations 
    source_relations = list(set([source[1] for source in source]))
    target_relations = list(set([target[1] for target in target]))
    #print(source)
    #get relation matches
    relation_matches = get_relation_matches(source_relations, target_relations,higher_threshold_for_relation,lower_threshold_for_relation)
    #set source and target for field matching
    for relation_match in relation_matches: 
        source_list = [source_fields for source_fields in source if source_fields[1] == relation_match["source_relation"]]        
        target_list = []
        for target_fields in relation_match["target_relations"]:
            target_list.extend([t for t in target if t[1]==target_fields["target_relation"]])
        matches_for_current_relation = perform_fuzzy_matching_for_relations_and_fields(source_list, target_list,threshold_for_fields)
        response_matche.extend(matches_for_current_relation)
    full_matches = set([match[3] for match in response_matche if match[4]==100.00])
    excluded_matches = [match for match in response_matche if match[4]==100.00]
    for i in [x for x in response_matche if x[4]!=100.00]:
        check_exist = check_and_add_record(full_matches,i[3])
        if check_exist:
            pass
        else:
            excluded_matches.append(i)
    return response_matche