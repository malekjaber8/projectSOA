const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

app.get('/generate-test-token', (req, res) => {
  const jwt = require('jsonwebtoken');
  
  const testToken = jwt.sign(
    { 
      userId: 'test-user-123', 
      email: 'admin@univ.fr', 
      role: 'Admin' 
    }, 
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
  
  res.json({
    token: testToken,
    usage: 'Utilisez ce token dans Postman: Authorization: Bearer ' + testToken
  });
});

// Routes principales
app.use('/students', require('./routes/studentRoutes'));

// Route de santé
app.get('/health', (req, res) => {
  res.json({ 
    status: 'Student Service is running!',
    timestamp: new Date().toISOString()
  });
});

// Connexion MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/studentDB')
  .then(() => console.log(' Connected to MongoDB'))
  .catch(err => console.log(' MongoDB connection error:', err));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(` Student Service running on port ${PORT}`);
});