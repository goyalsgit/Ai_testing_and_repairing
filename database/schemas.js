const mongoose = require('mongoose');

// User Schema
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});

// Bug Report Schema
const bugReportSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  filename: { type: String, required: true },
  code: { type: String, required: true },
  bugs: [{
    type: { type: String, required: true },
    location: { type: String },
    description: { type: String, required: true },
    severity: { type: String, enum: ['low', 'medium', 'high'], default: 'medium' }
  }],
  repairSuggestions: [{
    bugId: { type: mongoose.Schema.Types.ObjectId },
    suggestion: { type: String, required: true },
    confidence: { type: Number, min: 0, max: 1 }
  }],
  status: { type: String, enum: ['pending', 'completed', 'failed'], default: 'pending' },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);
const BugReport = mongoose.model('BugReport', bugReportSchema);

module.exports = { User, BugReport };
