import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 하이퍼파라미터
BATCH_SIZE = 16
EPOCHS = 10
LR = 1e-4
MODEL_PATH = "best_model.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 📦 1. 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)), # resize  244,244로 학습되었기 때문에 맞춰야 함 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], # 이미지 정규화 - 모델이 안정적으로 학습할 수 있게 도와주는 전처리
                         std=[0.229, 0.224, 0.225])
])

# 📂 2. 데이터 불러오기
train_dataset = datasets.ImageFolder(r"C:\Users\baby3\OneDrive\바탕 화면\햄버거 테스트용\model_data\train", transform=transform)
val_dataset = datasets.ImageFolder(r"C:\Users\baby3\OneDrive\바탕 화면\햄버거 테스트용\model_data\val", transform=transform)
test_dataset = datasets.ImageFolder(r"C:\Users\baby3\OneDrive\바탕 화면\햄버거 테스트용\model_data\test", transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

class_names = train_dataset.classes  # ['burger', 'non_burger']

# 🧠 3. EfficientNet-B0 모델
model = models.efficientnet_b0(pretrained=True) #ImageNet 기준으로 학습된 가중치 포함
model.classifier[1] = nn.Linear(1280, 2) # 마지막 출력층 수정 (1280개를 받아서 2개로 출력)
model = model.to(device)   # 모델 GPU  또는 CPU로 이동 

criterion = nn.CrossEntropyLoss()               # 손실함수 정의 : 다중 클래스 분류에 적합한 교차 엔트로피 손실
optimizer = torch.optim.AdamW(model.parameters(), lr=LR) # 옵티마이저 설정 : Adam (과적합 방지)

# 🔁 4. 학습 + 평가
train_losses, val_losses = [], []
metrics_per_epoch = []
best_val_loss = float('inf')   # 기초값 설정 트릭 (무한대의 값 설정)

for epoch in range(EPOCHS):
    model.train()
    running_train_loss = 0.0
    for images, labels in tqdm(train_loader, desc=f"[Train] Epoch {epoch+1}"):
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_train_loss += loss.item()
    avg_train_loss = running_train_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # 📊 검증
    model.eval()
    running_val_loss = 0.0
    y_true, y_pred = [], []

    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc=f"[Val] Epoch {epoch+1}"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_val_loss += loss.item()

            preds = torch.argmax(outputs, dim=1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    avg_val_loss = running_val_loss / len(val_loader)
    val_losses.append(avg_val_loss)

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    metrics_per_epoch.append({
        "epoch": epoch + 1,
        "train_loss": avg_train_loss,
        "val_loss": avg_val_loss,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1
    })

    print(f"\n📊 Epoch {epoch+1}")
    print(f"Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
    print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

    # 💾 best 모델 저장
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"✅ Best model saved (val loss: {avg_val_loss:.4f})")

# 📈 손실 그래프 시각화
plt.figure(figsize=(8, 5))
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Train vs Validation Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("loss_plot.png")
plt.show()

# 📋 전체 Epoch 요약
print("\n📊 전체 성능 요약:")
print("-" * 70)
print(f"{'Epoch':<6}{'TrainLoss':<12}{'ValLoss':<12}{'Acc':<8}{'Prec':<8}{'Recall':<8}{'F1':<8}")
print("-" * 70)
for m in metrics_per_epoch:
    print(f"{m['epoch']:<6}{m['train_loss']:<12.4f}{m['val_loss']:<12.4f}"
          f"{m['accuracy']:<8.4f}{m['precision']:<8.4f}{m['recall']:<8.4f}{m['f1']:<8.4f}")

# ✅ 5. 테스트셋 성능 평가
print("\n🧪 테스트셋 평가")
model.load_state_dict(torch.load(MODEL_PATH))  # best 모델 불러오기
model.eval()
y_true, y_pred = [], []

with torch.no_grad():
    for images, labels in tqdm(test_loader, desc="[Test]"):
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        preds = torch.argmax(outputs, dim=1)

        y_true.extend(labels.cpu().numpy())
        y_pred.extend(preds.cpu().numpy())

test_acc = accuracy_score(y_true, y_pred)
test_prec = precision_score(y_true, y_pred)
test_rec = recall_score(y_true, y_pred)
test_f1 = f1_score(y_true, y_pred)

print(f"✅ Test Accuracy: {test_acc:.4f} | Precision: {test_prec:.4f} | Recall: {test_rec:.4f} | F1: {test_f1:.4f}")
