import requests
import hmac
import hashlib
import json

def sign_data(data, secret):
  """
  Signs data using HMAC, returns an MD5 hex digest.
  """
  return hmac.new(secret, data, hashlib.md5).hexdigest()

class Grooveshark():
  """
  A Grooveshark API wrapper for Python
  """
  #TODO: add cacheing.

  def __init__(self, key, secret):
    self.key = key
    self.secret = secret
    self.api_host = "http://api.grooveshark.com/ws3.php"
    self.listen_host = "http://grooveshark.com/"

  def _build_json(self, method, **kwargs):
    payload = {'header': {'wsKey': self.key},
              'method': method,
              'parameters': kwargs}
    return json.dumps(payload)

  def _do_API_call(self, data, sign):
    #TODO(tian): add json headers, look for more elegant way to sign.
    return requests.post(self.api_host + "?sig="+ sign, data=data)

  def getUserID(self, username):
    json = self._build_json("getUserIDFromUsername", username = username)
    sign = sign_data(json, self.secret)
    result = self._do_API_call(json, sign)
    return result.json()["result"]["UserID"]

