from match import Country, win_prob, tie_prob, kowin_prob
from typing import List, Dict
# TODO: implement function that takes in 16 teams in order, for each team, returns prob that they advance to 8, 4, 2, and win
def semi_finals(table: List[List[str]], countries: Dict[str, Country], my_team: str, beta: float):
    # TODO: implement for list input
    visited = set()
    #sanity check
    p_win = 0
    p_4th = 0
    p_3rd = 0
    p_2nd = 0
    p_1st = 0
    for match in table:
        if my_team in match:
            opp = ""
            if match[0] == my_team:
                opp = match[1]
            else:
                opp = match[0]
            p_win = kowin_prob(countries[my_team], countries[opp], beta)
            break
    for match in table:
        if my_team in match:
            continue
        teamA = match[0]
        teamB = match[1]
        p_Awin = kowin_prob(countries[teamA], countries[teamB], beta)
        p_Bwin = 1 - p_Awin
        p_1st += p_win * p_Awin * kowin_prob(countries[my_team], countries[teamA], beta)
        p_1st += p_win * p_Bwin * kowin_prob(countries[my_team], countries[teamB], beta)
        p_2nd += p_win * p_Awin * kowin_prob(countries[teamA], countries[my_team], beta)
        p_2nd += p_win * p_Bwin * kowin_prob(countries[teamB], countries[my_team], beta)
        p_3rd += (1 - p_win) * p_Bwin * kowin_prob(countries[my_team], countries[teamA], beta)
        p_3rd += (1 - p_win) * p_Awin * kowin_prob(countries[my_team], countries[teamB], beta)
        p_4th += (1 - p_win) * p_Bwin * kowin_prob(countries[teamA], countries[my_team], beta)
        p_4th += (1 - p_win) * p_Awin * kowin_prob(countries[teamB], countries[my_team], beta)
    # Returns [P(4th, 3rd, 2nd place, 1st place)
    return [p_4th, p_3rd, p_2nd, p_1st]

def qtr_finals(table: List[List[List[str]]], countries: Dict[str, Country], my_team: str, beta: float):
    p_win = 0
    p_1st = 0
    p_2nd = 0
    p_3rd = 0
    p_4th = 0
    bracket_i = -1
    match_i = -1
    for b_ind in range(2):
        for m_ind in range(2):
            if my_team in table[b_ind][m_ind]:
                opp = ""
                if table[b_ind][m_ind][0] == my_team:
                    opp = table[b_ind][m_ind][1]
                else:
                    opp = table[b_ind][m_ind][0]
                bracket_i = b_ind
                match_i = m_ind
                p_win = kowin_prob(countries[my_team], countries[opp], beta)
    semi_table = [["",""],["",""]]
    semi_table[bracket_i][match_i] = my_team
    indices = []
    for b_ind in range(2):
        for m_ind in range(2):
            if b_ind == bracket_i and m_ind == match_i:
                continue
            indices.append((b_ind, m_ind))
    def recurse(index, p_table):
        nonlocal p_1st, p_2nd, p_3rd, p_4th
        if index == len(indices):
            probs = semi_finals(semi_table, countries, my_team, beta)
            p_4th += p_win * p_table * probs[0]
            p_3rd += p_win * p_table * probs[1]
            p_2nd += p_win * p_table * probs[2]
            p_1st += p_win * p_table * probs[3]
            return
        for i in range(2):
            b, m = indices[index]
            win_team = table[b][m][i]
            semi_table[b][m] = win_team
            lose_team = table[b][m][1-i]
            new_p = p_table * kowin_prob(countries[win_team], countries[lose_team], beta)
            recurse(index+1, new_p)
    recurse(0, 1)
    return [p_4th, p_3rd, p_2nd, p_1st]
    
def r16_outcome(table: List[List[List[List[str]]]], countries: Dict[str, Country], my_team: str, beta: float):
    p_win = 0
    p_1st = 0
    p_2nd = 0
    p_3rd = 0
    p_4th = 0
    group_i = -1
    bracket_i = -1
    match_i = -1
    for g_ind in range(2):
        for b_ind in range(2):
            for m_ind in range(2):
                if my_team in table[g_ind][b_ind][m_ind]:
                    group_i = g_ind
                    bracket_i = b_ind
                    match_i = m_ind
                    opp = ""
                    if table[g_ind][b_ind][m_ind][0] == my_team:
                        opp = table[g_ind][b_ind][m_ind][1]
                    else:
                        opp = table[g_ind][b_ind][m_ind][0]
                    p_win = kowin_prob(countries[my_team], countries[opp], beta)
    qtr_table = [[["",""],["",""]],[["", ""],["", ""]]]
    qtr_table[group_i][bracket_i][match_i] = my_team
    indices = []
    for g_ind in range(2):
        for b_ind in range(2):
            for m_ind in range(2):
                if g_ind == group_i and b_ind == bracket_i and m_ind == match_i:
                    continue
                indices.append((g_ind, b_ind, m_ind))
    def recurse(index, p_table):
        nonlocal p_1st, p_2nd, p_3rd, p_4th
        if index == len(indices):
            probs = qtr_finals(qtr_table, countries, my_team, beta)
            p_4th += p_win * p_table * probs[0]
            p_3rd += p_win * p_table * probs[1]
            p_2nd += p_win * p_table * probs[2]
            p_1st += p_win * p_table * probs[3]
            return
        for i in range(2):
            g, b, m = indices[index]
            win_team = table[g][b][m][i]
            qtr_table[g][b][m] = win_team
            lose_team = table[g][b][m][1-i]
            new_p = p_table * kowin_prob(countries[win_team], countries[lose_team], beta)
            recurse(index+1, new_p)
    recurse(0, 1)
    return [p_win, p_4th, p_3rd, p_2nd, p_1st]