const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

// Konfigurasi CORS untuk mendukung semua origin
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type'],
}));

app.post('/chat', async (req, res) => {
  const { message } = req.body;

  try {
    const response = await axios.post('http://localhost:5005/webhooks/rest/webhook', {
      sender: 'user',
      message: message,
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send(error.toString());
  }
});

app.listen(3001, () => {
  console.log('Server running on http://localhost:3001');
});
