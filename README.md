<h1 align="center" style="color:#2c3e50;">📧 Spam Classification Project</h1>

<p align="center" style="font-size:18px; color:#34495e;">
Welcome to the <b>Spam Classification</b> project!  
A powerful pipeline to detect spam emails using <b>Logistic Regression</b> and <b>TF-IDF</b> vectorization.
</p>

---

## 🚀 <span style="color:#2980b9;">Project Overview</span>

This project focuses on building and evaluating a **Logistic Regression** model to classify emails as spam or ham (non-spam). It includes:

<ul>
<li>📚 Text vectorization with <b>TF-IDF</b>.</li>
<li>⚙️ Optional dimensionality reduction to improve efficiency.</li>
<li>📊 Model training, evaluation, and visualization with ROC curves and classification reports.</li>
<li>🧪 Testing on unseen datasets to validate generalization.</li>
</ul>

---

## 🛠️ <span style="color:#16a085;">Step-by-Step Workflow</span>

Here’s a detailed explanation of each step performed in this project:

### 1️⃣ Data Loading and Preprocessing
- Loaded raw email data (text + labels).
- Cleaned text data by converting to lowercase and removing noise.
- Vectorized emails using **TF-IDF** to convert text into numerical features representing word importance.

### 2️⃣ Dimensionality Reduction (Optional)
- Applied **TruncatedSVD** to reduce high-dimensional TF-IDF features to fewer components (e.g., 300).
- This helps reduce memory consumption and speeds up training without major loss in information.

### 3️⃣ Model Training
- Used **Logistic Regression** as a baseline spam classifier.
- Logistic Regression is effective and interpretable for binary classification problems.
- Training performed either with:
  - A simple train-test split, or
  - **K-Fold Cross-Validation** (3, 5, or more folds) to robustly evaluate performance.

### 4️⃣ Model Evaluation
- Generated **Classification Reports** including precision, recall, f1-score, and accuracy.
- Precision/Recall balance analyzed for both classes (Ham and Spam).
- Produced **ROC Curves** for each fold or dataset to visualize trade-offs between true positive and false positive rates.
- Calculated **Area Under the Curve (AUC)** as a summary metric for classifier discrimination power.

### 5️⃣ Model Selection
- During cross-validation, tracked model performance per fold.
- Selected the model with the highest AUC as the **best model**.
- Saved this best model and the vectorizer for future predictions.

### 6️⃣ Testing on Unseen Data
- Applied the trained model on a completely new dataset to check generalization.
- Evaluated performance metrics again to confirm real-world effectiveness.

---

## 📂 <span style="color:#27ae60;">Folder Structure</span>

<table>
<tr>
<th align="left" style="padding-right:20px;">Folder</th>
<th align="left">Description</th>
</tr>
<tr>
<td><b>data/</b></td>
<td>Raw and processed datasets used for training and testing.</td>
</tr>
<tr>
<td><b>models/</b></td>
<td>Saved trained models and vectorizers for reuse.</td>
</tr>
<tr>
<td><b>notebooks/</b></td>
<td>Jupyter notebooks containing exploratory analysis and training workflows.</td>
</tr>
<tr>
<td><b>plots/</b></td>
<td>Visualizations such as ROC curves and confusion matrices.</td>
</tr>
<tr>
<td><b>scripts/</b></td>
<td>Python scripts for data preprocessing, training, and inference.</td>
</tr>
</table>

---

## 🧪 <span style="color:#8e44ad;">Model Evaluation Summary</span>

<table style="width:100%; border-collapse:collapse; font-size:16px;">
<thead style="background:#dcdde1;">
<tr>
<th align="left" style="padding:8px;">Label</th>
<th style="padding:8px;">Precision</th>
<th style="padding:8px;">Recall</th>
<th style="padding:8px;">F1-Score</th>
<th style="padding:8px;">Support</th>
</tr>
</thead>
<tbody>
<tr style="background:#f8f9fa;">
<td><b>Ham (0)</b></td>
<td style="text-align:center;">0.96</td>
<td style="text-align:center;">0.80</td>
<td style="text-align:center;">0.88</td>
<td style="text-align:center;">3900</td>
</tr>
<tr>
<td><b>Spam (1)</b></td>
<td style="text-align:center;">0.70</td>
<td style="text-align:center;">0.94</td>
<td style="text-align:center;">0.80</td>
<td style="text-align:center;">1896</td>
</tr>
<tr style="background:#dff9fb;">
<td><b>Overall</b></td>
<td colspan="4" style="text-align:center;">
🎯 <b>Accuracy:</b> 85% &nbsp;&nbsp;&nbsp; 📊 <b>Macro Avg F1-Score:</b> 0.84 &nbsp;&nbsp;&nbsp; 🧠 <b>Weighted Avg F1-Score:</b> 0.85
</td>
</tr>
</tbody>
</table>

---

## 💡 <span style="color:#e67e22;">Insights & Next Steps</span>

> - The classifier performs well in distinguishing spam from legitimate emails.  
> - Some false positives occur where legitimate emails are classified as spam.  
> - Future improvements may include:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Experimenting with advanced models (Random Forests, SVMs, transformers).  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Tuning feature extraction and hyperparameters.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Expanding the dataset for better generalization.

---

## 🛠️ <span style="color:#16a085;">How to Use</span>

```bash
# Install dependencies
pip install -r requirements.txt
````

```python
# Run training script or notebook
python train_model.py

# Use saved model to predict on new data
python predict.py --input new_emails.csv
```

---

## 📬 <span style="color:#c0392b;">Contact & Contribution</span>

For questions or contributions, please open an issue or submit a pull request.
We welcome your feedback and improvements!

---

<p align="center" style="font-size:14px; color:#7f8c8d;">
Thank you for exploring this project! Stay safe and spam-free! 🚫📧
</p>
```

