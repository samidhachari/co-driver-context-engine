import pandas as pd
import random 

NUM_SAMPLES = 1000

time_options = ["morning","afternoon","evening","night"]
location_options = ["city","highway","rural"]
traffic_options = ["low","medium","high"]

def compute_risk(fatigue,stress,battery,time_of_day,location):
    # high risk conditions
    if fatigue > 7 and time_of_day =="night":
        return "high"
    if fatigue > 7 and location == "highway":
        return "high"
    if battery < 10:
        return "high"
    if stress >10 and location == "rural" and fatigue >10 and time_of_day == "night":
        return "high"
        
    # medium risk
    if stress > 6 and location == "city":
        return "medium"
    if battery < 25:
        return "medium"
    
    # low risk 
    return "low"

def generate_data(hour):
    if hour < 6:
        time_of_day = "night"
        fatigue = random.randint(6,10)
    elif hour < 12:
        time_of_day = "morning"
        fatigue = random.randint(1,4)
    elif hour < 18:
        time_of_day = "afternoon"
        fatigue = random.randint(2,6)
    else:
        time_of_day = "evening"
        fatigue = random.randint(4,8)

    stress = random.randint(1,10)
    battery = random.randint(5,100)
    speed = random.randint(0,120)

    location = random.choice(location_options)
    traffic = random.choice(traffic_options)

    risk = compute_risk(fatigue,stress,battery,time_of_day,location)

    return {
        "fatigue_level":fatigue,
        "stress_level":stress,
        "battery_level":battery,
        "speed":speed,
        "location_type":location,
        "traffic_level":traffic,
        "time_of_day":time_of_day,
        "risk_level":risk
    }

def generate_dataset():
    data = []

    for _ in range(NUM_SAMPLES):
        hour = random.randint(0,23)
        sample = generate_data(hour)
        data.append(sample)

    return pd.DataFrame(data)


if __name__ == "__main__":
    data = generate_dataset()
    data.to_csv("driver_context_dataset.csv",index=False)
    print("Dataset Generated Successfully")





