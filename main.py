import sys
import os

sys.path.append(r'C:\Programs\3DS Max\3ds Max Design 2015')
import MaxPlus

scriptPassLimit = 'renderers.current.progressive_passLimit'
scriptNoiseLimit = 'renderers.current.adaptivity_targetError'
scriptTimeLimit = 'renderers.current.progressive_timeLimit'


def set_coronarenderer():
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


def get_limits():
    """
    Получает значения всех трех лимитов Corona Renderer'a
    Возвращает кортеж из них
    """
    return (MaxPlus.Core.EvalMAXScript(scriptPassLimit).GetInt64(),
            MaxPlus.Core.EvalMAXScript(scriptNoiseLimit).GetFloat(),
            MaxPlus.Core.EvalMAXScript(scriptTimeLimit).GetInt64())


def set_limits(passLim=-1, noiseLim=-1.0, timeLim=-1):
    """
    Устанавливает значения лимитов

    Несмотря на 'The format is HOURS:MINUTES:SECONDS' из документации,
    значение timeLimit задается в мс!
    """
    maxscript = ''
    if int(passLim)>=0:
        maxscript += '{0} = {1}'.format(scriptPassLimit, passLim)
    if float(noiseLim)>=0:
        maxscript += '{0} = {1}'.format(scriptNoiseLimit, noiseLim)
    if int(timeLim)>=0:
        maxscript += '{0} = {1}'.format(scriptTimeLimit, int(timeLim)*1000) # timeLimit в мс

    if maxscript:
        MaxPlus.Core.EvalMAXScript(maxscript)


def write_to_file(path, limits):
    f = open(path, 'w')
    f.write("PassLimit: {}\n".format(limits[0]))
    f.write("NoiseLimit: {}\n".format(limits[1]))
    f.write("TimeLimit: {} (sec)".format(limits[2] / 1000))
    f.close()


def read_params():
    """
    производит чтение параметров из файла. Затем файл удаляется
    """
    paramsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params.txt')
    f = open(paramsPath,'r')
    data = f.readlines()[1:] #пропускаем команду get/set
    f.close()
    os.remove(paramsPath)
    return data


def read_command():
    paramsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params.txt')
    f = open(paramsPath, 'r')
    data = f.readline().replace('\n', '')
    f.close()
    return data


command = read_command()
if set_coronarenderer():
    if command=='get':
        path = read_params()[0]
        limits = get_limits()  # получаем текущие значения лимитов
        write_to_file(path, limits)  # сохраняем результаты в файл
    else:
        passLim, noiseLim, timeLim = read_params()
        set_limits(passLim, noiseLim, timeLim)  # устанавливаем новые значения
else:
    print "Corona renderer not found!"