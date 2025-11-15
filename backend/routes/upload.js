const express = require('express');
const multer = require('multer');
const jwt = require('jsonwebtoken');
const { spawn } = require('child_process');
const { BugReport } = require('../database/schemas');

const router = express.Router();
const upload = multer({ dest: 'uploads/' });

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

// Upload code and run symbolic execution
router.post('/', verifyToken, upload.single('code'), async (req, res) => {
  try {
    const { path: filePath } = req.file;
    const userId = req.user.id;

    // Run symbolic execution pipeline (Python script)
    const pythonProcess = spawn('bash', ['-c', `source /home/dell/swe/venv/bin/activate && python3 /home/dell/swe/symbolic_execution/pipeline.py ${filePath}`], {
      cwd: '/home/dell/swe/backend'
    });
    let output = '';
    pythonProcess.stdout.on('data', (data) => { output += data.toString(); });
    pythonProcess.stderr.on('data', (data) => { output += data.toString(); });

    pythonProcess.on('close', async (code) => {
      try {
        const result = JSON.parse(output);
        const bugReport = new BugReport({
          userId,
          codeFile: req.file.originalname,
          bugs: result.bugs,
          repairs: result.repairs,
          executionTime: result.executionTime
        });
        await bugReport.save();
        res.json({ message: 'Analysis complete', reportId: bugReport._id });
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        console.error('Output was:', output);
        res.status(500).json({ error: 'Failed to parse analysis results', details: output });
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
