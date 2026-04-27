from dataclasses import dataclass


@dataclass
class SybilInputData:
    age: int
    bmi: float
    copd: int
    education: int
    ethnicity: int
    family_lc_history: int
    personal_cancer_history: int
    smoking_duration: float
    smoking_intensity: float
    smoking_quit_time: float
    smoking_status: int
    ct_scan_dir: str


@dataclass
class RiskResult:
    yearly_scores: list[float]
    epi_score: float
