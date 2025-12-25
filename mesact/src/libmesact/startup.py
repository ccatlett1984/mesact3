import os

from libmesact import openini

def hide(parent):
	# set main tab visibility
	parent.main_tw.setTabVisible(3, False)
	parent.main_tw.setTabVisible(4, False)
	parent.main_tw.setTabVisible(5, False)
	parent.main_tw.setTabVisible(6, False)

def load(parent):
	if parent.settings.contains('STARTUP/config'):
		if parent.settings.value('STARTUP/config', False, type=bool):
			config_file = parent.settings.value('STARTUP/config')
			if os.path.isfile(config_file):
				openini.load_ini(parent, config_file)



