import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# Load dataset
file_path = '/kaggle/input/datasets/lepakshi353/landslide-data/hp_landslide_dataset - hp_landslide_dataset.csv'
df = pd.read_csv(file_path)

# Features and targets (REMOVED month_num)
targets = ['p_spatial', 'p_temporal']
features = ['rainfall_mm', 'slope_deg', 'soil_index']

X = df[features].values
y = df[targets].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to torch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# Neural network model
class LandslideNN(nn.Module):
    def __init__(self):   # FIXED
        super(LandslideNN, self).__init__()
        self.fc1 = nn.Linear(X_train.shape[1], 16)
        self.fc2 = nn.Linear(16, 16)
        self.fc3 = nn.Linear(16, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = LandslideNN()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop with loss tracking
n_epochs = 200
losses = []

for epoch in range(n_epochs):
    model.train()
    optimizer.zero_grad()

    outputs = model(X_train)
    loss = criterion(outputs, y_train)

    loss.backward()
    optimizer.step()

    losses.append(loss.item())

    if (epoch+1) % 20 == 0:
        print(f'Epoch {epoch+1}/{n_epochs}, Loss: {loss.item():.4f}')

# Plot loss vs epochs
plt.figure()
plt.plot(range(1, n_epochs+1), losses)
plt.xlabel("Epochs")
plt.ylabel("Training Loss")
plt.title("Loss vs Epochs")
plt.show()

# Evaluation
model.eval()
with torch.no_grad():
    predictions = model(X_test)
    test_loss = criterion(predictions, y_test)
    print(f'Test Loss: {test_loss.item():.4f}')

# Save model
torch.save(model.state_dict(), 'landslide_nn.pth')
print('Model saved as landslide_nn.pth')