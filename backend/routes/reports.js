const express = require('express');
const jwt = require('jsonwebtoken');
const { BugReport } = require('../database/schemas');

const router = express.Router();

// Middleware to verify token
const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Access denied' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET || 'secret');
    next();
  } catch (error) {
    res.status(403).json({ error: 'Invalid token' });
  }
};

// Get user's bug reports
router.get('/', verifyToken, async (req, res) => {
  try {
    const reports = await BugReport.find({ userId: req.user.id });
    res.json(reports);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get specific report
router.get('/:id', verifyToken, async (req, res) => {
  try {
    const report = await BugReport.findOne({ _id: req.params.id, userId: req.user.id });
    if (!report) return res.status(404).json({ error: 'Report not found' });
    res.json(report);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
