import pandas as pd
from itertools import accumulate
import math

def get_partitions(data, qis):
    '''Divides the given dataframe into partitions and returns a list with all
    the partitions
    
    :param data: the dataframe to be evaluated
    :param qis: the quasi-identifiers of the dataframe
    
    :returns: a list with all the partitions'''

    grouped_data = data.groupby(qis)

    partitions = list()

    for qis, group in grouped_data:
        partitions.append(group)

    return partitions


def l_entropy(partition, sens_atts):
    '''Calculates the entropy for the given partition
    
    :param partition: equivalence class of an anonymized dataframe
    :param sas: the sensitive attributes of the dataframe
    
    :returns: the entropy of the partition'''

    sum_entropy = 0

    for sa in sens_atts:

        fs = partition[sa].value_counts()
        fs_dict = fs.to_dict()

        for key in fs_dict:

            fraction = (fs_dict[key] / len(partition))

            sum_entropy += (fraction * math.log(fraction))

    return (math.e ** -(sum_entropy))


def recursive_cl_diverse(partition, sens_atts, l):
    '''Calculates param c of recursive (c,l) diversity for the given partition
    
    :param partition: equivalence class of the dataframe
    :param sens_atts: list of sensitive attributes of the dataframe
    :param l: the amount of minimum distinct values each sensitive attribute has for each equivalence class / l for distinct l-diversity
    
    :returns: value of param c'''

    c = 0

    for sa in sens_atts:
        fs = partition[sa].value_counts().to_dict()
        fs = sorted(fs.items(), key= lambda x: x[1], reverse=True)

        r1 = fs[0][1]

        sum_r = 0

        for i in range(l-1, len(fs)):
            sum_r += fs[i][1]

        c = max(c, math.ceil(r1 / sum_r))

    return c



def t_closeness(partition, sens_atts, data_set):
    '''Calculates the param t of t-closeness for the given partition
    
    :param partition: equvivalence class of the dataframe
    :param sens_atts: sensitive attributes of the dataframe
    :param data_set: anonymized dataframe
    
    :returns: param t for the given partition'''
    
    t = 0

    for sa in sens_atts:

        if (pd.api.types.is_numeric_dtype(partition[sa])):
            t = max(t, t_close_numerical(partition, sa, data_set))
            
            
        elif (pd.api.types.is_string_dtype(partition[sa])):
            t = max(t, t_close_categorical(partition, sa, data_set))
                
             
    return t

def t_close_categorical(partition, sens_att, data_set):
    '''Calculates the param t of t-closeness for categorical attributes.
    For categorical attributes we use the equal distance metric where the distance 
    between any two different values is 1.
    
    :param partition: equvivalence class of the dataframe
    :param sens_att: sensitive attributeo to evaluate
    :param data_set: anonymized dataframe
    
    :returns: param t for the given partition'''
    
    partition = partition.copy()
    data = data_set.copy()

    partition = partition.sort_values(by= sens_att)
    data = data.sort_values(by= sens_att)
    
    values = data_set[sens_att].to_list()
    values_size = len(values)

    p = [len(data[data[sens_att] == v]) / len(data) for v in values]
    q = [len(partition[partition[sens_att] == v]) / len(partition) for v in values]

    r = [p[i] - q[i] for i in range(values_size)]

    abs_r = sum( abs(r_i) for r_i in r)

    t_partition = (1/2) * abs_r

    return t_partition


def t_close_numerical(partition, sens_att, data_set):
    '''Calculates the param t of t-closeness for numerical attributes.
    For categorical attributes the distance between any two different values is calculated as their difference.
    
    :param partition: equvivalence class of the dataframe
    :param sens_att: sensitive attributeo to evaluate
    :param data_set: anonymized dataframe
    
    :returns: param t for the given partition'''
    

    partition = partition.copy()
    data = data_set.copy()

    partition = partition.sort_values(by= sens_att)

    data = data.sort_values(by= sens_att)
    
    values = data_set[sens_att].to_list()
    values_size = len(values)

    p = [len(data[data[sens_att] == v]) / len(data) for v in values]
    q = [len(partition[partition[sens_att] == v]) / len(partition) for v in values]

    r = [p[i] - q[i] for i in range(values_size)]

    abs_r = sum(abs(aux_r) for aux_r in accumulate(r))

    t_partition = 1 / (values_size-1) * abs_r

    return t_partition