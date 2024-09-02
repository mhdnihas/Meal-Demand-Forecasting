import streamlit as st
import streamlit.components.v1 as components

# Sample data provided by the user
meal_category_mapping = {
    'Sandwich': [1971, 1754, 2826],
    'Beverages': [1248, 1230, 2539, 1993, 1207, 2631, 1778, 1062, 1885, 2322, 2707, 2139],
    'Biryani': [1902, 1247, 1770],
    'Pizza': [2581, 1558, 1962],
    'Pasta': [1216, 2306, 2126],
    'Desert': [2492, 2304, 1543],
    'Seafood': [1445, 2867, 2444],
    'Starters': [2577, 2640, 1878],
    'Rice Bowl': [2290, 1727, 1109],
    'Other Snacks': [2704, 2760, 1525],
    'Soup': [2494, 1847, 1438],
    'Extras': [1803, 1311, 1198],
    'Salad': [2664, 2569, 2490],
    'Fish': [2104, 2956, 1571]
}

# Reverse the mapping to find category by meal_id
meal_to_category = {meal_id: category for category, meal_ids in meal_category_mapping.items() for meal_id in meal_ids}

# Initialize session state for meal_id and category if not already set
if 'selected_meal_id' not in st.session_state:
    st.session_state.selected_meal_id = None

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Set default to user interface if not already set
if 'interface' not in st.session_state:
    st.session_state.interface = 'User'

# Create a horizontal layout for the buttons with equal width
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Center the buttons
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
    # Add your user interface code here

elif st.session_state.interface == 'Client':
    st.title("Food Forecasting System - Client Interface")
    st.sidebar.title("Client Options")

    # Embed Tableau Public dashboard
    st.write("Dashboard:")
    tableau_url = "https://public.tableau.com/shared/YXGCKBZPD?:display_count=n&:origin=viz_share_link"  # Replace with your actual Tableau Public URL
    components.iframe(tableau_url, height=600)  # Adjust height as needed

    st.write("Please input the required details:")

    # Dropdown list for meal_id
    all_meal_ids = sum(meal_category_mapping.values(), [])
    meal_id_input = st.selectbox("Select Meal ID", options=all_meal_ids)

    # Automatically set category based on meal_id
    if meal_id_input:
        st.session_state.selected_meal_id = meal_id_input
        st.session_state.selected_category = meal_to_category.get(meal_id_input, None)

    # Display the category
    category_display = st.text_input("Category", value=st.session_state.selected_category if st.session_state.selected_category else "", disabled=True)

    # Update meal_id list based on selected category
    if st.session_state.selected_category:
        related_meal_ids = meal_category_mapping.get(st.session_state.selected_category, [])
        st.selectbox("Meal ID in Selected Category", options=related_meal_ids, key='meal_id_in_category')

    # Additional inputs
    center_id = st.selectbox("Select Center ID", options=[10, 20, 30, 40])  # Example center_ids
    region_code = st.selectbox("Select Region Code", options=[1, 2, 3, 4])  # Example region_codes
    home_page = st.selectbox("Home Page Promotion", options=[0, 1])
    email_promotion = st.selectbox("Email Promotion", options=[0, 1])
    cusin = st.selectbox("Cuisine", options=["Indian", "Italian", "Chinese", "Mexican"])  # Example cuisines
    center_type = st.selectbox("Center Type", options=["Type 1", "Type 2", "Type 3"])  # Example center types
    city_code = st.selectbox("City Code", options=[111, 222, 333, 444])  # Example city_codes

    checkout_price = st.number_input("Checkout Price", min_value=0.0, max_value=1000.0, step=0.01)
    base_price = st.number_input("Base Price", min_value=0.0, max_value=1000.0, step=0.01)
    op_area = st.number_input("Operational Area", min_value=0.0, max_value=100.0, step=0.01)
    
    # Submit button
    if st.button("Submit"):
        st.write(f"Meal ID: {st.session_state.selected_meal_id}")
        st.write(f"Center ID: {center_id}")
        st.write(f"Region Code: {region_code}")
        st.write(f"Home Page Promotion: {home_page}")
        st.write(f"Email Promotion: {email_promotion}")
        st.write(f"Category: {st.session_state.selected_category}")
        st.write(f"Cuisine: {cusin}")
        st.write(f"Center Type: {center_type}")
        st.write(f"City Code: {city_code}")
        st.write(f"Checkout Price: {checkout_price}")
        st.write(f"Base Price: {base_price}")
        st.write(f"Operational Area: {op_area}")
