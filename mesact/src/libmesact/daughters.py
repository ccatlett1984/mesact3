

def changed(parent, tab, index):
	#print(f'index {index}')
	io = int(parent.sender().objectName()[-1])
	print(io)
	return
	#print(tab)
	#print(parent.sender().currentText())
	match index:
		case 0:
			parent.mainTW.setTabVisible(tab, False)
			parent.mainTW.setTabText(tab, '')
		case 1: # 7i76
			# 5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			print('7i76 selected')
			set_drives(parent, 5, tab)
			set_io(parent, io, 32, True, False, 16, True, False)
		case 2: # 7i77
			# 6 analog 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			print('7i77 selected')
			set_drives(parent, 6, tab)
		case 3: # 7i78
			# 4 step/dir 0 inputs 0 outputs
			print('7i78 selected')
			set_drives(parent, 4, tab)
		case 4: # 7i85
			print('7i85 selected')
			set_drives(parent, 5, tab) # FIXME dunno what this board has
		case 5: # 7i85S
			print('7i85S selected')
			set_drives(parent, 5, tab)

	'''
	else:
		#print(parent.sender().currentText())
		set_drives(parent, 0)
	'''

def set_drives(parent, drives, tab):
	parent.mainTW.setTabVisible(tab, True)
	parent.mainTW.setTabText(tab, parent.sender().currentText())

	for i in range(1, 7):
		getattr(parent, f'joint_tw_{tab}').setTabVisible(i, False)
	if drives > 0:
		for i in range(1, drives + 1):
			getattr(parent, f'joint_tw_{tab}').setTabVisible(i, True)

def set_io(parent, io, inputs, i_invert, i_debounce, outputs, o_invert, o_dir):
	# inputs, input invert, input debounce, outputs, output invert
	# first thing set all to disabled
	for i in range(32):
		getattr(parent, f'c{io}_input_{i}').setEnabled(False)
		getattr(parent, f'c{io}_input_invert_{i}').setVisible(False)
		getattr(parent, f'c{io}_input_debounce_{i}').setVisible(False)
	for i in range(16):
		getattr(parent, f'c{io}_output_{i}').setEnabled(False)
		getattr(parent, f'c{io}_output_invert_{i}').setVisible(False)
		getattr(parent, f'c{io}_output_type_{i}').setVisible(False)

	if inputs:
		parent.joint_tw_3.setTabVisible(7, True)
		for i in range(inputs):
			getattr(parent, f'c{io}_input_{i}').setEnabled(True)
			if i_invert:
				getattr(parent, f'c{io}_input_invert_{i}').setVisible(True)
			if i_debounce:
				getattr(parent, f'c{io}_input_debounce_{i}').setVisible(True)
	else:
		parent.joint_tw_3.setTabVisible(7, False)
	if outputs:
		parent.joint_tw_3.setTabVisible(8, True)
		for i in range(outputs):
			getattr(parent, f'c{io}_output_{i}').setEnabled(True)
			if o_invert:
				getattr(parent, f'c{io}_output_invert_{i}').setVisible(True)
			if o_dir:
				getattr(parent, f'c{io}_output_type_{i}').setVisible(True)
	else:
		parent.joint_tw_3.setTabVisible(8, False)
 # joint_tw_4


