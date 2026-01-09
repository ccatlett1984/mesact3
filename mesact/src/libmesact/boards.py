

from libmesact import utilities
from libmesact import firmware

def changed(parent, index):

	if index > 0: # set common items for all boards
		parent.board_name = parent.board_cb.currentText()
		parent.board_hal_name = parent.board_cb.currentData()
		parent.main_tw.setTabVisible(3, True)
		parent.main_tw.setTabText(3, parent.board_name)
		parent.c0_board_tw.setTabText(0, parent.board_name)
		if parent.mesaflash:
			parent.read_hmid_gb.setEnabled(True)
			firmware.load(parent)

	match index:
		case 0:
			address(parent, None)
			daughter_boards(parent, None , None)
			parent.main_tw.setTabVisible(3, False)
			parent.board_name = None
			parent.board_interface = None
			parent.board_0_type = None
			parent.board_0_hal_name = None
			parent.board_hal_name = None
			parent.mesaflash_name = None

		case 1: # 5i25 2 25 pin expansion ports
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'pci'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '5i25'
			parent.mesaflash_name = '5i25'
			check_mesaflash(parent, (3,4,2))
			info = ('Connector 5v Power\n'
			'W1 Up for P2\n'
			'W2 Up for P3\n'
			'\nDefault Firmware 5i25_g540x2.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 2: # 5i25T 2 25 pin expansion ports
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'pci'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '5i25'
			parent.mesaflash_name = '5i25t'
			check_mesaflash(parent, (3,4,8))
			info = ('Connector 5v Power\n'
			'W1 Up for P1\n'
			'W2 Up for P3\n'
			'\nDefault Firmware 5i25_g540x2.bit\n'
			'\nIf the PC will not boot up with the 5i25T installed\n'
			'disable PCI #SERR generation in the BIOS setup\n'
			'\nDo not write the fallback configuration to a\n'
			'5I25T unless you know _exactly_ what you are doing')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 3: # 6i25 2 25 pin expansion ports
			address(parent, None)
			daughter_boards(parent, 'P2' , 'P3')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'pci'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '5i25'
			parent.mesaflash_name = '5i25'
			check_mesaflash(parent, (3,4,2))
			info = ('Connector 5v Power\n'
			'W1 Up for P2\n'
			'W2 Up for P3\n'
			'\nDefault Firmware 5i25_g540x2.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 4: # 7c80 1 25 pin expansion port
			# 6 step/dir 24 inputs 8 outputs 1 potentiometer spindle 1 encoder
			address(parent, 'spi')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 24, True, True, 8, True, False)
			parent.board_interface = 'spi'
			parent.board_0_type = '' # FIXME
			parent.board_0_hal_name = '7c80'
			parent.mesaflash_name = '7c80'
			check_mesaflash(parent, (3,4,2))
			info = ('7c80 uses SPI for communications.\n'
			'The Rpi 5 requires hm2_spix which is available\nin LinuxCNC version 2.9.4 or newer\n'
			'The Rpi 4 will work with hm2_spix or hm2_spi\nwhich is in older versions of LinuxCNC\n'
			'\nDefault Firmware 7c80d.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 5: # 7c81 3 25 pin expansion ports
			address(parent, 'spi')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'spi'
			parent.board_0_type = '' # FIXME
			parent.board_0_hal_name = '7c81'
			parent.mesaflash_name = '7c81'
			check_mesaflash(parent, (3,4,2))
			info = ('7c81 uses SPI for communications.\n'
				'The Rpi 5 requires hm2_spix which is available in\nLinuxCNC version 2.9.4 or newer\n'
				'The Rpi 4 will work with hm2_spix or hm2_spi\nwhich is in older versions of LinuxCNC'
				'\nDefault Firmware 7c81_g540x2d.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 6: # 7i76E 2 25 pin expansion ports
			#5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 5)
			set_io(parent, 32, True, False, 16, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i76e'
			parent.mesaflash_name = '7i76e'
			check_mesaflash(parent, (3,4,2))
			info = ('Connector 5v Power\n'
			'W7 Up for P1\n'
			'W12 Up for P2\n'
			'\nIP Address\nW2 Down W3 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i76e_7i76x1D.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 7: # 7i76EU 2 25 pin expansion ports
			#5 step/dir 32 inputs 16 outputs 1 potentiometer spindle 1 encoder
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P3')
			set_drives(parent, 5)
			set_io(parent, 32, True, False, 16, True, True)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i76e'
			parent.mesaflash_name = '7i76eu'
			check_mesaflash(parent, (3,5,2))
			info = ('Connector 5v Power\n'
			'W3 Up for P1\n'
			'W15 Up for P2\n'
			'\nIP Address\nW13 Down W14 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i76eu_7i76x1dpl.bin\n'
			'\nOutputs can be Source, Sink or Push Pull\n'
			'Outputs do not require flyback diodes\n'
			'\nTB4 Spindle pins can be ENA & DIR or FWD & REV\n'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 8: # 7i92 2 25 pin expansion ports
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '7i92'
			parent.mesaflash_name = '7i92'
			check_mesaflash(parent, (3,4,2))
			info = ('Connector 5v Power\n'
			'W3 Up for P1\n'
			'W4 Up for P2\n'
			'\nIP Address Settings\n'
			'W5 Down W6 Up for 10.10.10.10\n'
			'Power off before moving jumpers\n'
			'\nDefault firmware 7i92_G540x2D.bit'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 9: # 7i92T 2 25 pin expansion ports
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '7i92'
			parent.mesaflash_name = '7i92t'
			check_mesaflash(parent, (3,4,5))
			info = ('Connector 5v Power\n'
			'W3 Up for P1\n'
			'W4 Up for P2\n'
			'\nIP Address Settings\n'
			'W5 Down W6 Up for 10.10.10.10\n'
			'Power off before moving jumpers\n'
			'\nDefault firmware 7i92t_g540d.bin'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 10: # 7i95 1 25 pin expansion port
			# 6 step/dir, 6 encoders, 24 inputs 6 outputs
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			# inputs invert and slow, output invert
			set_drives(parent, 6)
			set_io(parent, 24, True, True, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i95'
			parent.mesaflash_name = '7i95'
			check_mesaflash(parent, (3,4,2))
			info = ('IP Address Jumpers\nW16 Down W17 Up for 10.10.10.10\n'
			'\nDefault firmware 7i95_d.bit')
			parent.board_info_pte.setPlainText(info)

		case 11: # 7i95T 1 25 pin expansion port
			# 6 step/dir, 6 encoders, 24 inputs 6 outputs
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 24, True, True, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i95'
			parent.mesaflash_name = '7i95t'
			check_mesaflash(parent, (3,4,7))
			info = ('The 7i95T requires LinuxCNC version 2.10 or newer to run\n'
			'\nTo Flash the 7i95T Mesaflash version 3.4.7\nor newer must be installed\n'
			'\nIP Address Jumpers\nW15 Down W16 Up for 10.10.10.10\n'
			'\nDefault firmware 7i95t_d.bin'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 12: # 7i96 1 25 pin expansion port
			# 5 step/dir, 11 inputs 6 outputs
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 5)
			set_io(parent, 11, True, False, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i96'
			parent.mesaflash_name = '7i96'
			check_mesaflash(parent, (3,4,2))
			info = ('Connector 5v Power\n'
			'W8 Up for P1\n'
			'\nIP Address\nW5 Down W6 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i96d.bit\n'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

		case 13: # 7i96S 1 25 pin expansion port
			# 5 step/dir, 11 inputs 6 outputs 1 potentiometer spindle 1 encoder
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 5)
			set_io(parent, 11, True, True, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'stepper'
			parent.board_0_hal_name = '7i96s'
			parent.mesaflash_name = '7i96s'
			check_mesaflash(parent, (3,4,2))
			info = ('Expansion Connector 5v Power W6 Up for P1\n'
			'\nIP Address W4 Down W5 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i96s_d.bit\n'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 14: # 7i97 1 25 pin expansion port
			# 6 analog/encoder 16 inputs 6 outputs
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , None)
			set_drives(parent, 6)
			set_io(parent, 16, True, True, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'servo'
			parent.board_0_hal_name = '7i97'
			parent.mesaflash_name = '7i97'
			check_mesaflash(parent, (3,4,2))
			info = ('Breakout 5v Power W23 Up for P1\n'
			'\nIP Address W16 Down W17 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i97_D.bit\n'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 15: # 7i97T 1 25 pin expansion port
			# 6 analog/encoder 16 inputs 6 outputs
			address(parent, 'ip')
			address(parent, 'ip')
			daughter_boards(parent, 'P2' , None)
			set_drives(parent, 6)
			set_io(parent, 16, True, True, 6, True, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'servo'
			parent.board_0_hal_name = '7i97'
			parent.mesaflash_name = '7i97t'
			check_mesaflash(parent, (3,5,3))
			info = ('The 7i97T requires LinuxCNC version 2.10 or newer to run\n'
			'\nTo Flash the 7i97T Mesaflash version 3.5.3\nor newer must be installed\n'
			'\nIP Address Jumpers\nW11 Down W12 Up for 10.10.10.10\n'
			'\nDefault firmware 7i97t_d.bin\n'
			'\nIMPORTANT! Verify the following before running\n'
			'\nVerify encoders working, scaled right and in the right direction\n'
			'\nVerify drive enables are controlled by linuxcnc\n'
			'\nSet per axis following error limits wide enough to allow tuning (say 1 inch or 25 mm)\n'
			'\nExpect runaways you may have to change the sign of the analog outputs\n'
			)
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, True)

		case 16: # 7i98 3 25 pin expansion ports
			address(parent, 'ip')
			daughter_boards(parent, 'P1' , 'P2')
			set_drives(parent, 0)
			set_io(parent, None, False, False, None, False, False)
			parent.board_interface = 'eth'
			parent.board_0_type = 'mother'
			parent.board_0_hal_name = '' # FIXME
			parent.mesaflash_name = '7i98'
			check_mesaflash(parent, (3,4,2))
			info = ('IP Address W8 Down W9 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i98_g540x3d.bit\n')
			parent.board_info_pte.setPlainText(info)
			parent.main_tw.setTabVisible(6, False)

def check_mesaflash(parent, version):
	if parent.mesaflash_version >= version:
		parent.firmware_gb.setEnabled(True)
		parent.read_hmid_gb.setEnabled(True)
	else:
		parent.firmware_gb.setEnabled(False)
		parent.read_hmid_gb.setEnabled(False)

def address(parent, address_type):
	match address_type:
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
	parent.main_tw.setTabVisible(4, False)
	parent.main_tw.setTabVisible(5, False)

	boards = [
	['Select', None],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	['7i85', '7i85'],
	['7i85S', '7i85s']
	]

	parent.daughter_cb_1.blockSignals(True)
	parent.daughter_cb_2.blockSignals(True)

	parent.daughter_cb_1.clear()
	parent.daughter_lb_1.clear()
	parent.daughter_cb_2.clear()
	parent.daughter_lb_2.clear()

	if port_1:
		parent.daughter_lb_1.setText(port_1)
		for item in boards:
			parent.daughter_cb_1.addItem(item[0], item[1])

		# temp FIXME when daughters are programmed
		parent.daughter_cb_1.model().item(3).setEnabled(False)
		parent.daughter_cb_1.model().item(4).setEnabled(False)
		parent.daughter_cb_1.model().item(5).setEnabled(False)

	if port_2:
		parent.daughter_lb_2.setText(port_2)
		for item in boards:
			parent.daughter_cb_2.addItem(item[0], item[1])

		# temp FIXME when daughters are programmed
		parent.daughter_cb_2.model().item(3).setEnabled(False)
		parent.daughter_cb_2.model().item(4).setEnabled(False)
		parent.daughter_cb_2.model().item(5).setEnabled(False)

	parent.daughter_cb_1.blockSignals(False)
	parent.daughter_cb_2.blockSignals(False)

def set_drives(parent, drives):
	for i in range(1, 7):
		parent.c0_board_tw.setTabVisible(i, False)
	if drives > 0:
		for i in range(1, drives + 1):
			parent.c0_board_tw.setTabVisible(i, True)

def set_io(parent, inputs, i_invert, i_debounce, outputs, o_invert, o_dir):
	# inputs, input invert, input debounce, outputs, output invert
	# first thing set all to disabled
	for i in range(32):
		getattr(parent, f'c0_input_{i}').setEnabled(False)
		getattr(parent, f'c0_input_invert_{i}').setEnabled(False)
		getattr(parent, f'c0_input_debounce_{i}').setEnabled(False)
	for i in range(16):
		getattr(parent, f'c0_output_{i}').setEnabled(False)
		getattr(parent, f'c0_output_invert_{i}').setEnabled(False)
		getattr(parent, f'c0_output_type_{i}').setEnabled(False)

	if inputs:
		parent.c0_board_tw.setTabVisible(7, True)
		for i in range(inputs):
			getattr(parent, f'c0_input_{i}').setEnabled(True)
			getattr(parent, f'c0_input_invert_{i}').setEnabled(i_invert)
			getattr(parent, f'c0_input_debounce_{i}').setEnabled(i_debounce)
	else:
		parent.c0_board_tw.setTabVisible(7, False)
	if outputs:
		parent.c0_board_tw.setTabVisible(8, True)
		for i in range(outputs):
			getattr(parent, f'c0_output_{i}').setEnabled(True)
			getattr(parent, f'c0_output_invert_{i}').setEnabled(o_invert)
			getattr(parent, f'c0_output_type_{i}').setEnabled(o_dir)
	else:
		parent.c0_board_tw.setTabVisible(8, False)




