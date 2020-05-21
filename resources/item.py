from flask_restful import Resource, reqparse
from models.item import ItemModel


#api resources

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help= 'This field cannot be empty!')
    parser.add_argument('store_id',
            type=int,
            required=True,
            help= 'Every item needs store id!')
# http://127.0.0.1:5000/item/peru
# {"price": 12.0, "name": "peru"}
    # def get(self, name):
    #     for item in items:
    #         if item['name'] ==  name:
    #             return item
    #     return {'item': None}, 404

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

        # item = next(filter(lambda item : item['name'] == name, items), None)
        # return {'item' : item}, 200 if item else 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

       # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json()


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        

    def put(self, name):
        data = Item.parser.parse_args()
        # request_data = request.get_json()
        item = ItemModel.find_by_name(name)
      
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemsList(Resource):
# http://127.0.0.1:5000/items
    def get(self):
        return {"items" : [item.json() for item in ItemModel.query.all()]}

