from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Load and tokenize the data
def tokenize_function(examples, tokenizer):
    return tokenizer(examples['cleaned_body'], padding="max_length", truncation=True)

# Prepare dataset for training and evaluation
def load_dataset(file_path, tokenizer):
    df = pd.read_csv(file_path)
    dataset = Dataset.from_pandas(df[['cleaned_body', 'label']])
    
    # Tokenize the dataset
    dataset = dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    # Split dataset into train and test sets
    train_test_split = dataset.train_test_split(test_size=0.2)
    return train_test_split['train'], train_test_split['test']

# Train the model
def train_model(train_dataset, val_dataset):
    # Load tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    # Training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        evaluation_strategy="epoch",
        logging_dir='./logs',
    )

    # Trainer instance
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained('./model')

    print("Training complete. Model saved to './model'.")

if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    file_path = 'cleaned_comments.csv'

    # Load and tokenize dataset
    train_dataset, val_dataset = load_dataset(file_path, tokenizer)

    # Train the model
    train_model(train_dataset, val_dataset)

