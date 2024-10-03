import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import load_model
import json
import streamlit.components.v1 as components
import diet_recomentation
from diet_recomentation import calculate_nutritional_needs,recommand
import numpy as np
import pandas as pd

        
with open('Model/scaler_params.json', 'r') as file:
    scaler_params = json.load(file)

scaler_loaded = StandardScaler()
scaler_loaded.mean_ = np.array(scaler_params['mean'])
scaler_loaded.var_ = np.array(scaler_params['var'])
scaler_loaded.scale_ = np.sqrt(scaler_loaded.var_)

model=joblib.load('Model/lstmhyperparameter.pkl')

def predict_orders(features):
    input_data = np.array(features )
    
    input_data_reshaped = input_data.reshape(1, -1)

    
    scaled_data = scaler_loaded.transform(input_data_reshaped)

    print('scaled data :',scaled_data)
    prediction = model.predict(scaled_data)

    
    return prediction



import streamlit as st
import streamlit.components.v1 as components

import streamlit as st
import streamlit.components.v1 as components

def render_dashboard():
    st.write("## Dashboard Overview")
    st.write("""
    Here you can view detailed insights into your restaurant's performance 
    across different locations and meal categories, including historical 
    order data, trends, and other key metrics.
    """)

    query_params = st.query_params

    components.html(
        """
        <div class='tableauPlaceholder' id='viz1725323125508' style='position: relative'>
            <noscript><a href='#'>
                <img alt='Dashboard' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17240849634860&#47;Dashboard1&#47;1_rss.png' style='border: none'/>
            </a></noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F'/>
                <param name='embed_code_version' value='3'/>
                <param name='name' value='Book1_17240849634860&#47;Dashboard1'/>
                <param name='tabs' value='no'/>
                <param name='toolbar' value='yes'/>
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17240849634860&#47;Dashboard1&#47;1.png'/>
                <param name='animate_transition' value='yes'/>
                <param name='display_static_image' value='yes'/>
                <param name='display_spinner' value='yes'/>
                <param name='display_overlay' value='yes'/>
                <param name='display_count' value='yes'/>
                <param name='language' value='en-US'/>
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1725323125508');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = window.innerHeight + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
        """,
        height=query_params.get('height', [600])[0],
        width=query_params.get('width', [1200])[0]
    )






def render_prediction_interface(center_data, meal_data, predict_orders):
    st.write("## Predict Future Orders")
    st.write("Please input the required details for meal demand forecasting:")

    # Week Input
    week = st.number_input("Select the Week", step=1, min_value=1, max_value=28) + 117

    # Center ID and Meal ID Selection
    center_id_input = st.selectbox("Select Center ID", options=list(center_data.keys()))
    if center_id_input:
        center_details = center_data[center_id_input]
        op_area, center_type, city_code, region_code = center_details['op_area'][0], center_details['center_type'][0], center_details['city_code'][0], center_details['region_code'][0]
        
        st.write(f"Operational Area: **{op_area}**")
        st.write(f"Center Type: **{center_type}**")
        st.write(f"City Code: **{city_code}**")
        st.write(f"Region Code: **{region_code}**")

    meal_id_input = st.selectbox("Select Meal ID", options=list(meal_data.keys()))
    if meal_id_input:
        category, cusine = meal_data[meal_id_input][0], meal_data[meal_id_input][1]
        st.write(f"Category: **{category}**")
        st.write(f"Cuisine: **{cusine}**")

    # Promotion and Price Inputs
    home_page = st.selectbox("Home Page Promotion", options=[0, 1])
    email_promotion = st.selectbox("Email Promotion", options=[0, 1])
    checkout_price = st.number_input("Checkout Price", min_value=0.0, max_value=1000.0, step=0.01)
    base_price = st.number_input("Base Price", min_value=0.0, max_value=1000.0, step=0.01)

    # Feature Encoding for Prediction
    center_type_numeric = {'TYPE_A': 0, 'TYPE_B': 1, 'TYPE_C': 2}.get(center_type, 0)
    category_numeric = {
        'Beverages': 0, 'Biryani': 1, 'Desert': 2, 'Extras': 3, 'Fish': 4, 'Other Snacks': 5, 
        'Pasta': 6, 'Pizza': 7, 'Rice Bowl': 8, 'Salad': 9, 'Sandwich': 10, 'Seafood': 11, 
        'Soup': 12, 'Starters': 13
    }.get(category, 0)
    cuisine_numeric = {'Continental': 0, 'Indian': 1, 'Italian': 2, 'Thai': 3}.get(cusine, 0)

    features = [
        week, center_id_input, meal_id_input, checkout_price, base_price,
        email_promotion, home_page, city_code, region_code,
        center_type_numeric, op_area, category_numeric, cuisine_numeric
    ]

    # Submit and Predict
    if st.button("Submit"):
        num_orders = predict_orders(features)[0]
        st.markdown(f"<h1 style='font-size:50px;'>Predicted Number of Orders: {int(num_orders)}</h1>", unsafe_allow_html=True)



