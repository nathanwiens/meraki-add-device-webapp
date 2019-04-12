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

import merakiapi, config
from flask import Flask, render_template, redirect, flash, Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, validators

#CHANGE THESE TO MATCH DESIRED MERAKI ORGANIZATION
apikey = config.apikey
organizationid = config.organizationid

#BUILD FORM FIELDS AND POPULATE DROPDOWN 
class AddProvisionForm(FlaskForm):
    #ADDRESS FIELD
    addressField = TextAreaField('Street Address:&nbsp;&nbsp;', [validators.Optional(), validators.length(max=200)])
    
    #SERIAL NUMBER FIELDS
    serialField1 = StringField('Serial Number 1*:&nbsp;', [validators.InputRequired(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField2 = StringField('Serial Number 2:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField3 = StringField('Serial Number 3:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField4 = StringField('Serial Number 4:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField5 = StringField('Serial Number 5:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField6 = StringField('Serial Number 6:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField7 = StringField('Serial Number 7:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField8 = StringField('Serial Number 8:&nbsp;&nbsp;')
        
    nameField1 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField2 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField3 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField4 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField5 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField6 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField7 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField8 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    
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
    cleannetworks.insert(0, [None, '* Choose...'])
    networkField = SelectField(u'Network Name', choices = cleannetworks)

class CreateProvisionForm(FlaskForm):
    #ADDRESS FIELD
    addressField = TextAreaField('Street Address:&nbsp;&nbsp;', [validators.Optional(), validators.length(max=200)])

    #NETWORK CREATE FIELD
    networkTextField = StringField('New Network Name*', [validators.InputRequired()])
    
    #TEMPLATE DROPDOWN
    templates = merakiapi.gettemplates(apikey, organizationid)
    cleantemplates = []
    for template in templates:
        for key, value in template.items():
            if key == 'id':
                template_id = value
            elif key == 'name':
                template_name = value
            else:
                continue
        cleantemplates.append([template_id,template_name])
    cleantemplates.sort(key=lambda x:x[1])
    cleantemplates.insert(0, ["", '* No Template'])
    templateField = SelectField(u'Template to bind to*', choices = cleantemplates)

    #SERIAL NUMBER FIELDS
    serialField1 = StringField('Serial Number 1*:&nbsp;', [validators.InputRequired(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField2 = StringField('Serial Number 2:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField3 = StringField('Serial Number 3:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField4 = StringField('Serial Number 4:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField5 = StringField('Serial Number 5:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField6 = StringField('Serial Number 6:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField7 = StringField('Serial Number 7:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField8 = StringField('Serial Number 8:&nbsp;&nbsp;')
    
    nameField1 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField2 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField3 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField4 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField5 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField6 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField7 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField8 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    
    submitField = SubmitField('Submit')

class ReplaceDevice(FlaskForm):
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
    cleannetworks.insert(0, [None, '* Choose...'])
    networkField = SelectField(u'Network Name', choices = cleannetworks)
	
	#SERIAL NUMBER FIELDS
    oldMX = StringField('MX to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newMX = StringField('New MX:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    oldSwitch = StringField('Switch to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newSwitch = StringField('New Switch:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    oldAP = StringField('AP to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newAP = StringField('New AP:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    submitField = SubmitField('Submit')

#MAIN PROGRAM
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ikarem123'

@app.route('/', methods=['GET', 'POST'])
def provision():
    form = AddProvisionForm()
    if form.validate_on_submit():
        message = []
        postSerials = []
        postNames = []
        
        postNetwork = form.networkField.data
        print(postNetwork)
        
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
        
        postNames.append(form.nameField1.data)
        postNames.append(form.nameField2.data)
        postNames.append(form.nameField3.data)
        postNames.append(form.nameField4.data)
        postNames.append(form.nameField5.data)
        postNames.append(form.nameField6.data)
        postNames.append(form.nameField7.data)
        postNames.append(form.nameField8.data)
        #print(postSerials)
        
        for i,serial in enumerate(postSerials):
            #SKIP EMPTY SERIAL NUMBER TEXT BOXES
            if serial is '':
                continue
            #EASTER EGG
            elif "ILOVEMERAKI" in serial:
                message = Markup("<img src='/static/meraki.png' />")
            else:
                result = merakiapi.adddevtonet(apikey, postNetwork, serial)
                if result == None:
                    #SET ADDRESS AND NAME
                    merakiapi.updatedevice(apikey, postNetwork, serial, name=postNames[i], address=form.addressField.data, move='true')
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
    
@app.route('/createnetwork', methods=['GET', 'POST'])
def provisionNetwork():
    form = CreateProvisionForm()
    if form.validate_on_submit():
        message = []
        postSerials = []
        postNames = []
        
        postNetwork = form.networkTextField.data
        #print(postNetwork)
        
        postTemplate = form.templateField.data
        
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
        
        postNames.append(form.nameField1.data)
        postNames.append(form.nameField2.data)
        postNames.append(form.nameField3.data)
        postNames.append(form.nameField4.data)
        postNames.append(form.nameField5.data)
        postNames.append(form.nameField6.data)
        postNames.append(form.nameField7.data)
        postNames.append(form.nameField8.data)

        #CREATE NETWORK AND BIND TO TEMPLATE
        result = merakiapi.addnetwork(apikey, organizationid, postNetwork, "appliance switch wireless", "", "America/Los_Angeles")
        
        #GET NEW NETWORK ID
        networks = merakiapi.getnetworklist(apikey, organizationid)
        for network in networks:
            if network['name'] == postNetwork:
                newnetwork = network['id']
                break;
        message = Markup("New Network created: <strong>{}</strong> with ID: <strong>{}</strong>".format(postNetwork, newnetwork))
        flash(message)
        
        #BIND TO TEMPLATE
        if form.templateField.data is not "":
            bindresult = merakiapi.bindtotemplate(apikey, newnetwork, postTemplate)
            message = Markup("Network: <strong>{}</strong> bound to Template: <strong>{}</strong>".format(postNetwork, postTemplate))
            flash(message)

        #ADD SERIALS TO NETWORK
        for i,serial in enumerate(postSerials):
            #SKIP EMPTY SERIAL NUMBER TEXT BOXES
            if serial is '':
                continue
            #EASTER EGG
            elif "ILOVEMERAKI" in serial:
                message = Markup("<img src='/static/meraki.png' />")
            else:
                result = merakiapi.adddevtonet(apikey, newnetwork, serial)
                if result == None:
                    #SET ADDRESS AND NAME
                    merakiapi.updatedevice(apikey, newnetwork, serial, name=postNames[i], address=form.addressField.data, move='true')
                    #API RETURNS EMPTY ON SUCCESS, POPULATE SUCCESS MESSAGE MANUALLY
                    netname = merakiapi.getnetworkdetail(apikey, newnetwork)
                    message = Markup('Device with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(serial, netname['name']))
                #404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
                elif result == 'noserial':
                    message = Markup('Invalid serial <strong>{}</strong>'.format(serial))
                else:
                    message = result
            #SEND MESSAGE TO SUBMIT PAGE
            flash(message)
        return redirect('/submit')
    return render_template('indextemplate.html', title='Meraki Device Provisioning', form=form)

@app.route('/replace', methods=['GET', 'POST'])
def replaceForm():
    form = ReplaceDevice()
    if form.validate_on_submit():
        message = []
        
        postNetwork = form.networkField.data
        netname = merakiapi.getnetworkdetail(apikey, postNetwork)
        oldMX = form.oldMX.data
        newMX = form.newMX.data
        oldSwitch = form.oldSwitch.data
        newSwitch = form.newSwitch.data
        oldAP = form.oldAP.data
        newAP = form.newAP.data
        
        if oldMX is not '':
            oldconfig = merakiapi.getdevicedetail(apikey, postNetwork, oldMX)
            merakiapi.updatedevice(apikey, postNetwork, newMX, name=oldconfig['name'], tags=oldconfig['tags'], lat=oldconfig['lat'],
                 lng=oldconfig['lng'], address=oldconfig['address'], move='true')
            result = merakiapi.removedevfromnet(apikey, postNetwork, oldMX)
            if result == None:
                message = Markup('MX with serial <strong>{}</strong> successfully deleted from Network: <strong>{}</strong>'.format(oldMX, netname['name']))
            merakiapi.claim(apikey, organizationid, serial=newMX)
            result = merakiapi.adddevtonet(apikey, postNetwork, newMX)
            if result == None:
                message = Markup('MX with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(newMX, netname['name']))
        
        if oldSwitch is not '':
            #ADD NEW SWITCH TO NETWORK
            merakiapi.claim(apikey, organizationid, serial=newSwitch)
            result = merakiapi.adddevtonet(apikey, postNetwork, newSwitch)
            oldconfig = merakiapi.getdevicedetail(apikey, postNetwork, oldSwitch)
            merakiapi.updatedevice(apikey, postNetwork, newSwitch, name=oldconfig['name'], tags=oldconfig['tags'], lat=oldconfig['lat'],
                 lng=oldconfig['lng'], address=oldconfig['address'], move='true')
            if result == None:
                message = Markup('Switch with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(newSwitch, netname['name']))
                #CLONE L2 PORT CONFIGS
                if '24' in oldconfig['model']:
                    numports = 30
                elif '48' in oldconfig['model']:
                    numports = 54
                elif '16' in oldconfig['model']:
                    numports = 22
                elif '32' in oldconfig['model']:
                    numports = 38
                for port in range(1, numports):
                    config = merakiapi.getswitchportdetail(apikey, oldSwitch, port)
                    print(config)
                    # Clone corresponding new switch
                    # Tags needed to be input as a list
                    #if config['tags'] is not '':
                    #    tags = config['tags'].split()
                    #else:
                    tags = []

					# Access type port
                    if config['type'] == 'access':
                        merakiapi.updateswitchport(apikey, newSwitch, port,
                            name=config['name'], tags=tags, enabled=config['enabled'],
                            porttype=config['type'], vlan=config['vlan'], voicevlan=config['voiceVlan'],
                            poe='true', isolation=config['isolationEnabled'], rstp=config['rstpEnabled'],
                            stpguard=config['stpGuard'], accesspolicynum=config['accessPolicyNumber'])
					# Trunk type port
                    elif config['type'] == 'trunk':
                        merakiapi.updateswitchport(apikey, newSwitch, port,
                            name=config['name'], tags=tags, enabled=config['enabled'],
                            porttype=config['type'], vlan=config['vlan'], allowedvlans=config['allowedVlans'],
                            poe='true', isolation=config['isolationEnabled'], rstp=config['rstpEnabled'],
                            stpguard=config['stpGuard'])
            #404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
            elif result == 'noserial':
                message = Markup('Invalid serial <strong>{}</strong>'.format(serial))
            else:
                message = result
            #REMOVE OLD SWITCH FROM NETWORK
            merakiapi.removedevfromnet(apikey, postNetwork, oldSwitch)
        
        if oldAP is not '':
            oldconfig = merakiapi.getdevicedetail(apikey, postNetwork, oldAP)
            merakiapi.updatedevice(apikey, postNetwork, newAP, name=oldconfig['name'], tags=oldconfig['tags'], lat=oldconfig['lat'],
                 lng=oldconfig['lng'], address=oldconfig['address'], move='true')
            result = merakiapi.removedevfromnet(apikey, postNetwork, oldAP)
            if result == None:
                message = Markup('AP with serial <strong>{}</strong> successfully deleted from Network: <strong>{}</strong>'.format(oldMX, netname['name']))
            merakiapi.claim(apikey, organizationid, serial=newAP)
            result = merakiapi.adddevtonet(apikey, postNetwork, newAP)
            if result == None:
                message = Markup('AP with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(newMX, netname['name']))

        #SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('replace.html', title='Meraki Device Provisioning', form=form)

@app.route('/submit')
def submit():
   return render_template('submit.html')