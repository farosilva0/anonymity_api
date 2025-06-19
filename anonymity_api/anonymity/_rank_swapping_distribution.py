import pandas as pd
from anonymity_api.anonymity.utils import anon_functions


def rank_swapping_distribution(
    data: pd.DataFrame, quasi_idents: list[str], p: int, idents=[]
) -> pd.DataFrame:
    """Implementation of rank swapping with normal distribution for swapping values

    :param data: dataframe to be anonymized
    :param quasi_idents: quasi-identifiers of the dataset
    :param p: defines interval for swapping (p/2 is used as both the mean and the standard deviation of the normal distribution)
    :param idents: identifiers of the dataset

    :returns: Anonymizex dataframe"""

    data = data.copy()

    if idents != []:
        for attribute in idents:
            del data[attribute]

    qis = quasi_idents.copy()

    return anon_functions.rank_swap_distribution(data, qis, p).reset_index(drop=True)


def rank_swapping_categorical(
    data: pd.DataFrame, quasi_idents: list[str], p, idents=[]
) -> pd.DataFrame:
    data = data.copy()

    if idents != []:
        for attribute in idents:
            del data[attribute]

    qis = quasi_idents.copy()

    return anon_functions.rank_swap_categorical(data, qis, p).reset_index(drop=True)
