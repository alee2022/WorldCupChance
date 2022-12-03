import numpy as np
from scipy.stats import skellam

class Country:
    def __init__(self, name: str, skill: float, lambd: float) -> None:
        self.name = name
        self.lambd = lambd
        self.skill = skill

# skellam distribution
# Returns P(team 1 wins)
def win_prob(team1: Country, team2: Country, beta: float):
    lambd1 = max(team1.lambd + beta * team2.skill, 0.5)
    lambd2 = max(team2.lambd + beta * team1.skill, 0.5)
    return (1 - skellam.cdf(0, lambd1, lambd2))
    
def tie_prob(team1: Country, team2: Country, beta: float):
    lambd1 = max(team1.lambd + beta * team2.skill, 0.5)
    lambd2 = max(team2.lambd + beta * team1.skill, 0.5)
    return skellam.pmf(0, lambd1, lambd2)

def kowin_prob(team1: Country, team2: Country, beta: float):
    return win_prob(team1, team2, beta) + tie_prob(team1, team2, beta) / 2

def gd_prob(team1: Country, team2: Country, gd: int, beta: float):
    lambd1 = max(team1.lambd + beta * team2.skill, 0.5)
    lambd2 = max(team2.lambd + beta * team1.skill, 0.5)
    return skellam.pmf(gd, lambd1, lambd2)