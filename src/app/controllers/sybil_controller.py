from __future__ import annotations

import json
import threading
from dataclasses import asdict
from pathlib import Path

from sybil import Sybil
from sybil.serie import Serie

from app.controllers.base_controller import BaseController
from app.utils.event_bus import AppEvent, EventBus
from app.utils.sybil_epi import calculate_sybil_epi_score, epi_input_from_patient_data


class SybilController(BaseController):
    def __init__(self, root, bus: EventBus):
        super().__init__(root, bus)
        self._model = None
        self._pending = None

    def load_model(self):
        self._log("Loading Sybil model...")
        self._progress(0.05)

        def _task():
            try:
                self._model = Sybil("sybil_ensemble")
                self._log("Model ready.", "SUCCESS")
                self._progress(0.0)
            except Exception as exc:
                self._error(f"Model load failed: {exc}")

        threading.Thread(target=_task, daemon=True).start()

    def run(self, data) -> None:
        if not self._model:
            self._error("Model not loaded.")
            return

        path = Path(data.ct_scan_dir)
        if not path.is_dir():
            self._error("Invalid CT folder.")
            return

        dicoms = sorted(path.glob("*.dcm"))
        if not dicoms:
            self._error("No DICOM files found.")
            return

        self._pending = data
        self._set_state("running")
        self._log(f"Running Sybil on {len(dicoms)} slices…")
        self._progress(0.2)

        threading.Thread(
            target=self._infer,
            args=([str(f) for f in dicoms],),
            daemon=True,
        ).start()

    def _infer(self, paths: list[str]) -> None:
        try:
            serie = Serie(paths)
            prediction = self._model.predict([serie])
            scores = prediction.scores[0]
            self._on_complete(scores)
        except Exception as exc:
            self._error(f"Inference failed: {exc}")

    def _on_complete(self, yearly) -> None:
        try:
            self._log(f"Sybil Scores {yearly}")
            self._log(json.dumps(asdict(self._pending)))
            epi_in = epi_input_from_patient_data(self._pending, yearly[5])
            epi = calculate_sybil_epi_score(epi_in)
        except Exception as exc:
            self._error(f"EPI scoring failed: {exc}")
            return

        self._progress(1.0)
        self._log(f"Final 6-year risk: {epi:.1%}", "SUCCESS")

        # Structured result for the results panel
        self._emit(
            AppEvent(
                type="result",
                data={
                    "yearly": list(yearly),
                    "epi": epi,
                },
            )
        )
        self._set_state("idle")
