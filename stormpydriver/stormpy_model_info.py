import stormpy
import stormpy.info
import json

with open('model_inputs.json', 'r') as f:
    data = json.load(f)

model_specification = data["model_specification"]
constant_variables = data["constant_variables"]

orig_program = stormpy.parse_prism_program(model_specification)

if constant_variables != "":
    orig_program = orig_program.define_constants(stormpy.parse_constants_string(orig_program.expression_manager, constant_variables))

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

# "init_pod=1,init_lat=1,init_cpu=1,init_demand=1,init_pow=1,init_rt=1,maxPod=3"