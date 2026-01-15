import streamlit as st
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn.functional as F
from PIL import Image
import requests
import pandas as pd

# ------------------------------- #
# Page Setup #
# ------------------------------- #
st.set_page_config(
    page_title="Real-Time Image Classifier",
    layout="wide"
)

# ------------------------------- #
# Title and Caption #
# ------------------------------- #
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📷 Live Image Classification</h1>", unsafe_allow_html=True)
st.caption("Using Pretrained ResNet-18 Model | Computer Vision with OpenCV Output")

# ------------------------------- #
# Step 1: Library Setup #
# ------------------------------- #
device = torch.device("cpu")

# ------------------------------- #
# Step 2: Fetch ImageNet Class Labels #
# ------------------------------- #
IMAGENET_CLASSES_URL = "https://raw.githubusercontent.com/pytorch/hub/mast
import streamlit as st
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn.functional as F
from PIL import Image
import requests
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Real-Time Image Classification",
    layout="centered"
)

st.title("📷 Real-Time Image Classification Web App")
st.caption("Pretrained ResNet-18 | OpenCV-style Computer Vision Output")

# -------------------------------
# Step 1: Import libraries
# -------------------------------
device = torch.device("cpu")

# -------------------------------
# Step 2: Download ImageNet class labels
# -------------------------------
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
labels_response = requests.get(LABELS_URL)
imagenet_labels = labels_response.text.splitlines()

# -------------------------------
# Step 3: Load pretrained ResNet-18
# -------------------------------
model = models.resnet18(pretrained=True)
model.eval()
model.to(device)

# -------------------------------
# Step 4: Image preprocessing pipeline
# -------------------------------
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -------------------------------
# Step 5: Capture image from webcam
# -------------------------------
st.subheader("📸 Capture Image")
captured_image = st.camera_input("Take a picture using your webcam")

if captured_image is not None:
    image = Image.open(captured_image).convert("RGB")

    st.image(image, caption="Captured Image", use_column_width=True)

    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0).to(device)

    # -------------------------------
    # Step 6: Model prediction & softmax
    # -------------------------------
    with torch.no_grad():
        output = model(input_batch)

    probabilities = F.softmax(output[0], dim=0)

    top5_prob, top5_idx = torch.topk(probabilities, 5)

    results = pd.DataFrame({
        "Class Label": [imagenet_labels[i] for i in top5_idx],
        "Probability": top5_prob.cpu().numpy()
    })

    # -------------------------------
    # Display results
    # -------------------------------
    st.subheader("🔍 Top-5 Predictions")
    st.dataframe(results, use_container_width=True)

    st.bar_chart(
        results.set_index("Class Label"),
        horizontal=True
    )

    st.success(
        f"Top Prediction: {results.iloc[0]['Class Label']} "
        f"({results.iloc[0]['Probability']:.2%})"
    )

    st.info(
        "Softmax probabilities represent the confidence level of each predicted class."
    )
