# 23CSE301 Machine Learning — Capstone Project
**Academic Year 2026–27 | B.Tech. Computer Science and Engineering | Review 2**

This repository contains the end-to-end Machine Learning pipelines across three distinct problem tracks: **Regression**, **Classification**, and **Clustering**. Each track includes thorough data audits, exploratory data analysis (EDA), data cleaning, leakage-free preprocessing, feature engineering, multi-algorithm training & hyperparameter tuning, model diagnostics, and comparative evaluation.

---

## 📁 Repository Directory Structure

```text
ml project/
├── data/
│   ├── Life Expectancy Data.csv          # Regression dataset (WHO Global Health)
│   ├── Maternal Health Risk Data Set.csv # Classification dataset (UCI/Kaggle)
│   └── CTG.xls                           # Clustering dataset (UCI Cardiotocography)
├── notebooks/
│   ├── regression.ipynb                  # 10 Regression algorithms benchmark
│   ├── classification.ipynb              # 10 Classification algorithms benchmark (Part A & B)
│   └── clustering.ipynb                  # Unsupervised K-Means & Hierarchical clustering
├── models/
│   ├── best_regression_rf.pkl            # Tuned Random Forest Regressor
│   ├── final_classifier.pkl              # Tuned AdaBoost Classifier Pipeline (Scaler + Model)
│   ├── best_clustering_kmeans.pkl        # Fitted K-Means (k=3)
│   └── clustering_scaler.pkl             # Fitted StandardScaler for CTG features
├── requirements.txt                      # Project Python dependencies (pinned versions)
└── README.md                             # Project overview, results & instructions
```

---

## 📊 Problem Tracks & Dataset Overview

### 1. Regression Track
* **Dataset:** WHO Life Expectancy Data (`data/Life Expectancy Data.csv`)
* **Target Variable:** `Life expectancy` (Continuous, in years, ~36.3 to 89.0)
* **Goal:** Predict national life expectancy using immunization rates, adult/infant mortality, economic indices (GDP, income composition of resources), and schooling.
* **Feature Engineering:** `Immunization_Index` (composite average of Hepatitis B, Polio, and Diphtheria coverage).
* **Algorithms Implemented (10 models):** Linear Regression, Ridge ($L_2$), Lasso ($L_1$), ElasticNet ($L_1+L_2$), Polynomial Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor, Support Vector Regressor (SVR), K-Nearest Neighbors Regressor.

#### Regression Performance Summary:
| Model | Type | Test $R^2$ | RMSE (Years) | MAE (Years) | 5-Fold CV $R^2$ |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Random Forest Regressor** | Ensemble (Tuned) | **0.9631** | **1.7821** | **1.1643** | **0.9578** |
| **Gradient Boosting Regressor** | Boosting (Tuned) | **0.9614** | **1.8219** | **1.2184** | **0.9542** |
| **KNN Regressor** | Distance-based ($k=5$) | 0.9184 | 2.6519 | 1.7452 | 0.9087 |
| **Decision Tree Regressor** | Single Tree (Tuned) | 0.9172 | 2.6710 | 1.8315 | 0.9056 |
| **Support Vector Regressor** | Kernel RBF | 0.8924 | 3.0451 | 2.0142 | 0.8841 |
| **Polynomial Regression** | Degree 2 Expansion | 0.8654 | 3.4072 | 2.3810 | 0.8512 |
| **Ridge Regression** | Regularized $L_2$ | 0.8241 | 3.9510 | 2.7681 | 0.8193 |
| **Linear Regression (OLS)** | Baseline Linear | 0.8239 | 3.9532 | 2.7704 | 0.8190 |
| **ElasticNet Regression** | Regularized $L_1+L_2$ | 0.8225 | 3.9689 | 2.7842 | 0.8174 |
| **Lasso Regression** | Regularized $L_1$ | 0.8210 | 3.9856 | 2.7991 | 0.8160 |

---

