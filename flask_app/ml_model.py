import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

# ---- Model Definition ----
class LandslideNN(nn.Module):
    def __init__(self):
        super(LandslideNN, self).__init__()
        self.fc1 = nn.Linear(3, 16)
        self.fc2 = nn.Linear(16, 16)
        self.fc3 = nn.Linear(16, 2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()  # IMPORTANT

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return self.sigmoid(x)


# ---- Load Model ----
model = LandslideNN()
model.load_state_dict(torch.load('flask_app/landslide_nn.pth', map_location=torch.device('cpu')))
model.eval()

# ---- Load Dataset ----
env_df = pd.read_csv('flask_app/datasets/mandi_monthly_dataset.csv')

# ---- Scaler ----
scaler = StandardScaler()
scaler.fit(env_df[['rainfall_mm', 'slope_deg', 'soil_index']])


# # ---- City Mapping ----
# city_to_subdivision = {
#     "Mandi Sadar": "Mandi Sadar",
#     "Sundernagar": "Sundernagar",
#     "Jogindernagar": "Jogindernagar",
#     "Karsog": "Karsog",
#     "Chachyot": "Chachyot",
#     "Balh": "Balh",
#     "Sarkaghat": "Sarkaghat",
#     "Padhar": "Padhar",
#     "Thunag": "Thunag",
#     "Nihri": "Nihri",
#     "Dharampur": "Dharampur",
#     "Baggi": "Baggi",
#     "Gohar": "Gohar",
#     "Seraj": "Seraj",
#     "Pandoh": "Pandoh"
# }


# ---- Prediction Function ----
def get_ml_probabilities(city, month_num):
    subdivision = city

    row = env_df[
        (env_df['subdivision'] == subdivision) &
        (env_df['month_num'] == month_num)
    ]

    if row.empty:
        return 0.1, 0.1

    features = row[['rainfall_mm', 'slope_deg', 'soil_index']].values
    features_scaled = scaler.transform(features)

    X = torch.tensor(features_scaled, dtype=torch.float32)

    with torch.no_grad():
        output = model(X).numpy()[0]

    p_spatial = float(output[0])
    p_temporal = float(output[1])

    return p_spatial, p_temporal