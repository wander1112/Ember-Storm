"""
Bundle Loader Module
Loads pre-trained pipelines, benchmarks, and datasets with caching.
Falls back to building on-the-fly if needed.
"""

import os
import joblib
import streamlit as st
from modules.bundle_builder import build_and_save_bundle

@st.cache_resource(show_spinner="Loading pre-trained ML models & pipelines...")
def load_ml_bundle():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_path = os.path.join(base_dir, 'cache', 'models_bundle.joblib')

    if not os.path.exists(cache_path):
        bundle = build_and_save_bundle()
    else:
        try:
            bundle = joblib.load(cache_path)
        except Exception:
            bundle = build_and_save_bundle()

    return bundle
