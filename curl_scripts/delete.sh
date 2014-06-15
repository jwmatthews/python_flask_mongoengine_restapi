if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
NAME=$1
SERVER_IP="127.0.0.1"
PORT="80"
URL="/sampleapp/items/${NAME}"

echo ""
echo "Response:"
curl -X DELETE http://${SERVER_IP}:${PORT}/${URL}/ 
echo ""

