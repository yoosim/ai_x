import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from tqdm import tqdm
import gc
import warnings
warnings.filterwarnings('ignore')

class FoodImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        self.samples = []
        
        for cls in self.classes:
            cls_path = os.path.join(root_dir, cls)
            if os.path.isdir(cls_path):
                for img_name in os.listdir(cls_path):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.samples.append((os.path.join(cls_path, img_name), self.class_to_idx[cls]))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        try:
            image = Image.open(img_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            return image, label
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            return self.__getitem__(0)

class RTX4060OptimizedModel(nn.Module):
    """RTX 4060 8GB VRAM에 최적화된 모델"""
    def __init__(self, num_classes):
        super(RTX4060OptimizedModel, self).__init__()
        
        # EfficientNet-B2 사용 (B4 대신 - 메모리 효율적)
        self.backbone = models.efficientnet_b2(pretrained=True)
        
        # 백본 특성 추출기와 분류기 분리
        self.features = self.backbone.features
        self.avgpool = self.backbone.avgpool
        
        # 사용자 정의 분류기 (메모리 효율적)
        feature_dim = self.backbone.classifier[1].in_features
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(feature_dim, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes)
        )
        
#         # 그래디언트 체크포인팅 활성화 (메모리 절약)
#         self.backbone.set_swish(memory_efficient=True)
        
    def forward(self, x):
        # 메모리 효율적인 순전파
        features = self.features(x)
        features = self.avgpool(features)
        features = torch.flatten(features, 1)
        output = self.classifier(features)
        return output

