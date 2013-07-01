import requests
import hmac
import hashlib
import json

# Sign data
def sign(data, secret):
  return hmac.new(secret, data, hashlib.md5).hexdigest()


class Grooveshark():

  def __init__(self, key, secret):
    self.key = key
    self.secret = secret
    self.api_host = "api.grooveshark.com/ws3.php"
    self.listen_host = "http://grooveshark.com/"

  def _build_json(self, method, **kwargs):
    payload = {'header': {'wsKey': self.key},
              'method': method,
              'parameters': kwargs}
    return json.dumps(payload)