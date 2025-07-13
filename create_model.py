import torch as tc
from __torch__ import Model

# Instantiate and script the model
# This assumes Model is defined in __torch__.py
# If Model is not defined, replace with the actual model class
model = Model()
scripted_model = tc.jit.script(model)
scripted_model.save('doubleit_model.pt')
