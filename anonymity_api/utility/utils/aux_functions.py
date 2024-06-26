import numpy as np

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



def get_range(data, qis):
    '''Gets the maximum and minimum value for each quasi-identifier in the given anonymized dataframe
    
    :param data: anonymized dataframe
    :param qis: quasi-identifiers of the dataframe
    
    :returns: a list with the maximum values, and a list with the minimum values'''
    
    max_values = [float('-inf')] * len(qis)
    min_values = [float('inf')] * len(qis)
    
    for index, tuple in data.iterrows():
        
        
        for i in range(len(qis)):
            
            value = str(tuple[qis[i]])
            
            value_split = value.split(' ')
            
            if(len(value_split) > 1):
                if( np.isnan(float(value_split[0])) or np.isnan(float(value_split[2]))):
                    min_values[i] = 0
                    max_values[i] = 0
                else:
                    min_values[i] = min(min_values[i], float(value_split[0]))
                    
                    max_values[i] = max(max_values[i], float(value_split[2]))
            else:
                
                if( np.isnan(float(value))):
                    min_values[i]= 0
                    max_values[i] = 0
                else:
                    min_values[i] = float(value)
                    
                    max_values[i] = float(value)

                     
    range_values = [max_values[i] - min_values[i] for i in range(len(max_values))]
    return range_values


def is_num( value ):
    '''Verifies if a generalized value is composed of numbers or categorical values'''
    try:
        float(value)
        return True
    except ValueError:
        return False
            
            