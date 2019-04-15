# Meraki Device Provisioning Web App
Web App to allow users to add Meraki Devices to Meraki Networks

INSTALL AND RUN INSTRUCTIONS

1. Open the add_device_webapp.py file and change the 'apikey' and 'organizationid' variables to match your Meraki Organization

2. Create a Python Virtual Environment and install the required dependencies
```
python3 -m pip install --upgrade pip
python3 -m venv venv
. venv/bin/activate
pip3 install flask flask-wtf wtforms requests
```

3. Run the app
```
export FLASK_APP=add_device_webapp.py
flask run --host=0.0.0.0
```

4. Open http://127.0.0.1:5000 in a web browser


Here are screenshots to show what the app looks like:

![alt text](https://raw.githubusercontent.com/nathanwiens/meraki-add-device-webapp/master/static/webapp1.png)
![alt text](https://raw.githubusercontent.com/nathanwiens/meraki-add-device-webapp/master/static/webapp2.png)
![alt text](https://raw.githubusercontent.com/nathanwiens/meraki-add-device-webapp/master/static/webapp3.png)
