from enum import Enum


class ChannelEvent(Enum):
    # ==== GLOBAL EVENTS ====
    GLOBAL = 'global'

    # ==== ENGINE EVENTS ====
    AUDIO = 'audio'

    # ==== INPUT EVENTS ====
    INPUT_UI = 'input_ui'
    INPUT_GAME = 'input_game'

    # ==== LOGGING EVENTS ====
    LOGGING = 'logging'
