"""Application entry point."""

import os
import sys

from app.config.settings import BASE_PATH
from app.views.components.side_bar import SideBar
import customtkinter as ctk

from app.controllers.app_controller import AppController
from app.controllers.menubar_controller import MenuBarController
from app.controllers.sybil_controller import SybilController
from app.utils.event_bus import EventBus
from app.views.components.log_panel import LogPanel
from app.views.components.menu_bar import MenuBar
from app.views.components.split_view import SplitView
from app.views.main_view import MainWindow
from app.views.sybil_view import SybilView

from .constants import PROJECT_ROOT


def main() -> None:

    ctk.set_appearance_mode("System")

    full_theme_path = os.path.join(BASE_PATH, "GhostTrain.json")
    ctk.set_default_color_theme(full_theme_path)

    root = ctk.CTk()
    root.title("CustomTkinter App")
    width = int(root.winfo_screenwidth() * 0.9)
    height = int(root.winfo_screenheight() * 0.9)
    x = int((root.winfo_screenwidth() - width) / 2)
    y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    bus = EventBus(root)
    bus.start()

    split = SplitView(root)

    log_panel = LogPanel(split.right)
    bus.subscribe(log_panel.handle_event)

    # ── Views — each gets its own frame inside split.middle ───────────────
    home_frame = ctk.CTkFrame(split.middle, fg_color="transparent")
    MainWindow(home_frame)
    split.add_view("Home", home_frame, "house.png")

    sybil_ctrl = SybilController(root, bus)
    sybil_frame = ctk.CTkFrame(split.middle, fg_color="transparent")
    sybil_form = SybilView(sybil_frame, sybil_ctrl)
    bus.subscribe(sybil_form.handle_event)
    split.add_view("Sybil Risk Model", sybil_frame, "house.png")

    # ── Controllers ───────────────────────────────────────────────────────
    app_ctrl = AppController(root, bus, split, sybil_form)

    menubar_ctrl = MenuBarController(root, bus, app_ctrl)
    MenuBar(root, menubar_ctrl)

    # ── Load model AFTER all subscribers are registered ────────────────────
    # root.after ensures the mainloop is running and the UI is fully rendered
    # before the background thread starts emitting log events.
    root.after(100, sybil_ctrl.load_model)

    root.mainloop()


if __name__ == "__main__":
    main()
