import pandas as pd

from anonymity_api.anonymity.utils import anon_functions


def rank_swapping(
    data: pd.DataFrame, quasi_idents: list[str], p: int, idents=[]
) -> pd.DataFrame:
    """Rank swapping implementation

    :param data: dataframe to be anonymized
    :param quasi_idents: quasi-identifiers of the dataset
    :param p: interval for the swapping
    :param idents: identifiers of the dataset

    :returns: Anonymized dataframe"""

    if idents != []:
        for attribute in idents:
            del data[attribute]

    qis = quasi_idents.copy()

    data = data.copy()

    return anon_functions.rank_swap(data, qis, p).reset_index(drop=True)
