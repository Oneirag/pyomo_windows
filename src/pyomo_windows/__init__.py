import logging
from pathlib import Path

__version__="0.0.1"

solver_executables = {
    "glpk": "glpsol.exe",
    "ipopt": "ipopt.exe",
    "cbc": "cbc.exe",
}

logging.basicConfig(format="'%(asctime)s %(levelname)s %(name)s %(message)s'",
                    level=logging.INFO)
logger = logging


def get_target_folder(target: str | Path) -> Path:
    target = target or Path(__file__).parent
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    return target
