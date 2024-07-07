import os
import torch
import torch.nn as nn
import torchvision.models as models

# select model architecture and load the model with stat dict 

class ModelSelector:
    """
    A class to select and configure a pre-trained model for multi-class classification.

    This class provides functionality to select a pre-trained model from torchvision, 
    load its pre-trained weights, and modify its architecture for a specific classification task 
    with an additional dropout layer for regularization.

    Attributes:
        model_name (str): The name of the pre-trained model to use. Supported models are 'resnet34', 
                          'resnet50', 'efficientnet_b0', and 'efficientnet_b1'. 'efficientnet_b2'
        num_classes (int): The number of classes for the classification task.
        dropout_rate (float): The dropout rate for regularization.

    Methods:
        select_model():
            Selects the specified pre-trained model, loads its weights, freezes its parameters,
            and modifies its architecture for the classification task.
    """
    def __init__(self,config):
        """
      Initializes the ModelSelector with the specified parameters.

        Parameters:
            config (dict): A dictionary containing 'model_name' (str), 'num_classes' (int), 
                           'dropout' (float), and 'hidden_units' (int) keys.
        """
        self.model_name = config['model_name']
        self.num_classes = config['num_classes']
        self.dropout =config['dropout']
        self.hidden_units = config['hidden_units']
 

    def select_model(self):
        """
        Selects a pre-trained model based on the configured 'model_name', loads its pre-trained weights,
        freezes its parameters, and modifies its architecture for the classification task.

        Returns:
            torch.nn.Module: The modified pre-trained model with the specified architecture.
        """
        model_name = self.model_name
        base_model = None
        num_ftrs = 0

        if model_name == 'resnet18':
            base_model = models.resnet18(weights=None)
            num_ftrs = base_model.fc.in_features
        
        elif model_name == 'resnet34':
            base_model = models.resnet34(weights=None)
            num_ftrs = base_model.fc.in_features

        elif model_name == 'resnet50':
            base_model = models.resnet50(weights=None)
            num_ftrs = base_model.fc.in_features

        elif model_name == 'efficientnet_b0':
            base_model = models.efficientnet_b0(weights=None)
            num_ftrs = base_model.classifier[1].in_features

        elif model_name == 'efficientnet_b1':
            base_model = models.efficientnet_b1(weights=None)
            num_ftrs = base_model.classifier[1].in_features

        elif model_name == 'efficientnet_b2':
            base_model = models.efficientnet_b2(weights=None)
            num_ftrs = base_model.classifier[1].in_features

        elif model_name == 'efficientnet_b3':
            base_model = models.efficientnet_b3(weights=None)
            num_ftrs = base_model.classifier[1].in_features   

        elif model_name == 'efficientnet_b4':
            base_model = models.efficientnet_b4(weights=None)
            num_ftrs = base_model.classifier[1].in_features  
        
        elif model_name == 'efficientnet_b7':
            base_model = models.efficientnet_b7(weights=None)
            num_ftrs = base_model.classifier[1].in_features  
        else:
            raise ValueError(f"Model {self.model_name} is not supported. Choose from 'resnet18','resnet34', 'resnet50', 'efficientnet_b0', 'efficientnet_b1', 'efficientnet_b2','efficientnet_b3', 'efficientnet_b4' .")

       

        # Freeze the pre-trained model parameters
        for param in base_model.parameters():
            param.requires_grad = False
        
        # Modify the last fully connected layer in renset archtecture according the the trained model architecture
        if 'resnet' in model_name:

            base_model.fc = nn.Sequential(
                    nn.Linear(num_ftrs, self.hidden_units),
                    nn.ReLU(),
                    nn.Dropout(p=self.dropout),
                    nn.Linear( self.hidden_units, self.num_classes)
                )
            
        # Modify the final layer(classifer) in efficientnet architecture   
        elif 'efficientnet' in model_name :
            base_model.classifier = nn.Sequential(
                    nn.Dropout(p=self.dropout, inplace=True),
                    nn.Linear(num_ftrs, self.hidden_units),
                    nn.ReLU(),
                    nn.Dropout(p=self.dropout),
                    nn.Linear(self.hidden_units, self.num_classes)
                )
        
     

        return base_model
    
    


def load_model(file_path, config):
    """
    Load a pre-trained model from a file.

    This function attempts to load a pre-trained model from the specified file path. 
    If the loaded object is a dictionary, it's assumed to be a state_dict, and the function 
    will use the ModelSelector class to select and configure a pre-trained model based on 
    the provided configuration. The '_orig_mod.' prefix in the state_dict keys is removed 
    before loading the model's state_dict. If the loaded object is not a dictionary, it's 
    assumed to be a complete model, and it's returned as is.

    Parameters:
    file_path (str): The file path from which to load the model.
    config (dict): A dictionary containing the configuration parameters for the model. 
                   It should contain 'model_name' (str), 'num_classes' (int), 'dropout' (float), 
                   and 'hidden_units' (int) keys.

    Returns:
    torch.nn.Module: The loaded pre-trained model.

    Raises:
    ValueError: If an error occurs while loading the model.
    """
    # Try to load the file as a complete model
    try:
        loaded_model = torch.load(file_path)
        
        # If the loaded object is a dictionary, it's likely a state_dict
        if isinstance(loaded_model, dict):
            model_selector = ModelSelector(config=config)
            model = model_selector.select_model()
            # Remove the '_orig_mod.' prefix from the keys in the state_dict
            new_state_dict = {k.replace('_orig_mod.', ''): v for k, v in loaded_model.items()}
            model.load_state_dict(new_state_dict)
        else:
            # Otherwise, it's a complete model
            model = loaded_model

        model.eval()
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")

    return model
