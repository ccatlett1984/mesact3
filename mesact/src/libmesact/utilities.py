import os, subprocess
from datetime import datetime

from PyQt6.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox, QCheckBox
from PyQt6.QtWidgets import QFileDialog, QLabel

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def new_config(parent):
	# set main tab visibility
	parent.main_tw.setTabVisible(3, False)
	parent.main_tw.setTabVisible(4, False)
	parent.main_tw.setTabVisible(5, False)
	parent.main_tw.setTabVisible(6, False)
	parent.main_tw.setTabVisible(7, False)

	# clear all entries
	for child in parent.findChildren(QLineEdit):
		child.clear()
	for child in parent.findChildren(QComboBox):
		child.setCurrentIndex(0)
	for child in parent.findChildren(QDoubleSpinBox):
		child.setValue(0)
	for child in parent.findChildren(QCheckBox):
		child.setChecked(False)
	parent.servoPeriodSB.setValue(1000000)
	parent.introGraphicLE.setText('emc2.gif')
	parent.main_tw.setCurrentIndex(0)

def select_dir(parent):
	options = QFileDialog.Option.DontUseNativeDialog
	dir_path = False
	file_dialog = QFileDialog()
	print('here')
	file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
	file_dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
	file_dialog.setWindowTitle('Open File')
	dir_path, file_type = file_dialog.getOpenFileName(None,
	caption=caption, directory=parent.nc_code_dir,
	filter=parent.ext_filter, options=options)
	if dir_path:
		return dir_path
	else:
		return False

def open_manual(parent):
	if parent.installed:
		doc = os.path.join(parent.docs_path, 'mesact.pdf.gz')
	else:
		doc = os.path.join(parent.docs_path, 'mesact.pdf')
	subprocess.call(('xdg-open', doc))

def machine_name_changed(parent, text):
	if text:
		parent.machine_name = text.replace(' ','_').lower()
		parent.config_path = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.machine_name
		parent.config_path_lb.setText(parent.config_path)
		parent.ini_path = os.path.join(parent.config_path, f'{parent.machine_name}.ini')
	else:
		parent.pathLabel.setText('')
		parent.config_path = False
		parent.ini_path = False

def toggle_mdi(parent):
	if parent.sender().isChecked():
		parent.mdi_commands_gb.setEnabled(True)
	else:
		parent.mdi_commands_gb.setEnabled(False)

def changed(parent): # if anything is changed add * to title
	parent.status_lb.setText('Config Changed')
	parent.actionBuild.setText('Build Config *')

def backup_files(parent, config_path=None):
	parent.main_tw.setCurrentIndex(11)
	if not config_path:
		config_path = parent.config_path
	if not os.path.exists(config_path):
		parent.info_pte.setPlainText('Nothing found to Back Up')
		return
	backup_dir = os.path.join(config_path, 'backups')
	if not os.path.exists(backup_dir):
		os.mkdir(backup_dir)
	p1 = subprocess.Popen(['find',config_path,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backup_file = os.path.join(backup_dir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backup_file,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.info_pte.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.info_pte.appendPlainText(output.decode())

def add_mdi_row(parent):
	rows = parent.mdi_grid_layout.rowCount()
	# layout.addWidget(widget, row, column)
	parent.mdi_grid_layout.addWidget(QLabel('MDI Command'), rows, 0)
	le = QLineEdit(parent)
	le.setObjectName(f'mdi_le_{rows}')
	setattr(parent, f'mdi_le_{rows}', le) # add name to parent
	parent.mdi_grid_layout.addWidget(le, rows, 1)
	getattr(parent, f'mdi_le_{rows}').setFocus()
	getattr(parent, f'mdi_le_{rows}').returnPressed.connect(partial(add_mdi_row, parent))


