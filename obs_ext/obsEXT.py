import json

class obs:

	deviceTypeMap = {
		'wasapi_input_capture' 	: 'audio',
		'wasapi_output_capture' : 'audio'
	}
	def __init__(self, myOp):
		self.MyOp 					= myOp
		self.websocket 				= myOp.op('websocket_obs')
		self.SceneLabels 			= [] 
		self.SceneNames 			= []
		self.msgId 					= 0
		self.getScenesRequest		= False
		self.obsSceneLookup 		= {}
		self.obsTransitionsLookup 	= {}
		self.obsParLookup 			= {}
		self.setReady(False)
		pass


	################################################################
	## COMP Methods
	################################################################
	
	def setReady(self, state):
		self.MyOp.par['Ready'] = state

	def removeOldPars(self):
		keepPages = ['Websocket Config', 'OBS']
		for eachPage in self.MyOp.customPages:
			if eachPage not in keepPages:
				eachPage.destroy()

	def legalParName(self, nameString):
		newName = nameString.replace(" ", "").lower().capitalize()
		return newName

	def addSceneToLookup(self, **kwargs):
		obsName = kwargs.get('obsName')

	def addParToLookup(self, **kwargs):
		targetLookup 	= kwargs.get('targetLookup')
		tdName 			= kwargs.get('tdName')
		obsName 		= kwargs.get('obsName')
		targetLookup[tdName] = obsName

	def buildPage(self, **kwargs):
		pageName = kwargs.get('pageName')
		newPage = self.MyOp.appendCustomPage(pageName)
		return newPage

	def buildAudioPars(self, **kwargs):
		page 	= kwargs.get('page')
		newPars = kwargs.get('newPars')
		print(newPars)

		for tdName, obsName in newPars.items():
			page.appendFloat(tdName, label=obsName)
			pass

		pass

	def buildPars(self, **kwargs):
		# destroy all custom pars
		self.removeOldPars()

		audioPage = self.buildPage(pageName='Audio')

		# build audio pars
		self.buildAudioPars(page=audioPage, newPars=self.obsParLookup)
		pass

	def UpdateWidget(self, **kwargs):
		self.GetScenes()
		pass

	def RebuildPars(self, scenes):
		# loop through the list of scenes

		for eachScene in scenes:
			sceneName 	= eachScene.get('name')
			tdLegalName = self.legalParName(sceneName)
			self.addParToLookup(obsName=sceneName,
								tdName=tdLegalName,
								targetLookup=self.obsSceneLookup)
			
			# loop through each key and val in each scene dict
			for eachSceneInfoKey, eachSceneInfoVal in eachScene.items():
				#print(eachSceneInfoKey)

				# loop through sources:
				if eachSceneInfoKey == 'sources':

					# loop through list of sources
					for eachSource in eachSceneInfoVal:

						# loop through each key and val in each source dict
						for eachSourceKey, eachSourceVal in eachSource.items():

							# match audio types
							if eachSourceKey == 'type':
								sourceType = obs.deviceTypeMap.get(eachSourceVal)

								# if there's a valid audio source, create a new page
								if sourceType == 'audio':
									sourceName = eachSource.get('name')
									parName = self.legalParName(sourceName)
									self.addParToLookup(obsName=sourceName, 
														tdName=parName,
														targetLookup=self.obsParLookup)

		self.buildPars()
		self.updateScenesPar()
		self.setReady(True)
		pass

	def RebuildTransitions(self, transitions):
		self.obsTransitionsLookup = transitions
		self.updateTransitionsPar()
		pass

	def updateTransitionsPar(self):

		obsTransitions = [each.get('name') for each in self.obsTransitionsLookup]

		self.MyOp.par.Transitions.menuLabels 	= obsTransitions
		self.MyOp.par.Transitions.menuNames		= obsTransitions
		pass

	def updateScenesPar(self):
		
		labels 	= []
		names 	= []

		for tdName, obsName in self.obsSceneLookup.items():
			labels.append(tdName)
			names.append(obsName)

		self.MyOp.par.Scenes.menuLabels 	= labels
		self.MyOp.par.Scenes.menuNames		= names
		pass


	################################################################
	## Message Methods
	################################################################	
	
	def updateMsgId(self):
		self.msgId += 1
		return str(self.msgId)

	def SimpleObsRequest(self, **kwargs):
		requestType = kwargs.get('info').get('request-type')
		msgId 		= self.updateMsgId()

		msg = {
			'request-type' 		: requestType,
			'message-id' 		: msgId		
		}

		self.SendRequest( msg )		
		pass
	
	def StartStopRequest(self, **kwargs):
		parVal = kwargs.get('par')

		if parVal:
			infoDict = kwargs.get('info').get('parTrue')
		else:
			infoDict = kwargs.get('info').get('parFalse')

		print(infoDict)
		self.SimpleObsRequest(info=infoDict)

	def ChangeTransition(self, **kwargs):

		requestType 	= 'SetCurrentTransition'
		transitionName 	= kwargs.get('par')
		msgId 			= self.updateMsgId()

		msg = {
			'request-type' 		: requestType,
			'message-id' 		: msgId, 
			'transition-name' 	: transitionName
		}

		self.SendRequest(msg) 
		pass


	def ChangeScene(self, **kwargs):

		requestType = 'SetCurrentScene'
		sceneName 	= kwargs.get('par')
		msgId 		= self.updateMsgId()

		msg = {
			'request-type' 		: requestType,
			'message-id' 		: msgId, 
			'scene-name' 		: sceneName
		}

		self.SendRequest(msg) 
		pass

	def SendRequest(self, payload):
		jsonPayload = json.dumps(payload)
		self.websocket.sendText(jsonPayload)
		print(jsonPayload)
		pass


	def AudioUpdate(self, **kwargs):
		target 	= kwargs.get('parName')
		val 	= kwargs.get('val')
		obsName = self.obsParLookup.get(target)

		requestType = 'SetVolume'
		source 		= obsName
		msgId 		= self.updateMsgId()

		msg = {
			'request-type' 		: requestType,
			'source'			: source,
			'message-id' 		: msgId, 
			'volume' 			: val,
			'useDecibel'		: False
		}
		
		self.SendRequest(msg) 
		pass






