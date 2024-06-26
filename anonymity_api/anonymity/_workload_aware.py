from anonymity_api import anonymity
from anonymity_api.anonymity.utils import aux_functions
import pandas as pd

def workload_aware_k_anonymity( data, quasi_idents, k, queries, idents = [], taxonomies= None):
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymized dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param k: k to be used in k-anonymization
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    groups, queries_proc = aux_functions.check_group( queries )
    
    corr, queries_proc = aux_functions.check_corr( queries_proc )
    
    arg_corr = None
    
    arg_groups = val_groups = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
        
    if len(groups) != 0 :
            
            arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)
            
            data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)
            
            data_frames = [anonymity.k_anonymity(data_frames[i], quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies) for i in range(len(data_frames))]
            
            return pd.concat(data_frames).reset_index(drop=True)
    if len(queries_proc) != 0: 
        query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
        
        return pd.concat([anonymity.k_anonymity(query_df, quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies),
                    anonymity.k_anonymity(rest_df, quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    
    else:
        return anonymity.k_anonymity(data, quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)
    
    
def workload_aware_distinct_l_diversity(data, quasi_idents, sens_atts, l, queries, idents = [], taxonomies= None): 
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param l: l to be used in distinct l-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    groups, queries_proc = aux_functions.check_group( queries )
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    arg_corr = None
    
    arg_groups = val_groups = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    if len(groups) != 0 :
            
        arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)
        
        data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)
        
        data_frames = [anonymity.distinct_l_diversity(data_frames[i], quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies) for i in range(len(data_frames))]
        
        return pd.concat(data_frames).reset_index(drop=True)
    
    if len(queries_proc) != 0:   
        query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
        
        return pd.concat([anonymity.distinct_l_diversity(query_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.distinct_l_diversity(rest_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    else:
        return anonymity.distinct_l_diversity(data, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)

def workload_aware_entropy_l_diversity(data, quasi_idents, sens_atts, l, queries, idents = [], taxonomies= None): 
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param l: l to be used in entropy l-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    groups, queries_proc = aux_functions.check_group( queries )
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    arg_corr = None
    
    arg_groups = val_groups = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    if len(groups) != 0 :
        
        arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)
        
        data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)
        
        data_frames = [anonymity.entropy_l_diversity(data_frames[i], quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies) for i in range(len(data_frames))]
        
        return pd.concat(data_frames).reset_index(drop=True)
        
    if len(queries_proc) != 0:        
        query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
        
        return pd.concat([anonymity.entropy_l_diversity(query_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.entropy_l_diversity(rest_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    else:
        return anonymity.entropy_l_diversity(data, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)
    
def workload_aware_recursive_c_l_diversity(data, quasi_idents, sens_atts, c, l, queries, idents = [], taxonomies= None):  
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param c: value of c to be used in recursive (c,l)-diversity
    :param l: value of l to be used in recursive (c,l)-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    groups, queries_proc = aux_functions.check_group( queries )
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    arg_corr = None
    
    arg_groups = val_groups = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    if len(groups) != 0 :
        
        arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)
        
        data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)
        
        data_frames = [anonymity.recursive_cl_diversity(data_frames[i], quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies) for i in range(len(data_frames))]
        
        return pd.concat(data_frames).reset_index(drop=True)
        
    if len(queries_proc) != 0: 
        query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
               
        return pd.concat([anonymity.recursive_cl_diversity(query_df, quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.recursive_cl_diversity(rest_df, quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    else:
        return anonymity.recursive_cl_diversity(data, quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)

def workload_aware_t_closeness(data, quasi_idents, sens_atts, t, queries, idents = [], taxonomies= None):
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param t: t to be used in t-closeness
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    groups, queries_proc = aux_functions.check_group( queries )
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    arg_corr = None
    
    arg_groups = val_groups = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    if len(groups) != 0 :
        
        arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)
        
        data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)
        
        data_frames = [anonymity.t_closeness(data_frames[i], quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies) for i in range(len(data_frames))]
        
        return pd.concat(data_frames).reset_index(drop=True)

    if len(queries_proc) != 0:
        query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)

        return pd.concat([anonymity.t_closeness(query_df, quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.t_closeness(rest_df, quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    else:
        return anonymity.t_closeness(data, quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)
