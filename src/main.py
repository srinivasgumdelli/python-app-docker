import falcon
import hashlib
import json

from pymemcache.client.base import Client

client = Client(('memcached', 11211))
 
class MessageResource:
    def on_post(self, req, resp):
        """
        Handles POST requests, creates a digest for a message and stores
        it in memcached as "digest: message" format. The duplicates should
        be handled automatically and returns a 201 status code
        """
        input = json.loads(req.stream.read().decode('utf-8'))
        digest = hashlib.sha256(input['message']).hexdigest()
        client.set(digest, input['message'])
        resp.status = falcon.HTTP_201
        digest_json  = {
                'digest': digest
                }

        resp.body = json.dumps(digest_json)

    def on_get(self, req, resp, digest):
        """
        Handles GET requests, retrieves a message for digest, if it does not
        exist, returns a 404 status code; 200 status code along with the
        original message otherwise
        """
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
