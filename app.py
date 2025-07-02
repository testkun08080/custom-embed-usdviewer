"""Module providing a USD viewer application."""

import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from pxr import Usd, UsdUtils

from embed_usd_viewer import EmmbedUSDWidget


def get_ui_widget(ui_file_name):
    """Loads and returns a UI widget from a UI file.

    Args:
        ui_file_name (str): The path to the UI file to load.

    Returns:
        QWidget: The loaded UI widget.
    """
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    ui_widget = loader.load(ui_file)
    ui_file.close()

    return ui_widget


class EmbedUsdViewerController:
    """Controller class for the Embed USD viewer.

    Manages the loading of USD stages and the viewer widget.
    """

    def __init__(self, usd_file=None):
        """Initializes the USD viewer controller.

        Args:
            usd_file (str): USD file
        """

        self.ui = get_ui_widget("UI/usdViewerController.ui")

        # Load USD Stage
        with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
            self.stage = Usd.Stage.Open(usd_file)

        # Embed USD Viewer widget
        self.usd_widget = EmmbedUSDWidget(self.stage)
        self.ui.main_layout.addWidget(self.usd_widget)

        # Connect Save Image button event
        self.ui.save_image_button.clicked.connect(self.usd_widget.image_save)

        # Connect Reset Camera button event
        self.ui.reset_camera_button.clicked.connect(self.usd_widget.reset_camera)

    def setup_aov_ui(self):
        """Sets up the UI for AOVs selection.

        Retrieves the AOVs list and adds them to a combo box.
        """
        # Retrieve and add AOVs list to combo box
        aovs = self.usd_widget.view.GetRendererAovs()
        if not aovs:
            # Add default AOVs if the list is empty
            default_aovs = ["color", "primId", "depth", "Neye"]
            for aov in default_aovs:
                self.ui.aovs_combobox.addItem(aov)
        else:
            for aov in aovs:
                self.ui.aovs_combobox.addItem(aov)

        # Connect AOV selection event
        self.ui.aovs_combobox.currentTextChanged.connect(self.on_aov_changed)

    def on_aov_changed(self, aov_name):
        """Updates the view based on the selected AOV.

        Args:
            aov_name (str): The name of the selected AOV.
        """

        # Update view to the selected AOV
        if aov_name:
            self.usd_widget.view.SetRendererAov(aov_name)
            self.usd_widget.view.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    viewer_controller = EmbedUsdViewerController("assets/Sphere.usda")
    viewer_controller.ui.show()

    # You might need to call this after shop up the window
    viewer_controller.setup_aov_ui()
    sys.exit(app.exec_())
