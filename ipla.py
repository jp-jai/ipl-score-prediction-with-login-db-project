import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Page config
st.set_page_config(page_title="IPL Score Predictor", page_icon="🏏", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0e1117;
        color: #f8f9fa;
    }

    .stApp {
        padding: 2rem;
    }

    .stButton > button {
        background: linear-gradient(to right, #fc4a1a, #f7b733);
        color: white;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        transition: 0.4s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #ffffff, #ffffff);
        color: #f76b1c;
        font-weight: 700;
        border: 2px solid #f76b1c;
    }

    .sidebar .sidebar-content {
        background-color: #1c1f26;
        padding: 1rem;
        border-radius: 10px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h2, h3, h4 {
        color: #ffa94d !important;
    }

    .metric-container {
        background: #1c1f26;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }

    .stExpanderHeader {
        font-weight: bold;
        color: #ffc078 !important;
    }

    hr {
        border-top: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="background: linear-gradient(90deg, #fc4a1a, #f7b733); padding: 15px; border-radius: 12px; margin-bottom: 20px;">
        <h2 style="color: white; text-align: center;">🏏 IPL Score Predictor</h2>
        <p style="color: white; text-align: center;">Predict the Final IPL Score with AI-driven analytics!</p>
    </div>
""", unsafe_allow_html=True)

# Username from URL
query_params = st.query_params
username = query_params["username"] if "username" in query_params else None
if username:
    st.subheader(f"👋🏼 Welcome, {username}!")

# Match Result Card
today = datetime.now()
match_info = {
    'teams': 'Gujarat Titans vs Rajasthan Royals',
    'venue': 'Narendra Modi Stadium',
    'toss': 'Rajasthan Royals won toss and chose to field',
    'score': 'GT 197/6 (20), RR 199/7 (19.5)',
    'result': 'Rajasthan Royals won by 3 wickets',
    'top_performers': 'Sanju Samson 68*(42), Rashid Khan 2/32'
}

st.subheader(f"📅 Today's Match Result ({today.strftime('%d %b %Y')})")
with st.expander(f"🏟️ {match_info['teams']}"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"📍 **Venue:** {match_info['venue']}")
        st.markdown(f"🎯 **Toss:** {match_info['toss']}")
        st.markdown(f"🧮 **Score:** {match_info['score']}")
    with col2:
        st.markdown(f"🏆 **Result:** {match_info['result']}")
        st.markdown(f"⭐ **Top Performers:** {match_info['top_performers']}")
st.markdown("---")

# Sidebar Inputs
with st.sidebar:
    st.header("⚙️ Match Inputs")
    batting_team = st.selectbox("Batting Team", [
        'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore',
        'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
        'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'
    ])

    bowling_team = st.selectbox("Bowling Team", [
        'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore',
        'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
        'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'
    ], index=1)

    venue = st.selectbox("Venue", [
        'Wankhede Stadium', 'Chepauk', 'Eden Gardens', 'Chinnaswamy Stadium',
        'Arun Jaitley Stadium', 'PCA Stadium', 'Sawai Mansingh Stadium',
        'Rajiv Gandhi Stadium', 'Narendra Modi Stadium', 'Ekana Stadium'
    ])

    overs = st.slider("Overs Completed", 5, 19, 10)
    runs = st.number_input("Runs Scored", min_value=0, max_value=300, value=80)
    wickets = st.slider("Wickets Fallen", 0, 9, 2)
    predict_button = st.button("🔮 Predict Score")

# Model Loader
@st.cache_resource
def load_model():
    try:
        model = joblib.load('ipl_score_predictor.joblib')
        if hasattr(model, 'predict'):
            return model
    except:
        pass

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), 
             ['batting_team', 'bowling_team', 'venue'])
        ],
        remainder='passthrough'
    )

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])

    df = create_dummy_data()
    X = df[['batting_team', 'bowling_team', 'venue', 'overs', 'runs', 'wickets', 'year']]
    y = df['final_score']
    model.fit(X, y)
    joblib.dump(model, 'ipl_score_predictor.joblib')
    return model

def create_dummy_data():
    np.random.seed(42)
    teams = ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 
             'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
             'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants']
    venues = ['Wankhede Stadium', 'Chepauk', 'Eden Gardens', 'Chinnaswamy Stadium',
              'Arun Jaitley Stadium', 'PCA Stadium', 'Sawai Mansingh Stadium',
              'Rajiv Gandhi Stadium', 'Narendra Modi Stadium', 'Ekana Stadium']
    
    data = {
        'batting_team': np.random.choice(teams, 100),
        'bowling_team': np.random.choice(teams, 100),
        'venue': np.random.choice(venues, 100),
        'overs': np.random.randint(5, 20, 100),
        'runs': np.random.randint(30, 180, 100),
        'wickets': np.random.randint(0, 9, 100),
        'year': np.random.choice([2022, 2023], 100)
    }

    df = pd.DataFrame(data)
    df['final_score'] = df['runs'] + (20 - df['overs']) * 8 + (9 - df['wickets']) * 3 + np.random.normal(0, 5, 100)
    df['final_score'] = df['final_score'].astype(int)
    df = df[df['batting_team'] != df['bowling_team']].reset_index(drop=True)
    return df

model = load_model()

# Prediction
if predict_button:
    if batting_team == bowling_team:
        st.error("⚠️ Batting and Bowling teams cannot be the same!")
    else:
        input_df = pd.DataFrame([{
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'venue': venue,
            'overs': overs,
            'runs': runs,
            'wickets': wickets,
            'year': datetime.now().year
        }])

        try:
            prediction = model.predict(input_df)
            predicted_score = int(prediction[0])
            
            st.subheader("📊 Prediction Result")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Score", f"{runs}/{wickets}")
                st.metric("Overs", overs)
            with col2:
                st.metric("Predicted Final Score", predicted_score)
                rrr = (predicted_score - runs) / (20 - overs)
                st.metric("Req. Run Rate", f"{rrr:.2f}")

            # Progress Chart
            st.subheader("📈 Match Progression")
            chart_df = pd.DataFrame({
                'Overs': range(1, 21),
                'Projected Runs': [int(runs * (i/overs)) if i <= overs else 
                                   int(runs + (predicted_score - runs) * ((i - overs)/(20 - overs))) 
                                   for i in range(1, 21)]
            })
            st.line_chart(chart_df.set_index("Overs"))

        except Exception as e:
            st.error(f"Prediction Error: {str(e)}")

# Expanders
with st.expander("🧠 How It Works"):
    st.markdown("""
    - Model: **Random Forest Regressor**
    - Trained on synthetic match data
    - Inputs: Runs, Wickets, Overs, Venue, Teams
    - Outputs: Estimated Final Score
    """)

with st.expander("💡 Usage Tips"):
    st.markdown("""
    - Best used after **10+ overs**
    - Avoid selecting **same team** for both options
    - Venue & team combinations help accuracy
    """)

# Footer
st.markdown("---")
st.caption("⚠️ Note: Predictions are based on synthetic data. Use real data for production-level accuracy.")
st.markdown("<p style='text-align: center;'>🚀 Created by Jai Prakash | BSc Digital Forensics</p>", unsafe_allow_html=True)
#python -m streamlit run ipla.py
#pip install streamlit pandas scikit-learn joblib numpy
#python -m streamlit run ipls\ipla.py
