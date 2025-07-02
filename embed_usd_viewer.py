"""A simple application to embed a USD viewer using PySide6."""

import os
import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets
from pxr import Usd, UsdUtils
from pxr.Usdviewq.stageView import StageView, RenderModes


class EmmbedUSDWidget(QtWidgets.QWidget):
    """A widget to embed USD stage viewer."""

    def __init__(self, stage=None):
        super(EmmbedUSDWidget, self).__init__()
        self.model = StageView.DefaultDataModel()
        self.stage = stage
        self.view = StageView(dataModel=self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        if self.stage:
            self.set_stage(self.stage)

        # Reset View
        self.view.updateView(resetCam=True, forceComputeBBox=True)

    def image_save(self):
        """Save the current view as an image file."""
        print("GetRendererAovs", self.view.GetRendererAovs())
        image = self.view.grabFramebuffer()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/screenshot_{timestamp}.png"
        image.save(filename)

    def set_stage(self, stage):
        """Set the USD stage for the viewer

        Args:
            stage (QGLWidget): USD stage to set in the viewer.

        """
        self.model.stage = stage

    def set_render_mode(self, mode):
        """Set the render mode for the viewer.

        Args:
            mode (str): The render mode to set.
        """
        if mode in RenderModes:
            self.model.viewSettings.renderMode = mode
        else:
            print(f"Invalid render mode: {mode}")

    def reset_camera(self):
        """Resets the camera to fit the geometry in the view."""
        self.view.updateView(resetCam=True, forceComputeBBox=True)

    def show_hud(self, enable=True):
        """Show the HUD (Heads-Up Display) in the viewer.

        Args:
            enable (bool, optional): A value will handle HUD . Defaults to True.
        """

        self.model.viewSettings.showHUD = enable

    def show_bboxes(self, enable=True):
        """Show bounding boxes in the viewer.

        Args:
            enable (bool, optional): A value will handle bounding boxes. Defaults to True.
        """

        self.model.viewSettings.showBBoxes = enable


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    path = "assets/Sphere.usda"

    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(path)

    window = EmmbedUSDWidget(stage)
    window.setWindowTitle("USD Viewer")
    window.resize(QtCore.QSize(750, 750))
    window.show()

    sys.exit(app.exec_())
