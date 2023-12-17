from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


app = Flask(__name__)
api = Api(app)


# Задайте путь к директории, где сохранены модель и токенизатор
model_output_dir = "./model_save"

# Загрузка модели и токенизатора из сохраненной директории
model = GPT2LMHeadModel.from_pretrained(model_output_dir)
tokenizer = GPT2Tokenizer.from_pretrained(model_output_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

class GenerateText(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        input_text = data['text']

        # Преобразование текста в формат, подходящий для модели
        encoding = tokenizer.encode_plus(input_text, return_tensors="pt", padding='max_length', truncation=True, max_length=512)
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)

        # Генерация текста
        model.eval()
        with torch.no_grad():
            outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=512)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({
            'input_text': input_text,
            'generated_text': generated_text
        })

api.add_resource(GenerateText, '/generate-text')

if __name__ == '__main__':
    app.run(debug=True)