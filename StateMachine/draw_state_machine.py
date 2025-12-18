from transitions.extensions import GraphMachine

graph_title = 'TestSuiteStateMachine'
states = [
    'start',
    'set_dut_ip',
    'test_next_case',
    'check_full_test',
    'success',
    'failure',
    'op_select_mode',
    'set_mes_as_repair',
    'set_pass_fail_with_db',
    'end',
]
transitions = [
    {'trigger': 'start', 'source': 'start', 'dest': 'set_dut_ip', 'before': ['start_timer', 'disable_all_cases_option', 'let_ui_consistent_with_db']},
            {'trigger': 'next', 'source': 'set_dut_ip', 'dest': 'test_next_case'},
            {'trigger': 'start', 'source': 'start', 'dest': 'failure', 'before': ['start_timer', 'disable_all_cases_option']},
            {'trigger': 'next', 'source': 'test_next_case', 'dest': 'success', 'conditions': ['nothing_under_testing', 'is_exhausted']},
            {'trigger': 'next', 'source': 'test_next_case', 'dest': 'test_next_case'},
            {'trigger': 'disagree', 'source': 'test_next_case', 'dest': 'check_full_test'},
            {'trigger': 'next', 'source': 'check_full_test', 'dest': 'failure', 'conditions': ['is_exhausted', 'nothing_under_testing']},
            {'trigger': 'next', 'source': 'check_full_test', 'dest': 'test_next_case'},
            {'trigger': 'disagree', 'source': ['set_dut_ip', 'check_full_test'], 'dest': 'failure'},
            {'trigger': 'stop', 'source': ['test_next_case', 'success', 'failure', 'op_select_mode', 'set_mes_as_repair', 'set_pass_fail_with_db',
                                           'check_full_test'], 'dest': 'end', 'before': ['stop_timer', 'update_test_result', 'recover_all_cases_option']},
            {'trigger': 'disagree', 'source': ['success', 'set_pass_fail_with_db'], 'dest': 'end', 'before': ['stop_timer', 'update_test_result', 'recover_all_cases_option']},
            {'trigger': "TRIGGER_SKIP_OP_SELECT_MODE", 'source': 'failure', 'dest': 'end', 'before': ['stop_timer', 'update_test_result', 'recover_all_cases_option']},
            {'trigger': 'next', 'source': 'failure', 'dest': 'op_select_mode'},
            {'trigger': "TRIGGER_REPAIR", 'source': 'set_mes_as_repair', 'dest': 'set_pass_fail_with_db'},
            {'trigger': "TRIGGER_RETRY_TEST", 'source': 'op_select_mode', 'dest': 'set_pass_fail_with_db'},
            {'trigger': "TRIGGER_MES_EXIST_FAIL", 'source': 'op_select_mode', 'dest': 'set_pass_fail_with_db'},
            {'trigger': "TRIGGER_REPAIR", 'source': 'op_select_mode', 'dest': 'set_mes_as_repair'},
            {'trigger': "TRIGGER_USER_SAY_NO", 'source': 'op_select_mode', 'dest': 'set_pass_fail_with_db'},
            {'trigger': 'next', 'source': 'op_select_mode', 'dest': 'set_mes_as_repair'},
            {'trigger': 'stop', 'source': 'end', 'dest': 'end'},
        ]

# cmd_folder = os.path.realpath(
#     os.path.dirname(
#         os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])))
#
# if cmd_folder not in sys.path:
#     sys.path.insert(0, cmd_folder)


class Matter(object):
    # graph object is created by the machine
    def show_graph(self, **kwargs):
        self.get_graph(**kwargs).draw('{}.png'.format(graph_title), prog='dot', format='png')


model = Matter()
machine = GraphMachine(model=model,
                       states=states,
                       transitions=transitions,
                       initial='start',
                       show_auto_transitions=False, # default value is False
                       title=graph_title,
                       show_conditions=True)
model.show_graph()

print (Matter.__name__)