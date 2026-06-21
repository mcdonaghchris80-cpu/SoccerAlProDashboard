
def kelly(prob,odds):
    b=odds-1
    return max(0,((prob*b)-(1-prob))/b)
