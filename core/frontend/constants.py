from pyaudio import paInt16


CHUNK          = 1024                                                # форма ауди-сигнала
FRT            = paInt16                                             # шестнадцатибитный формат для задания амплитуды
CHAN           = 2                                                   # каналы записи звука
RT             = 44100                                               # частота
REC_SEC        = 5                                                   # длина записи
OUTPUT_PATH    =  r".\core\frontend\output\output.wav"                 # имя выходного файля
APP_NAME       = "Alenushka"
COMPANY_NAME   = "РЖД"
T_GREETINGS    = "Вас приветствует голосовой помощник Аленушка!"
T_CHANGE_THEME = "Изменить тему"
T_START_REC    = "Начать запись"
T_STOP_REC     = "Остановить запись"
RED            = '#E21A1A'
