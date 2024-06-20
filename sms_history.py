from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/sms/predict_spam', methods=['POST'])
def predict_spam_sms():
    text = request.form['text']
    processed_text = preprocess_text(text)
    prediction = best_model.predict([processed_text])[0]
    result = 'Spam' if prediction == 1 else 'Ham (Not Spam)'
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO sms_spam_predictions (text, result, created_at) VALUES (%s, %s, %s)"
    values = (text, result, current_time)
    cursor.execute(query, values)
    db.commit()
    
    return result

@app.route('/sms/history', methods=['GET'])
def get_sms_spam_history():
    query = "SELECT text, result, created_at FROM sms_spam_predictions ORDER BY created_at DESC"
    cursor.execute(query)
    predictions = cursor.fetchall()
    predictions_list = []
    for prediction in predictions:
        prediction_data = {
            'text': prediction[0],
            'result': prediction[1],
            'created_at': prediction[2].strftime("%Y-%m-%d %H:%M:%S")
        }
        predictions_list.append(prediction_data)
    return jsonify(predictions_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10002, debug=False)
