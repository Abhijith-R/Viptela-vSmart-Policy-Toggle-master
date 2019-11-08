[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/gve-sw/Viptela-vSmart-Policy-Toggle-master)

# Viptela vSmart policy Automation
Viptela has a set of APIs which can be used to integrate its functionalities with other solutions. This Proof of Value demonstrates the use of vManage APIs to automate the activation and deactivation of a vSmart policy based on a preset time and date. This application fetches all vSmart policies already present in vmanage and helps users to schedule a policy activation/deactivation based on a pre-selected time. This helps in operation automation where in the IT staff can schedule a policy activation/deactivation when the staff is not around or has no access to vmanage dashboard.

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

## Screenshot

![alt text](https://github.com/Abhijith-R/Viptela-vSmart-Policy-Toggle-master/blob/master/Policy_toggle.png)


#### API Reference/Documentation:
* [vManage REST APIs](https://sdwan-docs.cisco.com/Product_Documentation/Command_Reference/vManage_REST_APIs/vManage_REST_APIs_Overview)
* [vSmart Policy API](https://sdwan-d
