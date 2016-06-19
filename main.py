import sys
import os

sys.path.append(r'C:\Programs\3DS Max\3ds Max Design 2015')
import MaxPlus

scriptPassLimit = 'renderers.current.progressive_passLimit'
scriptNoiseLimit = 'renderers.current.adaptivity_targetError'
scriptTimeLimit = 'renderers.current.progressive_timeLimit'


def setCoronaRenderer():
    """
    Устанавливает Corona Renderer, если был выбран другой движок
    """
    scriptSwitchRenderer = '''if (classof renderers.current != Corona_1_4) then(
    renderers.current = Corona_1_4()
)'''
    try:
        MaxPlus.Core.EvalMAXScript(scriptSwitchRenderer)
        return True
    except:
        return False


def getLimits():
    """
    Получает значения всех трех лимитов Corona Renderer'a
    Возвращает кортеж из них
    """
    return (MaxPlus.Core.EvalMAXScript(scriptPassLimit).GetInt64(),
            MaxPlus.Core.EvalMAXScript(scriptNoiseLimit).GetFloat(),
            MaxPlus.Core.EvalMAXScript(scriptTimeLimit).GetInt64())


def setLimits(passLim=0, noiseLim=0.0, timeLim=0):
    """
    Устанавливает значения лимитов

    Несмотря на 'The format is HOURS:MINUTES:SECONDS' из документации,
    значение timeLimit задается в мс!
    """
    maxscript = '{0} = {1}\n'.format(scriptPassLimit, passLim) \
                + '{0} = {1}\n'.format(scriptNoiseLimit, noiseLim) \
                + '{0} = {1}\n'.format(scriptTimeLimit, timeLim*1000) # timeLimit в мс
    MaxPlus.Core.EvalMAXScript(maxscript)


def writeLimitsToFile(path, limits):
    f = open(path, 'w')
    f.write("PassLimit: {}\n".format(limits[0]))
    f.write("NoiseLimit: {}\n".format(limits[1]))
    f.write("TimeLimit: {} (сек)".format(limits[2]))
    f.close()


def readParams():
    """
    производит чтение параметров из файла. Затем файл удаляется
    """
    paramsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params.txt')
    f = open(paramsPath,'r')
    data = f.readlines()
    f.close()
    os.remove(paramsPath)
    return data


passLim, noiseLim, timeLim, path = readParams() # получаем значения параметров
if setCoronaRenderer(): # пытаемся установить CoronaRenderer в качестве рендер-движка
    setLimits(passLim, noiseLim, timeLim) # устанавливаем значения лимитов
    limits = getLimits() # получаем значения лимитов
    writeLimitsToFile(path, limits) # сохраняем результаты в файл
else:
    print "Corona renderer not found!"