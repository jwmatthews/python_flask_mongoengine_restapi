if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
NAME=$1

SERVER_IP="127.0.0.1"
PORT="80"
URL="/sampleapp/items/${NAME}"

export DATA="{\"name\": \"${NAME}\", \"description\": \"Updated description\", \"price\": 99.99}"

echo "Will attempt to update an item with the values:"
echo "${DATA}" | python -m json.tool

echo ""
echo "Response:"
curl -H "Content-Type: application/json" -X PUT -d "${DATA}" http://${SERVER_IP}:${PORT}/${URL}/ 
echo ""

