import pandas as pd
from itertools import accumulate
import math


def choose_dimension(partition, quasi_idents, explored_qis, corr_att):
    """Chooses the dimension to use for partitioning according to the highest diversity of values heuristic

    :param partition: partition to use for choosing the dimension
    :param quasi_idents: List with the quasi-identifers of the given partition
    :param explored_qis: List with the quasi-identiifers that have already been the chosen dimension for this partition
    :param corr_att: attribute to keep in the correlation, if it is hasn't been explored it will be selected

    :returns: The attribute chosen as dimension"""

    if explored_qis != []:
        quasi_idents = [qi for qi in quasi_idents if qi not in explored_qis]

    if corr_att is not None and len(corr_att) != 0:
        for corr in corr_att:
            if corr in quasi_idents:
                explored_qis.append(corr)
                return corr, explored_qis

    atts_dim = partition[quasi_idents].nunique().to_dict()
    sorted_atts_dim = sorted(atts_dim.items(), key=lambda x: x[1], reverse=True)

    dim = sorted_atts_dim[0][0]
    explored_qis.append(dim)

    return dim, explored_qis


def frequency_set(partition, dim):
    """Creates a list with all the the values in the dimension's collumn

    :param partition: dataframe used to create the frequency set
    :param dim: dimensation chosen for the frequency_set

    :returns: list with all the values for the dimension in the given dataframe"""
    return partition[dim].to_list()


def find_median(fs):
    """Calculates the value of the median in the frequency set

    :param fs: frequency set to evaluate

    :returns: value of the median"""

    data_len = len(fs)
    split = data_len // 2

    if data_len % 2 == 0:
        return (fs[split - 1] + fs[split]) / 2

    else:
        return fs[split]


def summary(partition, quasi_idents, taxonomies):
    """Generalizes the quasi_identifiers in the given partition, replacing them with an interval between the lowest and highest values

    :param partition: partition to be generalized
    :param quasi_idents: quasi-identifiers to be generalized
    :param taxonomies: hierarchy to be used for quasi-identifer anonymization ( categorical quasi-identifiers )

    :returns: generalized partition"""

    partition = partition.copy()

    for qi in quasi_idents:
        min_val = partition[qi].min()
        max_val = partition[qi].max()

        if pd.api.types.is_string_dtype(partition[qi]):
            if taxonomies is not None:
                vals = taxonomies.get(qi)

                if vals:
                    values_attribute = partition[qi].to_list()

                    gen_val = find_common_val(values_attribute, vals)

                    partition[qi] = gen_val

            else:
                gen_val = ""
                for val in partition[qi].unique():
                    gen_val += val + "-"

                gen_val = gen_val[:-1]
                partition[qi] = gen_val

        elif min_val != max_val:
            gen_val = f"{min_val} - {max_val}"
            partition[qi] = gen_val

    return partition


def is_entropy_ldiverse(partition, sens_atts, l):
    """Verifies if the given partition is entropy l-diverse for the given l

    :param partition: partition to evaluate
    :param sens_atts: sensitive attributes of the partition
    :param l: value for entropy l-diversity

    :returns: evaluates the partition and returns true if it is entropy l-diverse, otherwise false"""

    for sa in sens_atts:
        sum_entropy = 0

        fs = partition[sa].value_counts()
        fs_dict = fs.to_dict()

        for key in fs_dict:
            fraction = fs_dict[key] / len(partition)

            sum_entropy += fraction * math.log(fraction)

        if -sum_entropy < math.log(l):
            return False

    return True


def is_recursive_cldiverse(partition, sens_atts, c, l):
    """Verifies if the given partition is recursive cl-diverse for the given c and l, (r1 < c((rl) + (rl+1) + ...))

    :param partition: partition to be evaluated
    :param sens_atts: partition's sensitive attributes
    :param c: value for c in the formula
    :param l: value for l in the formula

    :returns: True if recursive cl-diverse, otherwise false"""

    if partition[sens_atts].nunique().min() < l:
        return False

    for sa in sens_atts:
        fs = partition[sa].value_counts().to_dict()
        fs = sorted(fs.items(), key=lambda x: x[1], reverse=True)

        r1 = fs[0][1]

        sum_r = 0

        for i in range(int(l - 1), len(fs)):
            sum_r += fs[i][1]

        if r1 > (c * sum_r):
            return False

    return True


