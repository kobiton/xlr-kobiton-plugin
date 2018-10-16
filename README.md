# The Kobiton plugin for XebiaLabs XL Release product

## Setup for development
Assume the environment is Mac OS
- Install Homebrew: `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
- Install Jython: `brew install jython`
- Install [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/download/#section=mac)
- Install [JDK 1.7](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html)

## Build and deploy
- Run command `gradle clean build` at the root directory
- Copy the `jar` from `build/libs` into `plugins/__local__` directory in XL-Release server
- ListDevices
  - `model`: The device model (Galaxy S8, iPhone 8, ...)
  - `devices`: (Output property) List of available devices
