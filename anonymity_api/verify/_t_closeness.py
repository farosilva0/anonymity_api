from anonymity_api.verify.utils import aux_functions
import pandas as pd


def t_closeness(data, qis, sens_atts):
    '''Calculates param t of t-closeness for the given anonymized dataframe.
    
    :param data: anonymized dataframe
    :param qis: quasi identifiers of the dataframe
    :param sens_atts: sensitive attributes of the dataframe
    
    :returns: value of param t'''

    partitions = aux_functions.get_partitions(data, qis)

    t = max(aux_functions.t_closeness(partition, sens_atts, data) for partition in partitions)

    return t