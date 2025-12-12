// Initialize MongoDB Replica Set for User Management Service
print('🔧 Initializing User Management MongoDB Replica Set...');

// Wait a bit for MongoDB to be ready
sleep(5000);

try {
    // Check if already initialized
    var status = rs.status();
    print('Replica set already initialized');
} catch (e) {
    // Initialize replica set
    print('Initializing replica set...');
    rs.initiate({
        _id: "user-rs",
        members: [
            { _id: 0, host: "user-mongodb-primary:27017", priority: 2 },
            { _id: 1, host: "user-mongodb-secondary:27017", priority: 1 }
        ]
    });
    print('✅ Replica set initialized');
}

// Wait for primary election
sleep(10000);

print('✅ User Management MongoDB Replica Set ready!');