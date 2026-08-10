// FoodExpress Restaurant Model
// MongoDB collection helper for restaurants

class Restaurant {
  constructor(db) {
    this.collection = db.collection('restaurants');
  }

  async findAll() {
    return this.collection.find({}).toArray();
  }

  async findById(id) {
    return this.collection.findOne({ id: id });
  }

  async findByCuisine(cuisine) {
    return this.collection.find({ cuisine: cuisine }).toArray();
  }

  async create(restaurantData) {
    const result = await this.collection.insertOne(restaurantData);
    return result;
  }

  async update(id, updateData) {
    const result = await this.collection.updateOne(
      { id: id },
      { $set: updateData }
    );
    return result;
  }

  async search(query) {
    return this.collection.find({
      name: { $regex: query, $options: 'i' }
    }).toArray();
  }

  async delete(id) {
    return this.collection.deleteOne({ id: id });
  }
}

module.exports = Restaurant;
