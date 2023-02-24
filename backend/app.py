from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from model import summarize
import nltk

app = Flask(__name__)
CORS(app)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

@app.route('/summarize', methods=['POST'])
def get_text_summary():
    summary = summarize(request.json)
    return jsonify({
        'message': 'success',
        'data': summary}), 200
  
if __name__ == '__main__':
    PORT = 3000
    app.run(debug=True, port=PORT)