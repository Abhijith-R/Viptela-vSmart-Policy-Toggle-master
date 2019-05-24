
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
               
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
import sys
import requests
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.secret_key = 'some_secret'


# Scheduler to schedule deactivation of a activated policy
scheduler = BackgroundScheduler()
scheduler.start()

# vManage login page
@app.route('/')
def check_credentials():
    return render_template('login.html')

# vManage home page
@app.route('/index')
def index():
    data_list = listvsmartpolicies()
    return render_template('index.html', data=data_list)


# vManage login and fetch session
@app.route('/login', methods=['POST'])
def login():
    """Login to vmanage"""
    session = {}
    
    global username
    global password
    global vmanage_ip
    
    username = request.form['uname']
    password = request.form['pwd']
    vmanage_ip = request.form['ip']

    base_url_str = 'https://%s/'%vmanage_ip

    login_action = '/j_security_check'

    #Format data for loginForm
    login_data = {'j_username' : username, 'j_password' : password}

    #Url for posting login data
    login_url = base_url_str + login_action

    url = base_url_str + login_url

    sess = requests.session()

    #If the vmanage has a certificate signed by a trusted authority change verify to True
    login_response = sess.post(url=login_url, data=login_data, verify=False)
    try:
        if login_response.status_code == 200:
            data_list = listvsmartpolicies()
            session[vmanage_ip] = sess
            global sessions
            sessions = session[vmanage_ip]
            return render_template('index.html', data=data_list)
        elif '<html>' in login_response.content:
            flash("Login Failed!! Please try again", 'danger')
            return render_template('login.html')
            print "Login Failed"
            sys.exit(0)
        else:
            print("Unknown exception")
    except Exception as err:
        flash('Login Failed!! Please try again -  '+ str(err), 'danger')
        return redirect("/")


    return session[vmanage_ip]

@app.route('/logout', methods=['POST'])
def logout():
    return redirect("/")


# List Policies
def listvsmartpolicies():
    policy_list = []
    r = requests.get("https://"+vmanage_ip+'/dataservice/template/policy/vsmart', auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
    policyJson = json.loads(r.text)
    for i in range(policyJson["data"].__len__()):
        policyName = policyJson.get("data")[i].get("policyName"), policyJson.get("data")[i].get("policyId"), policyJson.get("data")[i].get("isPolicyActivated")
        policy_list.append(policyName)
    print policy_list
    return policy_list


# Activate Policy
@app.route('/activate', methods=['POST'])
def activatePolicy():
    try:
        # Fetch current time
        now = datetime.datetime.now()
        nowTime = datetime.datetime.strftime(now, '%Y-%m-%d %I:%M %p')

        # Fetch date from the UI
        activateDate = request.form['activateDate']
        activateDate_obj = datetime.datetime.strptime(activateDate, '%Y-%m-%d')
        activate_Date = datetime.datetime.strftime(activateDate_obj, '%Y-%m-%d')

        # Fetch start time from the UI
        start = activate_Date+" "+request.form['nameStartTime']
        start_time_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
        startTime = datetime.datetime.strftime(start_time_obj, '%Y-%m-%d %I:%M %p')

        # Fetch end time from the UI
        end = activate_Date+" "+request.form['nameEndTime']
        end_time_obj = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')
        endTime = datetime.datetime.strftime(end_time_obj, '%Y-%m-%d %I:%M %p')

        # Fetch Policy ID and Policy Name
        policyid = request.form['policyIdName1']
        policy_name_1 = request.form['hiddenPolicyName1']

        headers = {'Content-Type': 'application/json'}
        payload = "{\n }"
        # Check if start time is equal to the current time
        if(start_time_obj<=now):
            url = 'https://' + vmanage_ip + '/dataservice/template/policy/vsmart/activate/' + policyid
            r = sessions.post(url, data=payload, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
            scheduler.add_job(lambda: autoDeactivatePolicy(policyid), 'date', run_date=end_time_obj)
            flash(policy_name_1+' Activated!! Will be deactivated automatically on '+endTime,'success')
            return redirect(url_for('index'))
        else:
            scheduler.remove_all_jobs()
            scheduler.add_job(lambda: scheduleActivation(policyid,end_time_obj), 'date', run_date=start_time_obj)
            scheduler.print_jobs()
            flash(policy_name_1 + ' Activation scheduled for '+startTime+'. Will be deactivated automatically on ' + endTime, 'success')
            return redirect(url_for('index'))
    except Exception as err:
        flash('Oops!! Unexpected Error -  '+ str(err), 'danger')
        return redirect(url_for('index'))


# Schedule Policy Activation
def scheduleActivation(policyId,endActivation):
    headers = {'Content-Type': 'application/json'}
    payload = "{\n }"
    try:
        url = 'https://' + vmanage_ip + '/dataservice/template/policy/vsmart/activate/' + policyId
        r = sessions.post(url, data=payload, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
        scheduler.add_job(lambda: autoDeactivatePolicy(policyId), 'date', run_date=endActivation)
        return
    except Exception as err:
        print(err)

# Deactivate Policy
@app.route('/deactivate', methods=['POST'])
def deactivatePolicy():
    policyid = request.form['policyIdName2']
    policy_name_2 = request.form['hiddenPolicyName2']
    headers = {'Content-Type': 'application/json'}
    payload = "{\n }"
    try:
        url = 'https://' + vmanage_ip + '/dataservice/template/policy/vsmart/deactivate/' + policyid
        r = sessions.post(url, data=payload, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
        flash(policy_name_2+' Deactivated', 'success')
        return redirect(url_for('index'))
    except Exception as err:
        flash('Oops!! Unexpected error -  '+ str(err), 'danger')
        return redirect(url_for('index'))

# Auto deactivate a policy on the specified end time
def autoDeactivatePolicy(policyId):
    headers = {'Content-Type': 'application/json'}
    payload = "{\n }"
    try:
        url = 'https://' + vmanage_ip + '/dataservice/template/policy/vsmart/deactivate/' + policyId
        r = sessions.post(url, data=payload, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
        print("Deactivated")
        return
    except Exception as err:
        print(err)


app.run("0.0.0.0")
