# app/models/gnn/UGraphSAGE.py

import torch
from torch_geometric.nn import GraphSAGE
from torch_geometric.nn import BatchNorm


class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GNN, self).__init__()
        self.sage = GraphSAGE(in_channels, hidden_channels, num_layers=2)
        self.norm = BatchNorm(hidden_channels)
        self.fc = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        h = self.sage(x, edge_index)
        h = self.norm(h)
        out = self.fc(h)
        return out
