from __future__ import annotations

from typing import TYPE_CHECKING

from app.controllers.base_controller import BaseController

if TYPE_CHECKING:
    from app.controllers.app_controller import AppController
    from app.utils.event_bus import EventBus


class MenuBarController(BaseController):
    """Event-driven controller for MenuBar."""

    def __init__(self, root: object, bus: EventBus, controller: AppController) -> None:
        super().__init__(root, bus)
        self.controller = controller

    def toggle_log(self):
        self.controller.toggle_log()

    def new_run(self):
        self.controller.new_run()

    def change_appearance(self, mode: str):
        self.controller.change_appearance(mode)

    def quit_app(self):
        self.controller.quit_app()
