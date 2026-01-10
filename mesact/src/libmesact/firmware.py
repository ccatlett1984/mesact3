import os

def load(parent):
	parent.firmware_cb.clear()
	parent.firmware_info_pte.clear()
	if parent.mesaflash_name:
		path = os.path.join(parent.firmware_path, parent.mesaflash_name)
		if os.path.exists(path):
			firmware = ['.bit', '.bin']
			extensions = list(set(os.path.splitext(file)[-1] for file in os.listdir(path)))
			if any(x in firmware for x in extensions):
				files = sorted([entry.path for entry in os.scandir(path) if entry.is_file()])
				parent.firmware_cb.addItem('Select', False)
				for file in files:
					if os.path.splitext(file)[1] in firmware:
						parent.firmware_cb.addItem(os.path.basename(file), file)
				parent.firmware_pte.clear()
				parent.firmware_tw.setCurrentIndex(0)
				if parent.read_hmid_gb.isEnabled(): # set mesaflash tools on if installed
					parent.firmware_gb.setEnabled(True)
		else:
			no_firmware(parent, parent.board_hal_name)
	else:
		no_firmware(parent, parent.board_hal_name)


def no_firmware(parent, board):
	parent.firmware_tw.setCurrentIndex(1)
	msg = (f'No Firmware found for the {board}\n'
	'Downloads > Firmware from the menu if you have an Internet connection\n'
	'The firmware will be to downloaded and installed\n'
	f'in {os.path.expanduser("~")}/.local/lib/libmesact/{board}\n\n'
	'If you do not have an Internet connection\nfrom another computer download from \n'
	f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz\n'
	f'Extract the firmware to {os.path.expanduser("~")}/.local/lib/libmesact/{board}')
	parent.firmware_pte.setPlainText(msg)
	parent.firmware_gb.setEnabled(False)
	parent.firmware_cb.clear()

	if parent.settings.value('NAGS/firmware', None, type=bool):
		msg = (f'No Firmware was found for the {board}.\n'
		'Do you want to download the firmware now?')
		response, no_nag = dialogs.msg_yes_no_check('Firmware', msg, "Don't Check for Firmware Again!")
		if response:
			downloads.downloadFirmware(parent)
		if no_nag:
			parent.settings.setValue('NAGS/firmware', False)
			parent.no_check_firmware_cb.setChecked(False)
		else:
			parent.settings.setValue('NAGS/firmware', True)
			parent.no_check_firmware_cb.setChecked(True)

