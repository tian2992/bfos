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
    self.country = self.getCountry()

  def _build_json(self, method, **kwargs):
    payload = {'header': {'wsKey': self.key},
              'method': method,
              'parameters': kwargs}
    return json.dumps(payload)

  def _do_API_call(self, data, sign):
    #TODO(tian): add json headers, look for more elegant way to sign.
    return requests.post(self.api_host + "?sig="+ sign, data=data)

  def getCountry(self, ip = None):
    """
    Gets the country object. IP is optional.
    """
    if (ip):
      json = self._build_json("getCountry", ip=ip)
    else:
      json = self._build_json("getCountry")
    sign = sign_data(json, self.secret)
    result = self._do_API_call(json, sign)
    return result.json()["result"]

  def getUserIDFromUsername(self, username):
    json = self._build_json("getUserIDFromUsername", username = username)
    sign = sign_data(json, self.secret)
    result = self._do_API_call(json, sign)
    #TODO: handle errors
    return result.json()["result"]["UserID"]

  def getUserPlaylistsByUserID(self, userID, limit=0):
    json = self._build_json("getUserPlaylistsByUserID", userID = userID, limit=limit)
    sign = sign_data(json, self.secret)
    result = self._do_API_call(json, sign)
    return result

  def getSongSearchResults(self, query, country=None, limit=0, offset=0):
    if not country:
      country = self.country
    json = self._build_json("getSongSearchResults", query=query, country=country)
    sign = sign_data(json, self.secret)
    result = self._do_API_call(json, sign)
    return result.json()["result"]["songs"]
