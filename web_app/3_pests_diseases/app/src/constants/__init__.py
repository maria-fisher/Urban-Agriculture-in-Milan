from pathlib import Path

# Define the base directory path relative to the local file
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# # Define paths to the raw and preprocessed directories
# RAW_DIR = BASE_DIR / 'datasets' / 'raw'
# PROCESSED_DIR = BASE_DIR / 'datasets' / 'processed'
# CLASS_COUNTS_PATH = BASE_DIR/ 'datasets' / 'crop_class_counts.json'
# #configs 
# CONFIG_MODEL_TRAINING = BASE_DIR / 'config' / 'training_config.yaml'
# CONFIG_UPDATE_IMG = BASE_DIR / 'config' / 'model_image_size.yaml'

# # Define paths to pre-trainned weights
# PRE_TRAINED_WEIGHTS_DIR = BASE_DIR / 'saved_models' / 'pre_trained_weights'
# TRAINED_MODELS_DIR = BASE_DIR / 'saved_models' / 'trained_weights'

# # define paths to save eval results
# EXPERIMENT_LOGS = BASE_DIR/'experiment_tracking'
# EXPERIMENT_PATH = BASE_DIR / 'experiment_tracking'/'experiments.json'

# prediction configurations 
PREDICTION_CONFIG_PATH = BASE_DIR / 'prediction_artifacts' / 'pred_configs' / 'pred_configs.yaml'
STATE_DICT_DIR = BASE_DIR / 'prediction_artifacts' / 'trained_weights'

#Output Configs 
GUIDELINES_PATH = BASE_DIR / 'prediction_artifacts' / 'pred_configs' / 'guidelines.yaml'
INSIGHTS_PATH = BASE_DIR / 'prediction_artifacts' / 'pred_configs' / 'insights.yaml'
