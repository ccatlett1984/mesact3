from functools import partial

from PyQt6.QtGui import QAction, QIcon

from libmesact import openini
from libmesact import download
from libmesact import utilities
from libmesact import boards
from libmesact import daughters

def connect(parent):
	# Menu Items
	# File Menu
	parent.actionNew.triggered.connect(partial(utilities.new_config, parent))
	parent.actionOpen.triggered.connect(partial(openini.open_ini, parent))

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

	# Help Menu
	parent.actionDocuments.triggered.connect(partial(utilities.open_manual, parent))


	# Machine Tab
	parent.boardCB.currentIndexChanged.connect(partial(boards.changed, parent))
	parent.daughterCB_1.currentIndexChanged.connect(partial(daughters.changed, parent, 4))
	parent.daughterCB_2.currentIndexChanged.connect(partial(daughters.changed, parent, 5))


