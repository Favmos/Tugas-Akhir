# =[Modules dan Packages]========================

from flask import Flask, request, jsonify, render_template
import joblib
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

# =[Variabel Global]=============================

app = Flask(__name__, static_url_path='/static')
model = None
tfidf_vectorizer = None

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]

@app.route("/")
def beranda():
    return render_template('index.html')

# Routing for API phishing

@app.route("/api/deteksi", methods=['POST'])
def apiDeteksi():
    global model
    global tfidf_vectorizer
    
    if request.method == 'POST':
        # Get the input URL from the request
        text_input = request.json.get('data', '')

        # Transform the input URL using the TF-IDF vectorizer
        features = tfidf_vectorizer.transform([text_input])

        # Predict using the model
        hasil = model.predict(features)[0]
        
        # Ensure the result is a Python int
        hasil = int(hasil)


        if hasil == 0:
            hasil_prediksi = ("Terindikasi URL Bad. Note: Jangan mengklik atau mengunjungi link tersebut. "
                              "Sebaiknya Anda menghapus email atau pesan yang berisi link tersebut, atau mengabaikan link "
                              "tersebut jika terdapat di dalam pesan atau situs web lain.")
        elif hasil == 1:
            hasil_prediksi = ("URL Good (URL Aman). Note: Tetaplah waspada dan hati-hati ketika mengklik link "
                              "tersebut. Pastikan bahwa Anda hanya mengklik link dari sumber yang terpercaya, seperti situs web resmi "
                              "atau email yang Anda harapkan dari pengirim yang dikenal.")

        # Return the prediction result as JSON
        return jsonify({
            "data": hasil_prediksi,
        })

# =[Main]========================================

if __name__ == '__main__':
    # Load model phishing yang telah ditraining
    model = joblib.load('model_phishing_lr.joblib')

    # Load the TF-IDF vectorizer
    with open('tfidf_vectorizer.pkl', 'rb') as handle:
        tfidf_vectorizer = pickle.load(handle)

    # Run Flask di localhost
    app.run(host="localhost", port=5000, debug=True)
