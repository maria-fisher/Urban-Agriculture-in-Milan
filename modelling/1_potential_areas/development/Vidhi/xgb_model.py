import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import metrics
import optuna
from xgboost import XGBClassifier
import mlflow
import mlflow.sklearn
import os
from matplotlib import pyplot as plt
import warnings
import pickle
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

warnings.filterwarnings("ignore")

# Set tracking URI and experiment
mlflow.set_experiment("Urban_Farming_Prediction_XGBClassifier")

# Load the dataset
dataset = pd.read_csv("dataset/Merged_2014.csv")

# Listing numerical and categorical features
numerical_cols = dataset.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical_cols.remove('Suitable_Areas')
categorical_cols = dataset.select_dtypes(include=['object']).columns.tolist()

log_columns = ["NDVI", "LST", "NDBI", "NDWI", "Roughness", "SAVI", "Slope", "SMI", "solar_radiation"]

# Apply log transformation
for col in log_columns:
    dataset[col] = dataset[col].apply(lambda x: np.log(x) if x > 0 else x)

# Create preprocessing steps
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Train test split
X = dataset.drop(columns=['Suitable_Areas'])
y = dataset['Suitable_Areas']
RANDOM_SEED = 6

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y)

# Hyperparameter Optimization with Optuna for XGBClassifier
def objective(trial):
    param = {
        'verbosity': 0,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'booster': 'gbtree',
        'lambda': trial.suggest_loguniform('lambda', 1e-3, 10.0),
        'alpha': trial.suggest_loguniform('alpha', 1e-3, 10.0),
        'subsample': trial.suggest_float('subsample', 0.4, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.4, 1.0),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 9),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'scale_pos_weight': trial.suggest_float('scale_pos_weight', 0.1, 10)
    }

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(**param))
    ])

    score = cross_val_score(model, X_train, y_train, cv=3, scoring='roc_auc').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print('Number of finished trials:', len(study.trials))
print('\n Best trial:', study.best_trial.params, "\n ")

# Train XGBClassifier with best hyperparameters
best_params = study.best_trial.params
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(**best_params))
])
full_pipeline.fit(X_train, y_train)

# Calculate Mean CV score for logging
mean_cv_score = cross_val_score(full_pipeline, X_train, y_train, cv=3, scoring='roc_auc').mean()

# Model evaluation metrics (keep this function as is)
def eval_metrics(actual, pred, pred_proba=None):
    accuracy = metrics.accuracy_score(actual, pred)
    f1 = metrics.f1_score(actual, pred, pos_label=1)
    precision = metrics.precision_score(actual, pred, pos_label=1)
    recall = metrics.recall_score(actual, pred, pos_label=1)
    if pred_proba is not None:
        fpr, tpr, _ = metrics.roc_curve(actual, pred_proba)
        auc = metrics.auc(fpr, tpr)
        plt.figure(figsize=(8, 8))
        plt.plot(fpr, tpr, color='blue', label='ROC curve area = %0.2f' % auc)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([-0.1, 1.1])
        plt.ylim([-0.1, 1.1])
        plt.xlabel('False Positive Rate', size=14)
        plt.ylabel('True Positive Rate', size=14)
        plt.legend(loc='lower right')
        # Save plot
        os.makedirs("plots", exist_ok=True)
        plt.savefig("plots/ROC_curve_XGBClassifier.png")
        # Close plot
        plt.close()
    else:
        auc = float('nan')
    return accuracy, f1, precision, recall, auc    

# Modify the mlflow_logging function to use the full pipeline
def mlflow_logging(pipeline, X, y, name, mean_cv_score, use_proba=False):
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.set_tag("run_id", run_id)
        if use_proba:
            pred_proba = pipeline.predict_proba(X)[:, 1]
            pred = (pred_proba > 0.5).astype(int)
            accuracy, f1, precision, recall, auc = eval_metrics(y, pred, pred_proba)
        else:
            pred = pipeline.predict(X)
            accuracy, f1, precision, recall, auc = eval_metrics(y, pred)
        
        # Logging best parameters
        mlflow.log_params(best_params)
        
        # Log the metrics
        mlflow.log_metric("Mean CV score", mean_cv_score)
        mlflow.log_metric("Accuracy", accuracy)
        mlflow.log_metric("f1-score", f1)
        mlflow.log_metric("Precision", precision)
        mlflow.log_metric("Recall", recall)
        mlflow.log_metric("AUC", auc)

        # Logging artifacts and model
        if use_proba:
            mlflow.log_artifact("plots/ROC_curve_XGBClassifier.png")
        mlflow.sklearn.log_model(pipeline, name)
        
        mlflow.end_run()

mlflow_logging(full_pipeline, X_test, y_test, "XGBClassifier_Pipeline", mean_cv_score, use_proba=True)

# Save the full pipeline (including preprocessing) as a pickle file
with open('XGBClassifier_Pipeline_Optuna_Vidhi.pkl', 'wb') as file:
    pickle.dump(full_pipeline, file)

print("Full pipeline (preprocessing + model) saved as XGBClassifier_Pipeline_Optuna_Vidhi.pkl")