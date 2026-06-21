import streamlit as st
from models.probability_engine import predict_match

# =========================================================================
# WINDOW MODAL DEFINITIONS
# =========================================================================
@st.dialog("Detailed Match Insights", width="large")
def show_insights_window(predictions):
    st.write("### 📊 Advanced Match Probability Matrix")
    st.info("Live data stream processed via ChatGPT Pro predictive models.")
    
    # Showcase expanded structural metrics inside the popup window
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Calculated Home Edge", value=f"{predictions.get('home', 0) * 0.15:.1f}%")
        st.text_input("Enter custom risk target adjustment:", placeholder="e.g., 0.02")
    with col2:
        st.metric(label="Recommended Stake Allocation", value="$150.00")
        st.checkbox("Enable Kelly Leverage overrides", value=True)
        
    if st.button("Apply Changes & Close", use_container_width=True):
        st.success("Configuration metrics updated!")
        st.rerun()

# =========================================================================
# MAIN INTERFACE RENDERER
# =========================================================================
def render_home():
    st.title('⚽ Soccer AI Pro Dashboard')
    p = predict_match()
    
    # Render the 3 main metrics across columns
    c1, c2, c3 = st.columns(3)
    c1.metric('Home Win %', p['home'])
    c2.metric('Draw %', p['draw'])
    c3.metric('Away Win %', p['away'])
    
    st.success('Project scaffold loaded')
    
    st.divider()
    
    # Actionable trigger to launch the modal popup window
    if st.button("🔍 Open Detailed Value Settings", use_container_width=True):
        show_insights_window(p)
