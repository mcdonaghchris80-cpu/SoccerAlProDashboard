import streamlit as st

def show_insights_window(match_data):
    """Placeholder for the modal popup window."""
    st.write("Displaying advanced analytics for:", match_data['fixture'])

def render_home():
    st.title('⚽ Soccer AI Pro Dashboard')
    
    # Mock data dictionary now includes true bookmaker decimal odds for Kelly calculation
    matches = {
        "Manchester City vs Real Madrid": {"home_pct": 52, "draw_pct": 25, "away_pct": 23, "home_odds": 2.10},
        "Inter Milan vs AC Milan": {"home_pct": 45, "draw_pct": 32, "away_pct": 23, "home_odds": 2.40},
        "Bayern Munich vs PSG": {"home_pct": 58, "draw_pct": 24, "away_pct": 18, "home_odds": 1.85},
        "Barcelona vs Arsenal": {"home_pct": 41, "draw_pct": 28, "away_pct": 31, "home_odds": 2.60}
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

    # --- KELLY STAKING ENGINE CALCULATIONS ---
    # Convert home team percentage win to a 0-1 probability
    home_prob = p['home_pct'] / 100.0
    bookie_odds = p['home_odds']
    
    # Implied probability from the bookmaker odds
    implied_prob = 1 / bookie_odds
    
    # Calculate model edge (Value)
    home_edge = (home_prob - implied_prob) * 100
    
    # Kelly Criterion Formula calculation
    b = bookie_odds - 1
    q = 1 - home_prob
    kelly_percentage = ((b * home_prob) - q) / b
    
    # Cap Kelly percentage to positive values or apply fractional Kelly (e.g., Half-Kelly)
    # This prevents the system from suggesting negative bets when there is no edge
    fractional_kelly = 0.5  
    if kelly_percentage > 0:
        recommended_stake_pct = kelly_percentage * fractional_kelly * 100
    else:
        recommended_stake_pct = 0.0

    # Displaying the Kelly Staking Engine metrics inside col1 and col2 matching your top layout
    st.subheader("📊 Kelly Staking Engine Allocation")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Model Value Edge (%)", value=f"{home_edge:.2f}%")
        st.caption(f"Bookmaker Home Odds: {bookie_odds}")
        
    with col2:
        # Generates recommended dollar stake based on a starting baseline of $1,000 max risk
        allocated_capital = 1000 * (recommended_stake_pct / 100)
        final_stake = max(25.00, allocated_capital) if home_edge > 0 else 0.00
        
        st.metric(label="Recommended Stake Allocation", value=f"${final_stake:.2f}")
        st.checkbox("Enable Kelly Leverage Overrides", value=True)
        
    if st.button("Apply Changes & Close", use_container_width=True):
        st.success("Configuration metrics updated!")
        st.rerun()

    st.divider()
    
    # Actionable trigger to launch the modal popup window with the chosen match data
    if st.button("👁️ Open Detailed Value Settings", use_container_width=True):
        show_insights_window(p)
