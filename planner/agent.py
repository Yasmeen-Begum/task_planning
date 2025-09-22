# planner/agent.py
import re
from planner.enrichers.weather import get_weather_forecast
from planner.enrichers.web_search import enrich_with_places  

def extract_city(goal: str):
    """
    Return the first recognized city from goal, or 'India' as a fallback.
    """
    cities = ["Hyderabad", "Visakhapatnam", "Vizag", "Delhi", "Mumbai",
              "Chennai", "Bangalore", "Bengaluru", "Jaipur", "Goa"]
    g = goal.lower()
    for city in cities:
        if city.lower() in g:
            if city.lower() == "bengaluru":
                return "Bangalore"
            if city.lower() in ["visakhapatnam", "vizag"]:
                return "Vizag"
            return city
    return "India"

def extract_days(goal: str, default: int = 3):
    """
    Detect number of days in the goal text.
    """
    m = re.search(r"(\d+)\s*[-]?\s*day", goal, re.IGNORECASE)
    if m:
        try:
            return max(1, int(m.group(1)))
        except:
            pass
    m2 = re.search(r"for\s+(\d+)\s+days?", goal, re.IGNORECASE)
    if m2:
        try:
            return max(1, int(m2.group(1)))
        except:
            pass
    return default

def generate_plan(goal: str):
    """
    Generate a plan based on the goal type.
    Supports: workout, study, food, sightseeing, hiking, general trips, etc.
    """
    city = extract_city(goal)
    days = extract_days(goal, default=3)
    g = goal.lower()
    tasks = []

    # --- Workout ---
    if any(word in g for word in ["workout", "strength", "gym", "training", "fitness"]):
        base = [
            "Day 1 – Push (Chest/Triceps/Shoulders): Bench Press, Overhead Press, Dips, Lateral Raises",
            "Day 2 – Pull (Back/Biceps): Deadlift, Pull-Ups, Barbell Rows, Bicep Curls",
            "Day 3 – Legs: Squats, Romanian Deadlift, Lunges, Calf Raises",
            "Day 4 – Rest / Mobility work",
            "Day 5 – Full Body Strength: Clean & Press, Weighted Pull-Ups, Front Squats",
            "Day 6 – Active Recovery: light cardio, yoga, or stretching",
            "Day 7 – Rest"
        ]
        for i in range(days):
            tasks.append(base[i % len(base)])

    # --- Vegetarian food / food tour ---
    elif "vegetarian" in g or "food" in g or "restaurant" in g:
        base = [
            f"Explore top vegetarian restaurants in {city}",
            f"Try street / market food in {city}",
            f"Visit a highly-rated restaurant and attend a cooking demo in {city}"
        ]
        for i in range(days):
            tasks.append(base[i % len(base)])

    # --- Study routine ---
    elif "study" in g or "learn" in g:
        for i in range(days):
            tasks.extend([
                f"Morning focused study session - Day {i+1}",
                f"Practice exercises / problem-solving - Day {i+1}",
                f"Review and summarize notes - Day {i+1}"
            ])

    # --- Beach / Hiking ---
    elif "beach" in g or "hiking" in g or "trek" in g:
        base = [
            f"Beach walk and sunrise in {city}",
            f"Hike to a scenic viewpoint near {city}",
            f"Enjoy local seafood lunch in {city}"
        ]
        for i in range(days):
            tasks.append(base[i % len(base)])

    # --- Default: sightseeing ---
    else:
        base = [
            f"Explore top attractions in {city}",
            f"Try local food in {city}",
            f"Visit cultural landmarks in {city}"
        ]
        for i in range(days):
            tasks.append(base[i % len(base)])

    # --- Build itinerary ---
    itinerary = []
    for i in range(days):
        task = tasks[i] if i < len(tasks) else tasks[-1]

        # Enrich only if relevant (not for workouts or study)
        if any(word in g for word in ["workout", "strength", "gym", "training", "fitness", "study", "learn"]):
            places = None
        else:
            places = enrich_with_places(task)

        weather = get_weather_forecast(city, day_offset=i)
        itinerary.append({
            "day": i + 1,
            "task": task,
            "places": places,
            "weather": weather
        })

    return itinerary
