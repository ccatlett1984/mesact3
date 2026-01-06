from functools import partial

from PyQt6.QtGui import QAction, QIcon

from libmesact import axes
from libmesact import openini
from libmesact import download
from libmesact import buildconfig
from libmesact import check
from libmesact import utilities
from libmesact import boards
from libmesact import daughters
from libmesact import sscards
from libmesact import flash
from libmesact import dialogs
from libmesact import samples

def connect(parent):
	# Menu Items
	# File Menu
	parent.actionNew.triggered.connect(partial(utilities.new_config, parent))
	parent.actionOpen.triggered.connect(partial(openini.load_ini, parent))

	exitAction = QAction(QIcon.fromTheme("application-exit"), 'Exit', parent)
	exitAction.setStatusTip('Exit application')
	exitAction.triggered.connect(parent.close)
	parent.menuFile.addAction(exitAction)

	# Downloads Menu
	parent.actionMesaCT_PC_64_bit.triggered.connect(partial(download.download_deb, 'amd64', parent))
	parent.actionMesaCT_Rpi_32_bit.triggered.connect(partial(download.download_deb, 'armhf', parent))
	parent.actionMesaCT_Rpi_64_bit.triggered.connect(partial(download.download_deb, 'arm64', parent))

	parent.actionFirmware.triggered.connect(partial(download.download_firmware, parent))

	parent.action5i25.triggered.connect(partial(download.download_manual, '5i25man.pdf', parent))
	parent.action5i25T.triggered.connect(partial(download.download_manual, '5i25tman.pdf', parent))
	parent.action6i25.triggered.connect(partial(download.download_manual, '6i25man.pdf', parent))
	parent.action7c81.triggered.connect(partial(download.download_manual, '7c81man.pdf', parent))
	parent.action7i98.triggered.connect(partial(download.download_manual, '7i98man.pdf', parent))
	parent.action7c80.triggered.connect(partial(download.download_manual, '7c80man.pdf', parent))
	parent.action7i76E.triggered.connect(partial(download.download_manual, '7i76eman.pdf', parent))
	parent.action7i76EU.triggered.connect(partial(download.download_manual, '7i76euman.pdf', parent))
	parent.action7i95.triggered.connect(partial(download.download_manual, '7i95man.pdf', parent))
	parent.action7i95T.triggered.connect(partial(download.download_manual, '7i95tman.pdf', parent))
	parent.action7i96.triggered.connect(partial(download.download_manual, '7i96man.pdf', parent))
	parent.action7i96S.triggered.connect(partial(download.download_manual, '7i96sman.pdf', parent))
	parent.action7i97.triggered.connect(partial(download.download_manual, '7i97man.pdf', parent))
	parent.action7i97T.triggered.connect(partial(download.download_manual, '7i97tman.pdf', parent))
	parent.action7i76.triggered.connect(partial(download.download_manual, '7i76man.pdf', parent))
	parent.action7i77.triggered.connect(partial(download.download_manual, '7i77man.pdf', parent))
	parent.action7i78.triggered.connect(partial(download.download_manual, '7i78man.pdf', parent))
	parent.action7i85.triggered.connect(partial(download.download_manual, '7i85man.pdf', parent))
	parent.action7i85S.triggered.connect(partial(download.download_manual, '7i85sman.pdf', parent))
	parent.action7i88.triggered.connect(partial(download.download_manual, '7i88man.pdf', parent))
	parent.action7i89.triggered.connect(partial(download.download_manual, '7i89man.pdf', parent))
	parent.action7i64.triggered.connect(partial(download.download_manual, '7i64man.pdf', parent))
	parent.action7i69.triggered.connect(partial(download.download_manual, '7i69man.pdf', parent))
	parent.action7i70.triggered.connect(partial(download.download_manual, '7i70man.pdf', parent))
	parent.action7i71.triggered.connect(partial(download.download_manual, '7i71man.pdf', parent))
	parent.action7i72.triggered.connect(partial(download.download_manual, '7i72man.pdf', parent))
	parent.action7i73.triggered.connect(partial(download.download_manual, '7i73man.pdf', parent))
	parent.action7i74.triggered.connect(partial(download.download_manual, '7i74man.pdf', parent))
	parent.action7i83.triggered.connect(partial(download.download_manual, '7i83man.pdf', parent))
	parent.action7i84.triggered.connect(partial(download.download_manual, '7i84man.pdf', parent))
	parent.action7i87.triggered.connect(partial(download.download_manual, '7i87man.pdf', parent))
	parent.action7i77ISOL.triggered.connect(partial(download.download_manual, '7i77isolman.pdf', parent))
	parent.actionTHCAD2.triggered.connect(partial(download.download_manual, 'thcad2man.pdf', parent))

	# Tools Menu
	parent.actionCheck.triggered.connect(partial(check.check_config, parent))
	parent.actionBackup_Config.triggered.connect(partial(utilities.backup_files, parent))
	parent.actionBuild.triggered.connect(partial(buildconfig.build, parent))

	# Help Menu
	parent.actionDocuments.triggered.connect(partial(utilities.open_manual, parent))
	parent.actionCheckUpdates.triggered.connect(partial(utilities.check_updates, parent))
	parent.actionAboutMesaCT.triggered.connect(partial(dialogs.about_dialog, parent))

	# Machine Tab
	parent.machine_name_le.textChanged[str].connect(partial(utilities.machine_name_changed, parent))
	parent.load_config_cb.stateChanged.connect(partial(utilities.update_settings, parent))
	parent.board_cb.currentIndexChanged.connect(partial(boards.changed, parent))
	parent.daughter_cb_1.currentIndexChanged.connect(partial(daughters.changed, parent))
	parent.daughter_cb_2.currentIndexChanged.connect(partial(daughters.changed, parent))
	parent.find_ip_board_pb.clicked.connect(partial(flash.find_ip_board, parent))
	parent.verify_board_pb.clicked.connect(partial(flash.verify_board, parent))

	parent.default_imperial_pb.clicked.connect(partial(samples.default_imperial, parent))
	parent.default_metric_pb.clicked.connect(partial(samples.default_metric, parent))
	parent.sample_5i25_7i76_pb.clicked.connect(partial(samples.sample_5i25_7i76, parent))
	parent.sample_5i25_7i77_pb.clicked.connect(partial(samples.sample_5i25_7i77, parent))
	parent.sample_7i76eu_pb.clicked.connect(partial(samples.sample_7i76eu, parent))
	parent.sample_7i92t_7i76_pb.clicked.connect(partial(samples.sample_7i92t_7i76, parent))
	parent.sample_7i92t_7i77_pb.clicked.connect(partial(samples.sample_7i92t_7i77, parent))
	parent.sample_7i95t_pb.clicked.connect(partial(samples.sample_7i95t, parent))
	parent.sample_7i96s_pb.clicked.connect(partial(samples.sample_7i96s, parent))
	parent.sample_7i97t_pb.clicked.connect(partial(samples.sample_7i97t, parent))

	# Firmware Tab
	parent.firmware_cb.currentIndexChanged.connect(partial(flash.firmware_changed, parent))

	# Settings Tab
	parent.gui_cb.currentIndexChanged.connect(partial(utilities.gui_changed, parent))
	parent.halui_cb.toggled.connect(partial(utilities.toggle_mdi, parent))
	parent.add_mdi_command_pb.clicked.connect(partial(utilities.add_mdi_row, parent))
	parent.mdi_le_0.returnPressed.connect(partial(utilities.add_mdi_row, parent))
	parent.linear_units_cb.currentIndexChanged.connect(partial(utilities.units_changed, parent))
	parent.traj_max_lin_vel_dsb.valueChanged.connect(partial(utilities.max_vel_changed, parent))

	# Drive Tabs
	for i in range(6):
		for j in range(3):
			getattr(parent, f'c{j}_axis_{i}').currentIndexChanged.connect(partial(axes.axis_changed, parent))
			getattr(parent, f'c{j}_scale_{i}').textChanged.connect(partial(axes.update_axis_info, parent))
			getattr(parent, f'c{j}_max_vel_{i}').textChanged.connect(partial(axes.update_axis_info, parent))
			getattr(parent, f'c{j}_max_accel_{i}').textChanged.connect(partial(axes.update_axis_info, parent))
			getattr(parent, f'c{j}_pid_default_{i}').clicked.connect(partial(axes.set_default_pid, parent))
			getattr(parent, f'c{j}_ferror_default_{i}').clicked.connect(partial(axes.set_default_ferror, parent))
			getattr(parent, f'c{j}_analog_default_{i}').clicked.connect(partial(axes.set_default_analog, parent))
			getattr(parent, f'c{j}_drive_{i}').currentIndexChanged.connect(partial(axes.drive_changed, parent))

	# Smart Serial Tab
	parent.ss_card_cb.currentIndexChanged.connect(partial(sscards.card_changed, parent))
	parent.ss7i73_keypad_cb.currentIndexChanged.connect(partial(sscards.ss7i73_changed, parent))
	parent.ss7i73lcd_cb.currentIndexChanged.connect(partial(sscards.ss7i73_changed, parent))



