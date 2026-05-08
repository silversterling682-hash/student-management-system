// ⚠️ THIS LINE MUST BE ABSOLUTELY FIRST — NO OTHER CODE ABOVE IT
require('dotenv').config();

// Now variables are loaded — we can import everything else
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');

// Connect to database AFTER env is loaded
connectDB();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', require('./routes/authRoutes'));

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});