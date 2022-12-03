import pandas as pd
import numpy as np
from match import Country
from knockoff import r16_outcome
import collections
import matplotlib.pyplot as plt

from util import estimate_coef
'''
Skill: Qualified for stage -
Goal differential: +1 per goal
Qualified for World Cup: +5
Wins in Group: +3
Ties in Group: +1
Round of 16: +5
Round of 8: +7
Round of 4: +10
Final: +15
3rd: +10
Champion: +15

Lambda: skill-adjusted goals / num-matches
'''

def load_data(my_team: str):
    matches = pd.read_csv("WorldCupMatches.csv")
    matches = matches[matches["Year"] > 1996]
    goals_mean = matches.groupby("Home Team Initials")["Home Team Goals"].mean()
    skills = dict()
    total_goals = dict()
    num_matches = dict()
    r16_matches = matches[matches["Stage"] == "Round of 16"]
    qf_matches = matches[matches["Stage"] == "Quarter-finals"]
    sf_matches = matches[matches["Stage"] == "Semi-finals"]
    third_matches = matches[matches["Stage"] == "Play-off for third place"]
    final_matches = matches[matches["Stage"] == "Final"]
    ko_stages = {"Round of 16", "Quarter-finals", "Semi-finals", "Play-off for third place", "Final"}
    group_matches = matches[matches.apply(lambda row: row["Stage"] not in ko_stages, axis = 1)]
    def process_matches(matches, winpoint: int):
        for _, row in matches.iterrows():
            hgoal = row["Home Team Goals"]
            agoal = row["Away Team Goals"]
            ht = row["Home Team Initials"]
            at = row["Away Team Initials"]
            if ht not in skills:
                skills[ht] = 0
                total_goals[ht] = collections.defaultdict(int)
                num_matches[ht] = collections.defaultdict(int)
            skills[ht] += hgoal - agoal
            total_goals[ht][at] += hgoal
            num_matches[ht][at] += 1
            if at not in skills:
                skills[at] = 0
                total_goals[at] = collections.defaultdict(int)
                num_matches[at] = collections.defaultdict(int)
            skills[at] += agoal - hgoal
            total_goals[at][ht] += agoal
            num_matches[at][ht] += 1
            if hgoal > agoal:
                skills[ht] += winpoint
            elif agoal > hgoal:
                skills[at]  += winpoint
            else:
                skills[ht] += winpoint // 2
                skills[at] += winpoint // 2
        return
    process_matches(group_matches, 1)
    process_matches(r16_matches, 3)
    process_matches(qf_matches, 4)
    process_matches(sf_matches, 5)
    process_matches(third_matches, 4)
    process_matches(final_matches, 5)
    # find beta for all teams, find mean of betas
    betas = []
    for team in total_goals:
        x = []
        y = []
        for opp in total_goals[team]:
            for _ in range(num_matches[team][opp]):
                x.append(skills[opp])
                y.append(total_goals[team][opp] / num_matches[team][opp])
        beta = estimate_coef(x, y)
        if beta != None:
            betas.append(estimate_coef(x, y))
    beta_skill = np.mean(betas)
    # print("mean of beta:", np.mean(betas))
    # print("STDV of beta:", np.std(betas))
    
    # find lambda for each team -> lambda = parameter against team with skill 0
    lambd = dict()
    min_lambd = 0
    for team in skills:
        adj_total = 0
        total_matches = 0
        for opp in total_goals[team]:
            adj_total += total_goals[team][opp] + beta_skill * skills[opp]
            total_matches += num_matches[team][opp]
        lambd[team] = adj_total / total_matches
        if lambd[team] < min_lambd:
            min_lambd = lambd[team]
    for team in lambd:
        lambd[team] += - min_lambd + 0.5
    countries = dict()
    for team in skills:
        countries[team] = Country(team, skills[team], lambd[team])
    table = [[[["NED", "USA"], ["ARG", "AUS"]], [["JPN", "CRO"], ["BRA", "KOR"]]], [[["FRA", "POL"], ["ENG", "SEN"]], [["MAR", "ESP"], ["POR", "SUI"]]]]
    print("Calculating the chances of", my_team, "in 2022 World Cup Knock-off stages")
    print("====================================================================")
    probs = r16_outcome(table, countries, my_team, beta_skill)
    print("Probability that", my_team, "advances to Quarter-Finals:", probs[0] * 100, "%")
    print("Probability that", my_team, "advances to Semi-Finals:", (probs[1] + probs[2] + probs[3] + probs[4]) * 100, "%")
    print("Probability that", my_team, "claims 3rd place:", probs[2] * 100, "%")
    print("Probability that", my_team, "claims runner-up:", probs[3] * 100, "%")
    print("PROBABILITY THAT", my_team, "WINS THE WORLD CUP:", probs[4] * 100, "%")
    print("====================================================================")


if __name__ ==  '__main__':
    team = input("Enter the initials of a country competing in the 2022 World Cup Knock-off stages: ")
    load_data(team)