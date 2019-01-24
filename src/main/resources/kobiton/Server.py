import sys
import re
import urllib2
import base64

errorLog = []

def verifyConnection(params={}, headers={}):
  try:
    request = urllib2.Request(params['url'], None, headers)
    urllib2.urlopen(request)
  except Exception as ex:
    errorLog.append("Error while connecting to {}: {}".format(params['server'], ex))

verifyConnection({
  "url": re.sub(r'\/$|\\$','',configuration.apiServer) + '/v1/devices',
  "server": "Api Server"
}, {
  "Authorization": 'Basic %s' % base64.b64encode('%s:%s' % (configuration.username, configuration.apiKey))
})

verifyConnection({
  "url": re.sub(r'\/$|\\$','',configuration.executorServer) + '/ping',
  "server": "Execution Server"
})

if errorLog != []:
  sys.exit(errorLog)
