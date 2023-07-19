import stormpy
import stormpy.info
import json

with open('model_inputs.json', 'r') as f:
    data = json.load(f)

model_specification = data["model_specification"]

orig_program = stormpy.parse_prism_program(model_specification)


options = stormpy.BuilderOptions(True, True)
options.set_build_state_valuations()
options.set_build_choice_labels()
model = stormpy.build_sparse_model_with_options(orig_program, options)

edges = dict()

for state in model.states:
    edges[int(state)] = []
    for action in state.actions:
        for transition in action.transitions:
            state = int(state)
            next_state = int(transition.column)
            edges[int(state)].append(next_state)

print(edges)
