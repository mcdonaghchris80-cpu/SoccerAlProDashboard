import streamlit as st
import plotly.graph_objects as go

@st.dialog("📊 Advanced Fixture Insights & Value Edge")
def show_insights_window(match_data):
    """
    Renders an interactive breakdown modal comparing Model Probabilities 
    against implied bookmaker probabilities using Plotly.
    """
    st.write(f"### Analytics for: **{match_data['fixture']}**")
    
    # Extract data parameters safely
    home_pct = match_data['home_pct']
    draw_pct = match_data['draw_pct']
    away_pct = match_data['away_pct']
    bookie_odds = match_data['home_odds']
    
    # Calculate bookmaker's implied market probability for the Home Win
    implied_home_pct = round((1 / bookie_odds) * 100, 1)
    
    st.markdown("---")
    st.write("#### 📈 Probability Distribution Comparison")
    
    # Build a clean data visualization using Plotly chart objects
    categories = ['Home Win', 'Draw', 'Away Win']
    model_probabilities = [home_pct, draw_pct, away_pct]
    
    fig = go.Figure()
    
    # Trace 1: Our AI Engine Predictions
    fig.add_trace(go.Bar(
        x=categories,
        y=model_probabilities,
        name='SoccerAI Pro Model',
        marker_color='#10b981', # Green
        text=[f"{val}%" for val in model_probabilities],
        textposition='auto'
    ))
    
    # Trace 2: The Implied Bookmaker baseline marker line for Home Win
    fig.add_trace(go.Scatter(
        x=['Home Win'],
        y=[implied_home_pct],
        name=f'Bookie Implied ({implied_home_pct}%)',
        mode='markers',
        marker=dict(color='#ef4444', size=15, symbol='line-ew-open', line=dict(width=4)) # Red Line
    ))
    
    fig.update_layout(
        barmode='group',
        yaxis=dict(title='Probability Percentage (%)', range=[0, 100]),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Value Evaluation Assessment Box
    edge = home_pct - implied_home_pct
    st.write("#### 🧠 Market Valuation Strategy")
    if edge > 0:
        st.info(
            f"**Value Detected:** Your AI model estimates a **{home_pct}%** chance of a home victory, "
            f"while the bookmaker odds of {bookie_odds} imply only a **{implied_home_pct}%** chance. "
            f"This creates a mathematical value edge of **+{edge:.1f}%** supporting your Kelly stake."
        )
    else:
        st.warning(
            f"**No Market Value:** Your AI model estimates a **{home_pct}%** chance of a home victory, "
            f"which is lower than or equal to the bookmaker's implied market price (**{implied_home_pct}%**). "
            f"Avoid exposure on this match outcome."
        )

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

    # 5. Settings Configuration Panel
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
