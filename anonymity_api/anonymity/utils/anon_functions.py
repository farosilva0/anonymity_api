from codecs import ascii_encode
import random

import numpy as np
import pandas as pd

from anonymity_api.anonymity.utils import aux_functions
from sentence_transformers import SentenceTransformer
from scipy.cluster.hierarchy import linkage, leaves_list


def anonymize_k(partition, quasi_idents, k, explored_qis, corr_att, taxonomies):
    """Anonymizes a dataset according to k-anonymization

    :param partition: partition to be anonymized
    :param quasi_idents: quasi-identifiers of the given partition
    :param k: the value of k to be used in k-anonymization
    :param explored_qis: quasi-identifiers that have already been used when trying to partition the given dataset
    :param corr_att: attribute to keep in the correlation
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized version of the partition"""

    qis = quasi_idents.copy()

    qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(partition[qi])]

    if (len(partition) < (2 * k)) or (set(qis) == set(explored_qis)):
        return aux_functions.summary(partition, quasi_idents, taxonomies)

    dim, explored_qi = aux_functions.choose_dimension(
        partition, qis, explored_qis, corr_att
    )
    partition = partition.sort_values(by=dim).reset_index(drop=True)

    fs = aux_functions.frequency_set(partition, dim)

    split_val = aux_functions.find_median(fs)

    lhs = partition[partition[dim] <= split_val]
    rhs = partition[partition[dim] > split_val]

    if (len(lhs) >= k) and (len(rhs) >= k):
        return pd.concat(
            [
                anonymize_k(lhs, quasi_idents, k, [], corr_att, taxonomies),
                anonymize_k(rhs, quasi_idents, k, [], corr_att, taxonomies),
            ]
        ).reset_index(drop=True)

    return anonymize_k(partition, quasi_idents, k, explored_qi, corr_att, taxonomies)


def anonymize_distinct_l(
    partition, quasi_idents, sens_atts, l, explored_qis, corr_att, taxonomies
):
    """Anonymizes a dataset according to distinct l-diversity

    :param partition: partition to be anonymized
    :param quasi_idents: quasi-identifiers of the given partition
    :param sens_atts: list with the sensitive attributes for the given dataframe
    :param l: the value of l to be used in distinct l-diversity
    :param explored_qis: quasi-identifiers that have already been used when trying to partition the given dataset
    :param corr_att: attribute to keep in the correlation
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized version of the partition"""

    qis = quasi_idents.copy()

    qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(partition[qi])]

    if (len(partition) < (2 * l)) or (set(qis) == set(explored_qis)):
        return aux_functions.summary(partition, quasi_idents, taxonomies)

    dim, explored_qi = aux_functions.choose_dimension(
        partition, qis, explored_qis, corr_att
    )
    partition = partition.sort_values(by=dim).reset_index(drop=True)

    fs = aux_functions.frequency_set(partition, dim)

    split_val = aux_functions.find_median(fs)

    lhs = partition[partition[dim] <= split_val]
    rhs = partition[partition[dim] > split_val]

    if (lhs[sens_atts].nunique().min() >= l) and (rhs[sens_atts].nunique().min() >= l):
        return pd.concat(
            [
                anonymize_distinct_l(
                    lhs, quasi_idents, sens_atts, l, [], corr_att, taxonomies
                ),
                anonymize_distinct_l(
                    rhs, quasi_idents, sens_atts, l, [], corr_att, taxonomies
                ),
            ]
        ).reset_index(drop=True)

    return anonymize_distinct_l(
        partition, quasi_idents, sens_atts, l, explored_qi, corr_att, taxonomies
    )


