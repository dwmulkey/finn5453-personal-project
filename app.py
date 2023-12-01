# %%
from flask import Flask, render_template, request
import portfolio_analyzer  # Ensure this import is correctly set up

app = Flask(__name__, template_folder='templates')

def calculate_investor_profile(investment_horizon, risk_profile, liquidity_needs, income_level, market_confidence):
    score_map = {"low": 1, "medium": 2, "high": 3}
    
    total_score = (score_map.get(investment_horizon, 1) + 
                   score_map.get(risk_profile, 1) +
                   score_map.get(liquidity_needs, 1) + 
                   score_map.get(income_level, 1) +
                   score_map.get(market_confidence, 1))

    if 5 <= total_score <= 8:
        return "conservative"
    elif 9 <= total_score <= 11:
        return "moderate"
    else:
        return "aggressive"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        investment_horizon = request.form.get('investment_horizon')
        risk_profile = request.form.get('risk_profile')
        liquidity_needs = request.form.get('liquidity_needs')
        income_level = request.form.get('income_level')
        market_confidence = request.form.get('market_confidence')

        profile_type = calculate_investor_profile(investment_horizon, risk_profile, liquidity_needs, income_level, market_confidence)
        results = portfolio_analyzer.calculate_portfolio_performance(profile_type)

        # Pass the profile type and the tickers to the template
        return render_template('results.html', profile_type=profile_type, results=results, 
                               growth=portfolio_analyzer.growth, 
                               middle=portfolio_analyzer.middle, 
                               stable=portfolio_analyzer.stable)

    return render_template('questionnaire.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

# %%
