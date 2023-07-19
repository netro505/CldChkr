import stormpy
import stormpy.info

lines = []
with open('model.txt') as f:
    lines = f.readlines()

file_name = lines[0]

prop_lines = []
with open('prop.txt') as f:
    prop_lines = f.readlines()

prop_input = prop_lines[0]

orig_program = stormpy.parse_prism_program(file_name)


options = stormpy.BuilderOptions(True, True)
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

formula_str = prop_input

# print(formula_str)

properties = stormpy.parse_properties(formula_str, orig_program)

result = stormpy.model_checking(model, properties[0], extract_scheduler=True)

print(result.get_values())