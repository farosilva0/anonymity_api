import pandas as pd
from anonymity_api.anonymity.utils import aux_functions
from anonymity_api import anonymity
from anonymity_api import utility


def suggest_anonymity(
    data: pd.DataFrame,
    quasi_idents: list[str],
    sens: list[str],
    idents: list[str] = [],
    queries: list[str] = None,
    taxonomies=None,
):
    """Analyzes the distribution of the quasi-identifiers values and tries to
    suggest an anonymization method to be used in the dataframe that retains utility

    :param data: dataframe to be anonymized
    :param quasi_idents: List with the quasi-identifiers for the dataset
    :param sens: List with the sensitive attributes for the dataset
    :param idents: List with the identifiers of the dataframe, empty if none are given
    :param queries: queries to be preserved on the anonymization
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized data"""

    start = "\033[1m"
    end = "\033[0;0m"

    unique_qis = data[quasi_idents].nunique()
    print(start + "Quasi-identifiers" + end)
    print(
        f"The dataframe has {len(quasi_idents)} quasi_identifiers, and the number of different values per quasi-identifier is: "
    )
    print(unique_qis)

    if queries is not None:
        corr, queries_proc = aux_functions.check_corr(queries)

        queries = corr

        if len(queries_proc) != 0:
            query_df, rest_df = aux_functions.get_query_dataframes(
                data, queries_proc, quasi_idents
            )

            k_val = min(
                aux_functions.find_k(query_df, quasi_idents),
                aux_functions.find_k(rest_df, quasi_idents),
            )

            l_val, entropy_l, c_val, recur_l = aux_functions.find_l(
                query_df, sens, k_val
            )
            l_val2, entropy_l2, c_val2, recur_l2 = aux_functions.find_l(
                data, sens, k_val
            )

            l_val = min(l_val, l_val2)
            entropy_l = min(entropy_l, entropy_l2)
            if recur_l2 < recur_l:
                recur_l = recur_l2
                c_val = c_val2

    print(start + "\nsensitive attributes" + end)
    unique_sas = data[sens].nunique()
    print(
        f"The dataframe has {len(sens)} sensitive attribute and the number of different values per attribute is: "
    )
    print(unique_sas)

    k_val = aux_functions.find_k(data, quasi_idents)
    l_val, entropy_l, c_val, recur_l = aux_functions.find_l(data, sens, k_val)

    print(start + "\nAttempting the following anonymizations: " + end)

    print(f"K-anonymization with k = {k_val:2f}")

    best_df, min_util = None, float("inf")
    chosen = ""

    k_anon = None

    if queries is None:
        k_anon = anonymity.k_anonymity(
            data, quasi_idents, k_val, idents, taxonomies=taxonomies
        )
    else:
        k_anon = anonymity.workload_aware_k_anonymity(
            data, quasi_idents, k_val, queries, idents, taxonomies=taxonomies
        )

    k_anon_utility = utility.global_certainty_penalty(data, k_anon, quasi_idents)
    print(f"Utility for k-anonymization: {str(k_anon_utility)}")

    if k_anon_utility < min_util:
        min_util = k_anon_utility
        best_df = k_anon
        chosen = "k-anonymity"

    print(f"\nDistinct l-diversity with l = {l_val}")

    l_div = None

    if queries is None:
        l_div = anonymity.distinct_l_diversity(data, quasi_idents, sens, l_val, idents)
    else:
        l_div = anonymity.workload_aware_distinct_l_diversity(
            data, quasi_idents, sens, l_val, queries, idents, taxonomies=taxonomies
        )

    l_div_utility = utility.global_certainty_penalty(data, l_div, quasi_idents)
    print(f"Utility for distinct l-diversity: {str(l_div_utility)}")

    if l_div_utility < min_util:
        min_util = l_div_utility
        best_df = l_div
        chosen = "l-diversity"

    print(f"\nEntropy l-diversity with l = {entropy_l:2f}")

    entropy_div = None

    if queries is None:
        entropy_div = anonymity.entropy_l_diversity(
            data, quasi_idents, sens, entropy_l, idents, taxonomies=taxonomies
        )
    else:
        entropy_div = anonymity.workload_aware_entropy_l_diversity(
            data, quasi_idents, sens, entropy_l, queries, idents, taxonomies=taxonomies
        )

    entropy_utility = utility.global_certainty_penalty(data, entropy_div, quasi_idents)
    print(f"Utility for entropy l-diversity: {str(entropy_utility)}")

    if entropy_utility < min_util:
        min_util = entropy_utility
        best_df = entropy_div
        chosen = "entropy l-diversity"

    print(f"\nRecursive (c,l)-diversity with c = {c_val} and l = {recur_l}")

    r_cl = None
    if queries is None:
        r_cl = anonymity.recursive_cl_diversity(
            data, quasi_idents, sens, c_val, recur_l, idents, taxonomies=taxonomies
        )
    else:
        r_cl = anonymity.workload_aware_recursive_c_l_diversity(
            data,
            quasi_idents,
            sens,
            c_val,
            recur_l,
            queries,
            idents,
            taxonomies=taxonomies,
        )

    r_cl_utility = utility.global_certainty_penalty(data, r_cl, quasi_idents)
    print(f"Utility for recursive (c,l)-anonymization: {str(r_cl_utility)}")

    if r_cl_utility < min_util:
        min_util = r_cl_utility
        best_df = r_cl
        chosen = "recursive_cl_diversity"

    print(
        f"{start}\nReturning the result from {chosen}, with utility of {min_util}.{end}"
    )

    return best_df


def suggest_anonymity_groups(
    data, quasi_idents, sens, queries, idents=[], taxonomies=None
):
    groups, queries_proc = aux_functions.check_group(queries)

    arg_groups, val_groups = aux_functions.process_groups(groups, quasi_idents)

    data_frames = aux_functions.get_group_dataframes(data, arg_groups, val_groups)

    data_frames = [
        suggest_anonymity(data_frames[i], quasi_idents, sens, idents, None, taxonomies)
        for i in range(len(data_frames))
    ]

    return pd.concat(data_frames).reset_index(drop=True)

