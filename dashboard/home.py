import streamlit as st

def show_insights_window(match_data):
    """Placeholder for the modal popup window."""
    st.write("Displaying advanced analytics for:", match_data['fixture'])

def render_home():
    st.title('⚽ Soccer AI Pro Dashboard')
    
    # 1. Mock Data (Updated to include bookmaker decimal odds for Kelly calculation)
    matches = {
        "Manchester City vs Real Madrid": {"home_pct": 52, "draw_pct": 25, "away_pct": 23, "home_odds": 2.10},
        "Inter Milan vs AC Milan": {"home_pct": 45, "draw_pct": 32, "away_pct": 23, "home_odds": 2.40},
        "Bayern Munich vs PSG": {"home_pct": 58, "draw_pct": 24, "away_pct": 18, "home_odds": 1.85},
        "Barcelona vs Arsenal": {"home_pct": 41, "draw_pct": 28, "away_pct": 31, "home_odds": 2.60}
    }
    
    # 2. Match Selector Dropdown
    selected_fixture = st.selectbox("Select Upcoming Live Fixture Scanner:", list(matches.keys()))
    p = matches[selected_fixture]
    p['fixture'] = selected_fixture
    
    st.divider()
    
    # 3. Main Metrics Grid (Win, Draw, Away Percentages)
    c1, c2, c3 = st.columns(3)
    c1.metric('Home Win %', f"{p['home_pct']}%")
    c2.metric('Draw %', f"{p['draw_pct']}%")
    c3.metric('Away Win %', f"{p['away_pct']}%")
    
    st.success(f'Live matrix sync active for: {selected_fixture}')
    
    st.divider()

    # 4. Kelly Staking Engine Logic
    home_prob = p['home_pct'] / 100.0
    bookie_odds = p['home_odds']
    
    # Calculate edge percentage against the bookmaker odds
    implied_prob = 1 / bookie_odds
    home_edge = (home_prob - implied_prob) * 100
    
    # Core Kelly Formula: ((b * p) - q) / b
    b = bookie_odds - 1
    q = 1 - home_prob
    kelly_percentage = ((b * home_prob) - q) / b if b > 0 else 0
    
    # Safe Fractional Kelly sizing (0.50 = Half-Kelly) to smooth out bankroll swings
    fractional_kelly = 0.5
    if kelly_percentage > 0:
        recommended_stake_pct = kelly_percentage * fractional_kelly * 100
    else:
        recommended_stake_pct = 0.0

    # 5. Settings Configuration Panel (Col1 & Col2 layout matching lines 18-25 in your view)
    st.subheader("⚙️ Staking & Valuation Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Model Value Edge (%)", value=f"{home_edge:.2f}%")
        st.caption(f"Current Bookmaker Home Odds: {bookie_odds}")
        
    with col2:
        # Dynamically calculate currency exposure from standard $1000 portfolio base
        recommended_stake = 1000 * (recommended_stake_pct / 100) if home_edge > 0 else 0.0
        
        # Ensures a minimum stake limit threshold of $25.00 if a positive edge exists
        final_stake = max(25.00, recommended_stake) if home_edge > 0 else 0.00
        
        st.metric(label="Recommended Stake Allocation", value=f"${final_stake:.2f}")
        st.checkbox("Enable Kelly Leverage Overrides", value=True)
        
    if st.button("Apply Changes & Close", use_container_width=True):
        st.success("Configuration metrics updated!")
        st.rerun()

    st.divider()
    
    # 6. Detailed Analysis Modal Launcher
    if st.button("👁️ Open Detailed Value Settings", use_container_width=True):
        show_insights_window(p)
