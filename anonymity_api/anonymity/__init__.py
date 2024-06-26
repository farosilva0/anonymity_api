from ._k_anonymity import k_anonymity
from ._l_diversity import distinct_l_diversity
from ._l_diversity import entropy_l_diversity
from ._l_diversity import recursive_cl_diversity
from ._t_closeness import t_closeness
from ._workload_aware import workload_aware_k_anonymity
from ._workload_aware import workload_aware_distinct_l_diversity
from ._workload_aware import workload_aware_entropy_l_diversity
from ._workload_aware import workload_aware_recursive_c_l_diversity
from ._workload_aware import workload_aware_t_closeness
from ._suggestion import suggest_anonymity
from ._suggestion import suggest_anonymity_groups

'''This module holds the functions to anonymize datasets'''

__all__ = [
    'k_anonymity',
    'distinct_l_diversity',
    'entropy_l_diversity',
    'recursive_cl_diversity',
    't_closeness',
    'workload_aware_k_anonymity',
    'workload_aware_distinct_l_diversity',
    'workload_aware_entropy_l_diversity',
    'workload_aware_recursive_c_l_diversity',
    'workload_aware_t_closeness',
    'suggest_anonymity',
    'suggest_anonymity_groups'
]