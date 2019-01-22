import urllib2
import json
import copy
import base64
import sys

executorServer = kobitonServer['executorServer']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']


def mergeDevicesInput():
  listDevices = []

  # Kobiton only allows execute automation test
  # by udid on in-house devices.
  for udid in inputDevicesUdid:
    listDevices.append({'udid': udid})

  for deviceUdid in availableDevices:
    if deviceUdid not in inputDevicesUdid: # Avoid duplication

      deviceComponents = availableDevices[deviceUdid].split(' | ')

      # All device componets will defined as
      # [<Device name>, <Device Platform>, <Platform version>, <Devices group>]
      if deviceComponents[3] == 'In-house':
        deviceData = {
          'udid': deviceUdid,
        }
      else:
        deviceData = {
          'deviceName' : deviceComponents[0],
          'platformName': deviceComponents[1],
          'platformVersion': deviceComponents[2]
        }

      listDevices.append(deviceData)

  if not listDevices:
    print "No devices found to execute Test"
    return False

  return listDevices


def executionHandler(listDevicesData): 
  executionJobIds = {}

  if len(listDevicesData) < 1:
    print 'No device to execute tests.'
    return

  executionOptions = getTestExecutionOptions()

  for device in listDevicesData:
      executionOptions['desiredCaps'].update(device)
      response = sendExecuteTestRequest(executionOptions)
      if 'err' in response:
        errorDevice = device['deviceName'] if 'udid' not in device else device['udid']
        print "Error while executing test on {} : {}\n{}".format(errorDevice, response['err'], response['msg'])
      else:
        # Display in output
        # Showing usid of devices if user using private
        if device.has_key('udid'):
          executionJobIds[response] = device['udid']
        else:
          executionJobIds[response] = device['deviceName']

  return executionJobIds


def sendExecuteTestRequest(requestBody):
  headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic %s' % base64.b64encode('%s:%s' % (username, apiKey))
  }
  request = urllib2.Request(executorServer + '/submit', json.dumps(requestBody), headers=headers)
  try:
    response = urllib2.urlopen(request)
  except urllib2.HTTPError as e:
    return {'err': e, 'msg': e.read()}
  except urllib2.URLError as e:
    return {'err': e, 'msg': 'Cannot reach to executor server.'}
  else:
    body = response.read()
    return json.loads(body)


def getTestExecutionOptions():
  # Get customize input in field
  try:
    template = {
      'desiredCaps': {
          'deviceOrientation': deviceOrientation,
          'captureScreenshots': captureScreenshots,
          'groupId': groupId,
          'deviceGroup': 'ANY'
      },
      'testConfig': {
          'git': gitUrl,
          'ssh': ssh,
          'branch': branch,
          'commands': configCmds
      }
    }

    if executionType == 'App':
      template['desiredCaps']['app'] = appUrl
    elif executionType == 'Browser':
      template['desiredCaps']['browserName'] = browserName.lower()
      
  except Exception as ex:
    print "Error while executing test: " + ex 
  return template


# Execute task
listDevicesData = mergeDevicesInput()
if listDevicesData:
  jobIds = executionHandler(listDevicesData)
else:
  sys.exit(1)