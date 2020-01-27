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
from wtforms import StringField, SelectField, SubmitField, TextAreaField, PasswordField, BooleanField, validators
import datetime
import re, sys

#CHANGE THESE TO MATCH DESIRED MERAKI ORGANIZATION
apikey = config.apikey
organizationid = config.organizationid

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

#TAG DROPDOWN
networks = merakiapi.getnetworklist(apikey, organizationid)
tags = []
tagchoices = []
hubchoices = []
networktypes = ['combined', 'appliance']
for network in networks:
    if ('combined' in network['type']) or ('appliance' in network['type']):
        hubchoices.append([network['id'],network['name']])
    if network['tags'] == '':
        continue
    else:
        temptags = str(network['tags']).split(' ')
        for tag in temptags:
            if (tag.strip() not in tags) and ('None' not in tag.strip()):
                tags.append(tag.strip())
                tagchoices.append([tag.strip(), tag.strip()])

hubchoices.sort(key=lambda x:x[1])
hubchoices.insert(0, ['none', '* Choose...'])

tagchoices.sort(key=lambda x:x[1])

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
    
    networkField = SelectField(u'Network Name', choices = cleannetworks)
    
    submitField = SubmitField('Submit')

class CreateProvisionForm(FlaskForm):
    #ADDRESS FIELD
    addressField = TextAreaField('Street Address:&nbsp;&nbsp;', [validators.Optional(), validators.length(max=200)])

    #NETWORK CREATE FIELD
    networkTextField = StringField('New Network Name*', [validators.InputRequired()])
    
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
    networkField = SelectField(u'Network Name', choices = cleannetworks)
	
	#SERIAL NUMBER FIELDS
    oldMX = StringField('MX to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newMX = StringField('New MX:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    oldSwitch = StringField('Switch to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newSwitch = StringField('New Switch:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    oldAP = StringField('AP to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newAP = StringField('New AP:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14, message='Invalid format. Must be Q2XX-XXXX-XXXX')])
	
    submitField = SubmitField('Submit')
    
class MilesForm(FlaskForm):
    #HTML FIELDS
    queryField = StringField('Query:&nbsp;&nbsp;', [validators.InputRequired()])
    submitField = SubmitField('Submit')
    