def anonymize_entropy_l(
    partition, quasi_idents, sens_atts, l, explored_qis, corr_att, taxonomies
):
    """Anonymizes a dataset according to entropy l-diversity

    :param partition: partition to be anonymized
    :param quasi_idents: quasi-identifiers of the given partition
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param l: the value of l to be used in entropy l-diversity
    :param explored_qis: quasi-identifiers that have already been used when trying to partition the given dataset
    :param corr_att: attribute to keep in the correlation
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized version of the partition"""

    qis = quasi_idents.copy()

    qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(partition[qi])]

    if set(qis) == set(explored_qis):
        if aux_functions.is_entropy_ldiverse(partition, sens_atts, l):
            return aux_functions.summary(partition, quasi_idents, taxonomies)

        else:
            return pd.DataFrame()

    dim, explored_qi = aux_functions.choose_dimension(
        partition, qis, explored_qis, corr_att
    )
    partition = partition.sort_values(by=dim).reset_index(drop=True)

    fs = aux_functions.frequency_set(partition, dim)

    split_val = aux_functions.find_median(fs)

    lhs = partition[partition[dim] <= split_val]
    rhs = partition[partition[dim] > split_val]

    if (not aux_functions.is_entropy_ldiverse(lhs, sens_atts, l)) or (
        not aux_functions.is_entropy_ldiverse(rhs, sens_atts, l)
    ):
        return anonymize_entropy_l(
            partition, quasi_idents, sens_atts, l, explored_qi, corr_att, taxonomies
        )

    return pd.concat(
        [
            anonymize_entropy_l(
                lhs, quasi_idents, sens_atts, l, [], corr_att, taxonomies
            ),
            anonymize_entropy_l(
                rhs, quasi_idents, sens_atts, l, [], corr_att, taxonomies
            ),
        ]
    ).reset_index(drop=True)


def anonymize_recursive_cl(
    partition, quasi_idents, sens_atts, c, l, explored_qis, corr_att, taxonomies
):
    """Anonymizes a dataset according to recursive c,l-diversity  (R1 < c(Rl + Rl+1 ...))

    :param partition: partition to be anonymized
    :param quasi_idents: quasi-identifiers of the given partition
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param c: the value of c to be used in recursive cl-diversity
    :param l: the value of l to be used in recursive cl-diversity
    :param explored_qis: quasi-identifiers that have already been used when trying to partition the given dataset
    :param corr_att: attribute to keep in the correlation
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized version of the partition"""

    qis = quasi_idents.copy()

    qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(partition[qi])]

    if set(qis) == set(explored_qis):
        if aux_functions.is_recursive_cldiverse(partition, sens_atts, c, l):
            return aux_functions.summary(partition, quasi_idents, taxonomies)

        else:
            return pd.DataFrame()

    dim, explored_qi = aux_functions.choose_dimension(
        partition, qis, explored_qis, corr_att
    )
    partition = partition.sort_values(by=dim).reset_index(drop=True)

    fs = aux_functions.frequency_set(partition, dim)

    split_val = aux_functions.find_median(fs)

    lhs = partition[partition[dim] <= split_val]
    rhs = partition[partition[dim] > split_val]

    if (not aux_functions.is_recursive_cldiverse(lhs, sens_atts, c, l)) or (
        not aux_functions.is_recursive_cldiverse(rhs, sens_atts, c, l)
    ):
        return anonymize_recursive_cl(
            partition, quasi_idents, sens_atts, c, l, explored_qi, corr_att, taxonomies
        )

    return pd.concat(
        [
            anonymize_recursive_cl(
                lhs, quasi_idents, sens_atts, c, l, [], corr_att, taxonomies
            ),
            anonymize_recursive_cl(
                rhs, quasi_idents, sens_atts, c, l, [], corr_att, taxonomies
            ),
        ]
    ).reset_index(drop=True)


def anonymize_t_closeness(
    partition, quasi_idents, sens_atts, t, data, explored_qis, corr_att, taxonomies
):
    """Anonymizes a dataset according to entropy l-diversity

    :param partition: partition to be anonymized
    :param quasi_idents: quasi-identifiers of the given partition
    :param sens_atts: List with the sensitive_attributes for the dataframe
    :param l: the value of l to be used in entropy l-diversity
    :param explored_qis: quasi-identifiers that have already been used when trying to partition the given dataset
    :param corr_att: attribute to keep in the correlation
    :param taxonomies: hierarchy to be used for quasi-identifer generalization

    :returns: anonymized version of the partition"""

    qis = quasi_idents.copy()

    qis = [qi for qi in quasi_idents if pd.api.types.is_numeric_dtype(partition[qi])]

    if set(qis) == set(explored_qis):
        if aux_functions.is_t_close(partition, sens_atts, t, data):
            return aux_functions.summary(partition, quasi_idents, taxonomies)

        else:
            return pd.DataFrame()

    dim, explored_qi = aux_functions.choose_dimension(
        partition, qis, explored_qis, corr_att
    )
    partition = partition.sort_values(by=dim).reset_index(drop=True)

    fs = aux_functions.frequency_set(partition, dim)

    split_val = aux_functions.find_median(fs)

    lhs = partition[partition[dim] <= split_val]
    rhs = partition[partition[dim] > split_val]

    if (
        len(lhs) < 2
        or len(rhs) < 2
        or not aux_functions.is_t_close(lhs, sens_atts, t, data)
    ) or (not aux_functions.is_t_close(rhs, sens_atts, t, data)):
        return anonymize_t_closeness(
            partition,
            quasi_idents,
            sens_atts,
            t,
            data,
            explored_qi,
            corr_att,
            taxonomies,
        )

    return pd.concat(
        [
            anonymize_t_closeness(
                lhs, quasi_idents, sens_atts, t, data, [], corr_att, taxonomies
            ),
            anonymize_t_closeness(
                rhs, quasi_idents, sens_atts, t, data, [], corr_att, taxonomies
            ),
        ]
    ).reset_index(drop=True)


