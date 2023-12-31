import stormpy
import stormpy.info
import json

with open('model_inputs.json', 'r') as f:
    data = json.load(f)

model_specification = data["model_specification"]
properties_specification = data["properties_specification"]
constant_variables = data["constant_variables"]

orig_program = stormpy.parse_prism_program(model_specification)

if constant_variables != "":
    orig_program = orig_program.define_constants(stormpy.parse_constants_string(orig_program.expression_manager, constant_variables))


formula_str = properties_specification 

# print(formula_str)

properties = stormpy.parse_properties(formula_str, orig_program)

options = stormpy.BuilderOptions([p.raw_formula for p in properties])
options.set_build_state_valuations()
options.set_build_choice_labels()

model = stormpy.build_sparse_model_with_options(orig_program, options)

# edges = dict()

# for state in model.states:
#     edges[int(state)] = []
#     for action in state.actions:
#         for transition in action.transitions:
#             state = int(state)
#             next_state = int(transition.column)
#             edges[int(state)].append(next_state)

# print(edges)

result = stormpy.model_checking(model, properties[0], extract_scheduler=True)

print(result.get_values())