import logging
import coloredlogs
import verboselogs

verboselogs.install()
coloredlogs.install(level="INFO", fmt=' %(levelname)s: %(message)s')


class TrackProgress:
    success = 0
    failure = 0
    file_exists = 0