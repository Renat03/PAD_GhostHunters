// MongoDB Replica Set Initialization Script

// Wait for MongoDB to be ready
sleep(5000);

// Initialize replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb-primary:27017", priority: 2 },
    { _id: 1, host: "mongodb-secondary:27017", priority: 1 }
  ]
});

// Wait for replica set to stabilize
sleep(10000);

// Print status
printjson(rs.status());