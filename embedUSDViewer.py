import sys
from PySide6 import QtCore, QtWidgets
from pxr import Usd, UsdUtils
from pxr.Usdviewq.stageView import StageView


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
        image.save("save.png")

    def set_stage(self, stage):
        """Set the USD stage for the viewer."""
        self.model.stage = stage

    def close_event(self, event):
        """Handle the close event to ensure renderer is closed."""
        # Ensure to close the renderer to avoid GlfPostPendingGLErrors
        self.view.closeRenderer()

    def reset_camera(self):
        """Resets the camera to fit the geometry in the view."""
        self.view.updateView(resetCam=True, forceComputeBBox=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    path = r"Sphere.usda"

    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(path)

    window = EmmbedUSDWidget(stage)
    window.setWindowTitle("USD Viewer")
    window.resize(QtCore.QSize(750, 750))
    window.show()

    sys.exit(app.exec_())
