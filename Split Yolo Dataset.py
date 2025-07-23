import os
import shutil
import random

# 기본 경로
base_dir = "C:/Users/LeeEunseo/Documents/GitHub/CXray"
img_src_dir = os.path.join(base_dir, "images/JPEGImages-no_enhance")
lab_src_dir = os.path.join(base_dir, "labels/labels")

# 대상 폴더
img_train_dir = os.path.join(base_dir, "images/train")
img_val_dir   = os.path.join(base_dir, "images/val")
img_test_dir  = os.path.join(base_dir, "images/test")
lab_train_dir = os.path.join(base_dir, "labels/train")
lab_val_dir   = os.path.join(base_dir, "labels/val")
lab_test_dir  = os.path.join(base_dir, "labels/test")

# 폴더 생성
for path in [img_train_dir, img_val_dir, img_test_dir, lab_train_dir, lab_val_dir, lab_test_dir]:
    os.makedirs(path, exist_ok=True)

# 이미지-라벨 매칭 리스트 생성
all_files = [f for f in os.listdir(img_src_dir) if f.lower().endswith(('.jpg', '.png'))]
all_files.sort()
random.seed(42)
random.shuffle(all_files)

# 분할 기준 (90% train / 5% val / 5% test)
num_total = len(all_files)
num_val = int(num_total * 0.05)
num_test = int(num_total * 0.05)
val_files = all_files[:num_val]
test_files = all_files[num_val:num_val + num_test]
train_files = all_files[num_val + num_test:]

# 복사 함수 정의
def copy_pair(img_name, dst_img_dir, dst_lab_dir):
    base = os.path.splitext(img_name)[0]
    img_path = os.path.join(img_src_dir, img_name)
    lab_path = os.path.join(lab_src_dir, base + ".txt")

    if os.path.exists(img_path) and os.path.exists(lab_path):
        shutil.copy2(img_path, os.path.join(dst_img_dir, img_name))
        shutil.copy2(lab_path, os.path.join(dst_lab_dir, base + ".txt"))
    else:
        print(f"파일 누락: {img_name}")

# 복사 실행
for f in train_files:
    copy_pair(f, img_train_dir, lab_train_dir)
for f in val_files:
    copy_pair(f, img_val_dir, lab_val_dir)
for f in test_files:
    copy_pair(f, img_test_dir, lab_test_dir)

print(f"분할 완료: train {len(train_files)}장, val {len(val_files)}장, test {len(test_files)}장")
