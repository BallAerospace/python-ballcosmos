from ballcosmos.script.script import *


def replay_select_file(filename, packet_log_reader="DEFAULT"):
    return ballcosmos.script.script.cmd_tlm_server.write(
        "replay_select_file", filename, packet_log_reader
    )


def replay_status():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_status")


def replay_set_playback_delay(delay):
    return ballcosmos.script.script.cmd_tlm_server.write(
        "replay_set_playback_delay", delay
    )


def replay_play():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_play")


def replay_reverse_play():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_reverse_play")


def replay_stop():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_stop")


def replay_step_forward():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_step_forward")


def replay_step_back():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_step_back")


def replay_move_start():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_move_start")


def replay_move_end():
    return ballcosmos.script.script.cmd_tlm_server.write("replay_move_end")


def replay_move_index(index):
    return ballcosmos.script.script.cmd_tlm_server.write("replay_move_index", index)
