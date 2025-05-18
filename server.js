const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const path = require('path');
const Event = require('./models/Event');

const app = express();

// === Middleware ===
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// === Session ===
app.use(session({
  secret: 'your_secret_key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    sameSite: 'lax'
  }
}));

// === MongoDB Connection ===
mongoose.connect('mongodb://127.0.0.1:27017/hoodhub', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log('✅ MongoDB Connected'))
  .catch(err => console.error('MongoDB error:', err));

// === Login Route ===
app.post('/login', (req, res) => {
  const { username } = req.body;
  if (!username) return res.status(400).send("Username required");

  req.session.userId = username;
  res.redirect('/dashboard.html');
});

// === API: Logged-in User Info ===
app.get('/api/me', (req, res) => {
  if (!req.session.userId) return res.status(401).json({ error: 'Not logged in' });
  res.json({ username: req.session.userId });
});

// === Get All Events ===
app.get('/api/events', async (req, res) => {
  const userId = req.session.userId;
  if (!userId) return res.status(401).send('Unauthorized');

  const allEvents = await Event.find({});
  const registered = allEvents.filter(e => e.registeredUsers.includes(userId));
  const explore = allEvents.filter(e => !e.registeredUsers.includes(userId));

  res.json({ registered, explore });
});

// === Register for Event ===
app.post('/api/register/:id', async (req, res) => {
  const userId = req.session.userId;
  if (!userId) return res.status(401).send('Unauthorized');

  await Event.findByIdAndUpdate(req.params.id, {
    $addToSet: { registeredUsers: userId }
  });

  res.sendStatus(200);
});

// === Host New Event ===
app.post('/api/host', async (req, res) => {
  const userId = req.session.userId;
  if (!userId) return res.status(401).send('Unauthorized');

  const { title, type, date, location } = req.body;
  await Event.create({
    title,
    type,
    date,
    location,
    host: userId,
    registeredUsers: []
  });

  res.sendStatus(201);
});

// === Start Server ===
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
