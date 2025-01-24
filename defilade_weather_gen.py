import random
import json


# List of possible weather types for the simulation
# Ensure any new weather type is also added to the weather transitions and visibility list for proper functionality
weather_type = ["Clear",
                "Overcast",
                "Light clouds",
                "Fog",
                "Light snow",
                "Heavy snow",
                "Blizzard",
                "Hail",
                "Sleet"
                ]
# List of random events that can occur each day
random_event = ["Heavy bombardment from the previous day has greatly damaged infrastructure, slowing vehicle movement.",
                "The sound of distant artillery can be heard in the distance.",
                "Stray bullets from an aerial dogfight pepper the land. Watch your heads!",
                "Airstrikes seem to be missing their mark, and are landing in your viscinity.",
                "Nearby radio towers seem to be disabled - radio contact is spotty at best."
                ]

def print_intro():
    # ASCII Art of an umbrella
    print("  .-'-.")
    print(",'.,-.,'.")
    print("    |")
    print("    J")

    # Welcome message/instructions
    print("Welcome to the Defilade Weather Gen.")
    print("This script generates incremental weather on a day-by-day basis.")
    print("This is set to winter for now..")
    print()
    print("----------")
    print("HOW TO USE")
    print("----------")
    print("Press 'enter' to generate the weather for the next day.")
    print("Type 'reset' to start over from Day 1.")
    print("Type 'exit' to quit the program.")
    print()
    print("If anyone except me is using this, thanks - Angus Macnaughton")

def alter_weather(current_weather):
    # Dictionary defining possible transitions between weather types
    weather_transitions = {
        "Clear": ["Clear", "Overcast", "Light clouds", "Light snow"],
        "Overcast": ["Clear", "Overcast", "Light clouds", "Fog", "Light snow"],
        "Light clouds": ["Clear", "Overcast", "Light clouds", "Fog"],
        "Fog": ["Overcast", "Light clouds", "Fog", "Light snow"],
        "Light snow": ["Fog", "Light snow", "Heavy snow", "Clear", "Overcast", "Light clouds"],
        "Heavy snow": ["Light snow", "Heavy snow", "Blizzard"],
        "Blizzard": ["Heavy snow", "Blizzard", "Hail"],
        "Hail": ["Clear", "Fog", "Overcast", "Hail", "Sleet", "Heavy snow", "Light snow"],
        "Sleet": ["Clear", "Fog", "Overcast", "Hail", "Sleet", "Heavy snow", "Light snow"]
    }
    # This randomly selects the next weather type based on current weather
    return random.choice(weather_transitions[current_weather])

def generate_daily_info(previous_night_weather):
    # Generates weather, temp, wind speed and a random event for the day 
    morning_weather = alter_weather(previous_night_weather)
    afternoon_weather = alter_weather(morning_weather)
    night_weather = alter_weather(afternoon_weather)
    
    # Generates the temperature for morning/afternoon/night based on weather conditions
    morning_temp = round(random.uniform(-3, 4) if morning_weather in {"Clear", "Overcast", "Light clouds", "Fog"} else random.uniform(-15, -3), 1)
    afternoon_temp = round(morning_temp + random.uniform(-2, 2), 1)
    night_temp = round(afternoon_temp + random.uniform(-2, 2), 1)
    
    # Generates the wind speed for morning/afternoon/night based on weather conditions
    morning_wind = round(random.uniform(5, 25) if morning_weather in {"Clear", "Overcast", "Light clouds", "Fog", "Light snow", "Sleet"} else random.uniform(25, 64), 1)
    afternoon_wind = round(morning_wind + random.uniform(-5, 5), 1)
    night_wind = round(afternoon_wind + random.uniform(-5, 5), 1)
    
    # Generates a random daily event - to increase the chances of a daily event, change the number before 'else "None."' (defaulting to 6)
    daily_event = random.choice(random_event) if random.randint(1, 10) >= 6 else "None."
    
    # 
    return (morning_weather, morning_temp, morning_wind, 
            afternoon_weather, afternoon_temp, afternoon_wind, 
            night_weather, night_temp, night_wind, daily_event)

def print_weather(day, morning_weather, morning_temp, morning_wind, 
                  afternoon_weather, afternoon_temp, afternoon_wind, 
                  night_weather, night_temp, night_wind, daily_event):
    print("------------------------")
    print(f"DAY {day}")
    print()
    
    def print_stage(stage, weather, temp, wind):
        # Visibility is determined based on the weather type
        visibility = {
            "Clear": "Good",
            "Overcast": "Fine",
            "Light clouds": "Good",
            "Fog": "Poor",
            "Light snow": "Fine",
            "Heavy snow": "Poor",
            "Blizzard": "Extremely Poor",
            "Hail": "Fine",
            "Sleet": "Poor"
            }.get(weather)
        print("    ----    ")
        print(f"{stage.upper()}")
        print("    ----    ")

        # Prints forecasts for morning, afternoon and night
        print(f"[WTHR]: {weather}")
        print(f"[TEMP]: {temp} degrees Celsius")
        print(f"[WIND]: {wind} mph")
        print(f"[VISI]: {visibility}")
        print()
    
    print_stage("Morning Forecast", morning_weather, morning_temp, morning_wind)
    print_stage("Afternoon Forecast", afternoon_weather, afternoon_temp, afternoon_wind)
    print_stage("Night Forecast", night_weather, night_temp, night_wind)
    
    print(f"[EVNT]: {daily_event}")

def save_progress(day, previous_night_weather):
    # Saves the current day and previous night's weather to a JSON file
    with open("weather_progress.json", "w") as file:
        json.dump({"day": day, "previous_night_weather": previous_night_weather}, file)

def load_progress():
    # Loads saved progress from the JSON file, or starts fresh if the file is missing
    try:
        with open("weather_progress.json", "r") as file:
            data = json.load(file)
            return data["day"], data["previous_night_weather"]
    except FileNotFoundError:
        return 1, random.choice(weather_type)

def reset_progress():
    # Resets the day back to 1
    with open("weather_progress.json", "w") as file:
        json.dump({"day": 1, "previous_night_weather": random.choice(weather_type)}, file)

def main():
       # Main program loop: initializes, handles user input, and generates weather
    print_intro()
    day, previous_night_weather = load_progress()
    while True:
        user_input = input().strip().lower()
        if user_input == "reset":
            reset_progress()
            day, previous_night_weather = load_progress()
            print("Weather has been reset. The next day will be Day 1!")
        elif user_input == "exit":
            break
        else:
            (morning_weather, morning_temp, morning_wind, 
             afternoon_weather, afternoon_temp, afternoon_wind, 
             night_weather, night_temp, night_wind, daily_event) = generate_daily_info(previous_night_weather)
            print_weather(day, morning_weather, morning_temp, morning_wind, 
                          afternoon_weather, afternoon_temp, afternoon_wind, 
                          night_weather, night_temp, night_wind, daily_event)
            previous_night_weather = night_weather
            save_progress(day, previous_night_weather)
            print("------------------------")
            day += 1

if __name__ == "__main__":
    main()

