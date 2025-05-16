from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset to extract dropdown options
df = pd.read_csv('sales_data.csv')

dropdown_columns = ['Source', 'Sales_Agent', 'Location', 'Delivery_Mode', 'Status']
dropdown_options = {col: sorted(df[col].dropna().unique()) for col in dropdown_columns}

def dummy_predict(data):
    lead_score = float(data.get('Lead_Score', 0))
    status = data.get('Status', '').strip().lower()

    lead_score = max(0, min(lead_score, 100))

    if status == 'open' and lead_score >= 70:
        prediction = "High Potential"
        confidence = round(70 + (lead_score - 70) * 0.9, 2)  
    elif status == 'open' and lead_score >= 50:
        prediction = "Medium Potential"
        confidence = round(60 + (lead_score - 50) * 0.7, 2)  
    else:
        prediction = "Low Potential"
        confidence = round(50 - (50 - lead_score) * 0.6, 2) 

    return prediction, confidence


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    if request.method == 'POST':
        form_data = request.form.to_dict()
        prediction, confidence = dummy_predict(form_data)

    return render_template('index.html',
                           dropdown_options=dropdown_options,
                           prediction=prediction,
                           confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)