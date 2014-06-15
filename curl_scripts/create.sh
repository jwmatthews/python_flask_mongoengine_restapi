export SERVER_IP="127.0.0.1"
export PORT="80"
URL="/sampleapp/items/"

if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
NAME=$1

export DATA="{\"name\": \"${NAME}\", \"description\": \"This is a description for ${NAME}\", \"price\": 1.00}"

echo "Will attempt to create an item with the values:"
echo "${DATA}" | python -m json.tool

echo ""
echo "Response:"
curl -s -H "Content-Type: application/json" -X POST -d "${DATA}" http://${SERVER_IP}:${PORT}/${URL}/ 
echo ""

