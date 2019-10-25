[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/gve-sw/Viptela-vSmart-Policy-Toggle-master)

# Viptela vSmart policy Automation
Viptela has a set of APIs which can be used to integrate its functionalities with other solutions. This Proof of Value demonstrates the use of vManage APIs to automate the activation and deactivation of a vSmart policy based on a preset time and date.

#### Author:

* Abhijith R (abhr@cisco.com)
*  Dec 2018
***

## Prerequisites
* Python 2.7
* APScheduler 3.5.3
* PyCharm/Any text editor
* Flask

## Steps to Reproduce
* Download/clone the repository
* Import the code into a text editor like pycharm or Atom
* Install the required dependencies using requirements.txt ```pip install -r requirements.txt```
* Open controller.py file and make necessary changes as mentioned in the comment in the file
* After necessary changes are made to the code, execute controller.py file on the editor or on the terminal (```python controller.py```)

#### API Reference/Documentation:
* [vManage REST APIs](https://sdwan-docs.cisco.com/Product_Documentation/Command_Reference/vManage_REST_APIs/vManage_REST_APIs_Overview)
* [vSmart Policy API](https://sdwan-docs.cisco.com/Product_Documentation/Command_Reference/vManage_REST_APIs/Device_Configuration_APIs/vSmart_Policy#Activate_vSmart_Policy)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
