import urllib2
import json
import copy
import base64
import configs

executorServer = kobitonServer['executorServer']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']


def mergeDevicesInput():
  listDevices = []

  # Kobiton only allows execute automation test
  # by udid on in-house devices.
  for udid in inputDevicesUdid:
    listDevices.append({'udid': udid})

  if availableDevices:
    for deviceUdid in availableDevices:
      if deviceUdid not in inputDevicesUdid: # Avoid duplication

        deviceComponents = availableDevices[deviceUdid].split(' | ')

        # All device componets will defined as
        # [<Device name>, <Device Platform>, <Platform version>, <Devices group>]
        if deviceComponents[3] == configs.deviceGroup['inHouse']:
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

  return listDevices


def executionHandler(listDevicesData): 
  executionJobIds = {}

  if not listDevicesData:
    print 'No device to execute tests.'
    return

  executionOptions = getTestExecutionOptions()
  
  for device in listDevicesData:
    try:
      executionOptions['desiredCaps'].update(device)
      eId = sendExecuteTestRequest(executionOptions)

      # Display in output
      # Showing usid of devices if user using private
      if device.has_key('udid'):
        executionJobIds[eId] = device['udid']
      else:
        executionJobIds[eId] = device['deviceName']

    except Exception as ex:
      errorDevice = device['deviceName'] if 'udid' not in device else device['udid']
      print "Error while executing test on {} : {}".format(errorDevice, ex)

  return executionJobIds

def sendExecuteTestRequest(requestBody):
  headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic %s' % base64.b64encode('%s:%s' % (username, apiKey))
  }
  url = executorServer + '/submit'

  request = urllib2.Request(url, json.dumps(requestBody), headers=headers)
  response = urllib2.urlopen(request)
  body = response.read()
  return body


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
          'commands': config
      }
    }

    if testType == 'App':
      template['desiredCaps']['app'] = appUrl
    elif testType == 'Browser':
      template['desiredCaps']['browserName'] = browserName.lower()
      
  except Exception as ex:
    print "Error while executing test: " + ex 

  return template

# Execute task
listDevicesData = mergeDevicesInput()
jobIds = executionHandler(listDevicesData)
