# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    #noise=0 so the agent is not scared to take risky short paths
    #small discount factor so future rewards matter less and the agent prefer nearby small rewards (+1)
    #living reward = -1 so the agent is punished for moving too much and try to reach the end quickly
    return {
        "noise": 0,
        "discount_factor": 0.2,
        "living_reward": -1
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    # adding some noise so the agent does not take risky paths
    #slightly higher discount factor so short term rewards are considered
    #living reward = -0.3 to push the agent to finish faster but still stay safe
    return {
        "noise": 0.2,
        "discount_factor": 0.4,
        "living_reward": -0.3
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    # noise =0 so the agent is not scared to take risky short paths
    # high discount factor so future rewards are important and the agent goes for far high reward
    # living reward= -1 so the agent is punished for moving a lot and tries to finish fast
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -1
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    # adding some noise so the agent avoid risky paths
    # living reward = -0.3 to make the agent choose shorter paths but still stay safe
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.3
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # living reward =large +ve value larger than any terminal state reward to make the robot not want to finish
    return {
        "noise": 0,
        "discount_factor": 0.2,
        "living_reward": 100
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    # living reward = large -ve value larger than any terminal state reward to make the robot trying to finish in the shortest time possible
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100
    }