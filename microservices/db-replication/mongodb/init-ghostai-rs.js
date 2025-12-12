// Initialize MongoDB Replica Set for Ghost AI Service
print('🔧 Initializing Ghost AI MongoDB Replica Set...');

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
        _id: "ghostai-rs",
        members: [
            { _id: 0, host: "ghost-ai-mongodb-primary:27017", priority: 2 },
            { _id: 1, host: "ghost-ai-mongodb-secondary:27017", priority: 1 }
        ]
    });
    print('✅ Replica set initialized');
}

// Wait for primary election
sleep(10000);

print('✅ Ghost AI MongoDB Replica Set ready!');