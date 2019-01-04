import json
import re
import urllib2
import copy
import configs

apiServer = kobitonServer['url']
username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

deviceGroups = {
  'cloudDevices': isCloud,
  'privateDevices': isPrivate,
  'favoriteDevices': isFavorite
}

platformOptions = {
  'Android': isAndroid,
  'iOS': isiOS
}

def getAvailableDevices():
  try:
    devicesFetchingParams = getDevicesFetchingParams(customFetchingParams, platformOptions, groupId)
    rawDevicesList = getDevicesList(devicesFetchingParams)

    filteredDevicesList = filterDevices(deviceGroups, rawDevicesList) 
    print str(filteredDevicesList)

  except Exception as error:
    print 'Failed to get devices list ' + str(error)
  finally:
    return filteredDevicesList


def getDevicesFetchingParams(customFetchingParams, platformOptions, groupId):
  devicesFetchingParams = {}
  
  # Add custom params that declare from user
  customParams = getCustomParams(customFetchingParams)
  devicesFetchingParams.update(customParams)

  # Add require params for fetching devices
  platformFilterParam = getDevicesPlatformParams(platformOptions)
  if (platformFilterParam):
    devicesFetchingParams['platformName'] = platformFilterParam

  if (groupId):
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
  response = urllib2.urlopen(request)
  return json.loads(response.read())


def getDevicesPlatformParams(platformOptions):
  selectedPlatform = []

  for platformName in platformOptions:
    if platformOptions[platformName]:
      selectedPlatform.append(platformName)

  if (len(selectedPlatform) < 1):
    raise ValueError('No devices platform is selected, cannot get devices.')
  elif (len(selectedPlatform) == 1):
    # Since default will get both Android and iOS,
    # this will return one selected plaform type
    return selectedPlatform[0]


def getCustomParams(customFetchingParams):
  customParams = {}

  for params in customFetchingParams:
    if params not in configs.listIgnoreCustomeParams:  # Ignore these params since this task will use default value or avoid duplication
      customParams[params] = customFetchingParams[params]

  return customParams


def getBasicAuth():
  return 'Basic ' + (username + ':' + apiKey).encode('base64').rstrip()


def filterDevices(deviceGroups, rawDevicesList):
  formattedDevicesData = {}

  for group in deviceGroups:
    if deviceGroups[group]:
      for device in rawDevicesList[group]:
        udid = device['udid']
        if formattedDevicesData.get(udid) is None:
          formattedDevicesData[udid] = formatDeviceData(device)
          
  return  formattedDevicesData


def formatDeviceData(device):
  deviceGroup = configs.deviceGroup['cloud']

  if device['isMyOwn']:
    deviceGroup = configs.deviceGroup['inHouse']

  return device['deviceName'] + ' | ' + device['platformName'] + ' | ' + device['platformVersion'] + ' | ' + deviceGroup


def formatParams(devicesFetchingParams):
  formattedParams = '?'

  for param in devicesFetchingParams:
    formattedParams += param + '=' + str(devicesFetchingParams[param]) + '&'

  return formattedParams[:-1] # Remove last char '&' to avoid Forbidden Error


# Execute task
devices = getAvailableDevices()
