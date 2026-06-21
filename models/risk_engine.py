
def risk_score(injuries,rotation,form):
    return round((injuries*0.4)+(rotation*0.3)+(form*0.3),2)