class SSIDForm(FlaskForm):

    networkField = SelectField(u'Network Name', choices = cleannetworks)

    #ADDRESS FIELD
    ssidname = StringField('SSID Name:&nbsp;', [validators.Optional()])
    ssidenabled = SelectField('Enabled:&nbsp;', choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')])
    ssidpsk = PasswordField('Pre-Shared Key:&nbsp;', [validators.Optional()])
    ssidvlanid = StringField('VLAN ID:&nbsp;', [validators.Optional()])
    ssidipassignment = SelectField('IP Assignment Mode:&nbsp;', choices=[('Bridge mode', 'Bridge Mode'), ('NAT mode', 'NAT Mode'), ('Layer 3 roaming', 'Layer 3 Roaming')])
    
    submitField = SubmitField('Submit')
    
class PSKForm(FlaskForm):
    networkField = SelectField(u'Network Name', choices = cleannetworks)

    #ADDRESS FIELD
    pskname = StringField('PSK Group Name:&nbsp;', [validators.Optional()])
    pskkey = PasswordField('Key:&nbsp;', [validators.Optional()])
    pskvlanid = StringField('VLAN ID:&nbsp;', [validators.Optional()])
    
    submitField = SubmitField('Submit')
    
class BulkForm(FlaskForm):

    tagField = SelectField(u'Network Tag to Apply Changes to: ', choices = tagchoices)

    #IPS
    setips = BooleanField('IPS:&nbsp')
    ipsmode = SelectField('Mode:&nbsp;', choices=[('disabled', 'Disabled'), ('detection', 'Detection'), ('prevention', 'Prevention')])
    ipsrules = SelectField('Rule Set:&nbsp;', choices=[('connectivity', 'Connectivity'), ('balanced', 'Balanced'), ('security', 'Security')])
    
    #VPN
    setvpn = BooleanField('VPN Hub Config:&nbsp')
    hub1 = SelectField('1:&nbsp;', choices=hubchoices)
    default1 = BooleanField('Default Route?:&nbsp')
    hub2 = SelectField('2:&nbsp;', choices=hubchoices)
    default2 = BooleanField('Default Route?:&nbsp')
    hub3 = SelectField('3:&nbsp;', choices=hubchoices)
    default3 = BooleanField('Default Route?:&nbsp')
    
    #PSK
    setpsk = BooleanField('SSID PSK:&nbsp')
    ssidnum = SelectField('SSID Number:&nbsp;', choices=[('0','1'), ('1','2'), ('2','3'), ('3','4'), ('4','5')])
    ssidpsk = PasswordField('PSK:&nbsp;', [validators.Optional()])
    
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
    
@app.route('/miles', methods=['GET', 'POST'])
def miles():
    form = MilesForm()
    if form.validate_on_submit():

        apikey = 'b085d5d5afd8d448948e1e9b35ee03a6d5db6543'
        organizationid = '209700'

        messages = []
        
        networks = merakiapi.getnetworklist(apikey, organizationid)
        
        query = form.queryField.data.lower()
        
        
        workingquestion = ['how is ', 'how\'s ', 'hows ']
        workingwords = [' working', ' doing', ' operating', ' performing']
        
        for word in workingwords:
            if word in query:
                for question in workingquestion:
                    if question in query:
                        part1 = query.split(question, 1)[1]
                        netordev = part1.split(word, 1)[0]
            
                        for network in networks:
                            if network['name'].lower() == netordev:
                                netname = network['name']
                                netid = network['id']
                        
                                result = merakiapi.getwhconnectionstats(apikey, netid, timespan=86400)
                                messages.append(Markup("In the last day, <strong>{}</strong> had: ".format(netname)))
                                messages.append(Markup("<strong>{}</strong> association failures".format(result['assoc'])))
                                messages.append(Markup("<strong>{}</strong> authentication failures".format(result['auth'])))
                                messages.append(Markup("<strong>{}</strong> DHCP failures".format(result['dhcp'])))
                                messages.append(Markup("<strong>{}</strong> DNS failures".format(result['dns'])))
                                messages.append(Markup("and <strong>{}</strong> successful connections".format(result['success'])))
                                print(messages)
                                continue

        listclients = ['list clients for ', 'client list for ', 'list of clients for ', 'show me clients for', 'show me a list of clients for', 'show clients for ']

        for word in listclients:
            if word in query:
                netordev = query.split(word, 1)[1]
                for network in networks:
                    if network['name'].lower() == netordev:
                        netname = network['name']
                        netid = network['id']
                        clientcount = 0
                        clients = merakiapi.getnetworkclients(apikey, netid, timespan=86400, perpage=100)
                        messages.append(Markup("<table><th colspan=5><h3>Clients for {}</h3></th><tr><td><strong>Description</strong></td><td><strong>MAC Address</strong></td><td><strong>IP Address</strong></td><td><strong>VLAN</strong></td><td><strong>SSID</strong></td></tr>".format(str(netname))))
                        for client in clients:
                            clientcount +=1
                            messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(client['description']), str(client['mac']), str(client['ip']), str(client['vlan']), str(client['ssid']))))
                        messages.append(Markup("<tr><td colspan=5><strong>Total: {}</strong></td></tr>".format(clientcount)))
                        messages.append(Markup("</table>"))
                        continue
                        
        clientevents = ['list client events for ', 'client events for ', 'list events for client ', 'list events for ', 'get client events for ', 'show client events for ']

        for word in clientevents:
            if word in query:
                c = query.split(word, 1)[1]
                r = re.compile('..:..:..:..:..:..')
                netid = "L_584342051651325437"
                clientmac = ""
                if r.match(c) is not None:
                    client = merakiapi.getclientdetail(apikey, netid, c)
                    clientmac = c
                else:
                    clients = merakiapi.getnetworkclients(apikey, netid, timespan=86400, perpage=100)
                    for client in clients:
                        if str(client['description']).lower() == c:
                            print("MATCHED! Client {} is {}".format(str(client['description']), str(client['mac'])))
                            clientmac = client['mac']
                            client = merakiapi.getclientdetail(apikey, netid, clientmac)
                            break
                print("Client: {}".format(clientmac))
                
                lastweek = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
                print(lastweek)
                
                events = merakiapi.getclientevents(apikey, netid, clientmac, lastweek)
                print(events)
                
                messages.append(Markup("<table><th colspan=3><h3>Events for Client {}</h3></th><tr><td><strong>Network Device</strong></td><td><strong>Occurred At</strong></td><td><strong>Event</strong></td></tr>".format(str(client['description']))))
                for event in reversed(events):
                    messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(event['deviceSerial']), datetime.datetime.utcfromtimestamp(event['occurredAt']).strftime('%Y-%m-%d %H:%M:%S'), str(event['type']))))
                messages.append(Markup("</table>"))
                continue
                
        ssidclients = ['how many clients on ssid ', 'list clients on ssid ', 'get clients on ssid ', 'show clients on ssid ', 'list clients for ssid ', 'get clients for ssid ', 'show clients for ssid ']

        for word in ssidclients:
            if word in query:
                ssid = query.split(word, 1)[1]
                netid = "L_584342051651325437"
                clientcount = 0
                clients = merakiapi.getnetworkclients(apikey, netid, timespan=86400, perpage=100)
                
                messages.append(Markup("<table><th colspan=6><h3>Clients for SSID: {}</h3></th><tr><td><strong>Description</strong></td><td><strong>MAC Address</strong></td><td><strong>IP Address</strong></td><td><strong>VLAN</strong></td><td><strong>User</strong></td></tr>".format(str(ssid))))
                for client in clients:
                    if ssid in str(client['ssid']):
                        clientcount +=1
                        messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(client['description']), str(client['mac']), str(client['ip']), str(client['vlan']), str(client['user']))))
                messages.append(Markup("<tr><td colspan=5><strong>Total: {}</strong></td></tr>".format(clientcount)))
                messages.append(Markup("</table>"))
                continue
                
        vlanclients = ['list clients on vlan ', 'get clients on vlan ', 'show clients on vlan ', 'list clients for vlan ', 'get clients for vlan ']

        for word in vlanclients:
            if word in query:
                vlan = query.split(word, 1)[1]
                netid = "L_584342051651325437"
                clientcount = 0
                clients = merakiapi.getnetworkclients(apikey, netid, timespan=86400, perpage=100)
                
                messages.append(Markup("<table><th colspan=5><h3>Clients for VLAN: {}</h3></th><tr><td><strong>Description</strong></td><td><strong>MAC Address</strong></td><td><strong>IP Address</strong></td><td><strong>SSID</strong></td></tr>".format(str(vlan))))
                for client in clients:
                    if vlan in str(client['vlan']):
                        clientcount +=1
                        messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(client['description']), str(client['mac']), str(client['ip']), str(client['ssid']))))
                messages.append(Markup("<tr><td colspan=4><strong>Total: {}</strong></td></tr>".format(clientcount)))
                messages.append(Markup("</table>"))
                continue
                        
        clientdetail = ['tell me about client ', 'tell me about ', 'show client details for ', 'show client ']

        for word in clientdetail:
            if word in query:
                c = query.split(word, 1)[1]
                r = re.compile('..:..:..:..:..:..')
                netid = "L_584342051651325437"
                clientmac = ""
                if r.match(c) is not None:
                    client = merakiapi.getclientdetail(apikey, netid, c)
                    clientmac = c
                else:
                    clients = merakiapi.getnetworkclients(apikey, netid, timespan=86400, perpage=100)
                    for client in clients:
                        if str(client['description']).lower() == c:
                            print("MATCHED! Client {} is {}".format(str(client['description']), str(client['mac'])))
                            clientmac = client['mac']
                            client = merakiapi.getclientdetail(apikey, netid, clientmac)
                            break
                    
                if clientmac is "":
                    print("No matching client found")
                    messages.append(Markup("<h3>No matching client found for: {}</h3>".format(c)))
                else:
                    print("Client: {}".format(c))
    
                    messages.append(Markup("<table><th colspan='6'><h3>Client Details for {}</h3></th><tr><td><strong>Description</strong></td><td><strong>MAC Address</strong></td><td><strong>IP Address</strong></td><td><strong>VLAN</strong></td><td><strong>Manufacturer</strong></td><td><strong>SSID</strong></td></tr>".format(str(client['description']))))
                    messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(client['description']), str(client['mac']), str(client['ip']), client['vlan'], str(client['manufacturer']), str(client['ssid']))))
                    messages.append(Markup("</table>"))
                    
                    apps = merakiapi.getclienttraffichistory(apikey, netid, clientmac)
                    
                    messages.append(Markup("<table><th colspan='3'><h3>Top Applications for {}</h3></th><tr><td><strong>Application</strong></td><td><strong>Sent</strong></td><td><strong>Received</strong></td></tr>".format(str(client['description']))))
                    unique = { each['application'] : each for each in apps }.values()
                    for app in unique:
                        messages.append(Markup("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(app['application']), str(app['sent']), str(app['recv']))))
                    messages.append(Markup("</table>"))
                break
        
    	#SEND MESSAGE TO SUBMIT PAGE
        for message in messages:
            flash(message)
        return redirect('/submit')
    return render_template('miles.html', title='Meraki Miles', form=form)
    
@app.route('/ssid', methods=['GET', 'POST'])
def ssidupdate():
    form = SSIDForm()
    if form.validate_on_submit():
        message = []
        
        ssidnum = '6'
        name = form.ssidname.data
        if form.ssidenabled.data == 'enabled':
            enabled = 'true'
        else:
            enabled = 'false'
        authmode = 'psk'
        encryptionmode = 'wpa'
        if len(form.ssidpsk.data) == 0:
            psk = None
        else:
            psk = form.ssidpsk.data
        ipassignmentmode = form.ssidipassignment.data
        vlan = form.ssidvlanid.data
        
        postNetwork = form.networkField.data
        print(postNetwork)
        
        result = merakiapi.updatessid(apikey, postNetwork, ssidnum, name, enabled, authmode, encryptionmode, ipassignmentmode, psk, vlan, suppressprint=False)
        
        if result == None:
            netname = merakiapi.getnetworkdetail(apikey, postNetwork)
            message = Markup('SSID Successfully updated for Network: <strong>{}</strong>'.format(netname['name']))
        else:
            message = result             

        #SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('ssid.html', title='Meraki SSID Provisioning', form=form)
    
@app.route('/psk', methods=['GET', 'POST'])
def pskgroups():
    form = PSKForm()
    if form.validate_on_submit():   
          
        message = []
        
        ssidnum = '5'
        
        postNetwork = form.networkField.data
        print(postNetwork)
        
        pskname = form.pskname.data
        pskkey = form.pskkey.data
        pskvlanid = form.pskvlanid.data
        
        result = merakiapi.createipskgrouppolicy(apikey, postNetwork, pskvlanid)
        groupPolicyId = result['groupPolicyId']
        
        result = merakiapi.createipsk(apikey, postNetwork, ssidnum, pskname, pskkey, groupPolicyId, suppressprint=False)
        
        netname = merakiapi.getnetworkdetail(apikey, postNetwork)
        message = Markup('PSK successfully created for Network: <strong>{}</strong>. PSK: <strong>{}</strong>, Key: <strong>{}</strong>, VLAN: <strong>{}</strong>'.format(netname['name'], pskname, pskkey, pskvlanid))
        
        #SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('psk.html', title='Meraki PSK Groups', form=form)
    
@app.route('/bulk', methods=['GET', 'POST'])
def bulkupdate():
    form = BulkForm()
    if form.validate_on_submit():
        message = []
        
        allnetworkstochange = []
        mxnetworkstochange = []
        mrnetworkstochange = []
        networks = merakiapi.getnetworklist(apikey, organizationid)
        
        for network in networks:
            mxnetworktypes = ['combined', 'appliance']
            mrnetworktypes = ['combined', 'wireless']
            if (network['tags'] == ''):
                continue
            else:
                temptags = str(network['tags']).split(' ')
                for tag in temptags:
                    if tag.strip() == form.tagField.data:
                        allnetworkstochange.append(network['id'])
                        if any(x in network['type'] for x in mxnetworktypes):
                            mxnetworkstochange.append(network['id'])
                        if any(x in network['type'] for x in mrnetworktypes):
                            mrnetworkstochange.append(network['id'])
                        continue
        
        #SET IPS
        if form.setips.data == True:
            for network in mxnetworkstochange:
                netname = merakiapi.getnetworkdetail(apikey, network)
                print("CHANGING IPS SETTINGS FOR NETWORK: {}".format(netname['name']))
                if form.ipsmode.data == 'disabled':
                    result = merakiapi.updateintrusion(apikey, network, mode=form.ipsmode.data)
                else:
                    result = merakiapi.updateintrusion(apikey, network, mode=form.ipsmode.data, idsRulesets=form.ipsrules.data)
                if result == None:
                    message.append('IPS settings successfully updated for Network: <strong>{}</strong>'.format(netname['name']))
                else:
                    message.append(result) 
        
        ###FINISH VPN            
        if form.setvpn.data == True:
            hubnets = []
            defaults = []
            if 'none' not in form.hub1.data:
                hubnets.append(form.hub1.data)
                defaults.insert(0, form.default1.data)
                if 'none' not in form.hub2.data:
                    hubnets.append(form.hub2.data)
                    defaults.insert(1, form.default2.data)
                    if 'none' not in form.hub3.data:
                        hubnets.append(form.hub3.data)
                        defaultsinsert(2, form.default3.data)
            for network in mxnetworkstochange:
                vpnsettings = merakiapi.getvpnsettings(apikey, network)
                print(vpnsettings)
                if 'subnets' in vpnsettings:
                    merakiapi.updatevpnsettings(apikey, network, mode='spoke', subnets=vpnsettings['subnets'], hubnetworks=hubnets, defaultroute=defaults)
                else:
                    merakiapi.updatevpnsettings(apikey, network, mode='spoke', hubnetworks=hubnets, defaultroute=defaults)
                
        #SET SSID PSK
        if form.setpsk.data == True:
            for network in mrnetworkstochange:
                ssid = merakiapi.getssiddetail(apikey, network, form.ssidnum.data)
                result = merakiapi.updatessid(apikey, network, form.ssidnum.data, ssid['name'], ssid['enabled'], ssid['authMode'], ssid['encryptionMode'], ssid['ipAssignmentMode'], form.ssidpsk.data)
        
                if result == None:
                    message = Markup('SSID Successfully updated for Network: <strong>{}</strong>'.format(network))
                else:
                    message = result             


        #SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('bulk.html', title='Meraki Bulk Changes', form=form)

@app.route('/ml')
def ml():
   return render_template('ml.html')

@app.route('/submit')
def submit():
   return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
