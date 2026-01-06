

def check_config(parent):

	config_errors = []
	tab_error = False
	next_header = 0

	# check the Machine Tab for errors
	if not parent.machine_name_le.text():
		tab_error = True
		config_errors.append('\tA configuration name must be entered')
	if not parent.board_cb.currentData():
		tab_error = True
		config_errors.append('\tA Board must be selected')
	else:
		if parent.board_interface == 'eth' and not parent.address_cb.currentData():
			tab_error = True
			config_errors.append('\tAn Ethernet Address must be selected')
		elif parent.board_interface == 'spi' and not parent.address_cb.currentData():
			tab_error = True
			config_errors.append('\tA SPI Address must be selected')

	if tab_error:
		config_errors.insert(next_header, 'Machine Tab:')
		next_header = len(config_errors)
		tab_error = False
	# end of Machine Tab

	# check the Settings Display Tab for errors
	if parent.gui_cb.currentData() == 'axis':
		if parent.max_lin_jog_vel_dsb.value() == 0:
			tab_error = True
			config_errors.append('\tJog Settings requires the Maximum Linear Velocity to be more than 0')

	if parent.gui_cb.currentData() == 'flexgui':
		if parent.flex_gui_le.text() == '':
			tab_error = True
			config_errors.append('\tFlex GUI requires a ui file name to load')

	# check the Settings Jog Settings Tab for errors
	if set(parent.coordinates_lb.text()) & set('XYZUVW'): # linear axes
		if parent.default_lin_jog_vel_dsb.value() <= 0:
			tab_error = True
			config_errors.append('\tJog Settings Tab Default Linear Velocity must be greater than 0')

	if set(parent.coordinates_lb.text()) & set('ABC'): # rotary axes
		if parent.def_ang_jog_vel_dsb.value() <= 0:
			tab_error = True
			config_errors.append('\tJog Settings Tab Default Angular Velocity must be greater than 0')

	if tab_error:
		config_errors.insert(next_header, 'Settings Tab:')
		next_header = len(config_errors)
		tab_error = False
	# end of Settings Tab

	parent.info_pte.clear()
	parent.main_tw.setCurrentIndex(10)

	if config_errors:
		parent.info_pte.setPlainText('\n'.join(config_errors))
		return False
	else:
		parent.info_pte.setPlainText('Configuration checked OK')
		return True






