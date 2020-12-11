import json

class obs:

	def __init__(self, myOp):
		self.MyOp 					= myOp
		self.websocket 				= myOp.op('websocket_obs')
		self.msgId 					= 0
		pass

	################################################################
	## Message Methods
	################################################################	
	
	def updateMsgId(self):
		self.msgId += 1
		return str(self.msgId)

	def SendRequest(self, payload, debug=False):
		jsonPayload = json.dumps(payload)
		self.websocket.sendText(jsonPayload)
		
		if debug:
			print(jsonPayload)
		else:
			pass
		pass
	
	def StartStopRequest(self, **kwargs):
		parVal = kwargs.get('parVal')

		if parVal:
			infoDict = kwargs.get('info').get('parTrue')
		else:
			infoDict = kwargs.get('info').get('parFalse')

		msgId 		= self.updateMsgId()
		requestType = infoDict.get('request-type')

		msg = {
			'request-type' 		: requestType,
			'message-id' 		: msgId		
		}

		self.SendRequest( msg, debug = True)

	def ChangeScene(self, **kwargs):

		requestType = kwargs.get('info').get('request-type')
		sceneName 	= kwargs.get('parVal')
		msgId 		= self.updateMsgId()

		msg = {
			'request-type' 		: requestType,
			'message-id' 		: msgId, 
			'scene-name' 		: sceneName
		}

		self.SendRequest(msg) 
		
		pass

	def AudioUpdate(self, **kwargs):
		val 		= kwargs.get('parVal')
		source 		= kwargs.get('info').get('source')
		requestType = kwargs.get('info').get('request-type')
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