def rank_swap(data: pd.DataFrame, qis: list[str], p: int) -> pd.DataFrame:
    """Swaps values for the quasi-identifiers based on the given interval p

    :param data: Dataset to be anonymized
    :param qis: quasi-identifiers
    :param o: swapping interval

    :returns: anonymized dataset"""

    for qi in qis:
        data = data.sort_values(by=qi)

        data = data.reset_index()

        orig = data.copy()

        for i in range(len(data) - 1):
            if data[qi][i] == orig[qi][i]:
                swap_pos = i + random.randint(1, min(p, len(data) - 1 - i))

                data.at[i, qi], data.at[swap_pos, qi] = (
                    data.at[swap_pos, qi],
                    data.at[i, qi],
                )

        data = data.set_index("index")

        data = data.sort_index(axis=0, ascending=True, inplace=False)

    return data


def rank_swap_distribution(data: pd.DataFrame, qis: list[str], p: int) -> pd.DataFrame:
    """Swaps values for the quasi-identifiers based on the distribution given by p

    :param data: Dataset to be anonymized
    :param qis: quasi-identifiers
    :param p: swapping interval

    :returns: anonyimized dataset"""

    for qi in qis:
        data = data.sort_values(by=qi)

        data = data.reset_index()

        orig = data.copy()

        for i in range(len(data) - 1):
            if data[qi][i] == orig[qi][i]:
                swap_pos = i + round(np.random.normal(p / 2, p / 2))

                if swap_pos > 0 and swap_pos < len(data) - 1:
                    data.at[i, qi], data.at[swap_pos, qi] = (
                        data.at[swap_pos, qi],
                        data.at[i, qi],
                    )

        data = data.set_index("index")

        data = data.sort_index(axis=0, ascending=True, inplace=False)

    return data


def rank_swap_categorical(data: pd.DataFrame, qis: list[str], p: int) -> pd.DataFrame:
    """Swaps values for the quasi-identifiers based on the distribution given by p
    This function supports swapping categorical values, by using their encodings as their value

    :param data: Dataset to be anonymized
    :param qis: quasi-identifiers
    :param p: swapping interval

    :returns: anonymized dataset"""
    model = SentenceTransformer("all-mpnet-base-v2")

    for qi in qis:
        if not pd.api.types.is_string_dtype(data[qi]):
            data = data.sort_values(by=qi)
            data = data.reset_index()
            orig = data.copy()

            for i in range(len(data) - 1):
                if data[qi][i] == orig[qi][i]:
                    swap_pos = i + round(np.random.normal(p / 2, p / 2))

                    if swap_pos > 0 and swap_pos < len(data) - 1:
                        data.at[i, qi], data.at[swap_pos, qi] = (
                            data.at[swap_pos, qi],
                            data.at[i, qi],
                        )

            data = data.set_index("index")

            data = data.sort_index(axis=0, ascending=True, inplace=False)

        else:
            values = data[qi].unique().tolist()
            embeddings = model.encode(values)
            links = linkage(embeddings, method="ward")
            leaves = leaves_list(links)
            order = [values[i] for i in leaves]

            data[qi] = pd.Categorical(data[qi], categories=order, ordered=True)
            data = data.sort_values(by=qi)
            data = data.reset_index()

            orig = data.copy()

            for i in range(len(data) - 1):
                if data[qi][i] == orig[qi][i]:
                    swap_pos = i + round(np.random.normal(p / 2, p / 2))

                    if swap_pos > 0 and swap_pos < len(data) - 1:
                        data.at[i, qi], data.at[swap_pos, qi] = (
                            data.at[swap_pos, qi],
                            data.at[i, qi],
                        )

            data = data.set_index("index")

            data = data.sort_index(axis=0, ascending=True, inplace=False)

    return data
