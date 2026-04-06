#!/usr/bin/env python3
"""
Test script to verify the complete data pipeline
Run this to diagnose issues with Bronze->Silver->Gold->Dashboard flow
"""

import asyncio
import sys
import logging
from datetime import datetime, timedelta

sys.path.insert(0, 'path to your backend directory')  # Adjust this path as needed

from app.config import BUCKET_BRONZE, BUCKET_SILVER, BUCKET_GOLD, INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG
from app.db.influx_client import query_api, write_api, influx_client
from influxdb_client import Point

logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(levelname)s: %(message)s')
logger = logging.getLogger("Pipeline Test")

def test_influx_connection():
    """Test InfluxDB connection"""
    print("\n" + "="*60)
    print("1️⃣  TESTING INFLUXDB CONNECTION")
    print("="*60)
    try:
        # Test connection
        logger.info(f"Connecting to InfluxDB: {INFLUX_URL}")
        logger.info(f"Organization: {INFLUX_ORG}")
        
        # Get buckets
        result = influx_client.buckets_api().find_buckets()
        bucket_names = [b.name for b in result.buckets]
        logger.info(f"Available buckets: {bucket_names}")
        
        # Check our buckets exist
        for bucket_name in [BUCKET_BRONZE, BUCKET_SILVER, BUCKET_GOLD]:
            if bucket_name in bucket_names:
                logger.info(f"✅ Bucket '{bucket_name}' exists")
            else:
                logger.error(f"❌ Bucket '{bucket_name}' NOT FOUND")
                return False
        return True
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}", exc_info=True)
        return False

def test_bronze_bucket():
    """Check Bronze bucket for data"""
    print("\n" + "="*60)
    print("2️⃣  CHECKING BRONZE BUCKET")
    print("="*60)
    try:
        query = f'''
        from(bucket: "{BUCKET_BRONZE}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "raw_packets")
        |> limit(n: 5)
        '''
        df = query_api.query_data_frame(query)
        if df is None or df.empty:
            logger.warning("⚠️  No Bronze data found in last hour")
            logger.info("   → Check if MQTT is publishing data")
            return False
        
        logger.info(f"✅ Found {len(df)} Bronze records")
        logger.info(f"   Columns: {list(df.columns)}")
        logger.info(f"   Sample:\n{df.head(2)}")
        return True
    except Exception as e:
        logger.error(f"❌ Error querying Bronze: {e}", exc_info=True)
        return False

def test_silver_bucket():
    """Check Silver bucket for data"""
    print("\n" + "="*60)
    print("3️⃣  CHECKING SILVER BUCKET")
    print("="*60)
    try:
        query = f'''
        from(bucket: "{BUCKET_SILVER}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "features")
        |> limit(n: 5)
        '''
        df = query_api.query_data_frame(query)
        if df is None or df.empty:
            logger.warning("⚠️  No Silver data found in last hour")
            logger.info("   → Check if Silver Pipeline is running")
            logger.info("   → Check if Bronze data exists (step 2)")
            return False
        
        logger.info(f"✅ Found {len(df)} Silver records")
        logger.info(f"   Columns: {list(df.columns)}")
        logger.info(f"   Sample:\n{df.head(2)}")
        return True
    except Exception as e:
        logger.error(f"❌ Error querying Silver: {e}", exc_info=True)
        return False

def test_gold_bucket():
    """Check Gold bucket for data"""
    print("\n" + "="*60)
    print("4️⃣  CHECKING GOLD BUCKET")
    print("="*60)
    try:
        query = f'''
        from(bucket: "{BUCKET_GOLD}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "aggregates")
        |> limit(n: 5)
        '''
        result = query_api.query(query)
        
        records = []
        for table in result:
            for record in table.records:
                records.append({
                    "time": record.get_time().isoformat() if record.get_time() else "N/A",
                    "state": record.values.get("state", "N/A"),
                    "ml_confidence": record.values.get("ml_confidence", "N/A"),
                    "attack_detected": record.values.get("attack_detected", "N/A"),
                    "traffic": record.values.get("traffic", "N/A"),
                })
        
        if not records:
            logger.warning("⚠️  No Gold data found in last hour")
            logger.info("   → Check if Gold Pipeline is running")
            logger.info("   → Check if Silver data exists (step 3)")
            return False
        
        logger.info(f"✅ Found {len(records)} Gold records")
        for i, rec in enumerate(records[:3]):
            logger.info(f"   Record {i+1}: {rec}")
        return True
    except Exception as e:
        logger.error(f"❌ Error querying Gold: {e}", exc_info=True)
        return False

def test_data_insertion():
    """Test inserting sample data"""
    print("\n" + "="*60)
    print("5️⃣  TESTING DATA INSERTION")
    print("="*60)
    try:
        # Insert test Bronze data
        test_point = (
            Point("raw_packets")
            .tag("src", "AA:BB:CC:DD:EE:FF")
            .tag("dst", "11:22:33:44:55:66")
            .field("subtype", "deauth")
            .field("rssi", -50)
            .time(datetime.utcnow())
        )
        
        write_api.write(bucket=BUCKET_BRONZE, record=test_point)
        logger.info("✅ Successfully inserted test Bronze record")
        
        # Verify it was written
        import time
        time.sleep(1)
        query = f'''
        from(bucket: "{BUCKET_BRONZE}")
        |> range(start: -1m)
        |> filter(fn: (r) => r.src == "AA:BB:CC:DD:EE:FF")
        |> limit(n: 1)
        '''
        df = query_api.query_data_frame(query)
        if df is not None and not df.empty:
            logger.info(f"✅ Verified: Test record exists in Bronze bucket")
            return True
        else:
            logger.warning("⚠️  Test record was not found after insertion")
            return False
    except Exception as e:
        logger.error(f"❌ Error during insertion test: {e}", exc_info=True)
        return False

def print_summary(results):
    """Print summary of test results"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    status = {
        "InfluxDB Connection": results[0],
        "Bronze Bucket": results[1],
        "Silver Bucket": results[2],
        "Gold Bucket": results[3],
        "Data Insertion": results[4],
    }
    
    for test, passed in status.items():
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {test}")
    
    all_passed = all(results)
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - System is operational!")
    else:
        print("⚠️  SOME TESTS FAILED - Check the output above")
        print("\nTroubleshooting steps:")
        if not results[0]:
            print("  1. Verify InfluxDB is running and accessible")
        if not results[1]:
            print("  2. Check MQTT client is publishing to Bronze bucket")
        if not results[2]:
            print("  3. Ensure Silver Pipeline is running")
        if not results[3]:
            print("  4. Ensure Gold Pipeline is running")
        if not results[4]:
            print("  5. Check write permissions to buckets")
    print("="*60)

async def main():
    """Run all tests"""
    logger.info("Starting Pipeline Diagnostic Tests...")
    
    results = []
    results.append(test_influx_connection())
    results.append(test_bronze_bucket())
    results.append(test_silver_bucket())
    results.append(test_gold_bucket())
    results.append(test_data_insertion())
    
    print_summary(results)

if __name__ == "__main__":
    asyncio.run(main())
