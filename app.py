import streamlit as st
from PIL import Image
import pandas as pd
from prophet import Prophet
from prophet.plot import plot, plot_components
from pymongo import MongoClient

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

    CONNECTION_STRING = "mongodb+srv://2020s17981:pKEesWvsHOvMU3gl@leptocluster.qzu48.mongodb.net/?retryWrites=true&w=majority&appName=leptocluster"
    client = MongoClient(CONNECTION_STRING)
    db = client['Leptospirosis_Data']
    collection = db['world']
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    df = df.drop(['_id', 'Deaths'], axis=1)
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df['Cases'] = df['Cases'].interpolate(method='linear')
    df['Cases'].fillna(method='ffill', inplace=True)  # Forward-fill
    df['Cases'].fillna(method='bfill', inplace=True)  # Backward-fill

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
        # Filter data based on user selection
        df_country = df[df['Country'] == country_display[country]]
        
        if df_country.empty:
            st.error(f"No data available for {country_display[country]}.")
        else:
            # Prepare data for Prophet
            data_prophet = df_country[['Year', 'Cases']].dropna()
            data_prophet.columns = ['ds', 'y']

            if len(data_prophet) < 2:
                st.error("Not enough data to perform forecasting. Please select a different country or adjust the year.")
            else:
                # Initialize and fit the Prophet model
                model = Prophet()
                model.fit(data_prophet)

                # Create a future DataFrame for yearly forecasting
                future = model.make_future_dataframe(periods=26, freq='Y')

                # Forecast
                forecast = model.predict(future)

                # Filter forecast for the selected year
                selected_year_forecast = forecast[forecast['ds'].dt.year == int(year_display[year])]
                
                # Show the selected forecast
                forecast_value = round(selected_year_forecast['yhat'].values[0])
                st.write(f"Prediction result for {country_display[country]} in {year_display[year]}: {forecast_value}")


#########################################################################

  

    # When the button is clicked
    if st.button("Global Death Prediction", key="globald_button"):
        CONNECTION_STRING = "mongodb+srv://2020s17981:pKEesWvsHOvMU3gl@leptocluster.qzu48.mongodb.net/?retryWrites=true&w=majority&appName=leptocluster"
        client = MongoClient(CONNECTION_STRING)
        db = client['Leptospirosis_Data']
        collection = db['world']
        documents = list(collection.find())
        df = pd.DataFrame(documents)
        df = df.drop(['_id', 'Cases'], axis=1)
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df['Deaths'] = df['Deaths'].interpolate(method='linear')
        df['Deaths'].fillna(method='ffill', inplace=True)  # Forward-fill
        df['Deaths'].fillna(method='bfill', inplace=True)  # Backward-fill
        # Filter data based on user selection
        df_country = df[df['Country'] == country_display[country]]
        
        if df_country.empty:
            st.error(f"No data available for {country_display[country]}.")
        else:
            # Prepare data for Prophet
            data_prophet = df_country[['Year', 'Deaths']].dropna()
            data_prophet.columns = ['ds', 'y']

            if len(data_prophet) < 2:
                st.error("Not enough data to perform forecasting. Please select a different country or adjust the year.")
            else:
                # Initialize and fit the Prophet model
                model = Prophet()
                model.fit(data_prophet)

                # Create a future DataFrame for yearly forecasting
                future = model.make_future_dataframe(periods=26, freq='Y')

                # Forecast
                forecast = model.predict(future)

                # Filter forecast for the selected year
                selected_year_forecast = forecast[forecast['ds'].dt.year == int(year_display[year])]
                
                # Show the selected forecast
                forecast_value = round(selected_year_forecast['yhat'].values[0])
                st.write(f"Death prediction result for {country_display[country]} in {year_display[year]}: {forecast_value}")

