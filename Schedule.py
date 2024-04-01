# Boolean list of days where indian buffet is required
indian_buffet = [True, False, True, True, False, True, False]

# Predicted number of customers for each day of the week
predicted_customers = [100, 120, 80, 90, 110, 130, 95]

# Constants and variables initialization
FULL_TIME_HOURS = 40
PART_TIME_HOURS = 33
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Staff members
full_time_staff = {
    "kitchen_staff": 5,
    "service_staff": 5,
    "dishwashers": 2 #fixed
}
part_time_staff = {
    "service_staff": 3
}

# Buffet staffing requirements
indian_buffet_staffing = {100: 2, "else": 3}
chinese_buffet_staffing = {100: (1, 2), "else": (2, 3)}

# Initialize schedule
schedule = {day: [] for day in WEEK_DAYS}


# Iterate over each day of the week
for idx, day in enumerate(WEEK_DAYS):
    # Determine the number of staff needed for each shift
    # Food Court: 10am to 4:30pm
    food_court_staff = {"cashier": 2, "clearer": 1, "buffer_staff": 1}

    # Indian Buffet: 8pm to 10pm ## buffet customers part of predicted customers?
    indian_buffet_customers = predicted_customers[idx] if indian_buffet[idx] else 0
    indian_buffet_staff = indian_buffet_staffing[100] if indian_buffet_customers <= 100 else indian_buffet_staffing["else"]

    # Chinese Buffet: 7pm to 10pm
    chinese_customers = predicted_customers[idx]
    chinese_chefs, chinese_service_staff = chinese_buffet_staffing[100] if chinese_customers <= 100 else chinese_buffet_staffing["else"]

    # Total staff needed for the day
    total_staff = sum(food_court_staff.values()) + indian_buffet_staff + chinese_chefs + chinese_service_staff

    # Assign full-time and part-time staff to fulfill minimum working hours
    full_time_assigned = {role: min(full_time_staff[role], FULL_TIME_HOURS // 7) for role in full_time_staff}
    part_time_assigned = {role: min(part_time_staff[role], PART_TIME_HOURS // 7) for role in part_time_staff}



    # Assign staff to each shift
    # Assign full-time staff
    for role, count in full_time_assigned.items():
        for _ in range(count):
            schedule[day].append({"role": role, "hours": []})

    # Assign part-time staff
    for role, count in part_time_assigned.items():
        for _ in range(count):
            schedule[day].append({"role": role, "hours": []})

    # Assign staff to each hour
    for hour in range(24):
        # Food Court Shift
        if 10 <= hour < 16: #need to fix
            for _ in range(food_court_staff["cashier"]):
                schedule[day][hour]["hours"].append("cashier")
            for _ in range(food_court_staff["clearer"]):
                schedule[day][hour]["hours"].append("clearer")
            for _ in range(food_court_staff["buffer_staff"]):
                schedule[day][hour]["hours"].append("buffer_staff")

        # Indian Buffet Shift
        if 20 <= hour < 22 and indian_buffet[idx]:
            for _ in range(indian_buffet_staff):
                schedule[day][hour]["hours"].append("indian_staff")

        # Chinese Buffet Shift
        if 19 <= hour < 22:
            for _ in range(chinese_chefs):
                schedule[day][hour]["hours"].append("chinese_chef")
            for _ in range(chinese_service_staff):
                schedule[day][hour]["hours"].append("chinese_service_staff")

# Print the schedule
for day, shifts in schedule.items():
    print(day)
    for idx, shift in enumerate(shifts):
        print(f"\tHour {idx}: {', '.join(shift['hours'])}")
