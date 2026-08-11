const mongoose = require('mongoose');

// Event schema for QuickTicket
const eventSchema = new mongoose.Schema({
  name: {
    type: String,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  category: {
    type: String,
    enum: ['concert', 'sports', 'theatre', 'conference', 'festival'],
    required: true
  },
  date: {
    type: Date,
    required: true
  },
  venue: {
    type: String,
    required: true,
    trim: true
  },
  price: {
    type: Number,
    required: true
  },
  capacity: {
    type: Number,
    required: true,
    min: 1
  },
  availableSeats: {
    type: Number,
    required: true
  }
}, { timestamps: true });

// Static method to find events by category
eventSchema.statics.findByCategory = async function (category) {
  return this.find({});
};

const Event = mongoose.model('Event', eventSchema);

module.exports = Event;
