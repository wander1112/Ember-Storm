# ⚡ ML Studio — Machine Learning Analytics Platform

A complete, professional, browser-based Machine Learning web application built using **Streamlit**, **Plotly**, and **Scikit-learn**.

ML Studio provides an end-to-end analytics workflow: upload datasets, perform interactive exploratory data analysis (EDA), detect and treat statistical outliers, engineer features, train and benchmark all **10 Regression algorithms**, **10 Classification algorithms**, and **2 Clustering algorithm families**, evaluate models via interactive diagnostic charts, make real-time predictions, and generate exportable reports.

---

## 🚀 Key Features

* **🎨 Modern Analytics UI:** Dark navy sidebar (`#0F172A`), light background, colorful dynamic metric cards, and responsive layouts.
* **📁 Dataset Ingestion:** CSV and Excel upload support, schema auditing, missing value detection, and 1-click loading of pre-configured sample datasets (Maternal Health Risk, WHO Life Expectancy, Cardiotocography CTG).
* **📊 Interactive EDA:** Histograms with distribution moments, box plots, 2D scatter plots with OLS trendlines, interactive correlation heatmaps, and automated data-derived observations.
* **🛠️ Preprocessing & Outlier Treatment:** Configurable missing-value imputation (median, mean, mode, drop), duplicate removal, Interquartile Range (IQR) outlier detection with Retain / Remove / Winsorize Cap options, and feature engineering presets (MAP, Immunization Index, custom formulas).
* **📈 Regression Track (10 Models):**
  1. Linear Regression
  2. Ridge Regression
  3. Lasso Regression
  4. ElasticNet Regression
  5. Polynomial Regression (degree 2)
  6. Decision Tree Regressor
  7. Random Forest Regressor
  8. Gradient Boosting Regressor
  9. Support Vector Regressor (SVR)
  10. K-Nearest Neighbors Regressor
  * Evaluated across $R^2$, RMSE, MAE, 5-fold cross-validated $R^2$ for top performers, GridSearchCV tuning, actual vs. predicted parity plots, residual scatter plots, and feature importances.
* **🎯 Classification Track (10 Models):**
  1. Logistic Regression
  2. K-Nearest Neighbors Classifier
  3. Gaussian Naive Bayes
  4. Decision Tree Classifier
  5. Support Vector Classifier (SVC)
  6. Random Forest Classifier
  7. AdaBoost Classifier
  8. Gradient Boosting Classifier
  9. Bagging Classifier (Decision Tree base)
  10. Multi-Layer Perceptron (MLP Neural Net)
  * Evaluated across Accuracy, Precision, Recall, Weighted F1-Score, Multi-Class One-vs-Rest (OvR) ROC-AUC, confusion matrix heatmaps, and multi-class ROC curves.
* **🌌 Clustering Track (2 Algorithm Families):**
  1. K-Means Clustering
  2. Agglomerative Hierarchical Clustering (Ward, Complete, Average linkages)
  * Unsupervised protocol (no training labels used), Elbow curve (inertia vs. $k$), Silhouette analysis, Hierarchical Dendrogram, 2D PCA cluster projection with centroids, t-SNE 2D manifold embedding, and post-hoc clinical ground-truth validation (ARI & NMI).
* **🔮 Live Prediction Engine:** Dedicated real-time prediction page generating dynamic input fields based on trained model features, input validation, class probabilities breakdown, and session prediction logging with CSV export.
* **📑 Reports & Exports:** Consolidated report compilation with Markdown and CSV table downloads.

---

## 📁 Project Architecture

```text
ml-studio/
├── app.py                      # Main Streamlit application controller
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation & deployment guide
├── .gitignore                  # Git exclusions
├── assets/
│   └── style.css               # Dark navy + light canvas styling system
├── modules/
│   ├── __init__.py
│   ├── data_loader.py          # CSV/Excel loader & dataset audit
│   ├── eda.py                  # Plotly charts & statistical moments
│   ├── outlier_detection.py    # IQR detection & treatment
│   ├── preprocessing.py        # Imputation, scaling & pipelines
│   ├── regression.py           # 10 Regression models & diagnostics
│   ├── classification.py       # 10 Classification models & ROC curves
│   ├── clustering.py           # K-Means, Hierarchical, PCA, t-SNE
│   ├── evaluation.py           # Model leaderboards & best-model selector
│   ├── prediction.py           # Dynamic inference engine
│   └── reports.py              # Report generation
├── data/                       # Preloaded sample datasets
└── models/                     # Saved model artifacts
```

---

## 💻 Local Installation & Running

1. **Navigate to the application folder:**
   ```bash
   cd ml-studio
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

4. The application will open automatically in your browser at `http://localhost:8501`.

---

## ☁️ Deployment to Streamlit Community Cloud

1. Commit and push the `ml-studio` directory to your GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Select your repository and branch.
4. Set the **Main file path** to:
   ```text
   ml-studio/app.py
   ```
5. Click **Deploy**. Streamlit Cloud will automatically install dependencies from `ml-studio/requirements.txt` and launch the live application.