def is_t_close_numerical(partition, sa, t, data_set):
    """Checks t-closeness for numerical attributes using Ordered Distance

    :param partition: partition to evaluate
    :param sa: sensitive attribute to evaluate
    :param t: threshold for t-closeness
    :param data_set: original data set in order to compare the distance between distributions

    :returns: true if t-close, otherwise false"""

    partition = partition.copy()
    data = data_set.copy()

    partition = partition.sort_values(by=sa)
    data = data.sort_values(by=sa)

    values = data_set[sa].to_list()
    values_size = len(values)

    p = [len(data[data[sa] == v]) / len(data) for v in values]
    q = [len(partition[partition[sa] == v]) / len(partition) for v in values]

    r = [p[i] - q[i] for i in range(values_size)]

    abs_r = sum(abs(aux_r) for aux_r in accumulate(r))

    t_partition = 1 / (values_size - 1) * abs_r

    return t_partition <= t


def is_t_close_categorical(partition, sa, t, data_set):
    """Checks t-closeness for categorical attributes using Equal Distance

    :param partition: partition to evaluate
    :param sa: sensitive attribute to evaluate
    :param t: threshold for t-closeness
    :param data_set: original data set in order to compare the distance between distributions

    :returns: true if t-close, otherwise false"""

    partition = partition.copy()
    data = data_set.copy()

    partition = partition.sort_values(by=sa)
    data = data.sort_values(by=sa)

    values = data_set[sa].to_list()
    values_size = len(values)

    p = [len(data[data[sa] == v]) / len(data) for v in values]
    q = [len(partition[partition[sa] == v]) / len(partition) for v in values]

    r = [p[i] - q[i] for i in range(values_size)]

    abs_r = sum(abs(r_i) for r_i in r)

    t_partition = (1 / 2) * abs_r

    return t_partition <= t


def is_t_close(partition, sens_atts, t, data_set):
    """Checks t-closeness for the given partition

    :param partition: partition to evaluate
    :param sens_atts: partition's sensitive attributes
    :param t: threshold for t-closeness
    :param data_set: original data set in order to compare the distance between distributions

    :returns: true if t-close, otherwise false"""

    for sa in sens_atts:
        if pd.api.types.is_numeric_dtype(partition[sa]):
            if not is_t_close_numerical(partition, sa, t, data_set):
                return False

        elif pd.api.types.is_string_dtype(partition[sa]):
            if not is_t_close_categorical(partition, sa, t, data_set):
                return False

    return True


def get_group_dataframes(data, group_qi, val):
    """Divides the dataframe into groups that respect the given grouping

    :param data: dataframe to be divided
    :param group_qi: quasi-identifier to group
    :param val: value to group by

    :returns: list of dataframes that respect the grouping"""

    data = data.copy()
    total = 0
    groups = list()

    while total < data[group_qi].max():
        old_val = total
        total += val
        query = f"{group_qi} <= {total} and {group_qi} > {old_val}"
        groups.append(data.query(query))

    groups = [group for group in groups if not group.empty]
    return groups


def get_query_dataframes(data, querys, quasi_idents):
    """Executes all querys into the data and the returns two dataframes.
    1. Dataframe of the conjunction of all queries
    2. Rest of the original dataframe

    :param data: original dataframe
    :param querys: the querys to execute of the dataframe
    :param quasi_idents: quasi-identifers of the data

    :returns: 2 dataframes of the querys"""

    query_df = data

    for query_string in querys:
        if query_string.split(" ")[0] in quasi_idents:
            query_df = query_df.query(query_string)
        else:
            raise TypeError("The query must be done on a quasi-identifier")

    rest_df = data.drop(query_df.index)

    return query_df, rest_df


def check_corr(queries):
    """Receives all the queries and verifies if any of them is a correlation

    :param queries: the queries to analyzae

    :returns: the correlation if it exists, and the rest of the querys"""

    aux = queries.copy()

    corrs = list()

    for query in aux:
        if query.strip().find("corr") == 0:
            corrs.append(query)

    for query in corrs:
        aux.remove(query)

    return corrs, aux


def check_group(queries):
    """Receives all the queries and if verifies if any of them is a grouping

    :param queries: the queries to analyze

    :returns: the grouping if it exists, and the rest of the querys"""

    aux = queries.copy()

    groups = list()

    for query in aux:
        if query.strip().find("group") == 0:
            groups.append(query)

    for query in groups:
        aux.remove(query)

    return groups, aux


