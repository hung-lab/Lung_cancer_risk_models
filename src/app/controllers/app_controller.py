import os
import shutil
import subprocess
from pathlib import Path

import customtkinter as ctk

from app.controllers.base_controller import BaseController
from app.utils.event_bus import AppEvent, EventBus
from app.utils.helpers import find_integral_cli


class AppController(BaseController):
    """Handles top-level UI events: layout toggles, theme, lifecycle."""

    def __init__(self, root, bus: EventBus, split_view, sybil_form):
        super().__init__(root, bus)
        self._split = split_view
        self._form = sybil_form
        bus.subscribe(self._handle_event)

    def _handle_event(self, event: AppEvent):
        if event.type == "ui_toggle":
            if event.message == "log_panel":
                self._split.toggle_right_panel()

        elif event.type == "ui_state":
            if event.message in ("running", "running_single", "running_batch"):
                self._split.lock_tabs()
            elif event.message in ("idle", "error"):
                self._split.unlock_tabs()

        elif event.type == "action":
            if event.message == "new_run":
                self._form.reset()

        elif event.type == "ui_theme":
            ctk.set_appearance_mode(event.message or "System")

        elif event.type == "app" and event.message == "quit":
            self.root.quit()

    # called by menubar view
    def toggle_log(self):
        self.bus.emit(AppEvent(type="ui_toggle", message="log_panel"))

    def new_run(self):
        self.bus.emit(AppEvent(type="action", message="new_run"))

    def change_appearance(self, mode: str):
        self.bus.emit(AppEvent(type="ui_theme", message=mode))

    def quit_app(self):
        self.bus.emit(AppEvent(type="app", message="quit"))

    def check_and_install_integral(self):
        """Returns (available, message)."""

        self._log("Checking R dependencies")

        # Step 1: R itself must be installed by the user
        if not shutil.which("Rscript"):
            self._error(
                "R is not installed. Download and install from https://github.com/r-lib/rig"
            )
            self._emit(AppEvent(type="ui_state", message="R_missing"))
            return

        user_bin = Path.home() / ".local" / "bin"
        os.environ["PATH"] = f"{user_bin}:{os.environ.get('PATH', '')}"

        cli = find_integral_cli()

        if cli:
            self._log("integral-radiomics is ready")
            self._emit(AppEvent(type="ui_state", message="integral_radiomics_ready"))
            return

        self._log("Auto installing R packages and integral-radiomics")

        r_lib = Path.home() / "R" / "library"

        install_cmd = f"""
        dir.create("{r_lib}", recursive=TRUE, showWarnings=FALSE)

        if (!requireNamespace("pak", quietly=TRUE)) {{
        install.packages(
            "pak",
            repos="https://cloud.r-project.org",
            lib="{r_lib}"
        )
        }}

        .libPaths(c("{r_lib}", .libPaths()))

        pak::pak("mattwarkentin/INTEGRAL-Radiomics")

        library(Rapp)
        library(integralrad)

        Rapp::install_pkg_cli_apps("Rapp")
        integralrad::install_integralrad_cli()
        """

        env = os.environ.copy()
        env["R_LIBS_USER"] = str(r_lib)
        env["PATH"] = f"{user_bin}:{env.get('PATH', '')}"

        try:
            result = subprocess.run(
                ["Rscript", "-e", install_cmd],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout:
                self._log(result.stdout)

        except subprocess.CalledProcessError as e:
            self._log(f"Install failed:\n{e.stderr}")
            self._emit(AppEvent(type="ui_state", message="install_failed"))
            return

        # Verify install
        if cli:
            self._log(f"Installation complete: {cli}")
            self._emit(AppEvent(type="ui_state", message="install_complete"))
        else:
            self._log(
                "Installation finished but integral-radiomics executable was not found"
            )
            self._emit(AppEvent(type="ui_state", message="install_failed"))
