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

print("Number of states: {}".format(model.nr_states))
print("Number of transitions: {}".format(model.nr_transitions))
print("Labels: {}\n".format(model.labeling.get_labels()))

for state in model.states:
    if state.id in model.initial_states:
        print("State {} is initial".format(state.id))
    for action in state.actions:
        for transition in action.transitions:
            print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))

result = stormpy.model_checking(model, properties[0])

initial_state = model.initial_states[0]
print("\nExpected steps (from initial states): {}\n".format(result.at(initial_state)))

for i,r in enumerate(result.get_values()):
    print("\nExpected steps for state {}: {}".format(i,r))

print("\n")
result = stormpy.model_checking(model, properties[0], extract_scheduler=True)
scheduler = result.scheduler
assert scheduler.memoryless
assert scheduler.deterministic

buttons = dict()
for state in model.states:
    choice = scheduler.get_choice(state)
    action = choice.get_deterministic_choice()
    buttons[state.id] = action
    
print(buttons)

choice_labels = model.choice_labeling

for s, b in buttons.items():
    if s == 0: continue
    print("{}: {}".format(s, choice_labels.get_labels_of_choice(b+2*s+1)))