from anonymity_api.utility.utils import aux_functions
from anonymity_api import verify
import pandas as pd



def discernibility_metric(anon_df, qis):
    '''The discernibility metric gives a penalty to each equivalence class equal to its size.
    The higher the penalty the more indistinguishable records are from each other, resulting in a lower utitlity
    
    :param anon_df: the anonymized dataframe
    :param qis: list with the quasi-identifiers of the dataframe
    
    :returns: the value of the penalty'''

    partitions = aux_functions.get_partitions(anon_df, qis)

    return sum(len(partition) **2 for partition in partitions)

def average_equivalence_class_size(original_df, anon_df, qis):
    '''This metric measures how close the anonymized table is to the best case anonymization.
    It is calculated as |T| / ( |EQs| * k), where |T| represents the length of the original table,
    |EQs| the number of equivalence classes and k the param for k-anonymity
    The closer the final value is to 1 the closer the anonymization is to the best case
    
    :param original df: the original dataframe
    :param anon_df: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    
    :returns: value of the average equivalence class size metric'''
    

    df_size = len(original_df)

    partitions = aux_functions.get_partitions(anon_df, qis)

    ec_num = len(partitions)

    k = verify.k_anonymity(anon_df, qis)

    metric = df_size / (ec_num * k)

    return metric


def global_certainty_penalty(original_df, anon_df, quasi_idents):
    '''The global certainty metric takes the value of the normalized certainty penlaty and tranforms into a value in the range of 0 to 1,
    where 0 means nop information loss, and 1 means total information loss.
    The normalized certainty penalty in an equivalence class for a single quasi identifier is measured as the range of the qi values in the equivalence class
    divided by the range of values in the whole table.
    This functions only implements gcp for numerical attributes, as we would need the taxonomy tree to compute it for categorical attributes
    
    :original_df: original dataframe
    :param anon_df: anonymized dataframe
    :param quasi_idents: quasi-identifiers of the dataframe
    
    :returns: value os the global certainty penalty'''
     
    partitions = aux_functions.get_partitions(anon_df, quasi_idents)
    
    numeric_qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(original_df[qi])]
    if(len(numeric_qis) == 0):
        raise ValueError("Dataframe doesn't have numeric quasi-identifiers.")
    
    range_table = [(original_df[qi].max() - original_df[qi].min()) for qi in numeric_qis]
    
    ncp = 0
    for partition in partitions:
        p_ncp = 0
        
        range_partition = aux_functions.get_range(partition, numeric_qis)
        
        for i in range(len(numeric_qis)):
            
            if( range_table[i] == 0):
                continue
            p_ncp += (range_partition[i] / range_table[i])
            
        p_ncp *= len(partition)
        ncp += p_ncp
        
        
    ncp /=  (len(numeric_qis)  * len(original_df))
    return ncp