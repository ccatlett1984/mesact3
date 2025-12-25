


def build(parent):

	if parent.load_config_cb.isChecked():
		parent.settings.setValue('STARTUP/config', iniFile)
	else:
		parent.settings.setValue('STARTUP/config', False)