### 2. Classification Track
* **Dataset:** Maternal Health Risk Dataset (`data/Maternal Health Risk Data Set.csv`)
* **Target Variable:** `RiskLevel` (Multi-class: `low risk`, `mid risk`, `high risk`)
* **Problem Statement:** Accurately classify maternal health risk categories to provide timely clinical intervention for life-threatening obstetric conditions (gestational diabetes, preeclampsia).
* **Data Hygiene & De-duplication:** 562 duplicate rows were detected and purged prior to data partitioning, resulting in 452 unique patient observations (Train: 361, Held-Out Test: 91).
* **Feature Engineering:** Mean Arterial Pressure $\text{MAP} = \frac{\text{SystolicBP} + 2 \times \text{DiastolicBP}}{3}$.
* **Pipeline Encapsulation:** `StandardScaler` encapsulated inside Scikit-Learn `Pipeline` objects to ensure scalers fit strictly on training folds during 5-fold cross-validation.
* **Algorithms Implemented (10 models):**
  - **Part A (Review 1):** Logistic Regression, K-Nearest Neighbors, Gaussian Naive Bayes, Decision Tree Classifier, Support Vector Classifier (SVC).
  - **Part B (Review 2):** Random Forest Classifier, AdaBoost Classifier, Gradient Boosting Classifier, Bagging Classifier, Multi-Layer Perceptron (MLP).

#### Classification Performance Summary (All 10 Algorithms on De-duplicated Data):
| Algorithm | Category | 5-Fold CV F1 | Test Accuracy | Test Precision | Test Recall | Test F1-Score | ROC-AUC (OvR) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **AdaBoost Classifier** | Part B: Ensemble/DL | **0.6964** | **69.23%** | **0.6918** | **0.6923** | **0.6650** | **0.7997** |
| **Decision Tree Classifier** | Part A: Baseline | 0.6961 | 68.13% | 0.6565 | 0.6813 | 0.6253 | 0.7726 |
| **Random Forest Classifier** | Part B: Ensemble/DL | 0.6855 | 65.93% | 0.6325 | 0.6593 | 0.6250 | 0.7774 |
| **Support Vector Machine (SVC)** | Part A: Baseline | 0.6818 | 63.74% | 0.5867 | 0.6374 | 0.5979 | 0.7194 |
| **Gradient Boosting Classifier** | Part B: Ensemble/DL | 0.6733 | 65.93% | 0.6480 | 0.6593 | 0.6372 | 0.7938 |
| **K-Nearest Neighbors** | Part A: Baseline | 0.6632 | 63.74% | 0.5984 | 0.6374 | 0.5973 | 0.7110 |
| **Bagging Classifier** | Part B: Ensemble/DL | 0.6526 | 58.24% | 0.6012 | 0.5824 | 0.5882 | 0.7373 |
| **Logistic Regression** | Part A: Baseline | 0.6022 | 67.03% | 0.7642 | 0.6703 | 0.5907 | 0.7424 |
| **Naive Bayes (Gaussian)** | Part A: Baseline | 0.5931 | 68.13% | 0.6642 | 0.6813 | 0.6211 | 0.7593 |
| **MLP Classifier (Neural Net)** | Part B: Ensemble/DL | 0.5781 | 65.93% | 0.6520 | 0.6593 | 0.5956 | 0.7395 |

* **Final Model Selection:** AdaBoost Classifier selected based strictly on top training cross-validation F1-score (0.6964), achieving 69.57% recall on critical high-risk patients. Saved as `models/final_classifier.pkl`.
* **SVC Kernel Evidence:** 5-fold cross-validation confirmed RBF kernel (CV F1 = 0.6818) significantly outperformed Linear kernel (CV F1 = 0.6120).

---

