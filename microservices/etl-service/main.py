import time
import schedule
import pandas as pd
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import os
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ETL-Service")

# --- Configuration ---
# Data Warehouse Connection
DW_URI = os.getenv("DW_URI", "postgresql://dw_user:dw_pass@data-warehouse:5432/data_warehouse")

# Source Connections
# Note: In production, we would read from Replicas. For stability here, we read from Primaries.
SHOP_DB_URI = os.getenv("SHOP_DB_URI", "postgresql://shopuser:shoppass@shop-postgres-primary:5432/shopdb")
USER_MONGO_URI = os.getenv("USER_MONGO_URI", "mongodb://user-mongodb-primary:27017/user_management")

def get_dw_engine():
    return create_engine(DW_URI)

def extract_shop_data():
    """Extract Items and Price History from Shop Postgres"""
    logger.info("Extracting Shop Data...")
    engine = create_engine(SHOP_DB_URI)
    
    try:
        with engine.connect() as conn:
            # Read items
            df_items = pd.read_sql("SELECT * FROM items", conn)
            # Read price history
            df_prices = pd.read_sql("SELECT * FROM price_history", conn)
            
        return df_items, df_prices
    except Exception as e:
        logger.error(f"Error extracting shop data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def extract_user_data():
    """Extract Users from MongoDB"""
    logger.info("Extracting User Data...")
    try:
        client = MongoClient(USER_MONGO_URI)
        db = client.get_database()
        users_collection = db.users
        
        # Fetch all users, exclude _id
        users = list(users_collection.find({}, {"_id": 0}))
        
        if not users:
            return pd.DataFrame()
            
        df_users = pd.DataFrame(users)
        return df_users
    except Exception as e:
        logger.error(f"Error extracting user data: {e}")
        return pd.DataFrame()

def run_etl_job():
    logger.info("--- Starting ETL Job ---")
    dw_engine = get_dw_engine()
    
    # 1. Extract
    df_items, df_prices = extract_shop_data()
    df_users = extract_user_data()
    
    # 2. Transform (Example: Denormalize or Clean)
    # Let's just add a 'last_updated' timestamp to everything
    now = pd.Timestamp.now()
    
    if not df_items.empty:
        df_items['dw_last_updated'] = now
    
    if not df_users.empty:
        df_users['dw_last_updated'] = now
        # Convert complex Mongo objects to string if necessary
        if 'address' in df_users.columns:
            df_users['address'] = df_users['address'].astype(str)

    # 3. Load to Data Warehouse
    try:
        if not df_items.empty:
            df_items.to_sql('dim_items', dw_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df_items)} items to DW.")
            
        if not df_prices.empty:
            df_prices.to_sql('fact_price_history', dw_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df_prices)} price records to DW.")

        if not df_users.empty:
            df_users.to_sql('dim_users', dw_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df_users)} users to DW.")
            
        logger.info("--- ETL Job Completed Successfully ---")
        
    except Exception as e:
        logger.error(f"Error loading data to DW: {e}")

# Schedule the job
# Run once immediately on startup
time.sleep(10) # Wait for DBs to boot
run_etl_job()

# Then run every 1 minute
schedule.every(1).minutes.do(run_etl_job)

if __name__ == "__main__":
    logger.info("ETL Service Started")
    while True:
        schedule.run_pending()
        time.sleep(1)