####################################################################################################
# Meraki Device Provisioning Form
# Created by Nathan Wiens (nathan@wiens.co)
#
# MIT License
#
# Copyright (c) 2019 Nathan Wiens
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################################

#INSTALL AND RUN INSTRUCTIONS
#
#Change the 'apikey' and 'organizationid' variables to match your Meraki Organization
#
#python3 -m venv venv
#. venv/bin/activate
#pip install flask flask-wtf wtforms requests
#
#export FLASK_APP=add_device_webapp.py
#flask run --host=0.0.0.0
#

import merakiapi
from flask import Flask, render_template, redirect, flash, Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, validators

#CHANGE THESE TO MATCH DESIRED MERAKI ORGANIZATION
apikey = 'PLEASE_CHANGE_ME'
organizationid = 'CHANGE_ME'

#BUILD FORM FIELDS AND POPULATE DROPDOWN 
class ProvisionForm(FlaskForm):
    #SERIAL NUMBER FIELDS
    serialField1 = StringField('Serial Number 1*:&nbsp;', [validators.DataRequired(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField2 = StringField('Serial Number 2:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField3 = StringField('Serial Number 3:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField4 = StringField('Serial Number 4:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField5 = StringField('Serial Number 5:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField6 = StringField('Serial Number 6:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField7 = StringField('Serial Number 7:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField8 = StringField('Serial Number 8:&nbsp;&nbsp;')
    submitField = SubmitField('Submit')

    #NETWORK DROPDOWN
    networks = merakiapi.getnetworklist(apikey, organizationid)
    cleannetworks = []
    for network in networks:
        for key, value in network.items():
            if key == 'id':
                net_id = value
            elif key == 'name':
                net_name = value
            else:
                continue
        cleannetworks.append([net_id,net_name])
        cleannetworks.sort(key=lambda x:x[1])
    networkField = SelectField(u'Network Name', choices = cleannetworks)

#MAIN PROGRAM
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ikarem123'

@app.route('/', methods=['GET', 'POST'])
def provision():
    form = ProvisionForm()
    if form.validate_on_submit():
        message = []
        postSerials = []
        
        postNetwork = form.networkField.data
        #print(postNetwork)
        
        #BUILD ARRAY OF SERIAL NUMBERS FROM FORM
        postSerials.append(form.serialField1.data)
        postSerials.append(form.serialField2.data)
        postSerials.append(form.serialField3.data)
        postSerials.append(form.serialField4.data)
        postSerials.append(form.serialField5.data)
        postSerials.append(form.serialField6.data)
        postSerials.append(form.serialField7.data)
        postSerials.append(form.serialField8.data)
        postSerials = [element.upper() for element in postSerials]; postSerials
        #print(postSerials)
        
        for serial in postSerials:
            serial.upper()
            #SKIP EMPTY SERIAL NUMBER TEXT BOXES
            if serial is '':
                continue
            #EASTER EGG
            elif "ILOVEMERAKI" in serial:
                message = Markup("<img src='/static/meraki.png' />")
            else:
                result = merakiapi.adddevtonet(apikey, postNetwork, serial)
                if result == None:
                    #API RETURNS EMPTY ON SUCCESS, POPULATE SUCCESS MESSAGE MANUALLY
                    netname = merakiapi.getnetworkdetail(apikey, postNetwork)
                    message = Markup('Device with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(serial, netname['name']))
                #404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
                elif result == 'noserial':
                    message = 'Invalid serial {}'.format(serial)
                else:
                    message = result
            #SEND MESSAGE TO SUBMIT PAGE
            flash(message)
        return redirect('/submit')
    return render_template('index.html', title='Meraki Device Provisioning', form=form)
    
@app.route('/submit')
def submit():
   return render_template('submit.html')