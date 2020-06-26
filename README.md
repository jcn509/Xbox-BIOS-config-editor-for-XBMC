# iND-BiOS Config Editior for XBMC4XBOX [![Build Status](https://travis-ci.com/jcn509/Xbox-BIOS-config-editor-for-XBMC.svg?branch=master)](https://travis-ci.com/jcn509/Xbox-BIOS-config-editor-for-XBMC) 
This is an an addon for XBMC4XBOX that allows you to edit your iND-BiOS config file from within XBMC. In the future it may also support the X2 BIOS.

This should help you to more easily experiment with the various configuration options iND-BiOS provides. 
This addon allows you to save and load presets for that boot animation animation 
colours and model so that you can easily swap out the look of your Xbox in 
seconds. It (will soon) even comes bundled with several presets out of the box.

# This project is still a work in progress and should not be used yet!

# PLEASE NOTE
If iND-BiOS cannot find any of the custom dashboard paths you have set up. It
will try to load:
1. \Device\Harddisk0\Partition2\evoxdash.xbe (C:\evoxdash.xbe)
2. \Device\Harddisk0\Partition2\xboxdash.xbe (C:\xboxdash.xbe)
3. \Device\Harddisk0\Partition2\avalaunch.xbe (C:\avalaunch.xbe)
Please make sure you have a working dashboard installed in at least one of 
these locations in case something goes wrong with the dashboard paths
exported by this tool (or in case you accidentally delete your dash). Ideally
you should make sure you have custom dashboards installed at both
C:\evoxdash.xbe and C:\avalaunch.xbe and eiter the MS dash or a custom dash at
C:\xboxdash.xbe.

## Video preview
To Do

## Installation
To Do

### XBMC4Gamers Support
To do

## Usage
To Do

## Developer notes
This project was built using the 
[PyXBMCT](https://github.com/romanvm/script.module.pyxbmct) framework.

All controls (apart from buttons) need to inherit from the AbstractControl
class so that they all have the same basic interface. The default controls from
pyxbmct all have different methods that are used to set/get their values. (This
does not apply to buttons as they do not have a value to get or set.). All
controls should also pass their current value to whatever callback is connected
to them via window.connect.

I have tried to create the beginnings of a framework that can be used to create
config file editors. This project could be modified fairly easily to support the
editing of other config files.

Icons are taken from https://dribbble.com/shots/2888226-1800-Free-Minimal-Icon-Pack-20x20. Note: not all of them are actually square... Therefore I have to set funny padding values in the code sometimes to get them to line up right :/

### Installation for source code editing
You will need to use Python 2.7 (as that is the version that is embedded in XBMC4XBOX). After cloning the repo you can install the project and all its dependencies (including the dev dependencies needed for testing) using:
```sh
pip install -e ".[dev]"
```


### Tests
Run the tests with `pytest`
