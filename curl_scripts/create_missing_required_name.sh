SERVER_IP="127.0.0.1"
PORT="80"
URL="/sampleapp/items/"

DATA="{\"description\": \"This is a description\", \"price\": 1.00}"

echo "Will attempt to create an item with the values:"
echo "${DATA}" | python -m json.tool

echo ""
echo "Response:"
curl -H "Content-Type: application/json" -X POST -d "${DATA}" http://${SERVER_IP}:${PORT}/${URL}/ 
echo ""

