from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import librosa
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load your trained model
model = load_model('path_to_your_model.h5')

def extract_features(waveform):
    try:
        # Trimming silence
        waveform, _ = librosa.effects.trim(waveform)
        
        # Extracting features using VGGish
        return vggish(waveform).numpy()
    except:
        return None

def predict_genre(audio_data):
    # Convert base64 audio data to numpy array
    audio_binary = base64.b64decode(audio_data.split(",")[1])
    audio_np = np.frombuffer(audio_binary, dtype=np.int16)

    # Extract features
    features = extract_features(audio_np)

    if features is not None:
        # Pad features array
        features = pad_sequences([features], dtype='float32', padding='post', truncating='post', maxlen=43)
        
        # Make prediction
        prediction = model.predict(features)
        
        # Get the predicted class
        predicted_class = np.argmax(prediction)
        
        return predicted_class
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    audio_data = request.form['audio_data']
    predicted_class = predict_genre(audio_data)

    return jsonify({'predicted_class': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
