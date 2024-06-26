import pandas as pd
from anonymity_api.anonymity.utils import anon_functions
from anonymity_api.anonymity.utils import aux_functions



def k_anonymity( data, quasi_idents, k, idents = [], corr_att= None, taxonomies = None):
    '''Achieves k-anonymity for the given dataframe and k. 
    A dataframe is said to be k-anonymies if for every tuple there are at least k-1 tuples
    with the same values for the quasi-identifier attributes

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the dataset
    :param k: The k to be used in anonymization (each tuple should have k-1 tuples with the same values for quasi-identifiers after anonymization)
    :param idents: List with the identifiers of the dataframe, default is the empty list (no identifiers)
    :param corr_att: attempt to preserve the correlation between this attribute and the sensitive attributes
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: Anonymized dataframe'''
    
    if (k < 1 or k > len(data)):
        raise ValueError(f"Invalid value for K. K must be higher than 0 and lower or equal to the the dataframe's length ({len(data)}).")

    if(idents != []):
        for sa in idents:
            del(data[sa])
            
    if( taxonomies is not None):
        for key in taxonomies.keys():
            if( pd.api.types.is_string_dtype(data[key])):
                filename = taxonomies.get(key)
                
                hierarchy_map = aux_functions.create_hierarchies(filename)
                
                taxonomies.update({key: hierarchy_map})
            else:
                del(taxonomies[key])
        
    return anon_functions.anonymize_k(data, quasi_idents, k, [], corr_att, taxonomies)