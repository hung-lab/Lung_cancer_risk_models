import datetime

import customtkinter as ctk

from app.utils.event_bus import AppEvent

_LEVEL_META = {
    "INFO": ("i", "info"),
    "SUCCESS": ("✓", "success"),
    "WARNING": ("⚠", "warning"),
    "ERROR": ("✗", "error"),
}


class LogPanel:
    def __init__(self, parent: ctk.CTkFrame) -> None:
        self.parent = parent

        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self.parent, fg_color="transparent", border_width=0)
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=(12, 4))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Activity Log",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="Clear",
            width=56,
            height=24,
            command=self.clear,
        ).grid(row=0, column=1)

        # Log box
        self.box = ctk.CTkTextbox(
            self.parent,
            state="disabled",
            wrap="word",
            font=ctk.CTkFont(family="Courier", size=11),
        )
        self.box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Tags
        self.box.tag_config("info", foreground="#5B9BD5")
        self.box.tag_config("success", foreground="#4CAF50")
        self.box.tag_config("warning", foreground="#FF9800")
        self.box.tag_config("error", foreground="#F44336")
        self.box.tag_config("ts", foreground="#888888")

    def log(self, message: str, level: str = "INFO") -> None:
        prefix, tag = _LEVEL_META.get(level.upper(), ("•", "info"))
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.box.configure(state="normal")
        self.box.insert("end", f"[{timestamp}] ", "ts")
        self.box.insert("end", f"{prefix} {message}\n", tag)
        self.box.see("end")
        self.box.configure(state="disabled")

    def clear(self) -> None:
        self.box.configure(state="normal")
        self.box.delete("1.0", "end")
        self.box.configure(state="disabled")

    def handle_event(self, event: AppEvent) -> None:
        if event.type == "log":
            self.log(event.message or "", event.level)
