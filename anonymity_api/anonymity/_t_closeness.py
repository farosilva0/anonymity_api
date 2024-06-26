import pandas as pd
from anonymity_api.anonymity.utils import anon_functions
from anonymity_api.anonymity.utils import aux_functions


def t_closeness( data, quasi_idents, sens_atts, t, idents = [], corr_att = None, taxonomies= None):
    '''Achieves entropy l-diversity for the given l

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the dataset
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param l: The l to be used in anonymization
    :param idents: List with the identifiers of the dataframe, default is the empty list (no identifiers)
    :param corr_att: attempt to preserve the correlation between this attribute and the sensitive attributes
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: Anonymized dataframe'''

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
    
    return anon_functions.anonymize_t_closeness(partition=data, quasi_idents=quasi_idents, sens_atts=sens_atts, t=t, data=data, explored_qis=[], corr_att= corr_att, taxonomies= taxonomies)