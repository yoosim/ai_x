#  EfficientNet-B0 기반 이진분류 모델 만들기 + 전이학습
# test1 버전에서 데이터 증강 추가 , 정규화 강화  (0.3 -> 0.5로 과감하게 변경)
# 그래프에서 훈련 정화도가 검증 정확도보다 높음 = 과적합 , Dropuout 
# 초기 학습률 빠르게, 후반 작은 학습률로 세밀 조정 
import os
import copy
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from tqdm import tqdm
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image


# 디바이스 설정 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")



#이미지 전처리
# 훈련용 변환 (데이터 증강 포함)
train_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(0.5),      # 50% 확률로 좌우 반전 - 햄버거는 뒤집어도 햄버거니까
    transforms.RandomRotation(15),             # ±15도 회전 - 약간 기울어진 사진도 인식하게
    transforms.ColorJitter(brightness=0.2, contrast=0.2),  # 밝기/대비 조정 - 조명 변화에 강해짐
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
])

# 검증/테스트용 변환 (증강 없음)
val_test_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
])


# 예측 함수 정의 (외부에서도 사용 가능)
def predict_image_from_url(model, image_url, threshold=0.5):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_tensor = val_test_transform(img).unsqueeze(0).to(device)

        model.eval()
        with torch.no_grad():
            output = model(img_tensor)
            prob = torch.sigmoid(output).item()

        if prob > threshold:
            print(f"이미지 예측 결과: 햄버거 (확률: {prob:.4f})")
            return True
        else:
            print(f"이미지 예측 결과: 비햄버거 (확률: {prob:.4f})")
            return False

    except Exception as e:
        print(f"예측 실패: {e}")
        return None

# 그래프 저장 함수 (검증 손실도 추가) 그래프저장 이름 수정 
def save_training_graph(train_acc_list, val_acc_list, train_loss_list, val_loss_list, save_path="0712_training_result.png"):
    epochs = range(1, len(train_acc_list) + 1)
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(epochs, train_acc_list, label='Train Acc')
    plt.plot(epochs, val_acc_list, label='Val Acc')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Accuracy per Epoch')
    plt.legend()

    plt.subplot(1, 3, 2)
    plt.plot(epochs, train_loss_list, label='Train Loss', color='red')
    plt.plot(epochs, val_loss_list, label='Val Loss', color='orange')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss per Epoch')
    plt.legend()

    plt.subplot(1, 3, 3)
    # 학습률 변화 시각화 (참고용)
    plt.plot(epochs, [1e-4] * len(epochs), label='Learning Rate', color='green')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.title('Learning Rate Schedule')
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    
if __name__ == "__main__":
    # 데이터 경로
    data_dir = r"C:\Users\baby3\ai_x\source\Project\0711~0713 성미정리\3.ml_data\1. 모델 구성\model_data"    
    
    # 데이터셋 로드
    train_ds = datasets.ImageFolder(os.path.join(data_dir,"train"), transform=train_transform)
    val_ds = datasets.ImageFolder(os.path.join(data_dir,"val"), transform=val_test_transform)
    test_ds = datasets.ImageFolder(os.path.join(data_dir,"test"), transform=val_test_transform)

    #배치사이즈 : 한번에 학습하는 이미지 , 일반적으로 16,32,64 
    # shuffle = True는 훈련 데이터의 순서를 매 epoch마다 랜덤하게 섞는다는 뜻
    train_loader = DataLoader(train_ds,batch_size=32, shuffle=True) 
    val_loader = DataLoader(val_ds,batch_size=32, shuffle=False)
    test_loader = DataLoader(test_ds,batch_size=32, shuffle=False)

    # EfficientNet-B0 모델 불러오기 
    model = models.efficientnet_b0(weights='DEFAULT')
    model.classifier = nn.Sequential(
        nn.Dropout(0.5),  # 50%의 뉴런을 랜덤하게 끔 (강한 정규화)
        nn.Linear(1280, 1))
        # model.classifier[1] = nn.Linear(in_features=1280, out_features=1)  # 이진 분류 
        # 맨 마지막 분류기 바꿔서 ↑ / sigmoid 는 내부적으로 하는것. 
    model = model.to(device)

    # 손실함수 & 옵티마이저 & 스케줄러
    # 스케줄러 적용 : epoch끝에 추가, 현재 학습률도 출력 
    # epoch 기준 1~10:0.0001 / 10~20:0.00001(10배 감소) / 21~30:0.000001(100배 감소)
    # 과적합 문제 개선, 안정적인 학습 목적으로 사용
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    # EarlyStopping & 최고 모델 저장 준비
    best_model_wts = copy.deepcopy(model.state_dict())
    best_val_acc = 0
    early_stop_count = 0
    early_stop_patience = 10  #10번 정체면 저장

    # epoch 저장 (기록용 리스트)
    train_acc_list = []
    val_acc_list = []
    train_loss_list = []
    val_loss_list = []  # 검증 손실도 추가

    # 학습 루프
    epochs = 30
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
            inputs, labels = inputs.to(device), labels.to(device).float().unsqueeze(1)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            preds = torch.sigmoid(outputs) > 0.5
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_acc = correct / total
        train_acc_list.append(train_acc)
        train_loss_list.append(running_loss)

        # 검증
        model.eval()
        correct = 0
        total = 0
        val_running_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device).float().unsqueeze(1)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_running_loss += loss.item()
                preds = torch.sigmoid(outputs) > 0.5
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        
        val_acc = correct / total
        val_acc_list.append(val_acc)
        val_loss_list.append(val_running_loss)

        # 현재 학습률 출력
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Epoch {epoch+1}  Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}, LR: {current_lr:.6f}")

        # 최고 성능 모델 저장
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_wts = copy.deepcopy(model.state_dict())
            torch.save(model.state_dict(), "efficientNetB0_0712_test_best_burger_model.pth")
            print("모델 저장됨 (최고 성능)")
            early_stop_count = 0
        else:
            early_stop_count += 1
            print(f"EarlyStopping 대기 중... ({early_stop_count}/{early_stop_patience})")

        if early_stop_count >= early_stop_patience:
            print("Early stopping 발생!")
            break

        # 스케줄러 스텝 실행 (여기가 중요!)
        scheduler.step()

    # 최고 성능 모델로 복원
    model.load_state_dict(best_model_wts)
    print("최고 모델로 복원 완료")

    # 테스트 정확도 확인
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device).float().unsqueeze(1)
            outputs = model(inputs)
            preds = torch.sigmoid(outputs) > 0.5
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    print(f"최종 테스트 정확도: {correct / total:.4f}")

    # 그래프 저장
    save_training_graph(train_acc_list, val_acc_list, train_loss_list, val_loss_list)
    
    # 예측 함수 사용 예시
    # predict_image_from_url(model, "https://example.com/burger.jpg")