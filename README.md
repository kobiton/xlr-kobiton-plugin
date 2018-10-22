# The Kobiton plugin for XebiaLabs XL Release product

- [The Kobiton plugin for XebiaLabs XL Release product](#the-kobiton-plugin-for-xebialabs-xl-release-product)
  - [Preface](#preface)
  - [Overview](#overview)
  - [Installation](#installation)
  - [Tasks](#tasks)
    - [Configuration plugin](#configuration-plugin)
    - [List Available Devices](#list-available-devices)
    - [Execute Script](#execute-script)
    - [Wait for execution](#wait-for-execution)
  - [Testing / Building](#testing---building)
    - [Setup for development](#setup-for-development)
    - [Executing:](#executing)
  - [References](#references)

## Preface

This document describes the functionality provided by the `xlr-Kobiton-plugin`

See the **[XL Release Reference Manual](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

## Overview

Kobiton plugin for XL release allows users to setup and run automation test on Kobiton devices.

Kobiton plugin tests can be sent to:
- Kobiton server with user private instance.
- User hosting server.
- On-Premises.


## Installation

Place the latest released version under the `plugins` dir.

## Tasks

### Configuration plugin
> Set up environment to use Kobiton plugin

**Input**
- `Title`: Server title

- `Kobiton username` and `Kobiton api key`: Follow instructions at **IV. Configure Test Scripts** for Kobiton section on [our blog article](https://kobiton.com/blog/tutorial/parallel-testing-selenium-webdriver/) to get Kobiton username and API key.

- `Kobiton Api url`: (**default**: https://api.kobiton.com)

- `Remote server domain`: Server to execute automation test

### List Available Devices
>This task will get all available devices. For params from input will use for filter to get correct devices in needed.

**Input:**
- Get devices from: (Type: Boolean)
  - `Favorite Devices`: Devices prefer to use
  - `In-house Devices`: Devices is hosting by user.
  - `Cloud Devices`: Kobiton devices.

- `Devices Name`: Filter devices by name model. Example: "Galaxy S, LG"

- Devices platform: (Type: Boolean) Tick to get exact devices platform `Android`, `iOS`

- `Group ID`: devices belong to group. 

**Output**
- `Devices list`: list devices that match above criterias

### Execute Script
>This task will consume the test script and perform automation test on each devices from the devices list.

**Input**

- `Kobiton devices list`: List devices, get from task **List Available Devices**

- `In-house Devices list`: List udid of private devices (hosing by current user), input manually

- `Override desiredCaps`: (Type: Boolean) If checked, **Orientation and Capture screenshot** setting will use the below value, else it will use from **config server**

- `Orientation`: **Portrait** or **Landscape**

- `Capture screenshot`: (Type: Boolean)

- `Test type`: **App** or **Browser**

- `Browser`: **Chrome**, **Chrome-beta** or **Safari** (If **test type** is **App**, ignore this value)

- `App URL/App ID`: Insert public url of the app or App Id from Kobiton (May need to upload app to Kobiton repository first) (If *test type* is **Browser**, ignore this value)
  
- `Group ID`: Testing devices belong to group. 

- `Git repository`: Test script repository, can use **Public** or **Private** repository link. If using **Private** repo, **ssh-key** will required. Kobiton will automatically download the repository to the instance for executing test.

- `Git repository ssh key`: Private key to download **Private repo**

- `Configuration Commands`: Each line will be a bash commands to execute the automation test. Currently, Kobiton support template as below
  ```bash
    commands:
    - <your commands>
  ```

  From Kobiton example: 
  ```bash
    commands:
    - git checkout demo-xl
    - cd javascript
    - yarn install
    - yarn run android-app-test
  ```

**Output**
- `Job ids`: list job ids

### Wait for execution
>Sleep the release to get automation test results. Can Terminate when get fail result

**Input**

- `Job ids`: list job ids

- `Terminate when failed`: (Type: Boolean)
  
**Output**

- `Test result`: Test result, it will display error report when devices fails

## Testing / Building

### Setup for development
Assume the environment is Mac OS

- Install [Homebrew](https://brew.sh/)

  - Install [Jython](http://brewformulas.org/Jython):
    ``` shell
    brew install jython
    ```

  - Install [Gradle](https://gradle.org/install/): 
    ``` shell
    brew install gradle
    ```

- Install [JDK 1.7](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html)


### Executing: 
``` shell
  gradle clean build
```

- Copy the `jar` file from **build/libs** into your plugins folder.

## References

- [Kobiton](https://kobiton.com/)
- [Kobiton docs](https://docs.kobiton.com/)
- [Kobiton API docs](https://api.kobiton.com/docs/)