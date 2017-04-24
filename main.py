import falcon
import json
import hashlib
from pymemcache.client.base import Client

client = Client(('localhost', 11211))
 
class MessageResource:
    def on_post(self, req, resp):
        """Handles GET requests"""
        input = json.loads(req.stream.read().decode('utf-8'))
        digest = hashlib.sha256(input['message']).hexdigest()
        client.set(digest, input['message'])
        digest_json  = {
                'digest': digest
                }

        resp.body = json.dumps(digest_json)

    def on_get(self, req, resp, digest):
        """ Handles GET Requests"""
        message = client.get(digest)
        if message is None:
            resp.status = falcon.HTTP_404
            message_json = {
                    'err_message': 'Message not found'
                    }
        elif message is not None:
            resp.status = falcon.HTTP_200
            message_json = {
                    'message': message
                    }
        resp.body = json.dumps(message_json)
 
api = falcon.API()
api.add_route('/messages', MessageResource())
api.add_route('/messages/{digest}', MessageResource())
