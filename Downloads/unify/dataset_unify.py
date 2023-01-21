from PIL import Image
import os
from torch.utils.data import Dataset
import numpy as np
from natsort import natsorted

# sar = zebra optical = horse

class OpticalSARDataset(Dataset):
    def __init__(self, root_sar, root_optical, root_mask, transform=None):
        self.root_sar = root_sar
        self.root_optical = root_optical
        self.root_mask = root_mask
        self.transform = transform

        self.sar_images = natsorted(os.listdir(root_sar))
        self.optical_images = natsorted(os.listdir(root_optical))
        self.mask_images = natsorted(os.listdir(root_mask))
        self.length_dataset = max(len(self.sar_images), len(self.optical_images),  len(self.mask_images)) # 1000000, 1500
        self.sar_len = len(self.sar_images)
        self.optical_len = len(self.optical_images)
        self.mask_len = len(self.mask_images)

    def __len__(self):
        return self.length_dataset

    def __getitem__(self, index):
        sar_img = self.sar_images[index % self.sar_len]
        optical_img = self.optical_images[index % self.optical_len]
        mask_img = self.mask_images[index % self.mask_len]

        sar_path = os.path.join(self.root_sar, sar_img)  #パスの結合
        optical_path = os.path.join(self.root_optical, optical_img)
        mask_path = os.path.join(self.root_mask, mask_img.replace( ".npy",".jpeg"))

        sar_img = np.array(Image.open(sar_path).convert("RGB"))
        optical_img = np.array(Image.open(optical_path).convert("RGB"))
        mask_img = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
        mask_img[mask_img == 255.0] = 1.0

        if self.transform:
            augmentations = self.transform(image=sar_img, image0=optical_img)
            sar_img = augmentations["image"]
            optical_img = augmentations["image0"]
            #mask_img = augmentations["image1"]

        return sar_img, optical_img, mask_img