def client_interface(center_data, meal_data, predict_orders):
    st.title("Food Forecasting System - Client Interface")
    
    # Sidebar for Navigation
    st.sidebar.title("Client Options")
    section = st.sidebar.radio("Select Section", options=["Prediction","Dashboard"])

    # Section Routing
    if section == "Dashboard":
        render_dashboard()
    elif section == "Prediction":
        render_prediction_interface(center_data, meal_data, predict_orders)




# Reverse the mapping to create a dictionary with meal_id as key and (category, cuisine) as value
meal_data = {
    1062: ('Beverages', 'Italian'),
    1109: ('Rice Bowl', 'Indian'),
    1198: ('Extras', 'Thai'),
    1207: ('Beverages', 'Continental'),
    1216: ('Pasta', 'Italian'),
    1230: ('Beverages', 'Continental'),
    1247: ('Biryani', 'Indian'),
    1248: ('Beverages', 'Indian'),
    1311: ('Extras', 'Thai'),
    1438: ('Soup', 'Thai'),
    1445: ('Seafood', 'Continental'),
    1525: ('Other Snacks', 'Thai'),
    1543: ('Desert', 'Indian'),
    1558: ('Pizza', 'Continental'),
    1571: ('Fish', 'Continental'),
    1727: ('Rice Bowl', 'Indian'),
    1754: ('Sandwich', 'Italian'),
    1770: ('Biryani', 'Indian'),
    1778: ('Beverages', 'Italian'),
    1803: ('Extras', 'Thai'),
    1847: ('Soup', 'Thai'),
    1878: ('Starters', 'Thai'),
    1885: ('Beverages', 'Thai'),
    1902: ('Biryani', 'Indian'),
    1962: ('Pizza', 'Continental'),
    1971: ('Sandwich', 'Italian'),
    1993: ('Beverages', 'Thai'),
    2104: ('Fish', 'Continental'),
    2126: ('Pasta', 'Italian'),
    2139: ('Beverages', 'Indian'),
    2290: ('Rice Bowl', 'Indian'),
    2304: ('Desert', 'Indian'),
    2306: ('Pasta', 'Italian'),
    2322: ('Beverages', 'Continental'),
    2444: ('Seafood', 'Continental'),
    2490: ('Salad', 'Italian'),
    2492: ('Desert', 'Indian'),
    2494: ('Soup', 'Thai'),
    2539: ('Beverages', 'Thai'),
    2569: ('Salad', 'Italian'),
    2577: ('Starters', 'Thai'),
    2581: ('Pizza', 'Continental'),
    2631: ('Beverages', 'Indian'),
    2640: ('Starters', 'Thai'),
    2664: ('Salad', 'Italian'),
    2704: ('Other Snacks', 'Thai'),
    2707: ('Beverages', 'Italian'),
    2760: ('Other Snacks', 'Thai'),
    2826: ('Sandwich', 'Italian'),
    2867: ('Seafood', 'Continental'),
    2956: ('Fish', 'Continental')
}

