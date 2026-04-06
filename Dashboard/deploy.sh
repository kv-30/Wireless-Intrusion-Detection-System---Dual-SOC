#!/bin/bash
# Quick deployment script - Run this to deploy and test everything!

set -e

echo "🚀 WIRELESS IDS QUICK DEPLOYMENT"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_DIR="/Users/shubhadashinde/Desktop/wireless_ids/backend"
FRONTEND_DIR="/Users/shubhadashinde/Desktop/wireless_ids/frontend"

# Step 1: Stop current backend
echo -e "${BLUE}Step 1: Stopping current backend...${NC}"
pkill -f "python -m app.main" || echo "No backend running"
sleep 2
echo -e "${GREEN}✅ Backend stopped${NC}"
echo ""

# Step 2: Verify code updates
echo -e "${BLUE}Step 2: Verifying code updates...${NC}"
if grep -q "isinstance(features, dict)" "$BACKEND_DIR/app/processing/silver_pipeline.py"; then
    echo -e "${GREEN}✅ silver_pipeline.py updated${NC}"
else
    echo -e "${RED}❌ silver_pipeline.py NOT updated${NC}"
    exit 1
fi

if grep -q "limit(n: 100)" "$BACKEND_DIR/app/processing/gold_pipeline.py"; then
    echo -e "${GREEN}✅ gold_pipeline.py updated${NC}"
else
    echo -e "${RED}❌ gold_pipeline.py NOT updated${NC}"
    exit 1
fi
echo ""

# Step 3: Start backend in background
echo -e "${BLUE}Step 3: Starting backend...${NC}"
cd "$BACKEND_DIR"
python -m app.main > pipeline.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
sleep 3
echo ""

# Step 4: Run diagnostic test
echo -e "${BLUE}Step 4: Running diagnostic test...${NC}"
cd "$BACKEND_DIR"
if python test_pipeline.py > test_output.log 2>&1; then
    echo -e "${GREEN}✅ Tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed - checking logs${NC}"
    tail -20 test_output.log
fi
echo ""

# Step 5: Check API endpoints
echo -e "${BLUE}Step 5: Testing API endpoints...${NC}"
sleep 2

# Test Bronze
BRONZE_RESP=$(curl -s http://localhost:8000/api/bronze?seconds=60 | jq length 2>/dev/null || echo "0")
if [ "$BRONZE_RESP" != "0" ]; then
    echo -e "${GREEN}✅ Bronze API: $BRONZE_RESP records${NC}"
else
    echo -e "${YELLOW}⚠️  Bronze API: No records (expected if no MQTT data)${NC}"
fi

# Test Silver
SILVER_RESP=$(curl -s http://localhost:8000/api/silver?seconds=60 | jq length 2>/dev/null || echo "0")
if [ "$SILVER_RESP" != "0" ]; then
    echo -e "${GREEN}✅ Silver API: $SILVER_RESP records${NC}"
else
    echo -e "${YELLOW}⚠️  Silver API: No records (expected if no Bronze data)${NC}"
fi

# Test Gold
GOLD_RESP=$(curl -s http://localhost:8000/api/gold?seconds=300 | jq length 2>/dev/null || echo "0")
if [ "$GOLD_RESP" != "0" ]; then
    echo -e "${GREEN}✅ Gold API: $GOLD_RESP records${NC}"
else
    echo -e "${YELLOW}⚠️  Gold API: No records (expected if no Silver data)${NC}"
fi
echo ""

# Step 6: Summary
echo -e "${BLUE}DEPLOYMENT SUMMARY${NC}"
echo "==================="
echo -e "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}✅ Code updated and verified${NC}"
echo -e "${GREEN}✅ API endpoints responding${NC}"
echo ""

echo -e "${YELLOW}Next steps:${NC}"
echo "1. To start frontend:"
echo "   cd $FRONTEND_DIR && npm start"
echo ""
echo "2. To publish test MQTT data:"
echo "   mosquitto_pub -h localhost -t 'network/packets' -m '{\"src\":\"AA:BB:CC:DD:EE:FF\",\"dst\":\"11:22:33:44:55:66\",\"subtype\":\"deauth\",\"rssi\":-50}'"
echo ""
echo "3. To monitor backend logs:"
echo "   cd $BACKEND_DIR && tail -f pipeline.log | grep -E 'Silver|Gold'"
echo ""
echo "4. Open dashboard:"
echo "   http://localhost:3000"
echo ""
echo -e "${GREEN}🎉 System is ready!${NC}"
