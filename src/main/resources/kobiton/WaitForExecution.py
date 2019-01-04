import urllib2
import json
import time
import sys
import base64
import configs

executorServer = kobitonServer['executorServer']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']


def main():
  results = {}

  # Duplicate jobs list for fetching result
  jobsPool = jobIds.keys()

  if len(jobIds) == 0:
    print 'No Jobs for waiting.'
    return

  while len(jobsPool) >= 1:
    for id in jobsPool:
      try:
        response = getTestExecutionResult(id)
      
        if response['status'] == configs.testResultStatus['error']:
          results[id] = configs.testResultStatus['error']
          printError(id, response['message'])
        
        elif response['status'] == configs.testResultStatus['success']:
          results[id] = str(response['message'])
          
      except Exception as ex:
        results[id] = configs.testResultStatus['error']
        printError(id, ex)

    # Remove job id from pool when it got result
    for jobId in results:
      index = jobsPool.index(jobId)
      del jobsPool[index]

    # Delay to avoid DDOS
    if len(jobsPool) > 0:
      time.sleep(30)
  
  return results

# Format error message to display
def printError(id, err):
  print 'Error - ' + id + '\n'
  print '--------------------------\n'
  print err
  print '--------------------------\n'


def terminateTaskProcessWhenFail(testResult):
  for resultMessage in testResult.values():
    if resultMessage == configs.testResultStatus['error'] and isExitWhenFail:
      sys.exit(1)


def getTestExecutionResult(jobId):
  headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic %s' % base64.b64encode('%s:%s' % (username, apiKey))
  }

  url = executorServer + '/' + jobId + '/status'
  request = urllib2.Request(url, headers=headers)
  response = urllib2.urlopen(request)
  return json.loads(response.read())


# Execute task
testResults = main()
terminateTaskProcessWhenFail(testResults)
