import sys
import pathlib

base_path = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(base_path))

from src.models import db 

db.create_all()