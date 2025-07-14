import torch
from PIL import Image
from test import FoodImageClassifier, FoodImageDataset, RTX4060OptimizedModel


# --------------------------------------------------------------------------
# 여기에 이전에 작성하셨던 FoodImageDataset, RTX4060OptimizedModel, 
# FoodImageClassifier 클래스 정의가 있다고 가정합니다.
# --------------------------------------------------------------------------


def predict_single_image(model_path, image_path):
    """
    저장된 모델을 불러와서 새로운 이미지의 클래스를 예측하는 함수
    """
    # 1. 장치 설정 (GPU 또는 CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"사용 장치: {device}")

    # 2. 체크포인트(저장된 모델 파일) 로드
    # map_location을 통해 현재 환경에 맞는 장치에 모델을 올립니다.
    try:
        checkpoint = torch.load(model_path, map_location=device)
    except FileNotFoundError:
        print(f"오류: 모델 파일 '{model_path}'을(를) 찾을 수 없습니다.")
        return
    
    # 3. 모델 구조 초기화
    # 체크포인트에 저장된 클래스 개수 정보를 가져와 모델을 생성합니다.
    num_classes = len(checkpoint['classes'])
    classifier = FoodImageClassifier(num_classes=num_classes)
    
    # 4. 저장된 가중치(State Dict)를 모델에 적용
    classifier.model.load_state_dict(checkpoint['model_state_dict'])
    
    # 5. 클래스 이름 정보 로드
    classifier.classes = checkpoint['classes']
    print("✅ 모델 로딩 완료!")

    # 6. 예측 실행
    # FoodImageClassifier에 이미 구현된 predict 메서드를 사용합니다.
    predicted_food, confidence = classifier.predict(image_path)
    
    # 7. 결과 출력
    if predicted_food is not None:
        print("\n===== 🚀 예측 결과 =====")
        print(f"🖼️  입력 이미지: {image_path}")
        print(f"🍕  예측된 음식: {predicted_food}")
        print(f"🎯  신뢰도: {confidence * 100:.2f}%")
    else:
        print("❌ 예측에 실패했습니다. 이미지 파일 경로를 확인해 주세요.")

if __name__ == "__main__":
    # --- 설정 ---
    # 훈련 시 저장된 모델 파일의 경로
    MODEL_CHECKPOINT_PATH = 'best_food_model_rtx4060.pth'
    
    
    # ★★★ 예측하고 싶은 이미지 파일의 경로를 여기에 입력하세요! ★★★
    IMAGE_TO_PREDICT_PATH = r'C:\Users\baby3\OneDrive\바탕 화면\햄버거 테스트용\model_data\test\not_hamburger\naver_img_0156.jpg' # 예시 경로
    
    # --- 실행 ---
    predict_single_image(MODEL_CHECKPOINT_PATH, IMAGE_TO_PREDICT_PATH)