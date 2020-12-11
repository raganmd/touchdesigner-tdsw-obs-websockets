import json
obs = mod.obsEXT.obs

class obsActions(obs):

	def __init__(self, myOp):
		obs.__init__(self, myOp)
		self.MyOp = myOp

	def FuncMap(self, targetFunc):
		funcMap = {
			'Updatewidget' : {
				'func' : parent.tool.SimpleObsRequest, 
				'info' : {
					'request-type' : 'GetSceneList'
				}
			},
			'Updatetransitions' : {
				'func' : parent.tool.SimpleObsRequest, 
				'info' : {
					'request-type' : 'GetTransitionList'
				}
			},
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
				'info'	: {}
			},
			'Transitions' : {
				'func' 	: parent.tool.ChangeTransition,
				'info'	: {}
			}
		}
		return funcMap.get(targetFunc)

	def ParCalls(self, **kwargs):
		par = kwargs.get('par')
		target = self.FuncMap(par.name)

		if target == None:
			if self.obsParLookup.get(par.name) != None:
				parent.tool.AudioUpdate(parName= par.name, 
										val=par.eval())
			else:
				pass

		else:
			try:
				func = target.get('func')
				info = target.get('info')
				func(par=par.eval(), info=info)

			except AssertionError as TDErr:
				print(TDErr)
				print("This Parameter does not have a function")
				pass


	def ParseMsg(self, message):
		msgDict = json.loads(message)
		if msgDict.get('scenes'):
			parent.tool.RebuildPars(msgDict.get('scenes'))
		elif msgDict.get('transitions'):
			parent.tool.RebuildTransitions(msgDict.get('transitions'))
