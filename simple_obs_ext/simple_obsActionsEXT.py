import json
obs = mod.obsEXT.obs

class obsActions(obs):

	def __init__(self, myOp):
		obs.__init__(self, myOp)
		self.MyOp = myOp

	def FuncMap(self, targetFunc):
		funcMap = {
			'Stream' : {
				'func' : parent.tool.StartStopRequest,
				'info' : {
					'parTrue' : {
						'request-type' 	: 'StartStreaming'			
					},
					'parFalse' : {
						'request-type' 	: 'StopStreaming'					
					}
				}
			},
			'Record' : {
				'func' : parent.tool.StartStopRequest,
				'info' : {
					'parTrue' : {
						'request-type' 	: 'StartRecording'					
					},
					'parFalse' : {
						'request-type' 	: 'StopRecording'					
					}
				}
			},
			'Scenes' : {
				'func' 	: parent.tool.ChangeScene,
				'info'	: {
					'request-type' : 'SetCurrentScene',

				}
			},
			'Desktopaudio' : {
				'func' 	: parent.tool.AudioUpdate,
				'info'	: {
					'request-type'	: 'SetVolume',
					'source' : 'Desktop Audio'
				}
			},
			'Mic' : {
				'func' 	: parent.tool.AudioUpdate,
				'info'	: {
					'request-type'	: 'SetVolume',
					'source' : 'Mic'
				}
			}
		}
		return funcMap.get(targetFunc)

	def ParMap(self, **kwargs):
		par = kwargs.get('par')
		target = self.FuncMap(par.name)
		
		try:
			func = target.get('func')
			info = target.get('info')
			func(parVal=par.eval(), info=info)

		except Exception as TDErr:
			print(TDErr)
			print("This Parameter does not have a fucntion")
			
		else:	
			pass


	def ParseMsg(self, message):
		msgDict = json.loads(message)
		if msgDict.get('scenes'):
			parent.tool.RebuildPars(msgDict.get('scenes'))
		
		elif msgDict.get('transitions'):
			parent.tool.RebuildTransitions(msgDict.get('transitions'))