def process_corr(corrs, quasi_idents):
    """Receives the correlation to be done and retreives the quasi-identifier
    in the correlation

    :param corrs: correlation to analyze
    :param quasi_idents: all the quasi-identifiers

    :returns: the quasi-identifier in the correlation"""

    args = list()

    for corr in corrs:
        params = corr.split("(")[1].split(")")[0].split(",")
        params = [param.strip() for param in params]

        for qi in quasi_idents:
            for arg in params:
                if qi == arg:
                    args.append(qi)

    return args


def process_groups(groups, quasi_idents):
    """Receives the grouping to be done and retreives the quasi-identifier
    in the grouping

    :param groups: grouping to analyze
    :param quasi_idents: all the quasi-identifiers

    :returns: the quasi-identifier in the grouping"""

    args = None
    vals = None

    for group in groups:
        params = group.split("(")[1].split(")")[0].split(",")
        params = [param.strip() for param in params]

        if params[0] in quasi_idents:
            args = params[0]
            vals = params[1]

    return args, int(vals)


def find_k(data, quasi_idents):
    """Tries to find a k to use in k-anonymization.
    Chooses the k has being the average number of unique values for all quasi-identifiers

    :param data: the dataframe
    :param quasi_idents: quasi-identifiers of the dataframe

    :returns: value for k"""

    list_avg = list()
    for qi in quasi_idents:
        df = data[qi].value_counts().to_list()
        avg = sum(df) / data[qi].nunique()
        list_avg.append(avg)

    k_val = sum(list_avg) / len(list_avg)

    uniques = data[quasi_idents].nunique().to_list()
    uniques.sort()

    return math.ceil(min(k_val, uniques[len(uniques) // 2 - 1]))


def find_l(data, sens, k_val):
    """Tries to find the values to use in all kinds of l-diversity.
    For l-diversity its chosen the minimum between the sensitive attribute with the lowest unique value, and the minimum average of tuples per different value in a sensitive attribute.
    The value of l for entropy l-diversity is log( average number of unique values per sensitive-attribute )

    :param data: dataframe to anonymize
    :param sens: sensitive attributes of the dataframe

    :returns: the values to use in distinct l-diversity, entropy l-diversity and
    recursive c,l-diversity"""

    unique_sas = data[sens].nunique()
    min_vals = unique_sas.idxmin()

    value_counts = data[min_vals].value_counts().to_list()

    least_common = 0

    for sa in sens:
        vc = data[sa].value_counts().to_list()

        med_vc = sum(vc) / len(vc)

        if med_vc > least_common:
            least_common = med_vc

    l_val = recur_l = int(min(least_common, data[sens].nunique().min()))

    entropy_l = (data_entropy(data, sens) + 1.1) / 2

    if l_val == 1:
        mean_log = math.log(unique_sas.mean())
        if mean_log > 1 and entropy_l < 1:
            entropy_l = mean_log
        elif mean_log > 1 and entropy_l > 1:
            entropy_l = min(entropy_l, math.log(unique_sas.mean()))

        l_val = k_val

    c_val = int(len(data) / sum(value_counts[recur_l - 1 :]))

    return l_val, entropy_l, c_val, recur_l


def data_entropy(partition, sens_atts):
    """Returns the data's entropy

    :param partition: partition to evaluate
    :param sens_atts: sensitive attributes of the partition

    :returns: the entropy value"""

    min_entropy = float("+inf")
    for sa in sens_atts:
        sum_entropy = 0

        fs = partition[sa].value_counts()
        fs_dict = fs.to_dict()

        for key in fs_dict:
            fraction = fs_dict[key] / len(partition)

            sum_entropy += fraction * math.log(fraction)

        if (math.e**-sum_entropy) < min_entropy:
            min_entropy = math.e**-sum_entropy

    return min_entropy


def create_hierarchies(filename):
    """Creates a dictionary with the hierarchy for the values stored in the given file

    :param filename: path to the file containing the hierarchies

    :returns: python dicionary with the hierarchy"""

    map = dict()

    file = open(filename, "r")

    for line in file:
        line = line.rstrip()
        values = line.split(";")

        values = [value.strip() for value in values]

        map.update({values[0]: values})

    return map


def find_common_val(attributes, hierachy_map):
    """Receives a group of attributes and finds the 1st value in common they share in their hierarchies

    :param attributes: the attributes to evaluate
    :param hierarchy_map: dictionary with hierarchys for all attributes

    :returns: 1st value they have in common, otherwise returns "*" """

    hierarchy = [hierachy_map[att] for att in attributes]

    common_vals = set.intersection(*map(set, hierarchy))

    for val in hierarchy[0]:
        if val in common_vals:
            return val

    return "*"

