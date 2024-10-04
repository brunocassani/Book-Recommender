from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the trained model
def load_model():
    tokenizer = BertTokenizer.from_pretrained('./model')
    model = BertForSequenceClassification.from_pretrained('./model')
    return tokenizer, model

# Make predictions on new data
def predict_book_titles(new_comments, tokenizer, model):
    inputs = tokenizer(new_comments, return_tensors="pt", padding=True, truncation=True)

    # Get model predictions
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)

    return predictions

if __name__ == "__main__":
    new_comments = [
        "Can anyone recommend '1984' by George Orwell?",
        "Looking for book suggestions."
    ]

    # Load model and tokenizer
    tokenizer, model = load_model()

    # Predict whether comments contain book titles
    predictions = predict_book_titles(new_comments, tokenizer, model)

    # Print predictions (0: no title, 1: contains title)
    for comment, prediction in zip(new_comments, predictions):
        print(f"Comment: '{comment}' => Prediction: {prediction.item()}")

