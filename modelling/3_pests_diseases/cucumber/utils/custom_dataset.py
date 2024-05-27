import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class CustomDataset(Dataset):
    def __init__(self, root_dir, split, transform=None):
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        self.data = []
        self.targets = []
        self.class_names = []
        
        # Determine the data directory based on the split
        data_dir = os.path.join(root_dir, split)
        
        # Walk through the class subfolders
        class_dirs = sorted(os.listdir(data_dir))
        for class_idx, class_dir in enumerate(class_dirs):
            class_path = os.path.join(data_dir, class_dir)
            self.class_names.append(class_dir)  # Store class names
            
            # Walk through the images in each class subfolder
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                self.data.append(img_path)
                self.targets.append(class_idx)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        img_path = self.data[idx]
        target = self.targets[idx]
        
        # Load the image
        image = Image.open(img_path)
        
        # Apply transformations if specified
        if self.transform:
            image = self.transform(image)
        
        return image, target
    
    def get_class_name(self, class_idx):
        return self.class_names[class_idx]
    
    def get_class_names(self):
        return self.class_names