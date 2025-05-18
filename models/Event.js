const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
  title: String,
  type: String,
  date: String,
  location: String,
  host: String,
  registeredUsers: [String]
});

module.exports = mongoose.model('Event', eventSchema);
