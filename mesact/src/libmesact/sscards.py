
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

from libmesact import menus

def host_changed(parent):
	parent.sserial_host_cb.clear()
	board_list = []
	board_list.append(parent.board_cb.currentData())
	board_list.append(parent.daughter_cb_1.currentData())
	board_list.append(parent.daughter_cb_2.currentData())

	sserial_hosts = ['7c80', '7i76', '7i77', '7i76e', '7i76eu', '7i95', '7i95t',
	'7i96', '7i97', '7i97t']

	if any(item in board_list for item in sserial_hosts):
		parent.sserial_host_cb.addItem('Select', False)
		for board in board_list:
			if board in sserial_hosts:
				parent.sserial_host_cb.addItem(board, board)
	else:
		parent.sserial_host_cb.addItem('N/A')

def host_selected(parent):
	if parent.sserial_host_cb.currentData():
		parent.ss_card_cb.setEnabled(True)
	else:
		parent.ss_card_cb.setEnabled(False)

def card_changed(parent):
	sscards = {
	'Select':'No Card Selected',
	'7i70':'48 Inputs',
	'7i71':'48 Sourcing Outputs',
	'7i72':'48 Sinking Outputs',
	'7i73':'Pendant Card',
	'7i83':'6 Channel Analog Outputs',
	'7i84U':'32 Inputs 16 Outputs',
	'7i87':'8 Analog Inputs',
	'7iAO':'48 Inputs 24, Outputs'
	}

	sspage = {
	'Select': 0,
	'7i70': 1,
	'7i71': 2,
	'7i72': 3,
	'7i73': 4,
	'7i83': 5,
	'7i84U': 6,
	'7i87': 7,
	'7iAO':8
	}
	parent.ss_info.setText(sscards[parent.ss_card_cb.currentText()])
	parent.ss_pages.setCurrentIndex(sspage[parent.ss_card_cb.currentText()])


def ss7i73_changed(parent):
	lcd = False
	keypad = False

	# Keypad

	if not parent.ss7i73_keypad_cb.currentData(): # no keypad
		parent.ss7i73w5w6_lb.setText('W5 Down W6 Down')
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+10}')
		parent.ss7173_key_1_gb.setTitle('Out 0 - 7')
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'In {i+8}')
		parent.ss7173_key_2_gb.setTitle('In 8 - 15')

	elif parent.ss7i73_keypad_cb.currentData() == '4x8': # 4x8 keypad
		parent.ss7i73w5w6_lb.setText('W5 Down W6 Up')
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+6}')
		parent.ss7173_key_1_gb.setTitle('Out 6 - 9')

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'N/A')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		parent.ss7173_key_2_gb.setTitle('N/A')


	elif parent.ss7i73_keypad_cb.currentData() == '8x8': # 8x8 keypad
		parent.ss7i73w5w6_lb.setText('W5 Up W6 Down')
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'N/A')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		parent.ss7173_key_1_gb.setTitle('N/A')
		parent.ss7173_key_2_gb.setTitle('N/A')

	return
	'''
	if parent.ss7i73_keypad_cb.currentData()[0] == 'w5d':
		if parent.ss7i73_keypad_cb.currentData()[1] == 'w6d': # no keypad
			parent.ss7i73w5_lb.setText('W5 Down')
			parent.ss7i73w6_lb.setText('W6 Down')
			keypad = False


		elif parent.ss7i73_keypad_cb.currentData()[1] == 'w6u': # 4x8 keypad
			parent.ss7i73w5_lb.setText('W5 Down')
			parent.ss7i73w6_lb.setText('W6 Up')
			keypad = True
			keys = '4x8'
	elif parent.ss7i73_keypad_cb.currentData()[0] == 'w5u': # 8x8 keypad
			parent.ss7i73w5_lb.setText('W5 Up')
			parent.ss7i73w6_lb.setText('W6 Down')
			keypad = True
			keys = '8x8'

	if parent.ss7i73lcd_cb.currentData() == 'w7d': # no LCD
		parent.ss7i73w7_lb.setText('W7 Down')
		lcd = False
	elif parent.ss7i73lcd_cb.currentData() == 'w7u': # LCD
		parent.ss7i73w7_lb.setText('W7 Up')
		lcd = True

	# No LCD No Keypad
	if not lcd and not keypad:
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		parent.ss7173_key_1_gb.setTitle('Out 0 - 7')
		parent.ss7173_key_2_gb.setTitle('In 8 - 15')
		parent.ss7173_lcd_1_gb.setTitle('Out 2 - 7')
		parent.ss7173_lcd_2_gb.setTitle('Out 8 - 21')

			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.inputs, menu)
			button.setMenu(menu)
		for i in range(8):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+10}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'In {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.inputs, menu)
			button.setMenu(menu)
		for i in range(4):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		parent.ss7173_lcd_1_gb.setTitle('Out 2 - 5')

		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)
		parent.ss7173_lcd_2_gb.setTitle('N/A')

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+6}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menus.add_menu(menus.outputs, menu)
			button.setMenu(menu)
	'''

