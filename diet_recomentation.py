from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
import numpy as np



dataset=pd.read_csv('DATA/recipes1.csv')
columns=['Name','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
dataset=dataset[columns]
print(dataset.head(5))

# maximum values of nutritions
max_Calories=35000
max_daily_fat=130
max_daily_Saturatedfat=40
max_daily_Cholesterol=350
max_daily_Sodium=2500
max_daily_Carbohydrate=550
max_daily_Fiber=100
max_daily_Sugar=80
max_daily_Protein=150
max_list=[max_Calories,max_daily_fat,max_daily_Saturatedfat,max_daily_Cholesterol,max_daily_Sodium,max_daily_Carbohydrate,max_daily_Fiber,max_daily_Sugar,max_daily_Protein]

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

    },[daily_calories,fat_grams,sat_fat_grams,Cholesterol,Sodium,carb_grams,fiber_grams,sugar_grams,protein_grams]


def scaling(dataframe):
    scaler=StandardScaler()
    print(dataframe.iloc[:,2:])
    prep_data=scaler.fit_transform(dataframe.iloc[:,2:].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    print('neighors,neigh:',neigh.kneighbors)
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,max_nutritional_values,ingredient_filter=None):
    extracted_data=dataframe.copy()
    for column,maximum in zip(extracted_data.columns[2:],max_nutritional_values):
        extracted_data=extracted_data[extracted_data[column]<maximum]
    if ingredient_filter!=None:
        for ingredient in ingredient_filter:
            extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient,regex=False)]
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    print('apply_pipeline:',extracted_data.iloc[pipeline.transform(_input)[0]])
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommand(_input,ingredient_filter=None,params={'return_distance':False}):
    extract_dataset=extract_data(dataset,max_nutritional_values=max_list)
    prep_data,scaler=scaling(extract_dataset)
    neigh=nn_predictor(prep_data)
    print('neigh:',neigh)
    pipeline=build_pipeline(neigh,scaler,params)
    recoment=apply_pipeline(pipeline,_input,extract_dataset)
    return recoment[['Name','RecipeIngredientParts','Calories', 'FatContent', 'SaturatedFatContent',
                     'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
                     'FiberContent', 'SugarContent', 'ProteinContent']]










weight = 80  
height = 180  
age = 30  
gender = 'male'  
activity_level = 'moderate' 
goal = 'muscle_gain'  

nutritional_needs,nutritions = calculate_nutritional_needs(weight, height, age, gender, activity_level, goal)
print(nutritional_needs)
print("Daily Nutritional Needs:")
nutritions=[]
for nutrient, value in nutritional_needs.items():
    print(f"{nutrient}: {value:.2f}")
    nutritions.append(value)

print(nutritions)