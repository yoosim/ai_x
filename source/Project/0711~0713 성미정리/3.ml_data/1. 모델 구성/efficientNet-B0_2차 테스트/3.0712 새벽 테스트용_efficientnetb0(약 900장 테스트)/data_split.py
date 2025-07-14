import os
import shutil
from sklearn.model_selection import train_test_split
import glob

# 저장 경로 설정
# source_dir : 원본데이터
# utput_dir : 분할데이터 
source_dir = r"C:\Users\baby3\ai_x\source\Project\0711~0713 성미정리\3.ml_data\1. 모델 구성\img"
output_dir = r"C:\Users\baby3\ai_x\source\Project\0711~0713 성미정리\3.ml_data\1. 모델 구성\split_data"

# 출력 폴더 생성
for split in ['train', 'val', 'test']:
    for class_name in ['hamburger','not_hamburger']: # 클래스명 설정
        os.makedirs(os.path.join(output_dir,split,class_name), exist_ok=True)

# 데이터 분할 함수
def split_and_copy_data(source_class_folder, target_class_name, test_size=0.4, val_size=0.2):
    import random

    # 이미지 파일 경로 불러오기
    image_extensions = ['*.jpg','*.jpeg','*.png','*.bmp','*.gif','*.webp']
    all_images=[]
    for ext in image_extensions:
        all_images.extend(glob.glob(os.path.join(source_class_folder,ext)))

    # 추가 셔플 (랜덤 사진 섞기)
    random.seed(42)
    random.shuffle(all_images)

    print(f"{target_class_name}: {len(all_images)}개 이미지 발견")

    if len(all_images) == 0:
        print(f"경고: {source_class_folder}에서 이미지를 찾을 수 없습니다.")
        return

    # train/temp 분할 (60% / 40%)
    train_files, temp_files = train_test_split(all_images, test_size=test_size, random_state=42)

    # temp를 vla/test로 분할 (각 20%씩)
    val_files, test_files = train_test_split(temp_files, test_size=0.5, random_state=42)

    print(f" - Train : {len(train_files)}개")
    print(f" - Val : {len(val_files)}개")
    print(f" - Test : {len(test_files)}개")

    # 파일 복사 
    file_sets = {
        'train':train_files,
        'val':val_files,
        'test':test_files
    }
    for split_name, file_list in file_sets.items():
        target_folder = os.path.join(output_dir, split_name, target_class_name)
        for i, file_path in enumerate(file_list):
            filename = os.path.basename(file_path)
            # 파일명 중복 방지 
            name, ext = os.path.splitext(filename)
            new_filename = f"{target_class_name}_{i:04d}{ext}"
            shutil.copy2(file_path,os.path.join(target_folder, new_filename))

#  ★★★★★★★★파일 분활 실행★★★★
print('데이터 분할 시작합니다.')
# 햄버거 데이터 분할 
hamburger_folder = os.path.join(source_dir, "hamburger")
if os.path.exists(hamburger_folder):
    split_and_copy_data(hamburger_folder,"hamburger")
else:
    print(f"햄버거 폴더 찾을 수 없음 : {hamburger_folder}")

#  비햄버거(홍보물,전단지,포스터,치킨,샐러드 등)
not_hamburger_folder = os.path.join(source_dir,"not_hamburger")
if os.path.exists(not_hamburger_folder):
    split_and_copy_data(not_hamburger_folder,"not_hamburger")
else:
    print(f"비햄버거 폴더 찾을 수 없음 :{not_hamburger_folder}")

print("데이터 분할 완료")
print(f"결과 폴더 : {output_dir}")