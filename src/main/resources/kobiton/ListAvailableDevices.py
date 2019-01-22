import json
import re
import urllib2
import copy
import sys

apiServer = kobitonServer['apiServer']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

inputDevicesGroups = {
  'cloudDevices': isCloud,
  'privateDevices': isPrivate,
  'favoriteDevices': isFavorite
}

platformOptions = {
  'Android': isAndroid,
  'iOS': isiOS
}

def checkInputValues():
  checkDevicesGroupSelected = inputDevicesGroups.values()
  if True not in checkDevicesGroupSelected:
    print "Error, cannot get list available devices because there are no devices group selected."
    return False
    
  checkSelectedPlatform = platformOptions.values()
  if True not in checkSelectedPlatform:
    print "Error, cannot get list available devices because there are no devices platform selected."
    return False
  
  return True


def getAvailableDevices():
  filteredDevicesList = {}

  devicesFetchingParams = getDevicesFetchingParams(customFetchingParams, platformOptions, groupId)
  rawDevicesList = getDevicesList(devicesFetchingParams)
  if 'err' in rawDevicesList:
    print "Error while fetching devices on: {}\n{}".format(rawDevicesList['err'], rawDevicesList['msg'])
  else:
    filteredDevicesList = filterDevices(inputDevicesGroups, rawDevicesList)
  
  return filteredDevicesList


def getDevicesFetchingParams(customFetchingParams, platformOptions, groupId):
  devicesFetchingParams = {}
  
  # Add custom params that declare from user
  customParams = getCustomParams(customFetchingParams)
  devicesFetchingParams.update(customParams)

  # Add require params for fetching devices
  platformFilterParam = getDevicesPlatformParams(platformOptions)
  if platformFilterParam:
    devicesFetchingParams['platformName'] = platformFilterParam

  if groupId:
    devicesFetchingParams['groupId'] = groupId

  # Add default value for fetching list available devices
  devicesFetchingParams.update({
    'isBooked': False,
    'isOnline': True,
    'appiumDisabled': False
  })
  # Format devices data for better looking
  return formatParams(devicesFetchingParams)


def getDevicesList(params):
  auth_token = getBasicAuth()
  url =  re.sub(r'\/$|\\$','', apiServer) + '/v1/devices' + params

  header = {
    'Content-Type': 'application/json',
    'Authorization': auth_token
  }

  request = urllib2.Request(url, headers=header)
  try:
    response = urllib2.urlopen(request)
  except urllib2.HTTPError as e:
    return {'err': e, 'msg': e.read()}
  except urllib2.URLError as e:
    return {'err': e, 'msg': 'Cannot reach to kobiton api server.'}
  else:
    body = response.read()
    return json.loads(body)


def getDevicesPlatformParams(platformOptions):
  selectedPlatform = []

  for platformName in platformOptions:
    if platformOptions[platformName]:
      selectedPlatform.append(platformName)

  if len(selectedPlatform) < 1:
    raise ValueError('No devices platform is selected, cannot get devices.')
  elif len(selectedPlatform) == 1:
    # Since default will get both Android and iOS,
    # this will return one selected plaform type
    return selectedPlatform[0]


def getCustomParams(customFetchingParams):
  listIgnoreCustomeParams = ['isBooked', 'isOnline', 'appiumDisabled', 'platformName', 'groupId']
  customParams = {}

  for params in customFetchingParams:
    if params not in listIgnoreCustomeParams:  # Ignore these params since this task will use default value or avoid duplication
      customParams[params] = customFetchingParams[params]

  return customParams


def getBasicAuth():
  return 'Basic ' + (username + ':' + apiKey).encode('base64').rstrip()


def filterDevices(inputDeviceGroups, rawDevicesList):
  formattedDevicesData = {}

  for group in inputDeviceGroups:
    if inputDeviceGroups[group]:
      for device in rawDevicesList[group]:
        udid = device['udid']
        if formattedDevicesData.get(udid) is None:
          formattedDevicesData[udid] = formatDeviceData(device)
          
  return  formattedDevicesData


def formatDeviceData(device):
  deviceGroup = 'Kobiton Cloud'

  if device['isMyOwn']:
    deviceGroup = 'In-house'

  return device['deviceName'] + ' | ' + device['platformName'] + ' | ' + device['platformVersion'] + ' | ' + deviceGroup


def formatParams(devicesFetchingParams):
  formattedParams = '?'

  for param in devicesFetchingParams:
    formattedParams += param + '=' + str(devicesFetchingParams[param]) + '&'

  formattedParams = formattedParams.replace(" ", "%20")
  return formattedParams[:-1] # Remove last char '&' to avoid Forbidden Error


# Execute task
canExecuteTask = checkInputValues()
if canExecuteTask:
  devices = getAvailableDevices()
else:
  sys.exit(1)