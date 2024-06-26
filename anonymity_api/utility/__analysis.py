from anonymity_api.utility.utils import aux_functions
import random

def generalize_intervals( data, qis, decimals = None ):
    '''This function receives an anonymized dataset and replaces the generalized values ( intervals or a list of possible values ) with a random value.
    This allows the data to be used in data analysis functions such as correlations, or means that will evaluate these values
    
    :param data: dataframe to evaluate
    :param qis: attributes that are anonymized
    :param decimals: attributes that should be anonymized into decimal values rahter than integers'''
    
    df = data.copy()
    
    if( decimals is None ):
        for index, row in df.iterrows():
            for i in range(len(qis)):
                value = str(row[qis[i]]).rstrip()
                value_str = value.split(' - ')
                
                if len(value_str) > 1:
                    if len(value_str) > 2:
                        df.loc[index, qis[i]] = value_str[random.randint(0, len(value_str) - 1)]
                    else:
                        if aux_functions.is_num(value_str[0]):
                            df.loc[index, qis[i]] = random.randint(int(float(value_str[0])), int(float(value_str[1])))
                        else:
                            df.loc[index, qis[i]] = value_str[random.randint(0, len(value_str) - 1)]
    else:
        for index, row in df.iterrows():
            for i in range(len(qis)):
                value = str(row[qis[i]]).rstrip()
                value_str = value.split(' - ')
                
                if len(value_str) > 1:
                    if len(value_str) > 2:
                        df.loc[index, qis[i]] = value_str[random.randint(0, len(value_str) - 1)]
                    else:
                        if aux_functions.is_num(value_str[0]):
                            if qis[i] in decimals:
                                df.loc[index, qis[i]] = random.uniform(int(float(value_str[0])), int(float(value_str[1])))
                            else:    
                                df.loc[index, qis[i]] = random.randint(int(float(value_str[0])), int(float(value_str[1])))
                        else:
                            df.loc[index, qis[i]] = value_str[random.randint(0, len(value_str) - 1)]
                        
    return df