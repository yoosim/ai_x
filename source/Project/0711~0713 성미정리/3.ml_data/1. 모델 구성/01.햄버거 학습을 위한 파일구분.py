# 햄버거 이진분류 학습을 위한 파일구분
import os
import random
import shutil

def split_class_data(source_class_dir, target_root, class_name, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    """
    각 클래스별로 데이터를 train/val/test로 분할하는 함수
    """
    # 해당 클래스의 모든 이미지 파일 목록 불러오기
    image_files = [f for f in os.listdir(source_class_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if len(image_files) == 0:
        print(f"경고: {class_name} 폴더에 이미지가 없습니다!")
        return
    
    random.shuffle(image_files)
    
    # 개수 계산
    total = len(image_files)
    train_cnt = int(total * train_ratio)
    val_cnt = int(total * val_ratio)
    test_cnt = total - train_cnt - val_cnt  # 잔여를 테스트셋으로
    
    # 데이터 분할
    train_files = image_files[:train_cnt]
    val_files = image_files[train_cnt:train_cnt + val_cnt]
    test_files = image_files[train_cnt + val_cnt:]
    
    print(f"\n=== {class_name} 클래스 분할 ===")
    print(f"전체: {total}개")
    print(f"Train: {len(train_files)}개 ({len(train_files)/total*100:.1f}%)")
    print(f"Val: {len(val_files)}개 ({len(val_files)/total*100:.1f}%)")
    print(f"Test: {len(test_files)}개 ({len(test_files)/total*100:.1f}%)")
    
    # 각 분할에 대해 파일 복사
    for split_name, file_list in zip(['train', 'val', 'test'], [train_files, val_files, test_files]):
        # 목표 디렉토리 생성 (예: model_data/train/hamburger/)
        split_class_dir = os.path.join(target_root, split_name, class_name)
        os.makedirs(split_class_dir, exist_ok=True)
        
        # 파일 복사
        for filename in file_list:
            src_path = os.path.join(source_class_dir, filename)
            dst_path = os.path.join(split_class_dir, filename)
            shutil.copy2(src_path, dst_path)
        
        print(f"  {split_name}: {len(file_list)}개 파일 복사 완료")

def main():
    # 경로 설정
    source_root = "C:/Users/baby3/OneDrive/바탕 화면/햄버거 테스트용/img"
    target_root = "C:/Users/baby3/OneDrive/바탕 화면/햄버거 테스트용/model_data"
    
    # 클래스별 폴더명 (img 폴더 안의 하위 폴더들)
    class_folders = {
        "hamburger": "햄버거",      # img/햄버거 폴더
        "not_hamburger": "비햄버거"  # img/비햄버거 폴더
    }
    
    # 비율 설정 (6:2:2)
    train_ratio = 0.6
    val_ratio = 0.2
    test_ratio = 0.2
    
    print("햄버거 이진분류용 데이터 분할을 시작합니다...")
    print(f"비율: Train {train_ratio*100}% / Val {val_ratio*100}% / Test {test_ratio*100}%")
    
    # 기존 model_data 폴더가 있으면 삭제 (선택사항)
    if os.path.exists(target_root):
        response = input(f"{target_root} 폴더가 이미 존재합니다. 삭제하고 새로 만들까요? (y/n): ")
        if response.lower() == 'y':
            shutil.rmtree(target_root)
            print("기존 폴더 삭제 완료")
    
    # 각 클래스별로 데이터 분할
    total_files = 0
    for class_name, folder_name in class_folders.items():
        source_class_dir = os.path.join(source_root, folder_name)
        
        # 폴더 존재 여부 확인
        if not os.path.exists(source_class_dir):
            print(f"경고: {source_class_dir} 폴더가 존재하지 않습니다!")
            continue
        
        # 각 클래스 데이터 분할
        split_class_data(source_class_dir, target_root, class_name, train_ratio, val_ratio, test_ratio)
        
        # 총 파일 수 계산
        class_files = len([f for f in os.listdir(source_class_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        total_files += class_files
    
    print(f"\n" + "="*50)
    print(f"전체 분할 완료!")
    print(f"총 처리된 파일: {total_files}개")
    print(f"\n생성된 폴더 구조:")
    print(f"{target_root}/")
    print(f"├── train/")
    print(f"│   ├── hamburger/")
    print(f"│   └── not_hamburger/")
    print(f"├── val/")
    print(f"│   ├── hamburger/")
    print(f"│   └── not_hamburger/")
    print(f"└── test/")
    print(f"    ├── hamburger/")
    print(f"    └── not_hamburger/")
    
    # 최종 확인
    print(f"\n최종 파일 개수 확인:")
    for split in ['train', 'val', 'test']:
        split_dir = os.path.join(target_root, split)
        if os.path.exists(split_dir):
            for class_name in ['hamburger', 'not_hamburger']:
                class_dir = os.path.join(split_dir, class_name)
                if os.path.exists(class_dir):
                    count = len([f for f in os.listdir(class_dir) 
                               if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                    print(f"  {split}/{class_name}: {count}개")

if __name__ == "__main__":
    main()