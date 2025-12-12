#!/bin/bash
// filepath: microservices/db-replication/postgres/failover.sh
set -e

# PgPool-II failover script
# Arguments: %d = backend id, %h = backend hostname, %p = backend port,
# %D = database name, %m = new master node id, %H = new master hostname,
# %M = old master node id, %P = old master port, %r = new master port,
# %R = new master database name, %N = old primary node id, %S = new primary node id

BACKEND_ID=$1
BACKEND_HOST=$2
BACKEND_PORT=$3
DATABASE_NAME=$4
NEW_MASTER_ID=$5
NEW_MASTER_HOST=$6
OLD_MASTER_ID=$7
OLD_MASTER_PORT=$8
NEW_MASTER_PORT=$9
NEW_MASTER_DB=${10}
OLD_PRIMARY_ID=${11}
NEW_PRIMARY_ID=${12}

echo "Failover triggered: Backend $BACKEND_ID ($BACKEND_HOST:$BACKEND_PORT) failed"
echo "New master: $NEW_MASTER_ID ($NEW_MASTER_HOST:$NEW_MASTER_PORT)"

# Log the failover event
logger -t pgpool "Failover: $BACKEND_ID $BACKEND_HOST:$BACKEND_PORT failed, new master is $NEW_MASTER_ID $NEW_MASTER_HOST:$NEW_MASTER_PORT"

# If this is a primary failure, PgPool will automatically promote the replica
# No additional action needed as PgPool handles the promotion