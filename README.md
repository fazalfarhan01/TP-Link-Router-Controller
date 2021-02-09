# TP-link WiFi Router Controller
- Based on Selenium.
- Uses the WebUI as you would normally do.
- Made due to the lack of any kind of __API__ to interact with any TP-Link Routers.

## Tested On:
- 1. Hardware: __Archer C1200 v2.0__
  2. Firmware Version: __2.0.2 Build 20180118 rel.38979 (EU)__

## To get started:
1. Clone the repository.
2. Create a virtual environment.
3. Install all the packages from [requirements.txt](./requirements.txt)
4. Download the [__Chrome webdriver__](https://chromedriver.chromium.org/downloads) and place it in [./bin/](./bin/) folder for windows.
5. For __Raspberry Pi__ install .deb packages from [here](https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+build/14482955). No need to set bin path, packages will be installed in right directory.
6. Run the program. See examples [here](./examples).