for i in {1..1000}; do
  SRC="device_$((RANDOM%10+1))"
  DST="device_$((RANDOM%10+1))"
  SUBTYPE=$(shuf -n1 -e wifi ble zigbee)
  RSSI=$((RANDOM%60-90))  # -90 to -30
  TIMESTAMP=$(date +%s%N)
  echo "raw_packets,src=$SRC,dst=$DST subtype=\"$SUBTYPE\",rssi=$RSSI $TIMESTAMP"
done > bronze_data.lp