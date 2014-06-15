SERVER_IP="127.0.0.1"
PORT="80"
URL="/sampleapp/items/"

echo ""
echo "Response:"
curl -s -X GET http://${SERVER_IP}:${PORT}/${URL}/ | python -m json.tool 
echo ""

