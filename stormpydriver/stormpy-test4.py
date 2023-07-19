import stormpy
import stormpy.info

# print("Stormpy version: " + stormpy.__version__ + " using Storm in version: " + stormpy.info.storm_version())
# lines = []
# with open('model.txt') as f:
#     lines = f.readlines()
# # print(lines[0])

# file_name = lines[0]

# # print(type(lines[0]))

# orig_program = stormpy.parse_prism_program(file_name)
# program = orig_program.define_constants(stormpy.parse_constants_string(orig_program.expression_manager, "init_pod=1, init_lat=1, init_cpu=1, init_demand=1, init_pow=1, init_rt=1, maxPod=100"))

# options = stormpy.BuilderOptions(True, True)
# options.set_build_state_valuations() 
# options.set_build_choice_labels()
# model = stormpy.build_sparse_model_with_options(program, options)
# print("Number of states: {}".format(model.nr_states))
# print("Labels: {}".format(model.labeling.get_labels()))

# # print(model.labeling.get_labels())

# for state in model.states:
#     if state.id in model.initial_states:
#         print("State {} is initial".format(state.id))
#     for action in state.actions:
#         for transition in action.transitions:
#             print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))

# properties = stormpy.parse_properties_for_prism_program("R{\"energy_consumption\"}max=? [ C<=1000 ]")
# result = stormpy.model_checking(model, properties[0])
# print(result.at(model.initial_states[0]))



# The probability

builder = stormpy.SparseMatrixBuilder(rows=0, columns=0, entries=0, force_dimensions=False, has_custom_row_grouping=True, row_groups=0)

builder.new_row_group(0)
builder.add_next_value(0, 1, 0.5)
builder.add_next_value(0, 2, 0.5)
builder.add_next_value(1, 1, 0.2)
builder.add_next_value(1, 2, 0.8)

builder.new_row_group(2)
builder.add_next_value(2, 3, 0.5)
builder.add_next_value(2, 4, 0.5)
builder.new_row_group(3)
builder.add_next_value(3, 5, 0.5)
builder.add_next_value(3, 6, 0.5)
builder.new_row_group(4)
builder.add_next_value(4, 7, 0.5)
builder.add_next_value(4, 1, 0.5)
builder.new_row_group(5)
builder.add_next_value(5, 8, 0.5)
builder.add_next_value(5, 9, 0.5)
builder.new_row_group(6)
builder.add_next_value(6, 10, 0.5)
builder.add_next_value(6, 11, 0.5)
builder.new_row_group(7)
builder.add_next_value(7, 2, 0.5)
builder.add_next_value(7, 12, 0.5)

for s in range(8, 14):
    builder.new_row_group(s)
    builder.add_next_value(s, s - 1, 1)

transition_matrix = builder.build()

choice_labeling = stormpy.storage.ChoiceLabeling(14)
choice_labels = {'a', 'b'}

for label in choice_labels:
    choice_labeling.add_label(label)

choice_labeling.add_label_to_choice('a', 0)
choice_labeling.add_label_to_choice('b', 1)
print(choice_labeling)

reward_models = {}
action_reward = [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
reward_models['coin_flips'] = stormpy.SparseRewardModel(optional_state_action_reward_vector=action_reward)

state_labeling = stormpy.storage.StateLabeling(13)

labels = {'init', 'one', 'two', 'three', 'four', 'five', 'six', 'done', 'deadlock'}
for label in labels:
    state_labeling.add_label(label)

state_labeling.add_label_to_state('init', 0)
print(state_labeling.get_states('init'))

state_labeling.add_label_to_state('one', 7)
state_labeling.add_label_to_state('two', 8)
state_labeling.add_label_to_state('three', 9)
state_labeling.add_label_to_state('four', 10)
state_labeling.add_label_to_state('five', 11)
state_labeling.add_label_to_state('six', 12)

print(state_labeling)

components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling, reward_models=reward_models, rate_transitions=False)
components.choice_labeling = choice_labeling

mdp = stormpy.storage.SparseMdp(components)
print(mdp)

for state in mdp.states:
    if state.id in mdp.initial_states:
        print("State {} is initial".format(state.id))
    for action in state.actions:
        for transition in action.transitions:
            print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))

