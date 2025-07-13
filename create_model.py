import torch as tc
from __torch__ import Model

# Instantiate and script the model
model = Model()
scripted_model = tc.jit.script(model)
scripted_model.save('doubleit_model.pt')