class FoodImageClassifier:
    def __init__(self, num_classes):
        # RTX 4060 최적화 설정
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_classes = num_classes
        
        # GPU 메모리 설정
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.set_per_process_memory_fraction(0.8)  # VRAM의 80%만 사용
            print(f"GPU: {torch.cuda.get_device_name()}")
            print(f"GPU 메모리: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        # 더 작은 이미지 크기로 메모리 절약
        self.train_transform = transforms.Compose([
            transforms.Resize((224, 224)),  # 384에서 224로 축소
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.val_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # 메모리 효율적인 모델 초기화
        self.model = RTX4060OptimizedModel(num_classes).to(self.device)
        
        # 혼합 정밀도 학습 설정 (RTX 4060 Tensor 코어 활용)
        self.scaler = torch.cuda.amp.GradScaler()
        
        # 최적화 설정
        self.optimizer = optim.AdamW(
            self.model.parameters(), 
            lr=0.001, 
            weight_decay=0.01,
            eps=1e-8
        )
        
        # 학습률 스케줄러
        self.scheduler = optim.lr_scheduler.OneCycleLR(
            self.optimizer,
            max_lr=0.003,
            epochs=30,
            steps_per_epoch=100,  # 추후 실제 값으로 업데이트
            pct_start=0.3,
            div_factor=10,
            final_div_factor=100
        )
        
        self.criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
        
        # 모니터링 변수
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        
    def create_dataloaders(self, train_dir, val_dir, test_dir, batch_size=32):
        """RTX 4060에 최적화된 데이터로더"""
        
        # 데이터셋 생성
        train_dataset = FoodImageDataset(train_dir, self.train_transform)
        val_dataset = FoodImageDataset(val_dir, self.val_transform)
        test_dataset = FoodImageDataset(test_dir, self.val_transform)
        
        # GPU 메모리에 맞춰 배치 크기 자동 조정
        if torch.cuda.is_available():
            gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            if gpu_memory_gb < 12:  # RTX 4060의 경우
                batch_size = min(batch_size, 24)  # 배치 크기 제한
        
        print(f"사용할 배치 크기: {batch_size}")
        
        # 데이터로더 생성 (메모리 효율적 설정)
        self.train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size, 
            shuffle=True, 
            num_workers=4,
            pin_memory=True,
            persistent_workers=False
        )
        
        self.val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size, 
            shuffle=False, 
            num_workers=4,
            pin_memory=True,
            persistent_workers=False
        )
        
        self.test_loader = DataLoader(
            test_dataset, 
            batch_size=batch_size, 
            shuffle=False, 
            num_workers=4,
            pin_memory=True,
            persistent_workers=False
        )
        
        # 스케줄러 업데이트
        self.scheduler = optim.lr_scheduler.OneCycleLR(
            self.optimizer,
            max_lr=0.003,
            epochs=30,
            steps_per_epoch=len(self.train_loader),
            pct_start=0.3,
            div_factor=10,
            final_div_factor=100
        )
        
        # 클래스 정보 저장
        self.classes = train_dataset.classes
        print(f"클래스 수: {len(self.classes)}")
        print(f"클래스: {self.classes}")
        
        return self.train_loader, self.val_loader, self.test_loader
    
    def train_epoch(self):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc="Training")
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device, non_blocking=True), target.to(self.device, non_blocking=True)
            
            self.optimizer.zero_grad()
            
            # 혼합 정밀도 학습 (RTX 4060 Tensor 코어 활용)
            with torch.cuda.amp.autocast():
                output = self.model(data)
                loss = self.criterion(output, target)
            
            # 역전파 및 최적화
            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.scheduler.step()
            
            running_loss += loss.item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
            
            # 메모리 정리
            if batch_idx % 50 == 0:
                torch.cuda.empty_cache()
            
            pbar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{100.*correct/total:.2f}%',
                'LR': f'{self.scheduler.get_last_lr()[0]:.6f}'
            })
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate_epoch(self):
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            pbar = tqdm(self.val_loader, desc="Validation")
            for data, target in pbar:
                data, target = data.to(self.device, non_blocking=True), target.to(self.device, non_blocking=True)
                
                # 혼합 정밀도 추론
                with torch.cuda.amp.autocast():
                    output = self.model(data)
                    loss = self.criterion(output, target)
                
                running_loss += loss.item()
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)
                
                pbar.set_postfix({
                    'Loss': f'{loss.item():.4f}',
                    'Acc': f'{100.*correct/total:.2f}%'
                })
        
        epoch_loss = running_loss / len(self.val_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def train(self, epochs=30, early_stopping_patience=8):
        best_val_acc = 0.0
        patience_counter = 0
        
        print(f"디바이스: {self.device}")
        print(f"모델 파라미터 수: {sum(p.numel() for p in self.model.parameters()):,}")
        
        # GPU 메모리 모니터링
        if torch.cuda.is_available():
            print(f"초기 GPU 메모리 사용량: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch+1}/{epochs}")
            print("-" * 30)
            
            # 훈련
            train_loss, train_acc = self.train_epoch()
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)
            
            # 검증
            val_loss, val_acc = self.validate_epoch()
            self.val_losses.append(val_loss)
            self.val_accuracies.append(val_acc)
            
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            # GPU 메모리 모니터링
            if torch.cuda.is_available():
                print(f"GPU 메모리 사용량: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
            
            # 모델 저장 (최고 성능)
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'scheduler_state_dict': self.scheduler.state_dict(),
                    'best_val_acc': best_val_acc,
                    'classes': self.classes
                }, 'best_food_model_rtx4060.pth')
                patience_counter = 0
                print(f"새로운 최고 성능! 모델 저장됨 (Val Acc: {val_acc:.2f}%)")
            else:
                patience_counter += 1
            
            # 메모리 정리
            torch.cuda.empty_cache()
            gc.collect()
            
            # Early Stopping
            if patience_counter >= early_stopping_patience:
                print(f"Early stopping! {early_stopping_patience} 에포크 동안 개선 없음")
                break
        
        print(f"\n훈련 완료! 최고 검증 정확도: {best_val_acc:.2f}%")
        
        # 최고 모델 로드
        checkpoint = torch.load('best_food_model_rtx4060.pth')
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        return best_val_acc
    
    def test(self):
        self.model.eval()
        correct = 0
        total = 0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            pbar = tqdm(self.test_loader, desc="Testing")
            for data, target in pbar:
                data, target = data.to(self.device, non_blocking=True), target.to(self.device, non_blocking=True)
                
                with torch.cuda.amp.autocast():
                    output = self.model(data)
                
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)
                
                all_preds.extend(pred.cpu().numpy().flatten())
                all_labels.extend(target.cpu().numpy())
                
                pbar.set_postfix({'Acc': f'{100.*correct/total:.2f}%'})
        
        test_acc = 100. * correct / total
        print(f"\n테스트 정확도: {test_acc:.2f}%")
        
        # 분류 리포트
        print("\n분류 리포트:")
        print(classification_report(all_labels, all_preds, target_names=self.classes))
        
        return test_acc, all_preds, all_labels
    
    def plot_training_history(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # 손실 플롯
        ax1.plot(self.train_losses, label='Train Loss')
        ax1.plot(self.val_losses, label='Validation Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # 정확도 플롯
        ax2.plot(self.train_accuracies, label='Train Accuracy')
        ax2.plot(self.val_accuracies, label='Validation Accuracy')
        ax2.set_title('Training and Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history_rtx4060.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def predict(self, image_path):
        """단일 이미지 예측"""
        self.model.eval()
        
        try:
            image = Image.open(image_path).convert('RGB')
            image = self.val_transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                with torch.cuda.amp.autocast():
                    output = self.model(image)
                probabilities = torch.softmax(output, dim=1)
                predicted_class = output.argmax(dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            return self.classes[predicted_class], confidence
        except Exception as e:
            print(f"예측 오류: {e}")
            return None, 0.0
    
    def get_gpu_memory_usage(self):
        """GPU 메모리 사용량 모니터링"""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3
            reserved = torch.cuda.memory_reserved() / 1024**3
            total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            
            print(f"GPU 메모리 사용량:")
            print(f"  할당됨: {allocated:.2f} GB")
            print(f"  예약됨: {reserved:.2f} GB")
            print(f"  전체: {total:.2f} GB")
            print(f"  사용률: {(allocated/total)*100:.1f}%")

# RTX 4060 최적화 사용 예시
def main():
    # 데이터 경로 설정
    train_dir = 'C:/Users/baby3/OneDrive/바탕 화면/햄버거 테스트용/model_data/train'
    val_dir = 'C:/Users/baby3/OneDrive/바탕 화면/햄버거 테스트용/model_data/val'
    test_dir = 'C:/Users/baby3/OneDrive/바탕 화면/햄버거 테스트용/model_data/test' # 평가용 데이터셋 경로
    
    # 클래스 수 자동 계산
    num_classes = 2
    
    # RTX 4060 최적화 모델 초기화
    classifier = FoodImageClassifier(num_classes)
    
    # GPU 메모리 상태 확인
    classifier.get_gpu_memory_usage()
    
    # 데이터로더 생성 (RTX 4060에 최적화된 배치 크기)
    train_loader, val_loader, test_loader = classifier.create_dataloaders(
        train_dir, val_dir, test_dir, batch_size=24  # RTX 4060에 적합한 배치 크기
    )
    
    # 모델 훈련
    print("RTX 4060 최적화 모델 훈련 시작...")
    best_val_acc = classifier.train(epochs=30, early_stopping_patience=8)
    
    # 메모리 사용량 확인
    classifier.get_gpu_memory_usage()
    
    # 테스트 평가
    print("\n테스트 평가...")
    test_acc, preds, labels = classifier.test()
    
    # 훈련 히스토리 시각화
    classifier.plot_training_history()
    
    # 최종 메모리 정리
    torch.cuda.empty_cache()

if __name__ == "__main__":
    main()