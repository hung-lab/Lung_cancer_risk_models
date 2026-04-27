"""Reusable full-frame loading overlay component.

Drop it onto any CTkFrame and call show()/hide() to block the UI while a
long-running background task is in progress.

Usage
-----
    overlay = RunningOverlay(parent_frame)

    # show with optional custom title / initial stage text
    overlay.show(title="Running model…", stage="Preparing pipeline")

    # update text as stages progress (called from handle_event)
    overlay.set_stage("Running CT analysis…")

    # update progress bar (keeps animated until value reaches 1.0)
    overlay.set_progress(0.7)

    # hide when done
    overlay.hide()
"""

from __future__ import annotations

import customtkinter as ctk


class RunningOverlay:
    """Full-frame animated loading overlay.

    Places itself over *parent* using ``place(relwidth=1, relheight=1)``
    and sits below the stacking order until :meth:`show` is called.

    Thread safety: all public methods must be called from the Tk main thread
    (i.e. from an EventBus subscriber or a ``root.after`` callback).
    """

    def __init__(self, parent: ctk.CTkFrame) -> None:
        self._parent = parent
        self._visible = False
        self._elapsed = 0

        self._build()

    # ── public API ────────────────────────────────────────────────────────

    def show(self, title: str = "Running…", stage: str = "Preparing…") -> None:
        """Lift the overlay and start the animation + elapsed timer."""
        self._visible = True
        self._elapsed = 0

        self._title_label.configure(text=title)
        self._stage_label.configure(text=stage)
        self._elapsed_label.configure(text="0s elapsed")

        # always start in indeterminate mode so the bar animates immediately
        self._bar.configure(mode="indeterminate")
        self._bar.start()

        self._frame.lift()
        self._tick()

    def hide(self) -> None:
        """Lower the overlay and stop the animation."""
        self._visible = False
        self._bar.stop()
        self._frame.lower()

    def set_stage(self, text: str) -> None:
        """Update the stage subtitle (e.g. 'Running CT analysis…')."""
        self._stage_label.configure(text=text)

    def set_progress(self, value: float) -> None:
        """React to a progress milestone.

        Keeps the bar in indeterminate (animated) mode for all intermediate
        values so it never appears frozen.  Switches to determinate only when
        *value* reaches 1.0 so the user sees a clear completion signal.
        """
        if value >= 1.0:
            self._bar.stop()
            self._bar.configure(mode="determinate")
            self._bar.set(1.0)
            self._stage_label.configure(text="Complete!")

        # For 0 < value < 1 just let the indeterminate animation keep running.
        # The stage label (updated via set_stage) already communicates which
        # phase is active — no need to freeze the bar at e.g. 20% or 70%.

    @property
    def is_visible(self) -> bool:
        return self._visible

    # ── internal ──────────────────────────────────────────────────────────

    def _build(self) -> None:
        self._frame = ctk.CTkFrame(self._parent, fg_color=("gray95", "#1A1F2E"))
        self._frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._frame.lower()

        # centred content block
        inner = ctk.CTkFrame(self._frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        self._title_label = ctk.CTkLabel(
            inner,
            text="Running…",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self._title_label.pack(pady=(0, 6))

        self._stage_label = ctk.CTkLabel(
            inner,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="gray60",
        )
        self._stage_label.pack(pady=(0, 24))

        self._bar = ctk.CTkProgressBar(inner, width=360, height=10)
        self._bar.pack()
        self._bar.set(0)

        self._elapsed_label = ctk.CTkLabel(
            inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
        )
        self._elapsed_label.pack(pady=(8, 0))

    def _tick(self) -> None:
        """Increment the elapsed-time counter every second while visible."""
        if not self._visible:
            return

        self._elapsed += 1
        mins, secs = divmod(self._elapsed, 60)
        text = f"{mins}m {secs:02d}s elapsed" if mins else f"{secs}s elapsed"
        self._elapsed_label.configure(text=text)

        self._parent.after(1000, self._tick)
