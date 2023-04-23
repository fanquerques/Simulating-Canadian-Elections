"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
                  [True, False, True, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
                  [False, True, True, True]]]
SAMPLE_ORDER_2 = ['NDP', 'LIBERAL', 'GREEN', 'CPC']

###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO'],
    ...         ['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]],[0, 1,
    ...             ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    """
    for sub_data in data:
        sub_data[COL_RIDING] = int(sub_data[COL_RIDING])
        sub_data[COL_VOTER] = int(sub_data[COL_VOTER])
        sub_data[COL_RANK] = sub_data[COL_RANK].split(SEPARATOR)
        sub_data[COL_RANGE] = sub_data[COL_RANGE].split(SEPARATOR)
        sub_data[COL_RANGE] = [int(
            sub_data[COL_RANGE][sub_data[COL_RANGE].index(ranges)]
            ) for ranges in sub_data[COL_RANGE]]

        sub_data[COL_APPROVAL] = (sub_data[COL_APPROVAL].split(SEPARATOR))
        j = 0
        while j < len(sub_data[COL_APPROVAL]):
            if sub_data[COL_APPROVAL][j] == 'NO':
                sub_data[COL_APPROVAL][j] = False
            else:
                sub_data[COL_APPROVAL][j] = True
            j += 1

###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> extract_column([[9,8,7,6,5]], 3)
    [6]
    >>> extract_column([['L', 'C', 'N', 'G'], ['C', 'G','L', 'N']], 1)
    ['C', 'G']
    """
    extracted_result = []
    item_index = 0
    sublist_index = 0

    while sublist_index < len(data):
        while item_index < len(data[sublist_index]):
            if item_index == column:
                extracted_result.append(data[sublist_index][item_index])
            item_index += 1
        item_index = 0
        sublist_index += 1

    return extracted_result

def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    """
    highest_ballot = []
    for sublist in data:
        highest_ballot.append(sublist[COL_RANK][0])
    return highest_ballot


def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    >>> expected = [[72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
    ...             [False, True, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_2, 72) == expected
    True
    """
    selected_riding = []
    for sublist in data:
        if sublist[COL_RIDING] == riding:
            selected_riding.append(sublist)
    return selected_riding

###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]
    >>> voting_plurality(['CPC', 'NDP', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_2)
    [2, 0, 1, 2]
    """
    order_index = 0
    vote_index = 0
    vote_counter = 0
    num_of_ballots = []

    while order_index < len(party_order):
        while vote_index < len(single_ballots):
            if single_ballots[vote_index] == party_order[order_index]:
                vote_counter += 1
            vote_index += 1
        num_of_ballots.append(vote_counter)
        vote_counter = 0
        order_index += 1
        vote_index = 0

    return num_of_ballots

###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]
    >>> voting_approval([[True, True, False, False],
    ...                  [False, True, False, True],
    ...                  [True, True, False, True]], SAMPLE_ORDER_2)
    [2, 3, 0, 2]
    """
    vote_counter = 0
    vote_sum = []
    vote_index = 0
    order_index = 0
    vote_true = True

    while order_index < len(party_order):
        for sublist in approval_ballots:
            if sublist[vote_index] == vote_true:
                vote_counter += 1
        vote_sum.append(vote_counter)
        vote_counter = 0
        vote_index += 1
        order_index += 1
    return vote_sum

###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    >>> voting_range([[3, 1, 5, 6], [10, 10, 3, 1], [1, 3, 6, 3]],
    ...              SAMPLE_ORDER_2)
    [14, 14, 14, 10]
    """
    vote_sums = []
    vote_index = 0
    sum_holder = 0
    sublist_index = 0

    while sublist_index < len(party_order):
        for ranges in range_ballots:
            sum_holder += ranges[vote_index]
        vote_sums.append(sum_holder)
        sum_holder = 0
        vote_index += 1
        sublist_index += 1

    return vote_sums

###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_2)
    [2, 8, 4, 4]
    """
    result = [0] * len(party_order)
    entry_index = 0
    for sublist in rank_ballots:
        for item in sublist:
            result[party_order.index(item)] += len(sublist) - (entry_index + 1)
            entry_index += 1
        entry_index = 0

    return result

###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'CPC')
    >>> ballots == [['LIBERAL', 'GREEN', 'NDP'],
    ...             ['NDP', 'LIBERAL', 'GREEN'],
    ...             ['NDP', 'GREEN', 'LIBERAL']]
    True
    """
    sublist = 0
    item = 0
    while sublist < len(rank_ballots):
        while item < len(rank_ballots[sublist]):
            if rank_ballots[sublist][item] == party_to_remove:
                rank_ballots[sublist].remove(rank_ballots[sublist][item])
            item += 1
        sublist += 1
        item = 0

def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    >>> get_lowest([0, 11, 4, 20], SAMPLE_ORDER_1)
    'CPC'
    """
    result = party_order[party_tallies.index(min(party_tallies))]
    return result

def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    >>> get_winner([16, 100, 4, 20], SAMPLE_ORDER_1)
    'GREEN'
    """
    result = party_order[party_tallies.index(max(party_tallies))]
    return result

def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']

    >>> order = ['NDP', 'LIBERAL', 'GREEN', 'CPC']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'CPC'
    >>> ballots == [['LIBERAL', 'CPC'],
    ...             ['CPC', 'LIBERAL'],
    ...             ['CPC', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'CPC']
    """
    min_votes = len(rank_ballots) // 2 + 1
    first_choice = extract_column(rank_ballots, 0)
    tallies = voting_plurality(first_choice, party_order)
    while max(tallies) < min_votes:
        remove_party(rank_ballots, get_lowest(tallies, party_order))
        party_order.remove(get_lowest(tallies, party_order))
        final = extract_column(rank_ballots, 0)
        tallies = voting_plurality(final, party_order)

    return get_winner(tallies, party_order)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
