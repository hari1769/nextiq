"""
seed.py — Run this once to populate the database with realistic sample data.
Usage: python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from backend.utils.sample_data import generate

if __name__ == "__main__":
    generate()
