from Tkinter import *
from os import environ as env
import tkMessageBox
import Tkinter
import keystoneclient.v2_0.client as ksclient
from glanceclient import Client as glclient
import novaclient.v1_1.client as nvclient

from utils import *
import json
import sys
import os

class SampleApp():
	    
	def __init__(self,**kwargs):
		
		self.root = Tk()
		self.root.title('Flyway')
		self.frame = Frame(self.root)

		self.pan = PanedWindow(self.root, orient=HORIZONTAL)
		self.pan.config(width=1000,height=400)
		self.pan.pack(fill=BOTH, expand=1)
	
		'''
		ksCredentials = {'auth_url':kwargs['auth_url'],
				 'username':kwargs['username'],
				 'password':kwargs['password'],
				 'tenant_name':kwargs['tenant_name']}

		nvCredentials = {'auth_url':kwargs['auth_url'],
				 'username':kwargs['username'],
				 'api_key':kwargs['password'],
				 'project_id':kwargs['tenant_name']}
		'''
		self.getSourceClient()
		self.getTargetClient()

		self.getOriginalResource()
		
		self.sourcePanel()
		self.targetPanel()
		
		self.pan.add(self.m)
		self.pan.add(self.n)

	def sAll(self):
		self.empty1()
		self.s_buttons['All'].config(bg='green')
		
	def tAll(self):
		self.empty2()
		self.t_buttons['All'].config(bg='green')
		
	def sProjectsDisplay(self):
		self.empty1()
		self.s_buttons['Projects'].config(bg='green')
		self.s_currentButton = 'Projects'
		for i, tenant in enumerate(self.s_keystone.tenants.list()):
			name = tenant.name
			self.slb.insert(i+1,name)

		self.slb.bind("<Double-Button-1>", self.AddItem)
		self.slb.pack()
		self.m2.add(self.slb)

		self.slb_res.bind("<Double-Button-1>", self.RemoveItem)
		for i, name in enumerate(self.res_toMigrate[self.s_currentButton]):
			self.slb_res.insert(i+1, name)
		self.slb_res.pack()
		self.m3.add(self.slb_res)
		

	def tProjectsDisplay(self):
		self.empty2()
		self.t_buttons['Projects'].config(bg='green')
		self.t_currentButton = 'Projects'
		for i, tenant in enumerate(self.t_keystone.tenants.list()):
			name = tenant.name
			self.tlb.insert(i+1,name)
		
		for i, name in enumerate(self.newResources[self.t_currentButton]):
			self.tlb_res.insert(i+1, name)

		self.tlb.pack()
		self.n2.add(self.tlb)

		self.tlb_res.pack()
		self.n3.add(self.tlb_res)
		
	def sImagesDisplay(self):
	
		self.empty1()
		self.s_buttons['Images'].config(bg='green')
		self.s_currentButton = 'Images'
		
		for i, image in enumerate(self.s_glance.images.list()):
			name = image.name
			self.slb.insert(i+1,name)
		self.slb.bind("<Double-Button-1>", self.AddItem)
		self.slb.pack()
		self.m2.add(self.slb)

		self.slb_res.bind("<Double-Button-1>", self.RemoveItem)
		for i, name in enumerate(self.res_toMigrate[self.s_currentButton]):
			self.slb_res.insert(i+1, name)
			
		self.slb_res.pack()
		self.m3.add(self.slb_res)

	def tImagesDisplay(self):
		self.empty2()
		self.t_buttons['Images'].config(bg='green')
		self.t_currentButton = 'Images'
		for i, image in enumerate(self.t_glance.images.list()):
			name =image.name
			self.tlb.insert(i+1,name)

		for i, name in enumerate(self.newResources[self.t_currentButton]):
			self.tlb_res.insert(i+1, name)
		
		self.tlb.pack()
		self.n2.add(self.tlb)

		self.tlb_res.pack()
		self.n3.add(self.tlb_res)
			
	def sKeypairsDisplay(self):
		self.empty1()
		self.s_buttons['Keypairs'].config(bg='green')
		self.s_currentButton = 'Keypairs'
		for i, keypair in enumerate(self.s_nova.keypairs.list()):
			name = keypair.name
			self.slb.insert(i+1,name)
		self.slb.bind("<Double-Button-1>", self.AddItem)
		self.slb.pack()
		self.m2.add(self.slb)

		self.slb_res.bind("<Double-Button-1>", self.RemoveItem)
		for i, name in enumerate(self.res_toMigrate[self.s_currentButton]):
			self.slb_res.insert(i+1, name)
		self.slb_res.pack()
		self.m3.add(self.slb_res)

	def tKeypairsDisplay(self):
		self.empty2()
		self.t_buttons['Keypairs'].config(bg='green')
		self.t_currentButton = 'Keypairs'
		for i, keypair in enumerate(self.t_nova.keypairs.list()):
			name = keypair.name
			self.tlb.insert(i+1,name)

		for i, name in enumerate(self.newResources[self.t_currentButton]):
			self.tlb_res.insert(i+1, name)
		
		self.tlb.pack()
		self.n2.add(self.tlb)

		self.tlb_res.pack()
		self.n3.add(self.tlb_res)
		
	def sUsersDisplay(self):
		self.empty1()
		self.s_buttons['Users'].config(bg='green')
		self.s_currentButton = 'Users'
		for i, user in enumerate(self.s_keystone.users.list()):
			name = user.name
			self.slb.insert(i+1,name)
		
		self.slb.bind("<Double-Button-1>", self.AddItem)
		self.slb.pack()
		self.m2.add(self.slb)
	
		self.slb_res.bind("<Double-Button-1>", self.RemoveItem)
		for i, name in enumerate(self.res_toMigrate[self.s_currentButton]):
			self.slb_res.insert(i+1, name)
		self.slb_res.pack()
		self.m3.add(self.slb_res)

	def tUsersDisplay(self):
		self.empty2()
		self.t_buttons['Users'].config(bg='green')
		self.t_currentButton = 'Users'
		for i, user in enumerate(self.t_keystone.users.list()):
			name = user.name
			self.tlb.insert(i+1,name)

		for i, name in enumerate(self.newResources[self.t_currentButton]):
			self.tlb_res.insert(i+1, name)
		
		self.tlb.pack()
		self.n2.add(self.tlb)
	
		self.tlb_res.pack()
		self.n3.add(self.tlb_res)
		
	def sRolesDisplay(self):
		self.empty1()
		self.s_buttons['Roles'].config(bg = 'green')
		self.s_currentButton = 'Roles'
		print 'qsd'

	def tRolesDisplay(self):
		self.empty2()
		self.t_buttons['Roles'].config(bg = 'green')
		print 'qsd'

	def sInstancesDisplay(self):
		self.empty1()
		self.s_buttons['Instances'].config(bg = 'green')
		self.s_currentButton = 'Instances'
		print 'qsd'
	def tInstancesDisplay(self):
		self.empty2()
		self.t_buttons['Instances'].config(bg = 'green')
		print 'qsd'

    	def AddItem(self, event):
		widget = event.widget
		selection=widget.curselection()
		value = widget.get(selection[0])
		#self.slb.delete(selection)
		
		if value not in self.res_toMigrate[self.s_currentButton]:
			self.res_toMigrate[self.s_currentButton].append(value)
			self.slb_res.insert(END, value)
		else: 
			print 'Items selected already in!'
		
		
	def RemoveItem(self, event):
		widget = event.widget
		selection=widget.curselection()
		value = widget.get(selection[0])
		self.slb_res.delete(selection)
		#self.slb.insert(END, value)
		self.res_toMigrate[self.s_currentButton].remove(value)
		
		
	def empty1(self):
		for key in self.s_buttons:
			self.s_buttons[key].config(bg='lightgrey')
		self.slb.delete(0, END)
		self.slb_res.delete(0, END)

	def empty2(self):
		for key in self.t_buttons:
			self.t_buttons[key].config(bg='lightgrey')
		self.tlb.delete(0, END)
		self.tlb_res.delete(0, END)

	def showInputWindow(self):
		self.root.destroy()
		self.inputWindow = InputCredentials()

	def startMigration(self):
		
		print self.res_toMigrate
		
		self.resourceSum = {}
		for name in self.res_toMigrate.keys():
			self.resourceSum[name] = {}
			for element in self.res_toMigrate[name]:
				self.resourceSum[name][element] = self.originalRes[name][element]
		"""
		with open('data.json', "w") as f:
			json.dump(self.resourceSum,f)
		"""
		projects = self.resourceSum['Projects']
		images = self.resourceSum['Images']
		keypairs = self.resourceSum['Keypairs']
		users = self.resourceSum['Users']
		
		self.migrateImages(images)
		self.migrateKeypairs(keypairs)
		self.migrateProjects(projects)
		self.migrateUsers(users)

		self.newResources = self.res_toMigrate 
		
	def getSourceClient(self):
		AUTH_URL = "http://172.16.45.184:5000/v2.0/"
		BYPASS_URL = "http://192.168.33.200:8774/v2/"
		USERNAME = "admin"
		PASSWORD = "openstack"
		PROJECTID = "admin"
		ENDPOINT="http://172.16.45.184:9292"
		
		s_ksCredentials = {'auth_url':AUTH_URL,
				 'username':USERNAME,
				 'password':PASSWORD,
				 'tenant_name':PROJECTID}

		s_nvCredentials = {'auth_url':AUTH_URL,
				 'username':USERNAME,
				 'api_key':PASSWORD,
				 'project_id':PROJECTID}
		
		#Get keystone
		self.s_keystone = ksclient.Client(**s_ksCredentials)

		auth_token = self.s_keystone.auth_ref['token']['id']
		tenant_id = self.s_keystone.auth_ref['token']['tenant']['id']
		print auth_token, tenant_id

		s_glCredentials = {'version':'1',
			         'endpoint':ENDPOINT,
				 'token':auth_token}

		#Get glance
		self.s_glance = glclient(**s_glCredentials)

		#Get nova
		self.s_nova = nvclient.Client(**s_nvCredentials)

	def getTargetClient(self):
		AUTH_URL = "http://172.16.45.183:5000/v2.0/"
		BYPASS_URL = "http://192.168.33.200:8774/v2/"
		USERNAME = "admin"
		PASSWORD = "openstack"
		PROJECTID = "admin"
		ENDPOINT="http://172.16.45.183:9292"
		
		t_ksCredentials = {'auth_url':AUTH_URL,
				 'username':USERNAME,
				 'password':PASSWORD,
				 'tenant_name':PROJECTID}

		t_nvCredentials = {'auth_url':AUTH_URL,
				 'username':USERNAME,
				 'api_key':PASSWORD,
				 'project_id':PROJECTID}
		
		#Get keystone
		self.t_keystone = ksclient.Client(**t_ksCredentials)

		auth_token = self.t_keystone.auth_ref['token']['id']
		tenant_id = self.t_keystone.auth_ref['token']['tenant']['id']
		print auth_token, tenant_id

		t_glCredentials = {'version':'1',
			         'endpoint':ENDPOINT,
				 'token':auth_token}

		#Get glance
		self.t_glance = glclient(**t_glCredentials)

		#Get nova
		self.t_nova = nvclient.Client(**t_nvCredentials)

	def sourcePanel(self):
		self.m = PanedWindow(orient=VERTICAL)
		self.m.config(width=500,height=400)
		self.m.pack(fill=BOTH, expand=1)
		
		self.m0 = PanedWindow(orient=HORIZONTAL)
		self.m0.config(width=450,height=30)
		self.m0.pack(fill=BOTH, expand=1)

		self.m1 = PanedWindow(orient=HORIZONTAL)
		self.m1.config(width=450,height=30)
		self.m1.pack(fill=BOTH, expand=1)

		self.m2 = PanedWindow(orient=VERTICAL)
		self.m2.config(width=200,height=100)
		self.m2.pack(fill=BOTH, expand=1)
		

		self.m3 = PanedWindow(orient=VERTICAL)
		self.m3.pack(fill=BOTH, expand=1)
		

		self.m4 = PanedWindow(orient=HORIZONTAL)
		self.m4.config(width=450,height=30)
		self.m4.pack(fill=BOTH, expand=1)

		for i, text in enumerate(self.buttonTexts):
			self.s_buttons[text] = Button(self.m1, text=text, command=self.s_actions[text])
			self.m1.add(self.s_buttons[text])

		self.slb = Listbox(self.m2)
		self.slb_res = Listbox(self.m3)

		self.sl0 = Label(self.m0, text='Source Cloud:')
		self.sl0.pack()

		self.sl1 = Label(self.m2, text='Resources:')
		self.sl1.pack()
		self.m2.add(self.sl1)

		self.sl2 = Label(self.m3, text='Resources to migration:')
		self.sl2.pack()
		self.start = Button(self.m4, text='Start Migration', bg = 'orange', command=self.startMigration)
		self.start.config(width=40)
		self.start.pack()
		self.sback = Button(self.m4, text='Return', bg = 'yellow', command=self.showInputWindow)
		self.sback.pack()
		self.m4.add(self.start)
		self.m4.add(self.sback)
		self.m3.add(self.m4)
		self.m3.add(self.sl2)
		
		self.m.add(self.m0)
		self.m.add(self.m1)
		self.m.add(self.m2)
		self.m.add(self.m3)

	def targetPanel(self):
		self.n = PanedWindow(orient=VERTICAL)
		self.n.config(width=500,height=400)
		self.n.pack(fill=BOTH, expand=1)
		
		self.n0 = PanedWindow(orient=HORIZONTAL)
		self.n0.config(width=450,height=30)
		self.n0.pack(fill=BOTH, expand=1)

		self.n1 = PanedWindow(orient=HORIZONTAL)
		self.n1.config(width=450,height=30)
		self.n1.pack(fill=BOTH, expand=1)

		self.n2 = PanedWindow(orient=VERTICAL)
		self.n2.config(width=200,height=100)
		self.n2.pack(fill=BOTH, expand=1)
		

		self.n3 = PanedWindow(orient=VERTICAL)
		self.n3.pack(fill=BOTH, expand=1)
		

		self.n4 = PanedWindow(orient=HORIZONTAL)
		self.n4.config(width=450,height=30)
		self.n4.pack(fill=BOTH, expand=1)

		for i, text in enumerate(self.buttonTexts):
			self.t_buttons[text] = Button(self.n1, text=text, command=self.t_actions[text])
			self.n1.add(self.t_buttons[text])

		self.tlb = Listbox(self.n2)
		self.tlb_res = Listbox(self.n3)

		self.tl0 = Label(self.n0, text='Target Cloud:')
		self.tl0.pack()

		self.tl1 = Label(self.n2, text='Resources:')
		self.tl1.pack()
		self.n2.add(self.tl1)

		self.tl2 = Label(self.n3, text='New Resources:')
		self.tl2.pack()
		
		self.tback = Button(self.n4, text='Return', bg = 'yellow', command=self.showInputWindow)
		self.tback.pack()
		
		self.n4.add(self.tback)
		self.n3.add(self.n4)
		self.n3.add(self.tl2)
		
		self.n.add(self.n0)
		self.n.add(self.n1)
		self.n.add(self.n2)
		self.n.add(self.n3)

	def getOriginalResource(self):
		self.s_buttons = {}	   
		self.t_buttons = {}	
		self.buttonTexts = ['All','Projects', 'Images', 'Keypairs', 'Users', 'Roles', 'Instances']
		self.s_actions = {'All':self.sAll,
				  'Projects':self.sProjectsDisplay,
				  'Images':self.sImagesDisplay,
				  'Keypairs':self.sKeypairsDisplay,
				  'Users':self.sUsersDisplay,
				  'Roles':self.sRolesDisplay,
				  'Instances':self.sInstancesDisplay}

		self.t_actions = {'All':self.tAll,
				  'Projects':self.tProjectsDisplay,
				  'Images':self.tImagesDisplay,
				  'Keypairs':self.tKeypairsDisplay,
				  'Users':self.tUsersDisplay,
				  'Roles':self.tRolesDisplay,
				  'Instances':self.tInstancesDisplay}

		self.originalRes = {}
		self.res_toMigrate = {}
		self.newResources = {}
		for text in self.buttonTexts:
			self.res_toMigrate[text] = []
			self.newResources[text] = []
			self.originalRes[text] = {}

		for i, tenant in enumerate(self.s_keystone.tenants.list()):
			self.originalRes['Projects'][tenant.name] = tenant.name
			
		for i, user in enumerate(self.s_keystone.users.list()):
			self.originalRes['Users'][user.name] = {}
			self.originalRes['Users'][user.name]['name'] = user.name 
			self.originalRes['Users'][user.name]['email'] = user.email 

		for i, image in enumerate(self.s_glance.images.list()):
			self.originalRes['Images'][image.name] = {}
			self.originalRes['Images'][image.name]['id'] = image.id
			self.originalRes['Images'][image.name]['name'] = image.name
			self.originalRes['Images'][image.name]['checksum'] = image.checksum

		for i, keypair in enumerate(self.s_nova.keypairs.list()):
			self.originalRes['Keypairs'][keypair.name] = {}
			self.originalRes['Keypairs'][keypair.name]['name'] = keypair.name
			self.originalRes['Keypairs'][keypair.name]['public_key'] = keypair.public_key

	def migrateImages(self, images):
		target_imageChecksums = []
		for target_image in self.t_glance.images.list():
			 target_imageChecksums.append(target_image.checksum)
	
		'''
		Find out whether the source cloud image exist in target cloud
		If not, migrate it to target cloud  
		'''
		path = os.getcwd()
		imagedatadir = path+'/.imagedata/'
		if not os.path.exists(imagedatadir):
			os.makedirs(imagedatadir)
		"""
		with open('data.json', "r") as f:
			self.data = json.load(f)
		"""
		for source_image in images.keys():
			image_id = images[source_image]['id']
			image_checksum = images[source_image]['checksum']
			image_name = images[source_image]['name']
			if image_checksum not in target_imageChecksums:
				
				image_data =self.s_glance.images.data(image=image_id, do_checksum=True)
				with open(imagedatadir+image_id,'wb') as f:
					for i in image_data:
						f.write(i)
			
				image = self.t_glance.images.create(name=image_name,
								    disk_format='qcow2',
								    container_format='bare',
								    is_public='True',
								    checksum=image_checksum,
								    data=open(imagedatadir+image_id,'rb'))
				os.remove(imagedatadir+image_id)

	def migrateKeypairs(self, keypairs):
		target_keypair_pubs = []
		for keypair in self.t_nova.keypairs.list():
			target_keypair_pubs.append(keypair.public_key)
		"""
		with open('data.json', "r") as f:
			self.data = json.load(f)
		"""
		for keypair in keypairs.keys():
			name = keypairs[keypair]['name']
			public_key = keypairs[keypair]['public_key']
			if public_key not in target_keypair_pubs:
				self.t_nova.keypairs.create(name=name, public_key=public_key)

	def migrateProjects(self, projects):
		target_tenantNames = []
		for tenant in self.t_keystone.tenants.list():
			target_tenantNames.append(tenant.name)
		print projects
		
		for source_tenant in projects.keys():
			name = projects[source_tenant]
			if name not in target_tenantNames:
				self.t_keystone.tenants.create(tenant_name=name)
		
	def migrateUsers(self, users):
		target_userNames = {}
		for target_user in self.t_keystone.users.list():
			target_userNames[target_user.name] = target_user.email
		
		for source_user in users.keys(): 
			name = users[source_user]['name']
			email = users[source_user]['email']
			if name not in target_userNames.keys():
				newPassword = generateNewPassword()
				self.t_keystone.users.create(name=name, 
						       	     password=newPassword,
						             email=email)

