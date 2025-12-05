from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pickle
import os

app = Flask(__name__)

class EmailClassifier:
    def __init__(self, model_path):
        # Load GBERT tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        
        # Load category mappings
        with open('category_mappings_gbert.pkl', 'rb') as f:
            mappings = pickle.load(f)
            self.id_to_category = mappings['id_to_category']
        
        print(" GERT Email classifier loaded successfully!")
        print(f" Model expects {self.model.config.num_labels} categories")
        print(f" Mappings have {len(self.id_to_category)} categories")
        print(f" Model device: {self.device}")

    def weighted_combine(self, subject, email):
        """EXACT same preprocessing as during training - subject emphasized"""
        return f"{subject} {subject} {email}"

    def predict(self, subject, email):
        """Predict email category using GBERT"""
        try:
            print(f" Starting prediction...")
            print(f"   Subject: '{subject}'")
            print(f"   Email length: {len(email)}")
            
            # Use the EXACT same preprocessing as training
            combined_text = self.weighted_combine(subject, email)
            print(f" Processed text length: {len(combined_text)}")
            
            # Use the EXACT same tokenization as training
            inputs = self.tokenizer(
                combined_text,
                padding=True,
                truncation=True,
                max_length=768,  # Same as training
                return_tensors="pt"
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            print(f" Tokenized input shape: {inputs['input_ids'].shape}")
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                print(f" Raw predictions shape: {predictions.shape}")
                
                predicted_class_id = predictions.argmax().item()
                confidence = predictions.max().item()
                
                print(f" Predicted class ID: {predicted_class_id}")
                print(f" Confidence: {confidence}")
            
            # DEBUG: Check if the predicted_class_id exists in mappings
            print(f" Available category IDs: {list(self.id_to_category.keys())}")
            if predicted_class_id not in self.id_to_category:
                raise ValueError(f"Predicted ID {predicted_class_id} not in available IDs {list(self.id_to_category.keys())}")
            
            predicted_category = self.id_to_category[predicted_class_id]
            print(f" Predicted category: {predicted_category}")
            
            # Get top 3 predictions
            top3_confidences, top3_indices = torch.topk(predictions, 3)
            print(f" Top 3 indices: {top3_indices.tolist()}")
            
            top3_predictions = []
            for conf, idx in zip(top3_confidences[0], top3_indices[0]):
                idx_item = idx.item()
                if idx_item not in self.id_to_category:
                    raise ValueError(f"Top prediction ID {idx_item} not in available IDs")
                top3_predictions.append({
                    'category': self.id_to_category[idx_item],
                    'confidence': round(conf.item(), 3)
                })
            
            result = {
                'success': True,
                'prediction': predicted_category,
                'confidence': round(confidence, 3),
                'top3_predictions': top3_predictions,
                'processed_text': combined_text[:200] + "..." if len(combined_text) > 200 else combined_text,
                'model': 'GBERT-Large'
            }
            
            print(f" Prediction successful: {result['prediction']} ({result['confidence']*100:.1f}%)")
            return result
            
        except Exception as e:
            print(f" Error in predict: {str(e)}")
            print(f" Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

# Initialize classifier with GBERT model
classifier = EmailClassifier("./champion_gbert")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'model': 'GBERT-Large',
        'device': str(classifier.device),
        'categories_count': len(classifier.id_to_category)
    })

@app.route('/api/classify', methods=['POST'])
def classify_email():
    try:
        data = request.get_json()
        print(f" Received classification request")
        
        if not data or 'subject' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing subject or email content'
            }), 400
        
        subject = data['subject']
        email_content = data['email']
        
        print(f"   Subject: '{subject}'")
        print(f"   Email length: {len(email_content)}")
        
        if not subject.strip() and not email_content.strip():
            return jsonify({
                'success': False, 
                'error': 'Both subject and email content are empty'
            }), 400
        
        result = classifier.predict(subject, email_content)
        print(f" Sending response: {result.get('success', False)}")
        return jsonify(result)
            
    except Exception as e:
        print(f" Server error in classify_email: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/categories')
def get_categories():
    """Get list of all possible categories"""
    return jsonify({
        'categories': list(classifier.id_to_category.values()),
        'model': 'GBERT-Large'
    })

if __name__ == '__main__':
    print(" Starting GBERT-Large Email Classification Web Service...")
    print(" Model: ./champion_gbert")
    print(" Categories: category_mappings_gbert.pkl")
    print(" Access the application at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)