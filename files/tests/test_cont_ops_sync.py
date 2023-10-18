"""
File in charge of testing the program
"""
# tests/test_tty_ov.py
import os
import sys
from platform import system
sys.path.append(os.path.join(os.getcwd(), "..", "src"))
sys.path.append(os.path.join(os.getcwd(), "src"))

print(os.getcwd())

if "../" == "../":
    import constants as CONST
    from main import Main
else:
    from src import constants as CONST
    from src.main import Main

ERR = CONST.ERR
ERROR = CONST.ERROR
SUCCESS = CONST.SUCCESS
CURRENT_SYSTEM = system()


def _initialise_class(argv: list = [""]) -> Main:
    """ Load the main class of the program for testing """
    COLOURISE_OUTPUT = True
    if "-nc" in argv or "--no-colour" in argv:
        COLOURISE_OUTPUT = False
    main = Main(COLOURISE_OUTPUT)
    main.call_injectors()
    main.add_spacing()
    return main


def _list_dict_to_dict(list_dict: list[dict]) -> dict:
    """ Transform a list of dictionary into a dictionary """
    result = {}
    for i in list_dict:
        result.update(i)
    return result


def _list_to_dict(list_input: list, filler: any) -> dict:
    """ Transform a list into a dictionary """
    filler_list = [filler] * len(list_input)
    tuples = zip(list_input, filler_list)
    result = dict(tuples)
    return result


def _de_initialise_class(main: Main) -> int:
    """ Unload the main class of the program """
    status = main.tty.unload_basics()
    main = None
    return status


def test_all_test_functions() -> None:
    """ Test all the pre_built functions """
    MI = _initialise_class([""])
    MI.tty.process_complex_input(["docker_class_test"])
    status1 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["docker_compose_class_test"])
    status2 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["kubernetes_class_test"])
    status3 = MI.tty.current_tty_status
    _de_initialise_class(MI)
    MI = None

    assert status1 == SUCCESS
    assert status2 == SUCCESS
    assert status3 == SUCCESS


def test_the_is() -> None:
    """ Test the boolean functions in charge of testing if an element is installed """
    expected_response = ERROR
    MI = _initialise_class([""])
    MI.tty.process_complex_input(["is_admin"])
    status1 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_docker_installed"])
    status2 = MI.tty.current_tty_status
    if status2 == SUCCESS and CURRENT_SYSTEM == "Windows":
        status2 = expected_response
    MI.tty.process_complex_input(["is_image_built"])
    status3 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_docker_compose_installed"])
    status4 = MI.tty.current_tty_status
    if status4 == SUCCESS and CURRENT_SYSTEM == "Windows":
        status4 = expected_response
    MI.tty.process_complex_input(["is_image_run"])
    status5 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_kubectl_installed"])
    status6 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_minikube_installed"])
    status7 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_kind_installed"])
    status8 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_k3s_installed"])
    status9 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_k3d_installed"])
    status10 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_microk8s_installed"])
    status11 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_k8s_installed"])
    status12 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_kubeadm_installed"])
    status13 = MI.tty.current_tty_status
    MI.tty.process_complex_input(["is_kubernetes_installed"])
    status14 = MI.tty.current_tty_status
    status0 = _de_initialise_class(MI)

    # print(f"status1 = {status1}, status2 = {status2}, status3 = {status3}, status4 = {status4}, status5 = {status5}, status6 = {status6}, status7 = {status7}, status8 = {status8}, status9 = {status9}, status10 = {status10}, status11 = {status11}, status12 = {status12}, status13 = {status13}, status14 = {status14}, status0 = {status0}")

    assert status1 == SUCCESS
    assert status2 == expected_response
    assert status3 == expected_response
    assert status4 == expected_response
    assert status5 == expected_response
    assert status6 == expected_response
    assert status7 == expected_response
    assert status8 == expected_response
    assert status9 == expected_response
    assert status10 == expected_response
    assert status11 == expected_response
    assert status12 == expected_response
    assert status13 == expected_response
    assert status14 == expected_response
    assert status0 == SUCCESS


def test_help() -> None:
    """ Test the help functions in order to see if some are miss programmed """
    MI = _initialise_class([""])
    help_options = _list_dict_to_dict(MI.tty.options)
    help_result = _list_to_dict(list(help_options), SUCCESS)
    print(f"help_options = {help_options}, help_result = {help_result}")
    for i in help_options:
        if i == "desc":
            continue
        MI.tty.process_complex_input(["help", i])
        help_result[i] = MI.tty.current_tty_status
    status0 = _de_initialise_class(MI)

    help_result_list = list(help_result.values())
    if ERR or ERROR in help_result_list:
        print(f"Help analysis result: {help_result}")
    assert ERROR not in help_result_list
    assert ERR not in help_result_list
    assert status0 == SUCCESS


if __name__ == "__main__":
    test_all_test_functions()
    test_the_is()
    test_help()
    print("All tests passed")
