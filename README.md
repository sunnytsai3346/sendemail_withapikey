Test with Postman ,
Usage:
To use this API, include the API key in the request headers as follows:

POST /api/send_email HTTP/1.1

Host: yourdomain.com

x-api-key: your_api_key

Content-Type: application/json

{
  "name": "John Doe",
  
  "sender_email": "john@example.com",
  
  "message": "Hello, I need some help!"
  
}
