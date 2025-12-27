

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
	if parent.board_type == 'eth' and not parent.address_cb.currentData():
		tab_error = True
		config_errors.append('\tAn Ethernet Address must be selected')
	elif parent.board_type == 'spi' and not parent.address_cb.currentData():
		tab_error = True
		config_errors.append('\tA SPI Address must be selected')



	if tab_error:
		config_errors.insert(next_header, 'Machine Tab:')
		next_header = len(config_errors)
		tab_error = False
	# end of Machine Tab


	parent.info_pte.clear()
	parent.main_tw.setCurrentIndex(10)

	if config_errors:
		parent.info_pte.setPlainText('\n'.join(config_errors))
		return False
	else:
		parent.info_pte.setPlainText('Configuration checked OK')
		return True






