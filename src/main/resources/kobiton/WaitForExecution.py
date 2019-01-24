import urllib2
import json
import time
import sys
import base64

executorServer = kobitonServer['executorServer']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

testResultStatus = {
  'success': 'SUCCESS',
  'error': 'ERROR'
}


def main():
  results = {}
  logs = {}

  if not jobIds:
    print 'No Jobs for waiting.'
    return False

  # Duplicate jobs list for fetching result
  jobsPool = jobIds.keys()
   
  while len(jobsPool) >= 1:
    for id in jobsPool:
      response = getTestExecutionResult(id)
      
      if 'err' in response:
        print "Error while fetching test result on {}: {}\n{}".format(id, response['err'], response['msg'])
      elif response['status'] == 'error':
        results[id] = testResultStatus['error']
        logs[id] = response['log']
      elif response['status'] == 'completed':
        results[id] = str(response['message'])
        logs[id] = response['log']
    
    # Remove job id from pool when it got result
    for jobId in results:
      if jobId in jobsPool:
        index = jobsPool.index(jobId)
        del jobsPool[index]

    # Delay to avoid DDOS
    if len(jobsPool) > 0:
      time.sleep(30)

  printResultLogs(logs)

  return results


def terminateTaskProcessWhenFail(testResult):
  for resultMessage in testResult.values():
    if resultMessage == testResultStatus['error'] and isExitWhenFail:
      sys.exit(1)


def getTestExecutionResult(jobId):
  headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic %s' % base64.b64encode('%s:%s' % (username, apiKey))
  }

  url = executorServer + '/' + jobId + '/status'
  request = urllib2.Request(url, headers=headers)
  try:
    response = urllib2.urlopen(request)
  except urllib2.HTTPError as e:
    return {'err': e, 'msg': e.read()}
  except urllib2.URLError as e:
    return {'err': e, 'msg': 'Cannot reach to executor server.'}
  else:
    body = response.read()
    return json.loads(body)


def printResultLogs(logs):
  for jobId in logs:
    print jobId  
    print '-------------------------------------------'
    print 'Logs url - ' + logs[jobId] 


# Execute task
testResults = main()
terminateTaskProcessWhenFail(testResults)