import pandas as pd
from anonymity_api.verify.utils import aux_functions

def distinct_l_diversity(data, qis, sa):
    '''Calculates the param l of distinct l-diversity for the given anonymized dataframe
    
    :param data: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    
    :returns: param l'''

    partitions = aux_functions.get_partitions(data, qis)

    l = min(partition[sa].nunique().min() for partition in partitions)

    return l



def entropy_l_diversity(data, qis, sens_atts):
    '''Calculates the param l of entropy l-diversity for the given anonymized dataframe
    
    :param data: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    :param sens_atts: sensitive attributes of the dataframe
    
    :returns: param l'''

    partitions = aux_functions.get_partitions(data, qis)

    l = min(aux_functions.l_entropy(partition, sens_atts) for partition in partitions)

    return l


def recursive_cl_diversity(data, qis, sens_atts):
    '''Calculates params c and l of recursice (c,l)-diversity for the given anonymized dataframe
    
    :param data: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    :param sens_atts: sensitive attributes of the dataframe
    
    :returns: params c and l'''
    
    l = distinct_l_diversity(data, qis, sens_atts)

    partitions = aux_functions.get_partitions(data, qis)

    c = max(aux_functions.recursive_cl_diverse(partition, sens_atts, l) for partition in partitions)

    return c, l

