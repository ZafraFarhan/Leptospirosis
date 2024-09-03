import streamlit as st
from PIL import Image
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder


# Load the RandomForestClassifier model from the pickle file
world_cases = pickle.load(open('./World cases.pkl', 'rb'))
sl_cases = pickle.load(open('./Sri Lanka.pkl', 'rb'))
world_deaths = pickle.load(open('./World deaths.pkl', 'rb'))
us_cases = pickle.load(open('./USA cases.pkl', 'rb'))


def run():
    st.set_page_config(layout="wide")
  
    st.markdown("""
    <head>
        <meta charset="UTF-8">
        <title>All Navigation Menu Hover Animation | CodingLab</title> 
        <style>
            .nav-links {
                list-style: none;
                display: flex;
                justify-content: space-around;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                font-size: 20px;
            }
            .nav-links li {
                position: relative;
                padding: 10px 20px;
                cursor: pointer;
                transition: transform 0.3s ease;
            }
            .nav-links li a {
                color: #000;
                text-decoration: none;
            }
            .center::after, .upward::after, .forward::after {
                content: '';
                position: absolute;
                width: 100%;
                height: 2px;
                bottom: -5px;
                left: 0;
                background-color: #000;
                transform: scaleX(0);
                transition: transform 0.3s ease;
            }
            .center::after {
                transform-origin: center;
            }
            .upward::after {
                transform-origin: bottom;
            }
            .forward::after {
                transform-origin: top right;
            }
            .nav-links li:hover::after {
                transform: scaleX(1);
            }
        </style>
    </head>
    """, unsafe_allow_html=True)

    st.markdown("""
    <body>
        <ul class="nav-links">
            <li class="center"><a href="https://zafrafarhan461.wixsite.com/leptospirosis">Home</a></li>
            <li class="center"><a href="https://zafrafarhan461.wixsite.com/leptospirosis">Phases & Signs</a></li>
            <li class="upward"><a href="https://zafrafarhan461.wixsite.com/leptospirosis">Diagnosis</a></li>
            <li class="upward"><a href="https://zafrafarhan461.wixsite.com/leptospirosis">Prevention</a></li>
            <li class="upward"><a href="https://charts.mongodb.com/charts-leptospirosis-tduzvva/dashboards/fdf19f6f-8237-4327-80a0-393fd24e0808">Dashboard</a></li>
            <li class="forward"><a href="#">Prediction</a></li>
        </ul>
    </body>
    """, unsafe_allow_html=True)

    image_path = "./bg.png"  # Assuming bg.jpg is in the same directory as your script
    img1 = Image.open(image_path)
    #img1 = img1.resize((80, 50), Image.BICUBIC)  # Use BICUBIC filter for better quality
    st.image(img1, use_column_width=True)


    st.markdown("# Leptospirosis Globally")
    col1, col2 = st.columns(2)

    with col1:
        country_display = ('Austria', 'Belgium', 'Bulgaria',
                           'Croatia', 'Cyprus', 'Czechia',
                           'Denmark', 'EU (with UK until 2019)',
                           'EU (without UK)', 'EU/EEA (with UK until 2019)',
                           'EU/EEA (without UK)', 'Estonia', 'Finland',
                           'France', 'Germany', 'Greece',
                           'Hungary', 'Iceland', 'Ireland',
                           'Italy', 'Latvia', 'Lithuania',
                           'Luxembourg', 'Malta', 'Netherlands',
                           'Poland', 'Portugal', 'Romania',
                           'Slovakia', 'Slovenia', 'Spain',
                           'Sri Lanka', 'Sweden', 'USA',
                           'United Kingdom')   
        country_options = list(range(len(country_display)))
        country = st.selectbox("Country", country_options, format_func=lambda x: country_display[x], key="global_country")

    with col2:
        year_display = tuple(str(year) for year in range(2024, 2051))
        year_options = list(range(len(year_display)))
        year = st.selectbox("Year", year_options, format_func=lambda x: year_display[x], key="global_year")

    # When the button is clicked
    if st.button("Global Cases Prediction", key="global_button"):
        le = LabelEncoder()
        le.fit(country_display)  # Fit the encoder on the actual country names
        selected_country_encoded = le.transform([country_display[country]])[0]

        num_features = 36  # Update this to the number of features used by your model
        feature_vector = np.zeros(num_features)
        
        feature_order = ['Austria', 'Belgium', 'Bulgaria',
                           'Croatia', 'Cyprus', 'Czechia',
                           'Denmark', 'EU (with UK until 2019)',
                           'EU (without UK)', 'EU/EEA (with UK until 2019)',
                           'EU/EEA (without UK)', 'Estonia', 'Finland',
                           'France', 'Germany', 'Greece',
                           'Hungary', 'Iceland', 'Ireland',
                           'Italy', 'Latvia', 'Lithuania',
                           'Luxembourg', 'Malta', 'Netherlands',
                           'Poland', 'Portugal', 'Romania',
                           'Slovakia', 'Slovenia', 'Spain',
                           'Sri Lanka', 'Sweden', 'USA',
                           'United Kingdom','Year']
        country_index = feature_order.index(country_display[country])
        feature_vector[country_index] = selected_country_encoded
        
        # Set the year in the correct position
        year_index = feature_order.index('Year')
        feature_vector[year_index] = int(year)

        # Perform the prediction
        prediction = world_cases.predict([feature_vector])
        rounded_prediction = round(prediction[0])
        st.write(f"Prediction result for {country_display[country]} in {year_display[year]}: {rounded_prediction[0]}")
        

    #################################################################################################


    if st.button("Global Death Prediction", key="globald_button"):
        le = LabelEncoder()
        le.fit(country_display)  # Fit the encoder on the actual country names
        selected_country_encoded = le.transform([country_display[country]])[0]

        num_features = 36  # Update this to the number of features used by your model
        feature_vector = np.zeros(num_features)
        
        feature_order = ['Austria', 'Belgium', 'Bulgaria',
                           'Croatia', 'Cyprus', 'Czechia',
                           'Denmark', 'EU (with UK until 2019)',
                           'EU (without UK)', 'EU/EEA (with UK until 2019)',
                           'EU/EEA (without UK)', 'Estonia', 'Finland',
                           'France', 'Germany', 'Greece',
                           'Hungary', 'Iceland', 'Ireland',
                           'Italy', 'Latvia', 'Lithuania',
                           'Luxembourg', 'Malta', 'Netherlands',
                           'Poland', 'Portugal', 'Romania',
                           'Slovakia', 'Slovenia', 'Spain',
                           'Sri Lanka', 'Sweden', 'USA',
                           'United Kingdom','Year']
        country_index = feature_order.index(country_display[country])
        feature_vector[country_index] = selected_country_encoded
        
        # Set the year in the correct position
        year_index = feature_order.index('Year')
        feature_vector[year_index] = int(year)

        # Perform the prediction
        prediction = world_deaths.predict([feature_vector])
        rounded_prediction = round(prediction[0])
        st.write(f"Death prediction result for {country_display[country]} in {year_display[year]}: {rounded_prediction[0]}")
        

    #################################################################################################

    st.markdown("# Leptospirosis in the USA")
    col1, col2 = st.columns(2)

    with col1:
        uregion_display = ('Alabama', 'Arizona', 'Arkansas',
       'California', 'Delaware', 'District of Columbia',
       'Florida', 'Georgia', 'Guam', 'Hawaii',
       'Illinois', 'Indiana', 'Kentucky',
       'Louisiana', 'Maryland', 'Massachusetts',
       'Michigan', 'Minnesota', 'Missouri',
       'Nebraska', 'New York City', 'North Carolina',
       'North Dakota', 'Ohio', 'Oregon',
       'Pennsylvania', 'Puerto Rico', 'Rhode Island',
       'U.S. Virgin Islands', 'Utah', 'Vermont',
       'Virginia', 'Wisconsin')  
        uregion_options = list(range(len(uregion_display)))
        uregion = st.selectbox("Region", uregion_options, format_func=lambda x: uregion_display[x], key="us_region")

    with col2:
        year_displaysu = tuple(str(year) for year in range(2024, 2051))
        year_optionssu = list(range(len(year_displaysu)))
        yearsu = st.selectbox("Year", year_optionssu, format_func=lambda x: year_displaysu[x], key="us_year")

    if st.button("USA Cases Prediction", key="us_button"):
        le = LabelEncoder()
        le.fit(uregion_display) 

        selected_regionu_encoded = le.transform([uregion_display[uregion]])[0]

        num_features = 34  
        feature_vector = np.zeros(num_features)

        feature_order = ['Alabama', 'Arizona', 'Arkansas',
       'California', 'Delaware', 'District of Columbia',
       'Florida', 'Georgia', 'Guam', 'Hawaii',
       'Illinois', 'Indiana', 'Kentucky',
       'Louisiana', 'Maryland', 'Massachusetts',
       'Michigan', 'Minnesota', 'Missouri',
       'Nebraska', 'New York City', 'North Carolina',
       'North Dakota', 'Ohio', 'Oregon',
       'Pennsylvania', 'Puerto Rico', 'Rhode Island',
       'U.S. Virgin Islands', 'Utah', 'Vermont',
       'Virginia', 'Wisconsin','Year']
        region_index = feature_order.index(uregion_display[uregion])
        feature_vector[region_index] = selected_regionu_encoded
        
        # Set the year in the correct position
        year_index = feature_order.index('Year')
        feature_vector[year_index] = int(yearsu)  

        # Perform the prediction
        prediction = us_cases.predict([feature_vector])
        rounded_prediction = round(prediction[0])
        st.write(f"Prediction result for {uregion_display[uregion]} in {year_displaysu[yearsu]}: {rounded_prediction[0]}")

  
    #################################################################################################

    st.markdown("# Leptospirosis in Sri Lanka")
    col1, col2 = st.columns(2)

    with col1:
        region_display = ('Ampara', 'Anuradhapura', 'Badulla',
       'Batticaloa', 'Colombo', 'Galle', 'Gampaha',
       'Hambantota', 'Jaffna', 'Kalmunai',
       'Kalutara', 'Kandy', 'Kegalle',
       'Kilinochchi', 'Kurunegala', 'Mannar',
       'Matale', 'Matara', 'Monaragala',
       'Mullaitivu', 'Nuwara Eliya', 'Polonnaruwa',
       'Puttalam', 'Ratnapura', 'Trincomalee',
       'Vavuniya')  
        region_options = list(range(len(region_display)))
        region = st.selectbox("Region", region_options, format_func=lambda x: region_display[x], key="sl_region")

    with col2:
        year_displaysl = tuple(str(year) for year in range(2024, 2051))
        year_optionssl = list(range(len(year_displaysl)))
        yearsl = st.selectbox("Year", year_optionssl, format_func=lambda x: year_displaysl[x], key="sl_year")

    if st.button("Sri Lanka Cases Prediction", key="sl_button"):
        le = LabelEncoder()
        le.fit(region_display)  
        selected_region_encoded = le.transform([region_display[region]])[0]

        num_features = 27  
        feature_vector = np.zeros(num_features)

        feature_order = ['Ampara', 'Anuradhapura', 'Badulla',
       'Batticaloa', 'Colombo', 'Galle', 'Gampaha',
       'Hambantota', 'Jaffna', 'Kalmunai',
       'Kalutara', 'Kandy', 'Kegalle',
       'Kilinochchi', 'Kurunegala', 'Mannar',
       'Matale', 'Matara', 'Monaragala',
       'Mullaitivu', 'Nuwara Eliya', 'Polonnaruwa',
       'Puttalam', 'Ratnapura', 'Trincomalee',
       'Vavuniya','Year']
        region_index = feature_order.index(region_display[region])
        feature_vector[region_index] = selected_region_encoded
        
        # Set the year in the correct position
        year_index = feature_order.index('Year')
        feature_vector[year_index] = int(yearsl)  

        # Perform the prediction
        prediction = sl_cases.predict([feature_vector])
        rounded_prediction = round(prediction[0])
        st.write(f"Prediction result for {region_display[region]} in {year_displaysl[yearsl]}: {rounded_prediction[0]}")

run()
