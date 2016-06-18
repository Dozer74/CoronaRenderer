import sys

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
                + '{0} = {1}\n'.format(scriptTimeLimit, timeLim)
    MaxPlus.Core.EvalMAXScript(maxscript)


def writeLimitsToFile(path, limits):
    f = open(path, 'w')
    f.write("PassLimit: {}\n".format(limits[0]))
    f.write("NoiseLimit: {}\n".format(limits[1]))
    f.write("TimeLimit: {} (сек)".format(limits[2] / 1000.0))
    f.close()


if setCoronaRenderer():
    setLimits(1, 2.08, 3000)
    limits = getLimits()
    writeLimitsToFile(r"C:\Users\dozer\Desktop\result.txt", limits)
else:
    print "Corona renderer not found!"