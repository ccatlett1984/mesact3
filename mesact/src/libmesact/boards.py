

from libmesact import utilities
from libmesact import firmware

def changed(parent, index):

	if index > 0: # set common items for all boards
		parent.board_name = parent.boardCB.currentText()
		parent.board_hal_name = parent.boardCB.currentData()
		parent.mainTW.setTabVisible(3, True)
		parent.mainTW.setTabText(3, parent.board_name)
		parent.joint_tw_3.setTabText(0, parent.board_name)
		if parent.mesaflash:
			parent.read_hmid_gb.setEnabled(True)
			firmware.load(parent)

	match index:
		case 0:
			print('no board selected')
			address(parent, None)
			daughter_boards(parent, None , None)
			parent.mainTW.setTabVisible(3, False)
			parent.board_name = None
			parent.board_hal_name = None
			parent.mesaflash_name = None
		case 1: # 5i25 2 25 pin expansion ports
			print('5i25 selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '5i25'
			parent.mesaflash_version = '3.4.2'
		case 2: # 5i25T 2 25 pin expansion ports
			print('5i25T selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '5i25t'
			# parent.mesaflash_version = 'FIXME'
		case 3: # 6i25 2 25 pin expansion ports
			print('6i25 selected')
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '5i25'
			parent.mesaflash_version = '3.4.2'
		case 4: # 7c80 1 25 pin expansion port
			# 6 step/dir 24 inputs 8 outputs 1 potentiometer spindle 1 encoder
			print('7c80 selected')
			address(parent, 'spi')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 24, False, False, 8, False, False)
			parent.mesaflash_name = '7c80'
			parent.mesaflash_version = '3.4.2'
		case 5: # 7c81 3 25 pin expansion ports
			print('7c81 selected')
			address(parent, 'spi')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '7c81'
			parent.mesaflash_version = '3.4.2'
		case 6: # 7i76E 2 25 pin expansion ports
			#5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			print('7i76E selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 5)
			set_io(parent, 32, True, False, 16, True, False)
			parent.mesaflash_name = '7i76e'
			parent.mesaflash_version = '3.4.2'
		case 7: # 7i76EU 2 25 pin expansion ports
			#5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			print('7i76EU selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P3')
			set_drives(parent, 5)
			set_io(parent, 32, True, False, 16, True, True)
			parent.mesaflash_name = '7i76eu'
			parent.mesaflash_version = '3.5.2'
		case 8: # 7i92 2 25 pin expansion ports
			print('7i92 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '7i92'
			parent.mesaflash_version = '3.4.2'
		case 9: # 7i92T 2 25 pin expansion ports
			print('7i92T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '7i92t'
			parent.mesaflash_version = '3.4.5'
		case 10: # 7i95 1 25 pin expansion port
			# 6 step/dir, 6 encoders, 24 inputs 6 outputs
			print('7i95 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			# FIXME check for invert etc
			set_drives(parent, 6)
			set_io(parent, 24, False, False, 6, False, False)
			parent.mesaflash_name = '7i95'
			parent.mesaflash_version = '3.4.2'
		case 11: # 7i95T 1 25 pin expansion port
			# 6 step/dir, 6 encoders, 24 inputs 6 outputs
			print('7i95T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 24, False, False, 6, False, False)
			parent.mesaflash_name = '7i95t'
			parent.mesaflash_version = '3.4.7'
		case 12: # 7i96 1 25 pin expansion port
			# 5 step/dir, 11 inputs 6 outputs
			print('7i96 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 5)
			set_io(parent, 11, False, False, 6, False, False)
			parent.mesaflash_name = '7i96'
			parent.mesaflash_version = '3.4.2'
		case 13: # 7i96S 1 25 pin expansion port
			# 5 step/dir, 11 inputs 6 outputs 1 potentiometer spindle 1 encoder
			print('7i96S selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 5)
			set_io(parent, 11, False, False, 6, False, False)
			parent.mesaflash_name = '7i96s'
			parent.mesaflash_version = '3.4.2'
		case 14: # 7i97 1 25 pin expansion port
			# 6 analog/encoder 16 inputs 6 outputs
			print('7i97 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 16, False, False, 6, False, False)
			parent.mesaflash_name = '7i97'
			parent.mesaflash_version = '3.4.2'
		case 15: # 7i97T 1 25 pin expansion port
			# 6 analog/encoder 16 inputs 6 outputs
			address(parent, 'ip')
			print('7i97T selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P2' , None)
			set_drives(parent, 6)
			set_io(parent, 16, False, False, 6, False, False)
			parent.mesaflash_name = '7i97t'
		case 16: # 7i98 3 25 pin expansion ports
			print('7i98 selected')
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.mesaflash_name = '7i98'


def address(parent, type):
	match type:
		case 'ip':
			ip_address = [
			['Select', False],
			['10.10.10.10', '10.10.10.10'],
			['192.168.1.121', '192.168.1.121']
			]
			parent.address_cb.clear()
			for item in ip_address:
				parent.address_cb.addItem(item[0], item[1])
			parent.address_cb.setEditable(True)
			parent.address_cb.setEnabled(True)
			parent.address_lb.setText('IP Address')
		case 'spi':
			spi_address = [
			['Select', False],
			['/dev/spidev0.0', '/dev/spidev0.0']]
			parent.address_cb.clear()
			for item in spi_address:
				parent.address_cb.addItem(item[0], item[1])
			parent.address_cb.setEditable(True)
			parent.address_cb.setEnabled(True)
			parent.address_lb.setText('SPI Address')
		case None:
			parent.address_cb.clear()
			parent.address_cb.setEditable(False)
			parent.address_cb.setEnabled(False)
			parent.address_lb.setText('N/A')

def daughter_boards(parent, port_1 , port_2):
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)

	boards = [
	['Select', None],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	['7i85', '7i85'],
	['7i85S', '7i85s']
	]

	parent.daughterCB_1.blockSignals(True)
	parent.daughterCB_2.blockSignals(True)

	parent.daughterCB_1.clear()
	parent.daughterLB_1.clear()
	parent.daughterCB_2.clear()
	parent.daughterLB_2.clear()

	if port_1:
		parent.daughterLB_0.setText(port_1)
		for item in boards:
			parent.daughterCB_1.addItem(item[0], item[1])

	if port_2:
		parent.daughterLB_1.setText(port_2)
		for item in boards:
			parent.daughterCB_2.addItem(item[0], item[1])

	parent.daughterCB_1.blockSignals(False)
	parent.daughterCB_2.blockSignals(False)

def set_drives(parent, drives):
	for i in range(1, 7):
		parent.joint_tw_3.setTabVisible(i, False)
	if drives > 0:
		for i in range(1, drives + 1):
			parent.joint_tw_3.setTabVisible(i, True)

def set_io(parent, inputs, i_invert, i_debounce, outputs, o_invert, o_dir):
	# inputs, input invert, input debounce, outputs, output invert
	# first thing set all to disabled
	for i in range(32):
		getattr(parent, f'c0_input_{i}').setEnabled(False)
		getattr(parent, f'c0_input_invert_{i}').setVisible(False)
		getattr(parent, f'c0_input_debounce_{i}').setVisible(False)
	for i in range(16):
		getattr(parent, f'c0_output_{i}').setEnabled(False)
		getattr(parent, f'c0_output_invert_{i}').setVisible(False)
		getattr(parent, f'c0_output_type_{i}').setVisible(False)

	if inputs:
		parent.joint_tw_3.setTabVisible(7, True)
		for i in range(inputs):
			getattr(parent, f'c0_input_{i}').setEnabled(True)
			if i_invert:
				getattr(parent, f'c0_input_invert_{i}').setVisible(True)
			if i_debounce:
				getattr(parent, f'c0_input_debounce_{i}').setVisible(True)
	else:
		parent.joint_tw_3.setTabVisible(7, False)
	if outputs:
		parent.joint_tw_3.setTabVisible(8, True)
		for i in range(outputs):
			getattr(parent, f'c0_output_{i}').setEnabled(True)
			if o_invert:
				getattr(parent, f'c0_output_invert_{i}').setVisible(True)
			if o_dir:
				getattr(parent, f'c0_output_type_{i}').setVisible(True)
	else:
		parent.joint_tw_3.setTabVisible(8, False)




