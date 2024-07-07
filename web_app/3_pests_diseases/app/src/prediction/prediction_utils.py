import torch
import torch.nn.functional as F
import torchvision.transforms as transforms


#calculate energy_score
def energy_score(logits, temperature=1):
    energy = -temperature * torch.logsumexp(logits / temperature, dim=1)
    return energy

# prediction on single image 
def predict_single_image(image, config, model, device):

    # Apply transformations
    preprocess = transforms.Compose([
        transforms.Resize((config['resize'], config['resize'])),
        transforms.CenterCrop((config['center_crop'], config['center_crop'])),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image_tr = preprocess(image)
    image_tr = image_tr.unsqueeze(0).to(device)

    # Predict the class with inference mode for optimization
    with torch.inference_mode():
        outputs = model(image_tr)

    # Calculate energy score
    e_score = energy_score(outputs).item()
    if e_score >config['energy_threshold']:
        return 'Unknown', 0.0

    # Calculate probabilities and predictions
    probabilities = F.softmax(outputs, dim=1)
    predicted_index = torch.argmax(probabilities, dim=1).item()
    predicted_class_name = config['class_map'][predicted_index]
    prediction_probability = probabilities[0][predicted_index].item()

    return predicted_class_name, prediction_probability
