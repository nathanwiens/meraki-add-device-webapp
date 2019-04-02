# Meraki Add Device Web App
Web App to allow users to add Meraki Devices to Meraki Networks

INSTALL AND RUN INSTRUCTIONS

1. Open the add_device_webapp.py file and change the 'apikey' and 'organizationid' variables to match your Meraki Organization

2. Create a Python Virtual Environment and install the required dependencies
```
python3 -m venv venv
. venv/bin/activate
pip install flask flask-wtf wtforms requests
```

3. Run the app
```
export FLASK_APP=add_device_webapp.py
flask run --host=0.0.0.0
```

![alt text](https://raw.githubusercontent.com/nathanwiens/meraki-add-device-webapp/master/webapp.png)
