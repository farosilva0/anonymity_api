import pandas as pd
from anonymity_api.anonymity.utils import anon_functions
from anonymity_api.anonymity.utils import aux_functions

def distinct_l_diversity( data, quasi_idents, sens_atts, l, idents= [], corr_att = None, taxonomies = None):
    '''Achieves distinct l-diversity for the given dataframe and l.
    A dataframe is distinct l-diverse if for every equivalence class there are at least l different values
    for every sensitive attribute

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the datafrane
    :param sens_atts: List with the sensitive attributes for the dataframe
    :param l: The l to be used in anonymization (each partition should have l distinct values for each sensitive attribute after anonymization)
    :param idents: List with the identifiers of the dataframe, default is the empty list (no identifiers)
    :param corr_att: attempt to preserve the correlation between this attribute and the sensitive attributes
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: Anonymized dataframe'''
    if (l < 1 or l > data[sens_atts].nunique().min()):
        raise ValueError(f"Invalid value for L. L must be higher than 0 and lower or equal to the number of different values for the least diverse sensitive attributes: ({data[sens_atts].nunique().min()}).")

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
                
    return anon_functions.anonymize_distinct_l(partition=data, quasi_idents=quasi_idents, sens_atts=sens_atts, l=l, explored_qis=[], corr_att= corr_att, taxonomies= taxonomies)




def entropy_l_diversity( data, quasi_idents, sens_atts, l, idents = [], corr_att = None, taxonomies = None):
    '''Achieves entropy l-diversity for the given l

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the dataset
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param l: The l to be used in anonymization
    :param idents: List with the identifiers of the dataframe, default is the empty list (no identifiers)
    :param corr_att: attempt to preserve the correlation between this attribute and the sensitive attributes
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: Anonymized dataframe'''

    if( (not aux_functions.is_entropy_ldiverse(data, sens_atts, l)) or (l <= 1)):
        raise ValueError(f"Invalid value for l")

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
                

    return anon_functions.anonymize_entropy_l(partition=data, quasi_idents=quasi_idents, sens_atts=sens_atts, l=l, explored_qis=[], corr_att= corr_att, taxonomies= taxonomies)


def recursive_cl_diversity(data, quasi_idents, sens_atts, c, l, idents = [], corr_att = None, taxonomies = None):
    '''Achieves recursive (c,l)-diversity for the given l

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the dataset
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param c: the value of c to be used in recursive cl-diversity
    :param l: the value of l to be used in recursive cl-diversity
    :param idents: List with the identifiers of the dataframe, default is the empty list (no identifiers)
    :param corr_att: attempt to preserve the correlation between this attribute and the sensitive attributes
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: Anonymized dataframe'''

    if( l > data[sens_atts].nunique().min()):
        raise ValueError(f"L must be lower or equal to {data[sens_atts].nunique().min()}")

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
                

    return anon_functions.anonymize_recursive_cl(partition=data, quasi_idents=quasi_idents, sens_atts=sens_atts, c=c, l=l, explored_qis=[], corr_att= corr_att, taxonomies = taxonomies)