###########################################################################

    st.markdown("# Leptospirosis in the USA")
    col1, col2 = st.columns(2)

    CONNECTION_STRING = "mongodb+srv://2020s17981:pKEesWvsHOvMU3gl@leptocluster.qzu48.mongodb.net/?retryWrites=true&w=majority&appName=leptocluster"
    client = MongoClient(CONNECTION_STRING)
    db = client['Leptospirosis_Data']
    collection = db['usa']
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    df = df.drop(['_id'], axis=1)
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df['Cases'] = df['Cases'].interpolate(method='linear')
    df['Cases'].fillna(method='ffill', inplace=True)  # Forward-fill
    df['Cases'].fillna(method='bfill', inplace=True)  # Backward-fill

    with col1:
        country_display = ('Alabama', 'Arizona', 'Arkansas',
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
        country_options = list(range(len(country_display)))
        country = st.selectbox("Region", country_options, format_func=lambda x: country_display[x], key="us_region")

    with col2:
        year_display = tuple(str(year) for year in range(2024, 2051))
        year_options = list(range(len(year_display)))
        year = st.selectbox("Year", year_options, format_func=lambda x: year_display[x], key="us_year")

    # When the button is clicked
    if st.button("USA Cases Prediction", key="us_button"):
        # Filter data based on user selection
        df_country = df[df['Region'] == country_display[country]]
        
        if df_country.empty:
            st.error(f"No data available for {country_display[country]}.")
        else:
            # Prepare data for Prophet
            data_prophet = df_country[['Year', 'Cases']].dropna()
            data_prophet.columns = ['ds', 'y']

            if len(data_prophet) < 2:
                st.error("Not enough data to perform forecasting. Please select a different country or adjust the year.")
            else:
                # Initialize and fit the Prophet model
                model = Prophet()
                model.fit(data_prophet)

                # Create a future DataFrame for yearly forecasting
                future = model.make_future_dataframe(periods=26, freq='Y')

                # Forecast
                forecast = model.predict(future)

                # Filter forecast for the selected year
                selected_year_forecast = forecast[forecast['ds'].dt.year == int(year_display[year])]
                
                # Show the selected forecast
                forecast_value = round(selected_year_forecast['yhat'].values[0])
                st.write(f"Prediction result for {country_display[country]} in {year_display[year]}: {forecast_value}")


#########################################################################

    st.markdown("# Leptospirosis in Sri Lanka")
    col1, col2 = st.columns(2)

    CONNECTION_STRING = "mongodb+srv://2020s17981:pKEesWvsHOvMU3gl@leptocluster.qzu48.mongodb.net/?retryWrites=true&w=majority&appName=leptocluster"
    client = MongoClient(CONNECTION_STRING)
    db = client['Leptospirosis_Data']
    collection = db['sri_lanka']
    documents = list(collection.find())
    df = pd.DataFrame(documents)
    df = df.drop(['_id'], axis=1)
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df['Cases'] = df['Cases'].interpolate(method='linear')
    df['Cases'].fillna(method='ffill', inplace=True)  # Forward-fill
    df['Cases'].fillna(method='bfill', inplace=True)  # Backward-fill

    with col1:
        country_display = ('Ampara', 'Anuradhapura', 'Badulla',
       'Batticaloa', 'Colombo', 'Galle', 'Gampaha',
       'Hambantota', 'Jaffna', 'Kalmunai',
       'Kalutara', 'Kandy', 'Kegalle',
       'Kilinochchi', 'Kurunegala', 'Mannar',
       'Matale', 'Matara', 'Monaragala',
       'Mullaitivu', 'Nuwara Eliya', 'Polonnaruwa',
       'Puttalam', 'Ratnapura', 'Trincomalee',
       'Vavuniya')  
        country_options = list(range(len(country_display)))
        country = st.selectbox("Region", country_options, format_func=lambda x: country_display[x], key="sl_region")

    with col2:
        year_display = tuple(str(year) for year in range(2024, 2051))
        year_options = list(range(len(year_display)))
        year = st.selectbox("Year", year_options, format_func=lambda x: year_display[x], key="sl_year")

    # When the button is clicked
    if st.button("Sri Lanka Cases Prediction", key="sl_button"):
        # Filter data based on user selection
        df_country = df[df['Region'] == country_display[country]]
        
        if df_country.empty:
            st.error(f"No data available for {country_display[country]}.")
        else:
            # Prepare data for Prophet
            data_prophet = df_country[['Year', 'Cases']].dropna()
            data_prophet.columns = ['ds', 'y']

            if len(data_prophet) < 2:
                st.error("Not enough data to perform forecasting. Please select a different country or adjust the year.")
            else:
                # Initialize and fit the Prophet model
                model = Prophet()
                model.fit(data_prophet)

                # Create a future DataFrame for yearly forecasting
                future = model.make_future_dataframe(periods=26, freq='Y')

                # Forecast
                forecast = model.predict(future)

                # Filter forecast for the selected year
                selected_year_forecast = forecast[forecast['ds'].dt.year == int(year_display[year])]
                
                # Show the selected forecast
                forecast_value = round(selected_year_forecast['yhat'].values[0])
                st.write(f"Prediction result for {country_display[country]} in {year_display[year]}: {forecast_value}")




  
run()
