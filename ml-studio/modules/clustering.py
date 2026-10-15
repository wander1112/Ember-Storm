"""
Clustering Track Module
K-Means and Agglomerative Hierarchical Clustering, Elbow Curve, Dendrogram, PCA, and t-SNE.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import (
    silhouette_score, davies_bouldin_score, calinski_harabasz_score,
    adjusted_rand_score, normalized_mutual_info_score
)
from scipy.cluster.hierarchy import dendrogram, linkage

def evaluate_kmeans_range(X_scaled, k_range=range(2, 9)):
    """
    Compute Inertia and Silhouette scores across cluster counts for Elbow curve.
    """
    inertias = []
    sil_scores = []
    
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(float(km.inertia_))
        sil_scores.append(float(silhouette_score(X_scaled, labels)))
        
    return list(k_range), inertias, sil_scores

def plot_elbow_curve(k_range, inertias, sil_scores, selected_k=3):
    """
    Interactive Plotly figure showing Elbow and Silhouette curves.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=k_range, y=inertias,
        mode='lines+markers',
        name='Inertia (Within-Cluster SS)',
        line=dict(color='#2563eb', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_vline(x=selected_k, line_dash="dash", line_color="#ef4444", annotation_text=f"Selected k={selected_k}")
    
    fig.update_layout(
        title="Elbow Curve: Inertia vs. Number of Clusters (k)",
        xaxis_title="Number of Clusters (k)",
        yaxis_title="Inertia",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def train_clustering_models(X_scaled, n_clusters=3, ground_truth=None):
    """
    Train K-Means and Hierarchical Clustering models and compute all metrics.
    """
    # 1. K-Means
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    km_labels = km.fit_predict(X_scaled)
    
    # 2. Agglomerative (Ward)
    agg_ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward_labels = agg_ward.fit_predict(X_scaled)
    
    # 3. Agglomerative (Complete)
    agg_comp = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete')
    comp_labels = agg_comp.fit_predict(X_scaled)
    
    # 4. Agglomerative (Average)
    agg_avg = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    avg_labels = agg_avg.fit_predict(X_scaled)
    
    experiments = [
        ('K-Means Clustering', 'Inertia Minimization', km_labels, km),
        ('Agglomerative Hierarchical', "Ward's Linkage", ward_labels, agg_ward),
        ('Agglomerative Hierarchical', 'Complete Linkage', comp_labels, agg_comp),
        ('Agglomerative Hierarchical', 'Average Linkage', avg_labels, agg_avg)
    ]
    
    summary = []
    models_dict = {}
    labels_dict = {}
    
    for name, link, labels, model in experiments:
        sil = float(silhouette_score(X_scaled, labels))
        db = float(davies_bouldin_score(X_scaled, labels))
        ch = float(calinski_harabasz_score(X_scaled, labels))
        
        row = {
            'Algorithm': name,
            'Linkage / Criterion': link,
            'Silhouette Score': round(sil, 4),
            'Davies-Bouldin Index': round(db, 4),
            'Calinski-Harabasz Index': round(ch, 2)
        }
        
        if ground_truth is not None:
            ari = float(adjusted_rand_score(ground_truth, labels))
            nmi = float(normalized_mutual_info_score(ground_truth, labels))
            row['Validation ARI'] = round(ari, 4)
            row['Validation NMI'] = round(nmi, 4)
            
        summary.append(row)
        key = f"{name} ({link})"
        models_dict[key] = model
        labels_dict[key] = labels
        
    res_df = pd.DataFrame(summary).sort_values(by='Silhouette Score', ascending=False).reset_index(drop=True)
    return res_df, models_dict, labels_dict

def plot_pca_clusters(X_scaled, labels, centroids=None, title="PCA 2D Cluster Visualisation"):
    """
    Project high-dimensional data to 2D PCA space with cluster coloring.
    """
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    df_pca = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Cluster': [f"Cluster {l}" for l in labels]
    })
    
    fig = px.scatter(
        df_pca, x='PC1', y='PC2', color='Cluster',
        title=f"{title} (Explained Var: {pca.explained_variance_ratio_.sum()*100:.1f}%)",
        color_discrete_sequence=px.colors.qualitative.Bold,
        opacity=0.75
    )
    
    if centroids is not None:
        centroids_pca = pca.transform(centroids)
        fig.add_trace(go.Scatter(
            x=centroids_pca[:, 0], y=centroids_pca[:, 1],
            mode='markers',
            marker=dict(symbol='x', size=14, color='red', line=dict(width=2, color='black')),
            name='Centroids'
        ))
        
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=50, b=40))
    return fig

def plot_tsne_clusters(X_scaled, labels, title="t-SNE 2D Manifold Visualisation"):
    """
    Project data into 2D using t-SNE for non-linear manifold validation.
    """
    # Sample if dataset is very large for responsiveness
    sample_size = min(len(X_scaled), 1000)
    idx = np.random.choice(len(X_scaled), sample_size, replace=False)
    
    tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=800)
    X_tsne = tsne.fit_transform(X_scaled[idx])
    
    df_tsne = pd.DataFrame({
        'Dim1': X_tsne[:, 0],
        'Dim2': X_tsne[:, 1],
        'Cluster': [f"Cluster {l}" for l in np.array(labels)[idx]]
    })
    
    fig = px.scatter(
        df_tsne, x='Dim1', y='Dim2', color='Cluster',
        title=title,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        opacity=0.75
    )
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=50, b=40))
    return fig

def generate_dendrogram_fig(X_scaled, max_samples=120):
    """
    Generate hierarchical dendrogram using Matplotlib.
    """
    np.random.seed(42)
    idx = np.random.choice(len(X_scaled), min(len(X_scaled), max_samples), replace=False)
    X_sub = X_scaled[idx]
    
    linkage_matrix = linkage(X_sub, method='ward')
    
    fig, ax = plt.subplots(figsize=(10, 4.5))
    dendrogram(linkage_matrix, truncate_mode='level', p=4, show_leaf_counts=True, ax=ax)
    ax.set_title("Hierarchical Clustering Dendrogram (Ward Linkage, Sample)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Sample Index or Cluster Size")
    ax.set_ylabel("Ward Distance")
    plt.tight_layout()
    return fig
