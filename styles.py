import streamlit as st

def apply_custom_styles():
    """Injects custom CSS to style the Streamlit application with a light theme."""
    st.markdown(
        """
        <style>
        /* Import Google Fonts for modern typography */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        :root {
            --primary-color: #21618C; /* A professional deep blue */
            --secondary-color: #2ECC71; /* A complementing green */
            --background-color: #F8F9FA; /* Off-white for a softer look */
            --card-background: #FFFFFF; /* Pure white for cards/containers */
            --text-color: #212529; /* Dark gray for readability */
            --light-text-color: #6C757D;
            --border-color: #DEE2E6;
            --shadow-light: rgba(0, 0, 0, 0.1);
            --shadow-heavy: rgba(0, 0, 0, 0.2);
            --gradient-blue-green: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        }

        body {
            font-family: 'Roboto', sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
        }

        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }

        .stContainer, .stExpander, .stDataFrame {
            background-color: var(--card-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }

        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stMultiSelect>div>div {
            background-color: var(--card-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
        }
        
        .stMarkdown p {
            text-align: center;
        }

        /* --- Gradient Text for Headings --- */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            background: var(--gradient-blue-green);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        .title-style, .notes-heading-style {
            background: var(--gradient-blue-green);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        .title-style {
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }

        .notes-heading-style {
            font-size: 28px;
            margin-top: 30px;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 5px;
        }
        
        /* --- Unified Gradient Button Styles --- */
        .stButton>button {
            background: var(--gradient-blue-green);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px var(--shadow-light);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 10px var(--shadow-heavy);
        }

        /* Make secondary buttons also use a gradient */
        .st-emotion-cache-1jxtm22 > button {
            background: linear-gradient(225deg, var(--primary-color), var(--secondary-color));
        }
        
        .st-emotion-cache-1jxtm22 > button:hover {
            background: linear-gradient(225deg, var(--secondary-color), var(--primary-color));
        }

        .main-notes-area {
            background-color: var(--card-background);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            color: var(--text-color);
        }
        
        .st-emotion-cache-1v06a5k {
            background-color: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            box-shadow: 0 2px 4px var(--shadow-light);
        }

        .st-emotion-cache-1v06a5k h3 {
            color: var(--primary-color);
        }
        </style>
        """,
        unsafe_allow_html=True
    )