import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

class RxRx1Dataset(Dataset):
    """
    Custom Dataset for loading RxRx1 microscopy images
    """
    def __init__(self, metadata_csv, root_dir, transform=None):
        self.metadata_df = pd.read_csv(metadata_csv)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.metadata_df)

    def __getitem__(self, idx):
        row = self.metadata_df.iloc[idx]
        img_path = os.path.join(self.root_dir, f"images/{row['experiment']}/Plate{row['plate']}/{row['well']}_s{row['site']}.png")
        image = Image.open(img_path)
        image = image.convert('RGB')  # Convert to RGB if needed

        if self.transform:
            image = self.transform(image)

        cell_type_id = {"HUVEC": 0, "HEPG2": 1, "RPE": 2, "U2OS": 3}[row['cell_type']]
        sirna_id = row['sirna_id']
        return image, cell_type_id, sirna_id

class RxRx1FullDataset(Dataset):
    """
    Custom Dataset for loading RxRx1 microscopy images
    """
    def __init__(self, metadata_csv, root_dir, transform=None):
        self.metadata_df = pd.read_csv(metadata_csv)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.metadata_df)

    def __getitem__(self, idx):
        row = self.metadata_df.iloc[idx]
        img_path = os.path.join(self.root_dir, f"images/{row['experiment']}/Plate{row['plate']}/{row['well']}_s{row['site']}.png")
        image = Image.open(img_path)
        image = image.convert('RGB')  # Convert to RGB if needed

        if self.transform:
            image = self.transform(image)

        #CHANGE THESE
        cell_type_id = {"HUVEC": 0, "HEPG2": 1, "RPE": 2, "U2OS": 3}[row['cell_type']]
        sirna_id = row['sirna_id']
        return image, cell_type_id, sirna_id


# class RxRx1DataModule(pl.LightningDataModule):
#     """
#     Data Module for RxRx1 Dataset, compatible with PyTorch Lightning
#     """
#     def __init__(self, batch_size=32, root_dir="/work/cvcs_2023_group23/AIB/data/rxrx1_v1.0", metadata_csv="metadata.csv"):
#         super().__init__()
#         self.batch_size = batch_size
#         self.root_dir = root_dir
#         self.metadata_csv = os.path.join(root_dir, metadata_csv)
#         self.transform = transforms.Compose([
#             transforms.Resize((256, 256)),
#             transforms.ToTensor(),
#         ])

#     def setup(self, stage=None):
#         if stage == 'fit' or stage is None:
#             self.train_dataset = RxRx1Dataset(self.metadata_csv, self.root_dir, transform=self.transform)
#             # For simplicity, using the same dataset for train/val split. Consider splitting your metadata.csv accordingly.
#             self.val_dataset = RxRx1Dataset(self.metadata_csv, self.root_dir, transform=self.transform)
#         if stage == 'test' or stage is None:
#             self.test_dataset = RxRx1Dataset(self.metadata_csv, self.root_dir, transform=self.transform)

#     def train_dataloader(self):
#         return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

#     def val_dataloader(self):
#         return DataLoader(self.val_dataset, batch_size=self.batch_size)

#     def test_dataloader(self):
#         return DataLoader(self.test_dataset, batch_size=self.batch_size)