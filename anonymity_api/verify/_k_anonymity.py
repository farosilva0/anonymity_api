from anonymity_api.verify.utils import aux_functions

def k_anonymity(data, qis):
    '''Calculates the param k of k-anonymity for the given anonymized dataframe
    
    :param data: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    
    :returns: param k'''

    partitions = aux_functions.get_partitions(data, qis)

    k = min(len(partition) for partition in partitions)

    return k