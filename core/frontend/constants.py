from pyaudio import paInt16


CHUNK          = 1024                                                # форма ауди-сигнала
FRT            = paInt16                                             # шестнадцатибитный формат для задания амплитуды
CHAN           = 2                                                   # каналы записи звука
RT             = 44100                                               # частота
REC_SEC        = 1                                                   # длина записи
OUTPUT_PATH =  r"core\frontend\output\output.wav"                   # имя выходного файля
APP_NAME       = "Alenushka"
COMPANY_NAME   = "РЖД"
T_GREETINGS    = "Вас приветствует голосовой помощник Аленушка!"
T_CHANGE_THEME = "изменить тему"
T_START_REC    = "начать запись"
T_STOP_REC     = "остановить запись"
RED            = '#E21A1A'