center_data={10: {'center_type': ['TYPE_B'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [6.3]},
 11: {'center_type': ['TYPE_A'],
  'city_code': [679],
  'region_code': [56],
  'op_area': [3.7]},
 13: {'center_type': ['TYPE_B'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [6.7]},
 14: {'center_type': ['TYPE_C'],
  'city_code': [654],
  'region_code': [56],
  'op_area': [2.7]},
 17: {'center_type': ['TYPE_A'],
  'city_code': [517],
  'region_code': [56],
  'op_area': [3.2]},
 20: {'center_type': ['TYPE_A'],
  'city_code': [522],
  'region_code': [56],
  'op_area': [4.0]},
 23: {'center_type': ['TYPE_A'],
  'city_code': [698],
  'region_code': [23],
  'op_area': [3.4]},
 24: {'center_type': ['TYPE_B'],
  'city_code': [614],
  'region_code': [85],
  'op_area': [3.6]},
 26: {'center_type': ['TYPE_C'],
  'city_code': [515],
  'region_code': [77],
  'op_area': [3.0]},
 27: {'center_type': ['TYPE_A'],
  'city_code': [713],
  'region_code': [85],
  'op_area': [4.5]},
 29: {'center_type': ['TYPE_C'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [4.0]},
 30: {'center_type': ['TYPE_A'],
  'city_code': [604],
  'region_code': [56],
  'op_area': [3.5]},
 32: {'center_type': ['TYPE_A'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [3.8]},
 34: {'center_type': ['TYPE_B'],
  'city_code': [615],
  'region_code': [34],
  'op_area': [4.2]},
 36: {'center_type': ['TYPE_B'],
  'city_code': [517],
  'region_code': [56],
  'op_area': [4.4]},
 39: {'center_type': ['TYPE_C'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [3.8]},
 41: {'center_type': ['TYPE_C'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [1.9]},
 42: {'center_type': ['TYPE_B'],
  'city_code': [561],
  'region_code': [77],
  'op_area': [3.9]},
 43: {'center_type': ['TYPE_A'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [5.1]},
 50: {'center_type': ['TYPE_A'],
  'city_code': [556],
  'region_code': [77],
  'op_area': [4.8]},
 51: {'center_type': ['TYPE_A'],
  'city_code': [638],
  'region_code': [56],
  'op_area': [7.0]},
 52: {'center_type': ['TYPE_B'],
  'city_code': [685],
  'region_code': [56],
  'op_area': [5.6]},
 53: {'center_type': ['TYPE_A'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [3.8]},
 55: {'center_type': ['TYPE_C'],
  'city_code': [647],
  'region_code': [56],
  'op_area': [2.0]},
 57: {'center_type': ['TYPE_C'],
  'city_code': [541],
  'region_code': [77],
  'op_area': [2.8]},
 58: {'center_type': ['TYPE_C'],
  'city_code': [695],
  'region_code': [77],
  'op_area': [3.8]},
 59: {'center_type': ['TYPE_A'],
  'city_code': [456],
  'region_code': [56],
  'op_area': [4.2]},
 61: {'center_type': ['TYPE_A'],
  'city_code': [473],
  'region_code': [77],
  'op_area': [4.5]},
 64: {'center_type': ['TYPE_A'],
  'city_code': [553],
  'region_code': [77],
  'op_area': [4.4]},
 65: {'center_type': ['TYPE_A'],
  'city_code': [602],
  'region_code': [34],
  'op_area': [4.8]},
 66: {'center_type': ['TYPE_A'],
  'city_code': [648],
  'region_code': [34],
  'op_area': [4.1]},
 67: {'center_type': ['TYPE_B'],
  'city_code': [638],
  'region_code': [56],
  'op_area': [7.0]},
 68: {'center_type': ['TYPE_B'],
  'city_code': [676],
  'region_code': [34],
  'op_area': [4.1]},
 72: {'center_type': ['TYPE_C'],
  'city_code': [638],
  'region_code': [56],
  'op_area': [3.9]},
 73: {'center_type': ['TYPE_A'],
  'city_code': [576],
  'region_code': [34],
  'op_area': [4.0]},
 74: {'center_type': ['TYPE_A'],
  'city_code': [702],
  'region_code': [35],
  'op_area': [2.8]},
 75: {'center_type': ['TYPE_B'],
  'city_code': [651],
  'region_code': [77],
  'op_area': [4.7]},
 76: {'center_type': ['TYPE_A'],
  'city_code': [614],
  'region_code': [85],
  'op_area': [3.0]},
 77: {'center_type': ['TYPE_A'],
  'city_code': [676],
  'region_code': [34],
  'op_area': [3.8]},
 80: {'center_type': ['TYPE_C'],
  'city_code': [604],
  'region_code': [56],
  'op_area': [5.1]},
 81: {'center_type': ['TYPE_A'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [4.0]},
 83: {'center_type': ['TYPE_A'],
  'city_code': [659],
  'region_code': [77],
  'op_area': [5.3]},
 86: {'center_type': ['TYPE_C'],
  'city_code': [699],
  'region_code': [85],
  'op_area': [4.0]},
 88: {'center_type': ['TYPE_A'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [4.1]},
 89: {'center_type': ['TYPE_A'],
  'city_code': [703],
  'region_code': [56],
  'op_area': [4.8]},
 91: {'center_type': ['TYPE_C'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [0.9]},
 92: {'center_type': ['TYPE_C'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [2.9]},
 93: {'center_type': ['TYPE_A'],
  'city_code': [461],
  'region_code': [34],
  'op_area': [3.9]},
 94: {'center_type': ['TYPE_C'],
  'city_code': [632],
  'region_code': [34],
  'op_area': [3.6]},
 97: {'center_type': ['TYPE_A'],
  'city_code': [628],
  'region_code': [77],
  'op_area': [4.6]},
 99: {'center_type': ['TYPE_A'],
  'city_code': [596],
  'region_code': [71],
  'op_area': [4.5]},
 101: {'center_type': ['TYPE_C'],
  'city_code': [699],
  'region_code': [85],
  'op_area': [2.8]},
 102: {'center_type': ['TYPE_A'],
  'city_code': [593],
  'region_code': [77],
  'op_area': [2.8]},
 104: {'center_type': ['TYPE_A'],
  'city_code': [647],
  'region_code': [56],
  'op_area': [4.5]},
 106: {'center_type': ['TYPE_A'],
  'city_code': [675],
  'region_code': [34],
  'op_area': [4.0]},
 108: {'center_type': ['TYPE_B'],
  'city_code': [579],
  'region_code': [56],
  'op_area': [4.4]},
 109: {'center_type': ['TYPE_A'],
  'city_code': [599],
  'region_code': [56],
  'op_area': [3.6]},
 110: {'center_type': ['TYPE_A'],
  'city_code': [485],
  'region_code': [77],
  'op_area': [3.8]},
 113: {'center_type': ['TYPE_C'],
  'city_code': [680],
  'region_code': [77],
  'op_area': [4.0]},
 124: {'center_type': ['TYPE_C'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [4.0]},
 126: {'center_type': ['TYPE_A'],
  'city_code': [577],
  'region_code': [56],
  'op_area': [2.7]},
 129: {'center_type': ['TYPE_A'],
  'city_code': [593],
  'region_code': [77],
  'op_area': [3.9]},
 132: {'center_type': ['TYPE_A'],
  'city_code': [522],
  'region_code': [56],
  'op_area': [3.9]},
 137: {'center_type': ['TYPE_A'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [4.4]},
 139: {'center_type': ['TYPE_C'],
  'city_code': [693],
  'region_code': [34],
  'op_area': [2.8]},
 143: {'center_type': ['TYPE_B'],
  'city_code': [562],
  'region_code': [77],
  'op_area': [3.8]},
 145: {'center_type': ['TYPE_A'],
  'city_code': [620],
  'region_code': [77],
  'op_area': [3.9]},
 146: {'center_type': ['TYPE_B'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [5.0]},
 149: {'center_type': ['TYPE_A'],
  'city_code': [478],
  'region_code': [77],
  'op_area': [2.4]},
 152: {'center_type': ['TYPE_B'],
  'city_code': [576],
  'region_code': [34],
  'op_area': [4.0]},
 153: {'center_type': ['TYPE_A'],
  'city_code': [590],
  'region_code': [56],
  'op_area': [3.9]},
 157: {'center_type': ['TYPE_A'],
  'city_code': [609],
  'region_code': [93],
  'op_area': [4.1]},
 161: {'center_type': ['TYPE_B'],
  'city_code': [658],
  'region_code': [34],
  'op_area': [3.9]},
 162: {'center_type': ['TYPE_C'],
  'city_code': [526],
  'region_code': [34],
  'op_area': [2.0]},
 174: {'center_type': ['TYPE_A'],
  'city_code': [700],
  'region_code': [56],
  'op_area': [7.0]},
 177: {'center_type': ['TYPE_A'],
  'city_code': [683],
  'region_code': [56],
  'op_area': [3.4]},
 186: {'center_type': ['TYPE_A'],
  'city_code': [649],
  'region_code': [34],
  'op_area': [3.4]}}


if 'selected_meal_id' not in st.session_state:
    st.session_state.selected_meal_id = None

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

if 'selected_cuisine' not in st.session_state:
    st.session_state.selected_cuisine = None

if 'interface' not in st.session_state:
    st.session_state.interface = 'User'

col1, col2, col3 = st.columns([1, 2, 1])

with col2:  
    col2_1, col2_2 = st.columns([1, 1])

    with col2_1:
        user_button = st.button("User", key='user_button')
    with col2_2:
        client_button = st.button("Client", key='client_button')

# Determine which button was clicked
if user_button:
    st.session_state.interface = 'User'
elif client_button:
    st.session_state.interface = 'Client'

# Show the interface based on the selected state
if st.session_state.interface == 'User':
    st.title("Food Forecasting System - User Interface")
    st.sidebar.title("User Options")
    # User-specific content
    st.write("Welcome to the User Interface!")
    st.title("Personalized Diet Recommendation")


    age = st.number_input("Enter your age", min_value=10, max_value=100, value=30)
    gender = st.selectbox("Select your gender", ["male", "female"])
    height = st.number_input("Enter your height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("Enter your weight (kg)", min_value=30, max_value=200, value=70)
    activity_level = st.selectbox("Select your activity level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    goal = st.selectbox("Select your goal", ["weight_gain", "weight_loss", "muscle_gain"])
    

    max_values = {
    'calories': 3000,  
    'carbohydrates (grams)': 550,  
    'protein (grams)': 150,  
    'fiber (grams)': 100,  
    'fat (grams)': 130,  
    'sat_fat_grams': 40,  
    'sugar (grams)': 80,  
    'Sodium': 3500,  
    'Cholesterol': 350,  
    }
    def get_progress_value(nutrient_value, max_value):
        return min(nutrient_value / max_value, 1) 
    

    
    if st.button("Get Nutritional Recommendations"):
        nutritional_needs,nutritions = calculate_nutritional_needs(weight, height, age, gender, activity_level, goal)

        st.subheader("Your Daily Nutritional Needs vs Maximum Recommended Nutrients:")

    # Splitting the content into two columns for comparison
        col1, col2 = st.columns(2)

    # Column 1 - User's Daily Nutritional Needs
        with col1:
            st.metric(label="Calories", value=f"{nutritional_needs['calories']} kcal", delta="Daily Requirement")

            st.write("🌾 **Carbohydrates**")
            st.progress(get_progress_value(nutritional_needs['carbohydrates (grams)'], max_values['carbohydrates (grams)']))
            st.write(f"{nutritional_needs['carbohydrates (grams)']}g / {max_values['carbohydrates (grams)']}g")

            st.write("🥩 **Protein**")
            st.progress(get_progress_value(nutritional_needs['protein (grams)'], max_values['protein (grams)']))
            st.write(f"{nutritional_needs['protein (grams)']}g / {max_values['protein (grams)']}g")

            st.write("🍞 **Fiber**")
            st.progress(get_progress_value(nutritional_needs['fiber (grams)'], max_values['fiber (grams)']))
            st.write(f"{nutritional_needs['fiber (grams)']}g / {max_values['fiber (grams)']}g")

        with col2:
            st.write("🍫 **Fat**")
            st.progress(get_progress_value(nutritional_needs['fat (grams)'], max_values['fat (grams)']))
            st.write(f"{nutritional_needs['fat (grams)']}g / {max_values['fat (grams)']}g")

            st.write("🍟 **Saturated Fat**")
            st.progress(get_progress_value(nutritional_needs['sat_fat_grams'], max_values['sat_fat_grams']))
            st.write(f"{nutritional_needs['sat_fat_grams']}g / {max_values['sat_fat_grams']}g")

            st.write("🍧 **Sugar**")
            st.progress(get_progress_value(nutritional_needs['sugar (grams)'], max_values['sugar (grams)']))
            st.write(f"{nutritional_needs['sugar (grams)']}g / {max_values['sugar (grams)']}g")

        st.subheader("Additional Nutritional Information:")
        col3, col4 = st.columns(2)
        with col3:
            st.write(f"🧂 **Sodium**: {nutritional_needs['Sodium']} mg / {max_values['Sodium']} mg")
            st.progress(get_progress_value(nutritional_needs['Sodium'], max_values['Sodium']))

        with col4:
            st.write(f"🍳 **Cholesterol**: {nutritional_needs['Cholesterol']} mg / {max_values['Cholesterol']} mg")
            st.progress(get_progress_value(nutritional_needs['Cholesterol'], max_values['Cholesterol']))

    # Nutritional Notes Section
        st.markdown("""
    ### Nutritional Notes:
    - 🟢 Keep an eye on your sugar and fat intake.
    - 🔴 Limit sodium consumption to avoid health risks.
            """)


        # 'calories': daily_calories,
        # 'fat (grams)': fat_grams,
        # 'sat_fat_grams':sat_fat_grams,
        # 'Cholesterol':Cholesterol,
        # 'Sodium':Sodium,
        # 'carbohydrates (grams)': carb_grams,
        # 'fiber (grams)':fiber_grams,
        # 'sugar (grams)':sugar_grams,
        # 'protein (grams)': protein_grams,
    # Highlight important notes
 
        st.subheader("Recommended Foods Based on Your Nutritional Needs:")

    # Assuming the `recommand` function returns a DataFrame with food recommendations
        recommended_foods = recommand(np.array(nutritions).reshape(1,-1))
        styled_table = recommended_foods.style.set_properties(**{
    'background-color': '#f0f0f0',  # Light gray background for data cells
    'border': '2px solid #bbbbbb',   # Light gray border for subtle separation
    'color': '#333333',              # Dark gray text for data cells
    'font-size': '18px',             # Standard font size
    'text-align': 'center',
    'padding': '10px'                # Padding for better spacing
        }).set_table_attributes('style="border-collapse:collapse;width:100%; background: linear-gradient(90deg, #d3d3d3, #d3d3d3);"')  # Gradient background for a modern feel

# Hide the index and set the column header styles
        styled_table = styled_table.hide(axis='index').set_table_styles([
        {'selector': 'th', 'props': [
        ('background-color', '#f0f0f0'),  # Match header background with data cells for consistency
        ('color', '#000000'),              # Set header text color to black for readability
        ('font-size', '18px'),
        ('text-align', 'center'),
        ('padding', '10px')
        ]}
        ])

# Render the styled table with HTML in Streamlit
        st.write("Here are the foods recommended for you:")
        st.write(styled_table.to_html(), unsafe_allow_html=True)
    # You can add images or color codes to make the output more visually appealing
        st.markdown("""
        **🥗 Suggested Food**
        - 📌 Calories, Protein, Fiber, etc. are matched with your goals!
        """)
    
elif st.session_state.interface == 'Client':
    client_interface(center_data, meal_data, predict_orders)
