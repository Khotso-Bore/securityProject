import torch
import torch.nn as nn
import torch.optim as optim

class InsiderTheatModel(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super(InsiderTheatModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),      # Output 1 value for Binary Classification          # Squishes output between 0 and 1
        )
        
    def forward(self, x):
        return self.network(x)