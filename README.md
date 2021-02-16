# TP-link WiFi Router Controller
# Installation
```BASH
pip install tp-link-controller
```

# Usage
1. Install [JDK-8](https://www.oracle.com/in/java/technologies/javase/javase-jdk8-downloads.html)
    - Using Chocolatey: `choco install jdk8`
2. Download [browsermob-proxy](https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4) pass the binary path to `TP_Link_controller` object.

```PYTHON
from TPLinkController import controller

email = "xyz@examplemail.com"
password = "topSecret"

bmp_path = r"bin\browsermob-proxy-2.1.4\bin\browsermob-proxy"

tplink = controller.TP_Link_Controller(email, password, browsermobproxy_location=bmp_path, DEBUG_MODE=True)
```
By default chrome runs in headless mode (NO UI WILL OPEN)
If `DEBUG_MODE` is `True` or `headless` option is `False`, it will open chrome.

## Note: Login before doing anything
```PYTHON
tplink.login()
```

## The following methods are available
No. | Method | Use
--- | --- | ---
1 | .login() | Logins to the admin panel
2 | .close() | Exits the browser and closes the proxy
3 | .get_status() | Returns a dictionary with a lot of status information.
4 | .turn_on_2G() | Turns on 2.4G WiFi.
5 | .turn_on_5G() | Turns on 5G WiFi.
6 | .turn_off_2G() | Turns off 2.4G WiFi.
7 | .turn_off_5G() | Turns off 5G WiFi.
8 | .toggle_2g_wifi() | Toggles 2.4G WiFi
9 | .toggle_5g_wifi() | Toggles 5G WiFi
10 | .is_2g_on() | Returns `True` if 2.4G WiFi is `on` else `False`.
11 | .is_5g_on() | Returns `True` if 5G WiFi is `on` else `False`.


- Based on Selenium.
- Uses the WebUI as you would normally do.
- Made due to the lack of any kind of __API__ to interact with any TP-Link Routers.

## Tested On:
1. - Hardware: __Archer C1200 v2.0__
   - Firmware Version: __2.0.2 Build 20180118 rel.38979 (EU)__

## To get started with package dev:
1. Clone the repository.
2. Create a virtual environment.
3. Install all the packages from [requirements.txt](./requirements.txt)
4. Install [JDK-8](https://www.oracle.com/in/java/technologies/javase/javase-jdk8-downloads.html)
    - Using Chocolatey
    ```CHOCO
    choco install jdk8
    ```
5. Download [Browsermob-proxy](https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4).
    - For windows, leave it as default, should work out of the box.
    - Pass it to the instance in code.
    - ```PYTHON
      tplink = TP_Link_Controller(email, password, browsermobproxy_location=r"bin\browsermob-proxy-2.1.4\bin\browsermob-proxy", DEBUG_MODE=True)
      ```
4. Download the [__Chrome webdriver__](https://chromedriver.chromium.org/downloads) and place it in [`./bin/`](./bin/) folder for windows.
5. For __Raspberry Pi__ install .deb packages from [here](https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+build/14482955). No need to set bin path, packages will be installed in right directory.