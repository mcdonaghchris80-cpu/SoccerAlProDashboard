import streamlit as st

# =========================================================================
# WINDOW MODAL DEFINITIONS
# =========================================================================
@st.dialog("Detailed Match Insights", width="large")
def show_insights_window(match_data):
    st.write(f"### 📊 Advanced Predictive Matrix: {match_data['fixture']}")
    st.info(f"Live data stream processed via ChatGPT Pro predictive models.")
    
    # Calculate custom edge based on mock probabilities
    home_edge = (match_data['home_pct'] - 45) * 0.25
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Calculated Home Edge", value=f"{home_edge:.1f}%")
        st.text_input("Enter custom risk target adjustment:", placeholder="e.g., 0.02")
    with col2:
        recommended_stake = 1000 * (home_edge / 100) if home_edge > 0 else 25.00
        st.metric(label="Recommended Stake Allocation", value=f"${max(25.00, recommended_stake):.2f}")
        st.checkbox("Enable Kelly Leverage overrides", value=True)
        
    if st.button("Apply Changes & Close", use_container_width=True):
        st.success("Configuration metrics updated!")
        st.rerun()

# =========================================================================
# MAIN INTERFACE RENDERER
# =========================================================================
def render_home():
    st.title('⚽ Soccer AI Pro Dashboard')
    
    # Mock data dictionary for upcoming fixtures
    matches = {
        "Manchester City vs Real Madrid": {"home_pct": 52, "draw_pct": 25, "away_pct": 23},
        "Inter Milan vs AC Milan": {"home_pct": 45, "draw_pct": 32, "away_pct": 23},
        "Bayern Munich vs PSG": {"home_pct": 58, "draw_pct": 24, "away_pct": 18},
        "Barcelona vs Arsenal": {"home_pct": 41, "draw_pct": 28, "away_pct": 31}
    }
    
    # Active dropdown selection box
    selected_fixture = st.selectbox("Select Upcoming Live Fixture Scanner:", list(matches.keys()))
    p = matches[selected_fixture]
    p['fixture'] = selected_fixture
    
    st.divider()
    
    # Render the dynamic main metrics across columns based on selection
    c1, c2, c3 = st.columns(3)
    c1.metric('Home Win %', f"{p['home_pct']}%")
    c2.metric('Draw %', f"{p['draw_pct']}%")
    c3.metric('Away Win %', f"{p['away_pct']}%")
    
    st.success(f'Live matrix sync active for: {selected_fixture}')
    
    st.divider()
    
    # Actionable trigger to launch the modal popup window with the chosen match data
    if st.button("🔍 Open Detailed Value Settings", use_container_width=True):
        show_insights_window(p)