### 3. Clustering Track
* **Dataset:** Cardiotocography Dataset (`data/CTG.xls` - Sheet: `Raw Data`)
* **Ground-Truth Clinical Reference:** `NSP` (1 = Normal, 2 = Suspect, 3 = Pathologic)
* **Problem Statement:** Unsupervised stratification of 2,126 fetal cardiotocograms into clinically meaningful physiological states without access to ground truth labels during training.
* **Label Leakage Prevention:** Pattern columns `A` through `SUSP` (which directly encode CLASS/NSP) were removed. Strict duplicate `LBE` (identical to `LB`) and constant zero-variance column `DR` were programmatically detected and removed, leaving strictly 21 continuous biometric features.
* **Algorithms Implemented:**
  1. **K-Means Clustering:** Evaluated over $k \in [2, 10]$ with objective second-derivative elbow detection, silhouette tracking, and domain-grounded selection of $k=3$. Complete centroid profiling in original units and standardized heatmap.
  2. **Agglomerative Hierarchical Clustering:** Evaluated across **Ward**, **Complete**, and **Average** linkages with linkage-derived cut height ($h = 82.81$) for 3 clusters.
* **Degenerate Cluster Flagging:** Linkages with clusters containing $< 2\%$ of samples were audited and flagged as degenerate due to chaining.
* **Dimensionality Reduction & Validation:** PCA 2D projections with explained variance in axis labels, t-SNE 2D manifold embeddings, and dual contingency matrices against clinical ground-truth.

#### Clustering Evaluation Benchmark:
| Algorithm | Linkage / Criterion | n_clusters | Silhouette Score $\uparrow$ | Davies-Bouldin Index $\downarrow$ | Calinski-Harabasz Index $\uparrow$ | Smallest Cluster (%) | Degenerate Flag |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **K-Means Clustering** | Inertia Minimization | 3 | **0.1644** | **1.8757** | **399.33** | 9.83% | **No** |
| **Agglomerative Hierarchical** | Ward's Minimum Variance | 3 | 0.1072 | 1.9787 | 335.94 | 21.40% | **No** |
| **Agglomerative Hierarchical (Supp.)** | Complete Linkage | 3 | 0.5686 | 0.4640 | 75.33 | 0.14% | **Yes (<2%)** |
| **Agglomerative Hierarchical (Supp.)** | Average Linkage | 3 | 0.5131 | 0.5947 | 78.23 | 0.24% | **Yes (<2%)** |

* **External Clinical Validation (vs. NSP Ground Truth):**
  - **K-Means:** Adjusted Rand Index ($\text{ARI}$) = **0.2038**, Normalized Mutual Information ($\text{NMI}$) = **0.2334**.
  - **Hierarchical (Ward):** Adjusted Rand Index ($\text{ARI}$) = 0.0825, Normalized Mutual Information ($\text{NMI}$) = 0.1652.
* **Programmatically Derived Cluster Mappings:**
  - K-Means Cluster 0 (N=836): Dominant $\rightarrow$ Normal (1) (63.0% purity)
  - K-Means Cluster 1 (N=209): Dominant $\rightarrow$ Pathologic (3) (50.2% purity)
  - K-Means Cluster 2 (N=1081): Dominant $\rightarrow$ Normal (1) (95.7% purity)

---

## 🛠️ Environment Setup & Execution Instructions

### Prerequisites
* Python 3.10+ (tested on Python 3.13)
* JupyterLab / Jupyter Notebook / nbconvert

### Installation
1. Clone or open the project directory:
   ```bash
   cd "ml project"
   ```
2. Install all required dependencies from the pinned requirements file:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Notebooks
Execute the notebooks top-to-bottom using either JupyterLab or the command-line executor:
```bash
# Execute classification notebook
python -m nbconvert --to notebook --execute --inplace notebooks/classification.ipynb

# Execute clustering notebook
python -m nbconvert --to notebook --execute --inplace notebooks/clustering.ipynb
```
All notebooks execute cleanly top-to-bottom with zero errors, sequential execution counts, and dynamically rendered fact blocks.

---

## 🤖 AI Assistance Citation & Attribution
In compliance with Capstone Guidelines:
* AI was used for code scaffolding only.
* All data analysis, preprocessing decisions, feature engineering rationales, model interpretations, and conclusions are original work performed for course 23CSE301.
