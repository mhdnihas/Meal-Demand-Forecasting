def calculate_fiber(age, gender):
    
    if gender == 'male':
        if age <= 50:
            return 38 
        else:
            return 30  
    elif gender == 'female':
        if age <= 50:
            return 25  
        else:
            return 21  
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'.")

def calculate_bmr(weight, height, age, gender):
    """Calculates Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation."""
    print('gender:',gender)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return bmr

def calculate_tdee(bmr, activity_level):
    """Calculates Total Daily Energy Expenditure (TDEE) based on activity level."""
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }
    return bmr * activity_factors.get(activity_level, 1.2)  
def calculate_calories(tdee, goal):
    """Adjusts TDEE based on the goal: maintenance, weight loss, or weight gain."""
    if goal == 'weight_loss':
        return tdee - 500  
    elif goal in ('weight_gain','muscle_gain'):
        return tdee + 500 
    else: 
        return tdee  

def calculate_protein_needs(weight, activity_level, goal):

    protein_factors = {
        'sedentary': 1.0, 
        'light': 1.2,
        'moderate': 1.4,
        'active': 1.6,
        'very active': 1.8
    }
    base_protein = protein_factors.get(activity_level, 1.0) * weight
    if goal == 'muscle_gain':
        return base_protein * 1.2
    return base_protein

def calculate_fat_needs(calories):
    fat_percentage = 0.25 
    fat_grams = (calories * fat_percentage)/9 
    return round(fat_grams,2)

def calculate_carbohydrates(calories, protein_grams, fat_grams):
    remaining_calories = calories - (protein_grams * 4 + fat_grams * 9)
    carb_grams = remaining_calories / 4 
    return round(carb_grams,2)


def calculate_sugar(total_calories, gender, added_sugar_limit=True):

    sugar_limits = {
        'male': 36,  
        'female': 25  
    }
    
    if added_sugar_limit:
        return sugar_limits.get(gender, 25) 
    else:
        return (total_calories * 0.10) / 4

def calculate_nutritional_needs(weight, height, age, gender, activity_level, goal):


    bmr = calculate_bmr(weight, height, age, gender )
    print('haihai')
    tdee = calculate_tdee(bmr, activity_level)

    daily_calories = calculate_calories(tdee, goal)

    protein_grams = calculate_protein_needs(weight, activity_level, goal)
    

    fat_grams = calculate_fat_needs(daily_calories)

    carb_grams = calculate_carbohydrates(daily_calories, protein_grams, fat_grams)

    fiber_grams=calculate_fiber(age,gender)

    sugar_grams=calculate_sugar(daily_calories,gender)

    Sodium=2300

    sat_fat_grams = round((daily_calories * 0.10) / 9,2)

    Cholesterol=300

    return {
        'calories': daily_calories,
        'fat (grams)': fat_grams,
        'sat_fat_grams':sat_fat_grams,
        'Cholesterol':Cholesterol,
        'Sodium':Sodium,
        'carbohydrates (grams)': carb_grams,
        'fiber (grams)':fiber_grams,
        'sugar (grams)':sugar_grams,
        'protein (grams)': protein_grams,

    }

weight = 80  
height = 180  
age = 30  
gender = 'male'  
activity_level = 'moderate' 
goal = 'muscle_gain'  

nutritional_needs = calculate_nutritional_needs(weight, height, age, gender, activity_level, goal)
print(nutritional_needs)
print("Daily Nutritional Needs:")
nutritions=[]
for nutrient, value in nutritional_needs.items():
    print(f"{nutrient}: {value:.2f}")
    nutritions.append(value)

print(nutritions)