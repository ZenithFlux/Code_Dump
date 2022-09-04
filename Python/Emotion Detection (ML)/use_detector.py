import numpy as np

class EmotionDetector:
    def __init__(self, model, count_vectorizer):
        self.model = model
        self.cv = count_vectorizer
    
    def predict(self, x):
        data = self.cv.transform(x)
        output = self.model.predict(data)
        return self.convert_emotions(output)
    
    @staticmethod
    def convert_emotions(x):
        emotions = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
        try:
            x = np.vectorize(int)(x)
            return np.vectorize(lambda i: emotions[i])(x)
        except ValueError:
            return np.vectorize(lambda i: emotions.index(i))(x)
    
if __name__ == '__main__':
    import joblib as jl
    
    detector = jl.load('emotion_detector.model')
    while True:
        x = input('\nWrite something: ')
        if x == 'exit':
            break
        print("Emotion:-", detector.predict([x])[0])