import streamlit as st

sensitivity = 0.25
specificity = 0.83

header = st.container()
data = st.container()
result = st.container()

with header:
    st.title('Welcome to Winemaker Decision Model!')

with data:
    st.subheader("Let's insert some numbers here!")
    botrytis = st.number_input('Chance of botrytis:')
    no_sug = st.number_input('Chance of no sugar level:')
    typ_sug = st.number_input('Chance of typical sugar level:')
    high_sug = st.number_input('Chance of high sugar level:')

Trocken = 5
Kabinett = 10
Spatlese = 15
Auslese = 30
Beerenauslese = 40
Trockenbeerenauslese = 120

prob_storm = 0.5
prob_no_storm = 1 - prob_storm
prob_storm_mold = botrytis
prob_storm_no_mold = 1 - prob_storm_mold
prob_no_sug = no_sug
prob_typical_sug = typ_sug
prob_high_sug = high_sug

pay_harvest = 6000 * Trocken * 12 + 2000 * Kabinett * 12 + 2000 * Spatlese * 12

storm_no_mold = (5000 * Trocken * 12 + 1000 * Kabinett * 12) * prob_storm * prob_storm_no_mold
storm_mold = (5000 * Trocken * 12 + 1000 * Kabinett * 12 + 2000 * Trockenbeerenauslese * 12) * prob_storm * prob_storm_mold
no_storm_no_sugar = (6000 * Trocken * 12 + 2000 * Kabinett * 12 + 2000 * Spatlese * 12) * prob_no_storm * prob_no_sug	
no_storm_typical_sugar = (5000 * Trocken * 12 + 1000 * Kabinett * 12 + 2500 * Spatlese * 12 + 1500 * Auslese * 12) * prob_no_storm * prob_typical_sug
no_storm_high_sugar = (4000 * Trocken * 12 + 2500 * Kabinett * 12 + 2000 * Spatlese * 12 + 1000 * Auslese * 12 + 500 * Beerenauslese * 12) * prob_no_storm * prob_high_sug

pay_noharv_storm = storm_mold + storm_no_mold
pay_noharv_nostorm = no_storm_no_sugar + no_storm_typical_sugar + no_storm_high_sugar

def bayes(metric, prob):
    numerator = metric * prob
    denom = (metric * prob) + (1 - metric) * (1 - prob)
    return numerator / denom, denom

def value_of_data(prob_storm, sens, spec, pay_harvest, pay_noharv_storm, pay_noharv_nostorm):
    if spec < 0.5:
        spec = 1 - spec
    prob_no_storm = 1 - prob_storm
    true_neg, pred_neg = bayes(spec, prob_no_storm)
    pred_pos = 1 - pred_neg
    exp_value = (pred_neg * (pay_noharv_nostorm * true_neg + pay_noharv_storm * (1 - true_neg))) + (pred_pos * (pay_harvest)) 
    return exp_value - pay_harvest

with result:
    e_val = value_of_data(prob_storm, sensitivity, specificity, pay_harvest, pay_noharv_storm, pay_noharv_nostorm)
    st.subheader("Here's the result!")
    st.text(f"The e-value of the decision is ${e_val}")
    if e_val <= 0:
        st.text("This model provides littele help for you to make the decision.")
    else:
        st.text("You should use the model to make your decisions.")







