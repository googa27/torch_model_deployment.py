import torch
import sys
sys.path.append('doubleit-model/archive/code')  # Path to __torch__.py
from __torch__ import Model

# Instantiate and script the model
model = Model()
scripted_model = torch.jit.script(model)
scripted_model.save('doubleit_model.pt')
