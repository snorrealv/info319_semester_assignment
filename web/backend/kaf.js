const WebSocket = require('ws');
const Kafka = require('kafka-node');

// Kafka setup
const client = new Kafka.KafkaClient({
  kafkaHost: 'localhost:9092'
});

const producer = new Kafka.Producer(client);

// WebSocket setup
const server = new WebSocket.Server({
  port: 8080
});

server.on('connection', (socket) => {
  // Subscribe to a Kafka topic
  const topic = 'tweets';
  const consumer = new Kafka.Consumer(client, [{ topic }], {
    autoCommit: true
  });

  consumer.on('message', (message) => {
    // Send the message to the connected WebSocket client
    socket.send(message.value);
  });

  // Listen for messages from the client
  socket.on('message', (message) => {
    // Publish the message to the Kafka topic
    producer.send([{ topic, messages: [message] }], (err, result) => {
      if (err) {
        console.error('Error:', err);
      } else {
        console.log('Message published to Kafka:', result);
      }
    });
  });
});