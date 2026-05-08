const express = require('express');
const { register, login, getMe } = require('../controllers/authController');
const { protect, authorize } = require('../middleware/authMiddleware');
const router = express.Router();

// Public routes
router.post('/register', register);
router.post('/login', login);

// Protected routes
router.get('/me', protect, getMe);
// Example: Only admins can access this
router.get('/admin-data', protect, authorize('admin'), (req, res) => {
  res.json({ message: 'Welcome Admin! Here is sensitive data.' });
});

module.exports = router;