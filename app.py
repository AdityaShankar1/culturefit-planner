import streamlit as st
from utils import (
    extract_lifestyle_tag_and_weight,
    get_lifestyle_cost,
    compute_monthly_savings,
    get_best_season
)

# ----- Custom CSS -----
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #EAF8ED, #D7F0DA) !important;
}
h1, h2, .st-cb, .st-ce, p {
    color: #2E5134 !important;
}
div.result-block {
    background-color: #90EE90;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #D5CDBE;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----- Page Header -----
st.title("🌿 CultureFit Financial Planner")
st.caption("Design your dream lifestyle and get a realistic monthly savings goal")

# ----- Inputs -----
prompt = st.text_input("Describe your lifestyle in ONE word (e.g. luxury, temple, foodie, minimalist)", "")
col1, col2 = st.columns(2)
current_age = col1.number_input("Current Age", min_value=18, max_value=60, value=22)
retire_age = col2.number_input("Target Retirement Age", min_value=30, max_value=65, value=50)
city = st.text_input("Preferred Base City (optional, for climate check)", "Chennai")
api_key = st.text_input("OpenWeatherMap API Key", type="password")

# ----- Button -----
if st.button("Get My CultureFit Plan"):
    if not prompt:
        st.warning("Please enter a lifestyle keyword.")
        st.stop()

    tag, wt = extract_lifestyle_tag_and_weight(prompt)
    yearly_cost = get_lifestyle_cost(tag)
    monthly = compute_monthly_savings(yearly_cost, retire_age, current_age, wt)

    st.markdown('<div class="result-block">', unsafe_allow_html=True)
    st.markdown("### 📌 Lifestyle Interpretation")
    st.markdown(f"*Mapped Category:* {tag.replace('_',' ').title()}")
    st.markdown(f"*Estimated Yearly Lifestyle Cost:* ₹ *{yearly_cost:,.0f}*")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="result-block">', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    col3.metric("💰 Suggested Monthly Saving", f"₹ {monthly:,.0f}")
    if api_key:
        season = get_best_season(city, api_key)
        col4.metric("🌤️ Climate Suitability", season)
    else:
        col4.metric("🌤️ Climate Suitability", "Enter API Key")
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("Made with ❤️ using Streamlit")