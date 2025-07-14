import torch
import torch.nn as nn
from torchvision import transforms, models, datasets
from torch.utils.data import DataLoader
from PIL import Image
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm
from torchvision import transforms

# ✅ 1. 설정
MODEL_PATH = "efficientNetB0_0712_test_best_burger_model.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ 2. transform 정의 (학습 시 사용한 것과 동일해야 함)
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # EfficientNet-B0 입력 크기
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # ImageNet 평균
                         std=[0.229, 0.224, 0.225])
])

# ✅ 3. 클래스 이름 정의 (ImageFolder에서 자동 추출한 순서 기준)
class_names = ['hamburger', 'not_hamburger']  # 순서가 중요한 경우 ImageFolder 써서 정확히 매칭해야 함

# ✅ 4. 모델 정의 및 로딩
model = models.efficientnet_b0(weights=None) # 이걸 쓰는 이유는? 
model.classifier[1] = nn.Linear(1280, 1)  # 출력층 수정
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

# ✅ 5. 테스트셋 평가 (선택)
def evaluate_testset(test_dir):
    test_dataset = datasets.ImageFolder(test_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    y_true, y_pred = [], []

    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="[Test]"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            preds = torch.argmax(outputs, dim=1)

            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print("\n🧪 Test Set 평가 결과:")
    print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1 Score: {f1:.4f}")

# ✅ 6. 단일 이미지 예측 함수
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probability = torch.sigmoid(output).item()  # 시그모이드로 확률 계산
        predicted_class = 1 if probability > 0.5 else 0
        confidence = probability if predicted_class == 1 else (1 - probability)

    return class_names[predicted_class], confidence

# ✅ 7. 사용 예시
if __name__ == "__main__":
    # (1) 테스트셋 평가
    test_folder = r"C:\Users\baby3\ai_x\source\Project\0711~0713 성미정리\3.ml_data\1. 모델 구성\model_data\test"
    evaluate_testset(test_folder)

    # (2) 이미지 예측
    # ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★  여기에 테스트용 이미지 바꾸기!!!!!!!
    image_path = r"https://i.ytimg.com/vi/ptOvSbyi6pY/maxresdefault.jpg"
    result, prob = predict(image_path)
    print(f"\n📷 예측 결과: {result} (신뢰도: {prob:.4f})")