class InputCredentials():
	    
	def __init__(self, *args, **kwargs):
		
		self.root = Tk()
		self.root.title('Flyway')
		self.frame = Frame(self.root)
		self.m = PanedWindow(self.root,orient=VERTICAL)
		self.m.config(width=800,height=30)
		self.m.pack(fill=BOTH, expand=1)

		AUTH_URL = "http://172.16.45.184:5000/v2.0/"
		BYPASS_URL = "http://192.168.33.200:8774/v2/"
		USERNAME = "admin"
		#api_key
		PASSWORD = "openstack"
		#Tenant_name
		PROJECTID = "admin"
		ENDPOINT="http://172.16.45.184:9292"

		self.texts = {'auth_url': None,
			      'username': None,
			      'password': None,
			      'tenant_name': None,
			      'endpoint': None}
		self.labels1 = []
		self.entries1 = {}
		self.labels2 = []
		self.entries2 = {}

		self.l0 = Label(self.m, text='Source cloud', fg='blue')
		self.l0.pack()
		for text in self.texts:
			self.labels1.append(Label(self.m, text=text))
			self.labels1[-1].pack()
			if text == 'password':
				self.entries1[text] = Entry(self.m, bd = 3, show='*', width = 40)
				self.entries1[text].pack()
			else:
				self.entries1[text] = Entry(self.m, bd = 3, width = 40)
				self.entries1[text].pack()
		
		self.l1 = Label(self.m, text='Target cloud', fg='blue')
		self.l1.pack()
		for text in self.texts:
			self.labels2.append(Label(self.m, text=text))
			self.labels2[-1].pack()
			if text == 'password':
				self.entries2[text] = Entry(self.m, bd = 3, show='*', width = 40)
				self.entries2[text].pack()
			else:
				self.entries2[text] = Entry(self.m, bd = 3, width = 40)
				self.entries2[text].pack()

		self.submit = Button(self.m, text='Submit', bg = 'orange', command=self.showResourceWindow)
		self.submit.pack()
		
	def showResourceWindow(self):
		
		for key in self.texts:
			self.texts[key] = self.entries1[key].get()
		credentials = self.texts
		print credentials
		self.root.destroy()
		SampleApp(**credentials)	

if __name__ == "__main__":
    	
	InputCredentials = InputCredentials()
	InputCredentials.root.mainloop()
	"""import json
	data = {'name':'wang',
		'age':26}
	with open('data.json', 'w') as outfile:
  		json.dump(data, outfile)

	with open('data.json', 'r') as outfile:
  		data = json.load(outfile)
		print data['name']
	"""
