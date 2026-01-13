from enum import Enum


class ChannelEvent(Enum):
    # ==== GLOBAL EVENTS ====
    GLOBAL = 'global'

    # ==== ENGINE EVENTS ====
    AUDIO = 'audio'

    # ==== LOGGING EVENTS ====
    LOGGING = 'logging'
