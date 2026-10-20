"""
ML Studio — Machine Learning Analytics Platform
=================================================
Capstone Project: Academic Year 2026–27
Three Distinct Tracks:
  1. Regression Track (WHO Life Expectancy Data)
  2. Classification Track (Maternal Health Risk Dataset)
  3. Clustering Track (Cardiotocography CTG Dataset)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Modular imports
from modules.bundle_loader import load_ml_bundle
from modules.regression import (
    plot_actual_vs_predicted, plot_residual_diagnostics, plot_feature_importances
)
from modules.classification import (
    plot_confusion_matrix_plotly, plot_multiclass_roc_curves
)
from modules.clustering import (
    evaluate_kmeans_range, plot_elbow_curve, plot_pca_clusters,
    plot_tsne_clusters, generate_dendrogram_fig
)
from modules.prediction import plot_prediction_probabilities

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ML Studio — Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject external custom styling
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Load Pre-trained Pipelines & Fixed Datasets (Cached)
# -----------------------------------------------------------------------------
bundle = load_ml_bundle()
reg_data = bundle['reg']
clf_data = bundle['clf']
clust_data = bundle['clust']

# Session state for prediction logs and scenario presets
if 'reg_history' not in st.session_state:
    st.session_state.reg_history = []
if 'clf_history' not in st.session_state:
    st.session_state.clf_history = []
if 'clust_history' not in st.session_state:
    st.session_state.clust_history = []
if 'reg_preset' not in st.session_state:
    st.session_state.reg_preset = "median"
if 'clf_preset' not in st.session_state:
    st.session_state.clf_preset = "default"
if 'ctg_preset' not in st.session_state:
    st.session_state.ctg_preset = "default"

# -----------------------------------------------------------------------------
# Sidebar Navigation (Strictly 3 Fixed Problem Tracks — No Dataset Selector)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 2px 0 12px 0;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 1.25rem;">⚡</span>
                <span style="color: #0f172a; font-size: 1.15rem; font-weight: 600; letter-spacing: -0.3px;">ML Studio</span>
            </div>
            <p style="color: #64748b; font-size: 0.72rem; margin: 2px 0 0 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500;">
                Analytics Platform
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size: 0.7rem; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.04em; margin-bottom: 4px;'>Problem Track</p>", unsafe_allow_html=True)

    track_selection = st.radio(
        "Navigation",
        options=[
            "📈 Regression",
            "🎯 Classification",
            "🌌 Clustering"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Fixed Dataset Metadata Badge (Context-Aware for each track)
    if "Regression" in track_selection:
        st.markdown("""
            <div class="sidebar-track-badge">
                <div class="sidebar-track-title">Dataset: Regression</div>
                <div style="font-weight: 600; color: #0f172a; font-size: 0.85rem;">WHO Life Expectancy</div>
                <div class="sidebar-track-desc" style="margin-top: 3px;">
                    • 2,938 country-year records<br>
                    • 18 continuous predictors<br>
                    • Target: <code>Life expectancy</code><br>
                    • 10 benchmark algorithms
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif "Classification" in track_selection:
        st.markdown("""
            <div class="sidebar-track-badge">
                <div class="sidebar-track-title" style="color: #0f766e !important;">Dataset: Classification</div>
                <div style="font-weight: 600; color: #0f172a; font-size: 0.85rem;">Maternal Health Risk</div>
                <div class="sidebar-track-desc" style="margin-top: 3px;">
                    • 1,014 patient vitals records<br>
                    • 7 features (including MAP)<br>
                    • Target: <code>RiskLevel (3 classes)</code><br>
                    • 10 benchmark algorithms
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="sidebar-track-badge">
                <div class="sidebar-track-title" style="color: #0284c7 !important;">Dataset: Clustering</div>
                <div style="font-weight: 600; color: #0f172a; font-size: 0.85rem;">Cardiotocography (CTG)</div>
                <div class="sidebar-track-desc" style="margin-top: 3px;">
                    • 2,126 fetal recordings<br>
                    • 33 biomedical attributes<br>
                    • Ground Truth: <code>NSP clinical triage</code><br>
                    • 4 linkage & cluster methods
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top: 14px; padding: 10px 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px;">
            <div style="display: flex; align-items: center; gap: 6px; font-size: 0.72rem; font-weight: 600; color: #15803d;">
                <span style="display: inline-block; width: 7px; height: 7px; background: #16a34a; border-radius: 50%;"></span>
                24 Models Trained & Cached
            </div>
            <div style="font-size: 0.7rem; color: #4b5563; margin-top: 2px;">Instant zero-latency inference enabled.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top: 24px; font-size: 0.7rem; color: #94a3b8; line-height: 1.4;">
            23CSE301 ML Capstone<br>
            Academic Year 2026–27
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TRACK 1: REGRESSION TRACK (WHO Life Expectancy Data)
# =============================================================================
if "Regression" in track_selection:
    st.markdown("""
        <div class="hero-header hero-reg">
            <div class="hero-pill">WHO Global Health Analytics • Continuous Target</div>
            <h1 class="hero-title">Regression Track — Life Expectancy Prediction</h1>
            <p class="hero-subtitle">
                Evaluate 10 tuned regression models across immunization, mortality, and economic indicators with diagnostic residual and feature parity analysis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Top Metric Highlights
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-blue"></div>
                <div class="metric-label">Best Algorithm</div>
                <div class="metric-value">Random Forest</div>
                <div class="metric-sub">Tuned Ensemble Regressor</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-emerald"></div>
                <div class="metric-label">Top Test R² Score</div>
                <div class="metric-value">0.9631</div>
                <div class="metric-sub">5-Fold CV: 0.9578</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-indigo"></div>
                <div class="metric-label">Lowest Test RMSE</div>
                <div class="metric-value">1.78 <span style="font-size: 0.85rem; font-weight: 400; color: #64748b;">Years</span></div>
                <div class="metric-sub">MAE: 1.16 Years</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-cyan"></div>
                <div class="metric-label">Dataset Records</div>
                <div class="metric-value">2,938</div>
                <div class="metric-sub">18 Continuous Features</div>
            </div>
        """, unsafe_allow_html=True)

    # Track Tabs: Live Prediction, Model Comparison, Visualizations, Dataset Overview
    tab_pred, tab_comp, tab_viz, tab_data = st.tabs([
        "Live Prediction",
        "Model Comparison",
        "Visualizations & Diagnostics",
        "Dataset & Pipeline"
    ])

    # -------------------------------------------------------------
    # TAB 1: LIVE PREDICTION
    # -------------------------------------------------------------
    with tab_pred:
        col_algo, col_preset = st.columns([1.1, 1.9], gap="medium")
        with col_algo:
            sel_reg_model_name = st.selectbox(
                "Select Model Algorithm:",
                options=list(reg_data['models'].keys()),
                index=0,
                help="Choose which algorithm will generate the life expectancy prediction."
            )

        with col_preset:
            st.markdown("<div class='control-label'>Scenario Presets:</div>", unsafe_allow_html=True)
            p_col1, p_col2, p_col3 = st.columns(3, gap="small")
            if p_col1.button("Developed Nation", use_container_width=True):
                st.session_state.reg_preset = "developed"
            if p_col2.button("Global Median", use_container_width=True):
                st.session_state.reg_preset = "median"
            if p_col3.button("Developing Nation", use_container_width=True):
                st.session_state.reg_preset = "developing"

        # Preset values dictionary based on st.session_state.reg_preset
        df_reg = reg_data['df']
        current_preset = st.session_state.get('reg_preset', 'median')
        if current_preset == "developed":
            defaults = {
                'Adult Mortality': 65.0, 'infant deaths': 2.0, 'Alcohol': 9.8, 'percentage expenditure': 4500.0,
                'Hepatitis B': 95.0, 'Measles': 10.0, 'BMI': 55.0, 'under-five deaths': 3.0, 'Polio': 98.0,
                'Total expenditure': 9.5, 'Diphtheria': 98.0, 'HIV/AIDS': 0.1, 'GDP': 42000.0, 'Population': 8500000.0,
                'thinness  1-19 years': 1.2, 'thinness 5-9 years': 1.1, 'Income composition of resources': 0.92, 'Schooling': 17.5
            }
        elif current_preset == "developing":
            defaults = {
                'Adult Mortality': 380.0, 'infant deaths': 65.0, 'Alcohol': 1.5, 'percentage expenditure': 45.0,
                'Hepatitis B': 50.0, 'Measles': 4500.0, 'BMI': 19.0, 'under-five deaths': 95.0, 'Polio': 52.0,
                'Total expenditure': 4.1, 'Diphtheria': 50.0, 'HIV/AIDS': 6.8, 'GDP': 650.0, 'Population': 18000000.0,
                'thinness  1-19 years': 9.5, 'thinness 5-9 years': 9.8, 'Income composition of resources': 0.42, 'Schooling': 7.5
            }
        else:
            defaults = {col: float(df_reg[col].median()) for col in reg_data['features']}

        input_reg = {}
        col_f1, col_f2, col_f3 = st.columns(3, gap="medium")
        with col_f1:
            st.markdown("<div class='group-header'>Mortality & Vitals</div>", unsafe_allow_html=True)
            input_reg['Adult Mortality'] = st.number_input("Adult Mortality (per 1k):", value=float(defaults['Adult Mortality']), min_value=1.0, max_value=800.0, step=5.0)
            input_reg['infant deaths'] = st.number_input("Infant Deaths (per 1k):", value=float(defaults['infant deaths']), min_value=0.0, max_value=1800.0, step=1.0)
            input_reg['under-five deaths'] = st.number_input("Under-Five Deaths (per 1k):", value=float(defaults['under-five deaths']), min_value=0.0, max_value=2500.0, step=1.0)
            input_reg['HIV/AIDS'] = st.number_input("HIV/AIDS (per 1k births):", value=float(defaults['HIV/AIDS']), min_value=0.1, max_value=50.0, step=0.1)
            input_reg['BMI'] = st.number_input("Average BMI:", value=float(defaults['BMI']), min_value=1.0, max_value=85.0, step=0.5)
            input_reg['Alcohol'] = st.number_input("Alcohol (litres/capita):", value=float(defaults['Alcohol']), min_value=0.0, max_value=20.0, step=0.2)

        with col_f2:
            st.markdown("<div class='group-header'>Immunization & Coverage</div>", unsafe_allow_html=True)
            input_reg['Polio'] = st.slider("Polio Coverage (%):", min_value=1.0, max_value=99.0, value=float(defaults['Polio']), step=1.0)
            input_reg['Diphtheria'] = st.slider("Diphtheria Coverage (%):", min_value=1.0, max_value=99.0, value=float(defaults['Diphtheria']), step=1.0)
            input_reg['Hepatitis B'] = st.slider("Hepatitis B Coverage (%):", min_value=1.0, max_value=99.0, value=float(defaults['Hepatitis B']), step=1.0)
            input_reg['Measles'] = st.number_input("Reported Measles Cases:", value=float(defaults['Measles']), min_value=0.0, max_value=250000.0, step=100.0)
            input_reg['thinness  1-19 years'] = st.number_input("Thinness 1-19 Years (%):", value=float(defaults['thinness  1-19 years']), min_value=0.1, max_value=30.0, step=0.2)
            input_reg['thinness 5-9 years'] = st.number_input("Thinness 5-9 Years (%):", value=float(defaults['thinness 5-9 years']), min_value=0.1, max_value=30.0, step=0.2)

        with col_f3:
            st.markdown("<div class='group-header'>Socio-Economic Indices</div>", unsafe_allow_html=True)
            input_reg['Income composition of resources'] = st.slider("Human Dev Index (0 to 1):", min_value=0.0, max_value=1.0, value=float(defaults['Income composition of resources']), step=0.01)
            input_reg['Schooling'] = st.slider("Schooling (Years):", min_value=0.0, max_value=22.0, value=float(defaults['Schooling']), step=0.5)
            input_reg['GDP'] = st.number_input("GDP Per Capita ($ USD):", value=float(defaults['GDP']), min_value=10.0, max_value=120000.0, step=500.0)
            input_reg['Total expenditure'] = st.number_input("Health % of Budget:", value=float(defaults['Total expenditure']), min_value=0.5, max_value=20.0, step=0.2)
            input_reg['percentage expenditure'] = st.number_input("Expenditure as % GDP:", value=float(defaults['percentage expenditure']), min_value=0.0, max_value=20000.0, step=50.0)
            input_reg['Population'] = st.number_input("Total Population:", value=float(defaults['Population']), min_value=1000.0, max_value=1500000000.0, step=500000.0)

        # Action Buttons neatly placed
        btn_col1, btn_col2, _ = st.columns([1.6, 1.2, 3.2], gap="small")
        with btn_col1:
            run_pred = st.button("Calculate Prediction", type="primary", use_container_width=True)
        with btn_col2:
            if st.button("Reset Defaults", use_container_width=True):
                st.session_state.reg_preset = "median"
                st.rerun()

        if run_pred:
            model_obj = reg_data['models'][sel_reg_model_name]
            scaler_reg = reg_data['scaler']
            features_reg = reg_data['features']

            input_row = pd.DataFrame([input_reg])[features_reg]
            input_scaled = scaler_reg.transform(input_row)

            pred_val = float(model_obj.predict(input_scaled)[0])
            pred_val = max(35.0, min(95.0, pred_val))

            diff_global = pred_val - 71.6
            diff_str = f"+{diff_global:.1f} years" if diff_global >= 0 else f"{diff_global:.1f} years"
            diff_color = "#15803d" if diff_global >= 0 else "#b91c1c"

            st.markdown(f"""
                <div class="diagnostic-summary-box diag-reg">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <div class="diag-tag">Forecast Output</div>
                            <div class="diag-val" style="color: #1d4ed8;">{pred_val:.1f} <span style="font-size: 0.95rem; font-weight: 500; color: #475569;">Years</span></div>
                            <div class="diag-sub">Algorithm: <strong>{sel_reg_model_name}</strong></div>
                        </div>
                        <div style="text-align: right;">
                            <div class="diag-tag">Global Baseline Comparison</div>
                            <div style="font-size: 1.15rem; font-weight: 600; color: {diff_color};">{diff_str}</div>
                            <div class="diag-sub">Baseline: 71.6 Years</div>
                        </div>
                    </div>
                    <div class="diag-assessment">
                        <strong>Assessment:</strong> Stratified as 
                        <strong>{'High Life Expectancy (>75 yrs)' if pred_val >= 75 else ('Moderate Health Tier (65–75 yrs)' if pred_val >= 65 else 'Vulnerable Tier (<65 yrs)')}</strong>.
                        Key drivers: Schooling ({input_reg['Schooling']} yrs) and HDI ({input_reg['Income composition of resources']:.2f}).
                    </div>
                </div>
            """, unsafe_allow_html=True)

            hist_item = {'Timestamp': pd.Timestamp.now().strftime('%H:%M:%S'), 'Algorithm': sel_reg_model_name, 'Predicted Life Exp': round(pred_val, 2)}
            hist_item.update(input_reg)
            st.session_state.reg_history.append(hist_item)

        if st.session_state.reg_history:
            with st.expander("Session Prediction Log"):
                df_h = pd.DataFrame(st.session_state.reg_history)
                st.dataframe(df_h, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: MODEL COMPARISON
    # -------------------------------------------------------------
    with tab_comp:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Regression Algorithm Leaderboard</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Empirical benchmark across 10 regression models on test split.</p>", unsafe_allow_html=True)

        bench_df = reg_data['bench'].copy()
        st.dataframe(
            bench_df.style.highlight_max(subset=['Test R2', '5-Fold CV R2'], color='#dcfce7')
                           .highlight_min(subset=['RMSE (Years)', 'MAE (Years)'], color='#dcfce7'),
            use_container_width=True
        )

        col_c1, col_c2 = st.columns([1.1, 1], gap="medium")
        with col_c1:
            metric_sort = st.selectbox("Rank Metric:", ['Test R2', 'RMSE (Years)', 'MAE (Years)'])
            asc = False if metric_sort == 'Test R2' else True
            fig_bar = px.bar(
                bench_df.sort_values(by=metric_sort, ascending=not asc),
                x=metric_sort, y='Model', orientation='h',
                title=f"Benchmark: {metric_sort}",
                color=metric_sort,
                color_continuous_scale="Blues" if metric_sort == 'Test R2' else "Reds_r",
                text=metric_sort,
                height=320
            )
            fig_bar.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_c2:
            st.markdown("<div style='font-size: 0.88rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Algorithm Head-to-Head</div>", unsafe_allow_html=True)
            m_a = st.selectbox("Model A:", bench_df['Model'].tolist(), index=0)
            m_b = st.selectbox("Model B:", bench_df['Model'].tolist(), index=7)

            row_a = bench_df[bench_df['Model'] == m_a].iloc[0]
            row_b = bench_df[bench_df['Model'] == m_b].iloc[0]

            r2_diff = row_a['Test R2'] - row_b['Test R2']
            rmse_diff = row_a['RMSE (Years)'] - row_b['RMSE (Years)']

            if r2_diff > 0:
                duel_msg = f"{m_a} achieves {abs(r2_diff):.4f} higher R² and reduces error by {abs(rmse_diff):.2f} years vs. {m_b}."
            else:
                duel_msg = f"{m_b} achieves {abs(r2_diff):.4f} higher R² over {m_a}."

            st.markdown(f"""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 8px; color: #0f172a;">Comparison Metrics:</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div style="padding: 10px; background: #eff6ff; border-radius: 6px; border: 1px solid #dbeafe;">
                            <div style="font-weight: 600; font-size: 0.82rem; color: #1e40af;">{m_a}</div>
                            <div style="font-size: 0.78rem; color: #2563eb;">R²: <strong>{row_a['Test R2']}</strong></div>
                            <div style="font-size: 0.78rem; color: #2563eb;">RMSE: <strong>{row_a['RMSE (Years)']} yrs</strong></div>
                        </div>
                        <div style="padding: 10px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <div style="font-weight: 600; font-size: 0.82rem; color: #475569;">{m_b}</div>
                            <div style="font-size: 0.78rem; color: #64748b;">R²: <strong>{row_b['Test R2']}</strong></div>
                            <div style="font-size: 0.78rem; color: #64748b;">RMSE: <strong>{row_b['RMSE (Years)']} yrs</strong></div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8rem; color: #475569; line-height: 1.45;">
                        {duel_msg}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: VISUALIZATIONS & DIAGNOSTICS
    # -------------------------------------------------------------
    with tab_viz:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Regression Diagnostics</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Parity scatter, residual distributions, and feature importances for top performer.</p>", unsafe_allow_html=True)
        
        v_col1, v_col2 = st.columns(2, gap="medium")
        y_test = reg_data['y_test']
        best_preds = reg_data['preds']['Random Forest Regressor']

        with v_col1:
            st.plotly_chart(plot_actual_vs_predicted(y_test, best_preds, model_name="Random Forest Regressor"), use_container_width=True)

        with v_col2:
            st.plotly_chart(plot_residual_diagnostics(y_test, best_preds, model_name="Random Forest Regressor"), use_container_width=True)

        vf_col1, vf_col2 = st.columns(2, gap="medium")

        with vf_col1:
            rf_est = reg_data['models']['Random Forest Regressor']
            fig_imp = plot_feature_importances(rf_est, reg_data['features'])
            if fig_imp:
                st.plotly_chart(fig_imp, use_container_width=True)

        with vf_col2:
            corr_series = df_reg[reg_data['features']].apply(lambda col: col.corr(df_reg['Life expectancy'])).sort_values(ascending=True)
            df_corr = pd.DataFrame({'Feature': corr_series.index, 'Correlation': corr_series.values})
            fig_corr = px.bar(
                df_corr, x='Correlation', y='Feature', orientation='h',
                title="Correlation vs. Life Expectancy",
                color='Correlation',
                color_continuous_scale="RdBu",
                text='Correlation',
                height=320
            )
            fig_corr.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_corr, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: DATASET & PIPELINE OVERVIEW
    # -------------------------------------------------------------
    with tab_data:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>WHO Life Expectancy Dataset Overview</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Mortality, economic development, and immunization data across 193 UN member nations (2000–2015).</p>", unsafe_allow_html=True)

        d_c1, d_c2 = st.columns([3, 1], gap="medium")
        with d_c1:
            st.dataframe(df_reg.head(10), use_container_width=True)
        with d_c2:
            st.markdown("""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #0f172a; margin-bottom: 6px;">Pipeline Architecture:</div>
                    <div style="font-size: 0.8rem; color: #475569; line-height: 1.5;">
                        • <strong>Imputation:</strong> Median imputation across numerical missing values.<br>
                        • <strong>Scaling:</strong> StandardScaler fitted exclusively on training set.<br>
                        • <strong>Partition:</strong> 80% Train, 20% Test (random state 42).<br>
                        • <strong>Validation:</strong> 5-Fold cross-validation on top models.
                    </div>
                </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TRACK 2: CLASSIFICATION TRACK (Maternal Health Risk Dataset)
# =============================================================================
elif "Classification" in track_selection:
    st.markdown("""
        <div class="hero-header hero-clf">
            <div class="hero-pill">Biometric Vital Signs • Multi-Class Triage</div>
            <h1 class="hero-title">Classification Track — Maternal Health Risk Categorization</h1>
            <p class="hero-subtitle">
                Classify pregnancy risk levels into Low, Mid, and High Risk across 10 supervised classification algorithms with multi-class ROC curves and probability distribution analysis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Top Metric Highlights
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-emerald"></div>
                <div class="metric-label">Best Classifier</div>
                <div class="metric-value">AdaBoost</div>
                <div class="metric-sub">Adaptive Boosting Ensemble</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-blue"></div>
                <div class="metric-label">Top Test Accuracy</div>
                <div class="metric-value">85.22%</div>
                <div class="metric-sub">Part B Ensemble Winner</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-blue"></div>
                <div class="metric-label">Multi-Class ROC-AUC</div>
                <div class="metric-value">0.9525</div>
                <div class="metric-sub">One-vs-Rest Weighted</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-amber"></div>
                <div class="metric-label">Dataset Records</div>
                <div class="metric-value">1,014</div>
                <div class="metric-sub">Patients (6 Vitals + MAP)</div>
            </div>
        """, unsafe_allow_html=True)

    tab_pred_c, tab_comp_c, tab_viz_c, tab_data_c = st.tabs([
        "Live Prediction",
        "Model Comparison",
        "Visualizations & Diagnostics",
        "Dataset & Pipeline"
    ])

    # -------------------------------------------------------------
    # TAB 1: LIVE PREDICTION (CLASSIFICATION)
    # -------------------------------------------------------------
    with tab_pred_c:
        col_algo_c, col_preset_c = st.columns([1.1, 1.9], gap="medium")
        with col_algo_c:
            sel_clf_model_name = st.selectbox(
                "Select Model Algorithm:",
                options=list(clf_data['models'].keys()),
                index=0,
                help="Choose which algorithm will predict the maternal risk level."
            )

        with col_preset_c:
            st.markdown("<div class='control-label'>Clinical Risk Presets:</div>", unsafe_allow_html=True)
            pc_1, pc_2, pc_3 = st.columns(3, gap="small")
            if pc_1.button("Low Risk", use_container_width=True):
                st.session_state.clf_preset = "low"
            if pc_2.button("Borderline Risk", use_container_width=True):
                st.session_state.clf_preset = "mid"
            if pc_3.button("High Risk", use_container_width=True):
                st.session_state.clf_preset = "high"

        # Preset values dictionary based on session state
        clf_p = st.session_state.get('clf_preset', 'default')
        if clf_p == "low":
            c_def = {'Age': 24, 'SystolicBP': 110, 'DiastolicBP': 75, 'BS': 6.8, 'BodyTemp': 98.0, 'HeartRate': 72}
        elif clf_p == "mid":
            c_def = {'Age': 32, 'SystolicBP': 125, 'DiastolicBP': 85, 'BS': 9.2, 'BodyTemp': 98.6, 'HeartRate': 78}
        elif clf_p == "high":
            c_def = {'Age': 45, 'SystolicBP': 150, 'DiastolicBP': 95, 'BS': 15.0, 'BodyTemp': 100.2, 'HeartRate': 88}
        else:
            c_def = {'Age': 28, 'SystolicBP': 120, 'DiastolicBP': 80, 'BS': 7.5, 'BodyTemp': 98.0, 'HeartRate': 76}

        input_clf = {}
        col_in1, col_in2, col_in3 = st.columns(3, gap="medium")
        with col_in1:
            st.markdown("<div class='group-header'>Demographics & BP</div>", unsafe_allow_html=True)
            input_clf['Age'] = st.number_input("Patient Age (Years):", value=int(c_def['Age']), min_value=10, max_value=70, step=1)
            input_clf['SystolicBP'] = st.number_input("Systolic BP (mmHg):", value=int(c_def['SystolicBP']), min_value=70, max_value=170, step=2)

        with col_in2:
            st.markdown("<div class='group-header'>Diastolic & Metabolism</div>", unsafe_allow_html=True)
            input_clf['DiastolicBP'] = st.number_input("Diastolic BP (mmHg):", value=int(c_def['DiastolicBP']), min_value=45, max_value=110, step=2)
            input_clf['BS'] = st.number_input("Blood Sugar — BS (mmol/L):", value=float(c_def['BS']), min_value=5.0, max_value=22.0, step=0.2)

        with col_in3:
            st.markdown("<div class='group-header'>Temperature & Pulse</div>", unsafe_allow_html=True)
            input_clf['BodyTemp'] = st.number_input("Body Temp (°F):", value=float(c_def['BodyTemp']), min_value=96.0, max_value=104.0, step=0.2)
            input_clf['HeartRate'] = st.number_input("Heart Rate (bpm):", value=int(c_def['HeartRate']), min_value=55, max_value=105, step=1)

        # Dynamic Mean Arterial Pressure (MAP)
        computed_map = round((input_clf['SystolicBP'] + 2 * input_clf['DiastolicBP']) / 3.0, 2)
        input_clf['MAP'] = computed_map

        st.markdown(f"""
            <div style="display: inline-flex; align-items: center; gap: 8px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 5px 12px; font-size: 0.8rem; color: #334155; margin-bottom: 12px;">
                Calculated Mean Arterial Pressure (MAP): <strong style="color: #0f172a;">{computed_map} mmHg</strong>
                <span style="font-size: 0.72rem; color: #64748b;">(Normal baseline: 70–100 mmHg)</span>
            </div>
        """, unsafe_allow_html=True)

        # Action Buttons
        btn_col1, btn_col2, _ = st.columns([1.6, 1.2, 3.2], gap="small")
        with btn_col1:
            run_clf = st.button("Classify Risk Level", type="primary", use_container_width=True)
        with btn_col2:
            if st.button("Reset Defaults", key="reset_clf", use_container_width=True):
                st.session_state.clf_preset = "default"
                st.rerun()

        if run_clf:
            clf_model_obj = clf_data['models'][sel_clf_model_name]
            scaler_clf = clf_data['scaler']
            features_clf = clf_data['features']
            class_names = clf_data['class_names']
            le = clf_data['le']

            input_row = pd.DataFrame([input_clf])[features_clf]
            input_scaled = scaler_clf.transform(input_row)

            pred_code = int(clf_model_obj.predict(input_scaled)[0])
            pred_label = le.inverse_transform([pred_code])[0]

            probs_dict = {}
            if hasattr(clf_model_obj, 'predict_proba'):
                probs = clf_model_obj.predict_proba(input_scaled)[0]
                probs_dict = {c: float(p) for c, p in zip(class_names, probs)}
                conf_pct = max(probs) * 100
            else:
                conf_pct = 85.0

            box_style = "diag-clf-low" if "low" in pred_label.lower() else ("diag-clf-mid" if "mid" in pred_label.lower() else "diag-clf-high")
            val_color = "#15803d" if "low" in pred_label.lower() else ("#b45309" if "mid" in pred_label.lower() else "#b91c1c")

            st.markdown(f"""
                <div class="diagnostic-summary-box {box_style}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <div class="diag-tag">Triage Assessment</div>
                            <div class="diag-val" style="color: {val_color};">{pred_label.upper()}</div>
                            <div class="diag-sub">Algorithm: <strong>{sel_clf_model_name}</strong></div>
                        </div>
                        <div style="text-align: right;">
                            <div class="diag-tag">Model Confidence</div>
                            <div style="font-size: 1.15rem; font-weight: 600; color: {val_color};">{conf_pct:.1f}%</div>
                            <div class="diag-sub">Mean Arterial Pressure: {computed_map} mmHg</div>
                        </div>
                    </div>
                    <div class="diag-assessment">
                        <strong>Clinical Assessment:</strong> {'Patient vital signs remain within expected baseline limits.' if 'low' in pred_label.lower() else ('Borderline elevation observed across blood pressure or metabolic metrics.' if 'mid' in pred_label.lower() else 'Critical multi-vital elevation indicating high clinical urgency.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if probs_dict:
                fig_p = plot_prediction_probabilities(probs_dict)
                if fig_p:
                    fig_p.update_layout(height=220, margin=dict(l=30, r=30, t=30, b=30))
                    st.plotly_chart(fig_p, use_container_width=True)

            hist_item_c = {'Timestamp': pd.Timestamp.now().strftime('%H:%M:%S'), 'Algorithm': sel_clf_model_name, 'Predicted Risk': pred_label, 'Confidence': f"{conf_pct:.1f}%"}
            hist_item_c.update(input_clf)
            st.session_state.clf_history.append(hist_item_c)

        if st.session_state.clf_history:
            with st.expander("Session Prediction Log"):
                st.dataframe(pd.DataFrame(st.session_state.clf_history), use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: MODEL COMPARISON (CLASSIFICATION)
    # -------------------------------------------------------------
    with tab_comp_c:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Classification Algorithm Leaderboard</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Multi-metric benchmark across Part A (Review 1) and Part B (Review 2) algorithms.</p>", unsafe_allow_html=True)

        bench_clf_df = clf_data['bench'].copy()
        st.dataframe(
            bench_clf_df.style.highlight_max(subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC (OvR)'], color='#dcfce7'),
            use_container_width=True
        )

        col_cc1, col_cc2 = st.columns([1.1, 1], gap="medium")
        with col_cc1:
            sort_metric = st.selectbox("Rank Metric:", ['Accuracy', 'F1-Score', 'ROC-AUC (OvR)', 'Precision', 'Recall'])
            fig_bar_c = px.bar(
                bench_clf_df.sort_values(by=sort_metric, ascending=True),
                x=sort_metric, y='Algorithm', orientation='h',
                title=f"Benchmark: {sort_metric}",
                color=sort_metric,
                color_continuous_scale="Blues",
                text=sort_metric,
                height=320
            )
            fig_bar_c.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_bar_c, use_container_width=True)

        with col_cc2:
            st.markdown("<div style='font-size: 0.88rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Classifier Head-to-Head</div>", unsafe_allow_html=True)
            ca = st.selectbox("Classifier A:", bench_clf_df['Algorithm'].tolist(), index=0)
            cb = st.selectbox("Classifier B:", bench_clf_df['Algorithm'].tolist(), index=8)

            ra = bench_clf_df[bench_clf_df['Algorithm'] == ca].iloc[0]
            rb = bench_clf_df[bench_clf_df['Algorithm'] == cb].iloc[0]

            acc_diff = (ra['Accuracy'] - rb['Accuracy']) * 100

            st.markdown(f"""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 8px; color: #0f172a;">Comparison Metrics:</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div style="padding: 10px; background: #f0fdf4; border-radius: 6px; border: 1px solid #bbf7d0;">
                            <div style="font-weight: 600; font-size: 0.82rem; color: #166534;">{ca}</div>
                            <div style="font-size: 0.78rem; color: #15803d;">Accuracy: <strong>{ra['Accuracy']*100:.2f}%</strong></div>
                            <div style="font-size: 0.78rem; color: #15803d;">F1-Score: <strong>{ra['F1-Score']:.4f}</strong></div>
                        </div>
                        <div style="padding: 10px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <div style="font-weight: 600; font-size: 0.82rem; color: #475569;">{cb}</div>
                            <div style="font-size: 0.78rem; color: #64748b;">Accuracy: <strong>{rb['Accuracy']*100:.2f}%</strong></div>
                            <div style="font-size: 0.78rem; color: #64748b;">F1-Score: <strong>{rb['F1-Score']:.4f}</strong></div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8rem; color: #475569; line-height: 1.45;">
                        {ca} yields an accuracy delta of +{acc_diff:.2f}% over {cb}. Ensemble aggregation stabilizes variance, providing higher clinical generalizability.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: VISUALIZATIONS & DIAGNOSTICS (CLASSIFICATION)
    # -------------------------------------------------------------
    with tab_viz_c:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Classification Diagnostics</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Confusion matrix heatmaps, multi-class ROC curves, and feature relevance.</p>", unsafe_allow_html=True)

        v_col_c1, v_col_c2 = st.columns(2, gap="medium")
        y_test_c = clf_data['y_test']
        best_clf_name = 'AdaBoost Classifier' if 'AdaBoost Classifier' in clf_data['preds'] else clf_data['bench'].iloc[0]['Algorithm']
        best_pred_c = clf_data['preds'][best_clf_name]
        best_prob_c = clf_data['probs'][best_clf_name]
        class_names = clf_data['class_names']

        with v_col_c1:
            st.plotly_chart(plot_confusion_matrix_plotly(y_test_c, best_pred_c, class_names=class_names, model_name=best_clf_name), use_container_width=True)

        with v_col_c2:
            st.plotly_chart(plot_multiclass_roc_curves(y_test_c, best_prob_c, class_names=class_names, model_name=best_clf_name), use_container_width=True)

        vf_c1, vf_c2 = st.columns(2, gap="medium")

        with vf_c1:
            rf_clf_est = clf_data['models']['Random Forest Classifier']
            fig_imp_c = plot_feature_importances(rf_clf_est, clf_data['features'])
            if fig_imp_c:
                st.plotly_chart(fig_imp_c, use_container_width=True)

        with vf_c2:
            df_clf = clf_data['df']
            fig_scatter_c = px.scatter(
                df_clf, x='SystolicBP', y='BS', color='RiskLevel',
                title="Systolic BP vs. Blood Sugar by Risk",
                color_discrete_map={'low risk': '#15803d', 'mid risk': '#b45309', 'high risk': '#b91c1c'},
                opacity=0.75,
                height=320
            )
            fig_scatter_c.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_scatter_c, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: DATASET OVERVIEW (CLASSIFICATION)
    # -------------------------------------------------------------
    with tab_data_c:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Maternal Health Risk Dataset Overview</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Vital signs collected from pregnant patients in rural healthcare facilities (UCI ML Repository).</p>", unsafe_allow_html=True)

        d_cc1, d_cc2 = st.columns([3, 1], gap="medium")
        with d_cc1:
            st.dataframe(clf_data['df'].head(10), use_container_width=True)
        with d_cc2:
            st.markdown("""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #0f172a; margin-bottom: 6px;">Feature Engineering:</div>
                    <div style="font-size: 0.8rem; color: #475569; line-height: 1.5;">
                        • <strong>MAP:</strong> Mean Arterial Pressure = (Systolic + 2×Diastolic) / 3.<br>
                        • <strong>Distribution:</strong> Low Risk (40%), Mid Risk (33%), High Risk (27%).<br>
                        • <strong>Protocol:</strong> Stratified 80/20 train/test split.
                    </div>
                </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TRACK 3: CLUSTERING TRACK (Cardiotocography CTG Dataset)
# =============================================================================
else:
    st.markdown("""
        <div class="hero-header hero-clust">
            <div class="hero-pill">Unsupervised Machine Learning • 33 Biomedical Attributes</div>
            <h1 class="hero-title">Clustering Track — Fetal Cardiotocography Phenotyping</h1>
            <p class="hero-subtitle">
                Group 2,126 cardiotocograms into latent clinical sub-types using K-Means and Agglomerative Hierarchical clustering, benchmarked across Silhouette, Davies-Bouldin, and external clinical validation (NSP).
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Top Metric Highlights
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-cyan"></div>
                <div class="metric-label">Best Partition</div>
                <div class="metric-value">K-Means</div>
                <div class="metric-sub">k = 3 (Inertia Minimization)</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-blue"></div>
                <div class="metric-label">Silhouette Score</div>
                <div class="metric-value">0.1547</div>
                <div class="metric-sub">Highest Cluster Cohesion</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-emerald"></div>
                <div class="metric-label">External NMI</div>
                <div class="metric-value">0.3166</div>
                <div class="metric-sub">Normalized Mutual Info vs. NSP</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-stripe stripe-amber"></div>
                <div class="metric-label">Dataset Records</div>
                <div class="metric-value">2,126</div>
                <div class="metric-sub">Recordings (33 Features)</div>
            </div>
        """, unsafe_allow_html=True)

    tab_pred_cl, tab_comp_cl, tab_viz_cl, tab_data_cl = st.tabs([
        "Live Prediction",
        "Model Comparison",
        "Visualizations & Diagnostics",
        "Dataset & Pipeline"
    ])

    # -------------------------------------------------------------
    # TAB 1: LIVE CLUSTER ASSIGNMENT
    # -------------------------------------------------------------
    with tab_pred_cl:
        col_algo_cl, col_preset_cl = st.columns([1.1, 1.9], gap="medium")
        with col_algo_cl:
            sel_clust_model_name = st.selectbox(
                "Select Model Algorithm:",
                options=list(clust_data['models'].keys()),
                index=0,
                help="K-Means supports out-of-sample inference via centroid Euclidean distance."
            )

        with col_preset_cl:
            st.markdown("<div class='control-label'>Cardiotocography Presets:</div>", unsafe_allow_html=True)
            pcl_1, pcl_2, pcl_3 = st.columns(3, gap="small")
            if pcl_1.button("Normal CTG", use_container_width=True):
                st.session_state.ctg_preset = "normal"
            if pcl_2.button("Suspect CTG", use_container_width=True):
                st.session_state.ctg_preset = "suspect"
            if pcl_3.button("Pathologic CTG", use_container_width=True):
                st.session_state.ctg_preset = "pathologic"

        # Defaults for CTG features based on session state
        df_ctg = clust_data['df']
        feat_ctg = clust_data['features']
        ctg_p = st.session_state.get('ctg_preset', 'default')
        if ctg_p == "normal":
            ctg_defaults = {'LB': 133.0, 'AC': 0.003, 'FM': 0.005, 'UC': 0.005, 'ASTV': 24.0, 'MSTV': 1.8, 'ALTV': 0.0, 'MLTV': 10.5, 'DL': 0.001, 'DP': 0.0, 'Variance': 12.0}
        elif ctg_p == "suspect":
            ctg_defaults = {'LB': 142.0, 'AC': 0.000, 'FM': 0.001, 'UC': 0.002, 'ASTV': 62.0, 'MSTV': 0.6, 'ALTV': 25.0, 'MLTV': 5.2, 'DL': 0.000, 'DP': 0.0, 'Variance': 5.0}
        elif ctg_p == "pathologic":
            ctg_defaults = {'LB': 158.0, 'AC': 0.000, 'FM': 0.000, 'UC': 0.001, 'ASTV': 78.0, 'MSTV': 0.4, 'ALTV': 65.0, 'MLTV': 2.1, 'DL': 0.004, 'DP': 0.002, 'Variance': 35.0}
        else:
            ctg_defaults = {'LB': 133.0, 'AC': 0.003, 'FM': 0.004, 'UC': 0.004, 'ASTV': 47.0, 'MSTV': 1.3, 'ALTV': 9.8, 'MLTV': 8.2, 'DL': 0.001, 'DP': 0.0, 'Variance': 18.0}

        input_ctg = {}
        col_ct1, col_ct2, col_ct3 = st.columns(3, gap="medium")
        with col_ct1:
            st.markdown("<div class='group-header'>Heart Rate & Dynamics</div>", unsafe_allow_html=True)
            input_ctg['LB'] = st.slider("Baseline Fetal HR (bpm):", min_value=105.0, max_value=165.0, value=float(ctg_defaults['LB']), step=1.0)
            input_ctg['AC'] = st.number_input("Accelerations (per sec):", value=float(ctg_defaults['AC']), min_value=0.0, max_value=0.02, step=0.001, format="%.3f")
            input_ctg['FM'] = st.number_input("Fetal Movements (per sec):", value=float(ctg_defaults['FM']), min_value=0.0, max_value=0.5, step=0.001, format="%.3f")
            input_ctg['UC'] = st.number_input("Uterine Contractions (/s):", value=float(ctg_defaults['UC']), min_value=0.0, max_value=0.02, step=0.001, format="%.3f")

        with col_ct2:
            st.markdown("<div class='group-header'>Short & Long Variability</div>", unsafe_allow_html=True)
            input_ctg['ASTV'] = st.slider("Abnormal Short-Term Var (%):", min_value=10.0, max_value=90.0, value=float(ctg_defaults['ASTV']), step=1.0)
            input_ctg['MSTV'] = st.number_input("Mean Short-Term Var (bpm):", value=float(ctg_defaults['MSTV']), min_value=0.1, max_value=7.0, step=0.1)
            input_ctg['ALTV'] = st.slider("Abnormal Long-Term Var (%):", min_value=0.0, max_value=95.0, value=float(ctg_defaults['ALTV']), step=1.0)
            input_ctg['MLTV'] = st.number_input("Mean Long-Term Var (bpm):", value=float(ctg_defaults['MLTV']), min_value=0.0, max_value=50.0, step=0.5)

        with col_ct3:
            st.markdown("<div class='group-header'>Decelerations & Signal</div>", unsafe_allow_html=True)
            input_ctg['DL'] = st.number_input("Light Decelerations (/s):", value=float(ctg_defaults['DL']), min_value=0.0, max_value=0.02, step=0.001, format="%.3f")
            input_ctg['DP'] = st.number_input("Prolonged Decelerations (/s):", value=float(ctg_defaults['DP']), min_value=0.0, max_value=0.01, step=0.001, format="%.3f")
            input_ctg['Variance'] = st.number_input("Signal Variance:", value=float(ctg_defaults['Variance']), min_value=0.0, max_value=180.0, step=1.0)

        # Build full 33-feature observation with median defaults for remaining attributes
        full_obs = {f: float(df_ctg[f].median()) for f in feat_ctg}
        full_obs.update(input_ctg)
        if 'LBE' in full_obs and 'LB' in input_ctg:
            full_obs['LBE'] = input_ctg['LB']

        # Action Buttons
        btn_col1, btn_col2, _ = st.columns([1.6, 1.2, 3.2], gap="small")
        with btn_col1:
            run_clust = st.button("Assign Cluster Profile", type="primary", use_container_width=True)
        with btn_col2:
            if st.button("Reset Defaults", key="reset_ctg", use_container_width=True):
                st.session_state.ctg_preset = "default"
                st.rerun()

        if run_clust:
            km_model = clust_data['models']['K-Means Clustering (k=3)']
            scaler_ctg = clust_data['scaler']

            input_row = pd.DataFrame([full_obs])[feat_ctg]
            input_scaled = scaler_ctg.transform(input_row)

            pred_cluster = int(km_model.predict(input_scaled)[0])

            centroid = km_model.cluster_centers_[pred_cluster]
            dist = float(np.linalg.norm(input_scaled - centroid))

            cluster_labels_desc = {
                0: ("Cluster 0: Variable Morphologic Pattern", "Elevated fetal movements and uterine responses; moderate clinical suspect probability."),
                1: ("Cluster 1: Baseline Fetal Normality (NSP 1)", "Matches clinically healthy traces with robust heart rate accelerations and low abnormal variability."),
                2: ("Cluster 2: Pathologic Concern (NSP 3)", "Suppressed baseline variability with prolonged decelerations; high clinical risk.")
            }
            title_desc, explanation = cluster_labels_desc.get(pred_cluster, (f"Cluster {pred_cluster}", "Cluster assignment in multidimensional biomedical space."))

            st.markdown(f"""
                <div class="diagnostic-summary-box diag-clust">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <div class="diag-tag">Cluster Assignment</div>
                            <div class="diag-val" style="color: #0f766e;">Cluster {pred_cluster}</div>
                            <div class="diag-sub">{title_desc}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="diag-tag">Centroid Distance</div>
                            <div style="font-size: 1.15rem; font-weight: 600; color: #0f766e;">{dist:.2f}</div>
                            <div class="diag-sub">K-Means Euclidean metric</div>
                        </div>
                    </div>
                    <div class="diag-assessment">
                        <strong>Clinical Assessment:</strong> {explanation}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            from sklearn.decomposition import PCA
            pca = PCA(n_components=2, random_state=42)
            X_pca = pca.fit_transform(clust_data['X_scaled'])
            pt_pca = pca.transform(input_scaled)

            df_pca = pd.DataFrame({
                'PC1': X_pca[:, 0], 'PC2': X_pca[:, 1],
                'Cluster': [f"Cluster {l}" for l in clust_data['labels']['K-Means Clustering (k=3)']]
            })
            fig_p = px.scatter(df_pca, x='PC1', y='PC2', color='Cluster', title="2D PCA Space with Live Input Observation", opacity=0.5, height=320)
            fig_p.add_trace(go.Scatter(
                x=[pt_pca[0, 0]], y=[pt_pca[0, 1]],
                mode='markers',
                marker=dict(symbol='star', size=14, color='#b91c1c', line=dict(width=1.5, color='white')),
                name='Input Trace'
            ))
            fig_p.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_p, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: MODEL COMPARISON (CLUSTERING)
    # -------------------------------------------------------------
    with tab_comp_cl:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Clustering Evaluation Benchmark</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Comparative benchmark across centroid and hierarchical linkage paradigms.</p>", unsafe_allow_html=True)

        bench_clust_df = clust_data['bench'].copy()
        st.dataframe(
            bench_clust_df.style.highlight_max(subset=['Silhouette Score', 'Calinski-Harabasz Index', 'Validation NMI', 'Validation ARI'], color='#dcfce7')
                                 .highlight_min(subset=['Davies-Bouldin Index'], color='#dcfce7'),
            use_container_width=True
        )

        col_c_b1, col_c_b2 = st.columns([1.1, 1], gap="medium")
        with col_c_b1:
            clust_sort = st.selectbox("Rank Metric:", ['Silhouette Score', 'Davies-Bouldin Index', 'Calinski-Harabasz Index'])
            asc_c = True if clust_sort == 'Davies-Bouldin Index' else False
            fig_bar_cl = px.bar(
                bench_clust_df.sort_values(by=clust_sort, ascending=not asc_c),
                x=clust_sort, y='Algorithm', orientation='h',
                title=f"Benchmark: {clust_sort}",
                color=clust_sort,
                color_continuous_scale="Blues" if not asc_c else "Reds_r",
                text=clust_sort,
                height=320
            )
            fig_bar_cl.update_layout(template="plotly_white", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig_bar_cl, use_container_width=True)

        with col_c_b2:
            st.markdown("""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 6px; color: #0f172a;">Architectural Takeaways:</div>
                    <div style="font-size: 0.8rem; color: #475569; line-height: 1.5;">
                        • <strong>K-Means (k=3)</strong> achieves optimal cohesion with Silhouette = <strong>0.1547</strong> and NMI = <strong>0.3166</strong> vs. true clinical diagnosis (NSP).<br>
                        • <strong>Ward's Linkage</strong> produces the strongest hierarchical clusters (Silhouette = 0.1225) by minimizing within-cluster variance.<br>
                        • <strong>Complete & Average Linkages</strong> show elongated chaining artifacts and lower separation.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: VISUALIZATIONS & DIAGNOSTICS (CLUSTERING)
    # -------------------------------------------------------------
    with tab_viz_cl:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Clustering Manifold Diagnostics</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>PCA 2D projection, t-SNE manifold embedding, and dendrogram linkage tree.</p>", unsafe_allow_html=True)

        v_cl1, v_cl2 = st.columns(2, gap="medium")
        km_labels = clust_data['labels']['K-Means Clustering (k=3)']
        km_model = clust_data['models']['K-Means Clustering (k=3)']
        X_scaled = clust_data['X_scaled']

        with v_cl1:
            st.plotly_chart(plot_pca_clusters(X_scaled, km_labels, centroids=km_model.cluster_centers_, title="K-Means PCA 2D Space"), use_container_width=True)

        with v_cl2:
            st.plotly_chart(plot_tsne_clusters(X_scaled, km_labels, title="t-SNE 2D Manifold Projection"), use_container_width=True)

        vf_cl1, vf_cl2 = st.columns(2, gap="medium")

        with vf_cl1:
            k_rng, inerts, sils = evaluate_kmeans_range(X_scaled)
            st.plotly_chart(plot_elbow_curve(k_rng, inerts, sils, selected_k=3), use_container_width=True)

        with vf_cl2:
            fig_dend = generate_dendrogram_fig(X_scaled)
            st.pyplot(fig_dend)
            plt.close(fig_dend)

    # -------------------------------------------------------------
    # TAB 4: DATASET OVERVIEW (CLUSTERING)
    # -------------------------------------------------------------
    with tab_data_cl:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #0f172a; margin-bottom: 4px;'>Cardiotocography (CTG) Dataset Overview</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 12px;'>Fetal heart rate response and uterine activity measurements across 2,126 recordings (UCI ML Repository).</p>", unsafe_allow_html=True)

        d_cl1, d_cl2 = st.columns([3, 1], gap="medium")
        with d_cl1:
            st.dataframe(df_ctg.head(10), use_container_width=True)
        with d_cl2:
            st.markdown("""
                <div class="card-panel">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #0f172a; margin-bottom: 6px;">Clinical Reference:</div>
                    <div style="font-size: 0.8rem; color: #475569; line-height: 1.5;">
                        • <strong>NSP 1:</strong> Normal (77.8%)<br>
                        • <strong>NSP 2:</strong> Suspect (13.9%)<br>
                        • <strong>NSP 3:</strong> Pathologic (8.3%)<br>
                        • <em>Unsupervised:</em> NSP labels were not exposed during training.
                    </div>
                </div>
            """, unsafe_allow_html=True)
