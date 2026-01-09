

def changed(parent, index): # index is the combobox index
	drive_tw = int(parent.sender().objectName()[-1])
	#print(drive_tw)
	main_tw_tab = drive_tw + 3
	if parent.sender().currentData():
		board = parent.sender().currentData()

		# FIXME might be better to match the board name and board would be false if not selected
		match board:
			case '7i76':
				# 5 step/dir, 32 inputs, 16 outputs, 1 pot spindle, 1 encoder
				#print('7i76 selected')
				set_drives(parent, 5, main_tw_tab, drive_tw, board)
				set_io(parent, drive_tw, 32, True, False, 16, True, False)
				setattr(parent, f'board_{drive_tw}_type', 'stepper')
				setattr(parent, f'board_{drive_tw}_hal_name', '7i76')
			case '7i77':
				# 6 analog, 32 inputs, 16 outputs, 1 pot spindle, 1 encoder
				#print('7i77 selected')
				set_drives(parent, 6, main_tw_tab, drive_tw, board)
				set_io(parent, drive_tw, 32, True, False, 16, True, False)
				setattr(parent, f'board_{drive_tw}_type', 'servo')
				setattr(parent, f'board_{drive_tw}_hal_name', '7i77')
			case '7i78':
				# 4 step/dir, 0 inputs, 0 outputs, 1 encoder, 1 spindle pot
				#print('7i78 selected')
				set_drives(parent, 4, main_tw_tab, drive_tw, board)
				set_io(parent, drive_tw, 0, False, False, 0, False, False)
				setattr(parent, f'board_{drive_tw}_type', 'stepper')
				setattr(parent, f'board_{drive_tw}_hal_name', '7i78')
			case '7i85': # 7i85 FIXME add set_io
				#print('7i85 selected')
				set_drives(parent, 5, main_tw_tab, drive_tw, board) # FIXME dunno what this board has
				setattr(parent, f'board_{drive_tw}_type', 'mother')
				setattr(parent, f'board_{drive_tw}_hal_name', '7i85')
			case '7i85s': # 7i85S FIXME add set_io
				# 4 step/dir, 0 inputs, 0 outputs, 4 encoders
				#print('7i85S selected')
				set_drives(parent, 5, main_tw_tab, drive_tw, board)
				setattr(parent, f'board_{drive_tw}_type', 'stepper')
				setattr(parent, f'board_{drive_tw}_hal_name', '7i85s')
	else: # no board selected
		setattr(parent, f'board_{drive_tw}_type', None)
		setattr(parent, f'board_{drive_tw}_hal_name', None)
		parent.main_tw.setTabVisible(main_tw_tab, False)
		parent.main_tw.setTabText(main_tw_tab, '')

def set_drives(parent, drives, main_tw_tab, drive_tw, board):
	parent.main_tw.setTabVisible(main_tw_tab, True)
	parent.main_tw.setTabText(main_tw_tab, board)

	for i in range(1, 7):
		getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(i, False)
	if drives > 0:
		for i in range(1, drives + 1):
			getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(i, True)

def set_io(parent, drive_tw, inputs, i_invert, i_debounce, outputs, o_invert, o_dir):
	# index, io, inputs, input invert, input debounce, outputs, output invert
	# first thing set all I/O to disabled
	for i in range(32):
		getattr(parent, f'c{drive_tw}_input_{i}').setEnabled(False)
		getattr(parent, f'c{drive_tw}_input_invert_{i}').setEnabled(False)
		getattr(parent, f'c{drive_tw}_input_debounce_{i}').setEnabled(False)
	for i in range(16):
		getattr(parent, f'c{drive_tw}_output_{i}').setEnabled(False)
		getattr(parent, f'c{drive_tw}_output_invert_{i}').setEnabled(False)
		getattr(parent, f'c{drive_tw}_output_type_{i}').setEnabled(False)

	if inputs:
		getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(7, True)
		for i in range(inputs):
			getattr(parent, f'c{drive_tw}_input_{i}').setEnabled(True)
			getattr(parent, f'c{drive_tw}_input_invert_{i}').setEnabled(i_invert)
			getattr(parent, f'c{drive_tw}_input_debounce_{i}').setEnabled(i_debounce)
	else:
		getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(7, False)
	if outputs:
		getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(8, True)
		for i in range(outputs):
			getattr(parent, f'c{drive_tw}_output_{i}').setEnabled(True)
			getattr(parent, f'c{drive_tw}_output_invert_{i}').setEnabled(o_invert)
			getattr(parent, f'c{drive_tw}_output_type_{i}').setEnabled(o_dir)
	else:
		getattr(parent, f'c{drive_tw}_board_tw').setTabVisible(8, False)



