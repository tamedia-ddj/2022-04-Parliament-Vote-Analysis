"""This file could contain helper functions
for use in multiple Python scripts and notebooks"""


def get_rice_index(group, vote_column="vote"):
    """Compute rice index for a given group.
    Input dataframe must contain a column containing each councillor’s vote."""
    substraction = abs(
        len(group[group[vote_column] == "Oui"])
        - len(group[group[vote_column] == "Non"])
    )
    addition = len(group[group[vote_column].isin(["Oui", "Non"])])
    assert addition > 0, "Total of yes and no votes is null."
    return substraction / addition


def get_splitted_share(group_a, group_b, vote_column="vote"):
    """Get share of “yes” votes for two groups"""
    len_yes_a = len(group_a[group_a[vote_column] == "Oui"])
    len_yes_b = len(group_b[group_b[vote_column] == "Oui"])
    len_yesno_a = len(group_a[group_a[vote_column].isin(["Oui", "Non"])])
    len_yesno_b = len(group_b[group_b[vote_column].isin(["Oui", "Non"])])
    share_yes_a = len_yes_a / len_yesno_a * 100
    share_yes_b = len_yes_b / len_yesno_b * 100
    return {
        "yes a": len_yes_a,
        "yes b": len_yes_b,
        "yes/no a": len_yesno_a,
        "yes/no b": len_yesno_b,
        "share a": share_yes_a,
        "share b": share_yes_b,
        "delta": abs(share_yes_a - share_yes_b),
    }
