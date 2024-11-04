from flask import Flask, request, jsonify
from dataclasses import dataclass
from typing import Optional, List
import datetime

app = Flask(__name__)


@dataclass
class Item:
    id: int
    name: str
    description: Optional[str]
    price: float

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }


items = []


@app.route('/')
def root():
    return jsonify({"message": "Welcome to the Simple API Server"})


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify([item.to_dict() for item in items])


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in items:
        if item.id == item_id:
            return jsonify(item.to_dict())
    return jsonify({"error": "Item not found"}), 404


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    if not all(key in data for key in ['name', 'price']):
        return jsonify({"error": "Missing required fields"}), 400

    new_item = Item(
        id=len(items) + 1,
        name=data['name'],
        description=data.get('description'),
        price=float(data['price'])
    )
    items.append(new_item)
    return jsonify(new_item.to_dict()), 201


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for index, item in enumerate(items):
        if item.id == item_id:
            deleted_item = items.pop(index)
            return jsonify(deleted_item.to_dict())
    return jsonify({"error": "Item not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)