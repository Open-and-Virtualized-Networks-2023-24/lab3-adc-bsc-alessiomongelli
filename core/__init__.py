import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol

color_dict = mcol.TABLEAU_COLORS


def lin2db(x):
    return 10 * np.log10(x)


def db2lin(x):
    return 10 ** (x / 10)


class ADC:
    fs_step = 2.75625e3

    def __init__(self):
        pass

    def __init__(self, nbit):
        self.nbit = nbit

    def qSNR(self):
        return 10 * np.log10(self.nbit * 6)


class BSC:

    def __init__(self):
        pass

    def __init__(self, Pe):
        self.Pe = Pe

    def bSNR(self):
        return 10 * np.log10(1 / (self.Pe * 4))


class PCM:

    def __init__(self):
        pass

    def __init__(self, analog_bandwidth, nbit_adc, Pe_bsc):
        self.analog_bandwidth = analog_bandwidth
        self.adc = ADC(nbit_adc)
        self.bsc = BSC(Pe_bsc)

    def snr(self):
        qsnr = self.adc.qSNR()
        bsnr = self.bsc.bSNR()
        return 1 / ((1 / qsnr) + (1 / bsnr))

    def critical_pe(self):
        qsnr = self.adc.qSNR()
        return 1 / (4 * 10 ** (qsnr / 20))


def exercise_1():
    nbitlist = np.array([2, 3, 4, 6, 8, 10, 12], np.int64)
    ADCSNR = ADC(nbitlist).qSNR()

    Pevals = np.logspace(-12, 0, 100)  # Utilizziamo logspace per generare valori logaritmici in modo uniforme
    bSnrvals = [BSC(Pe).bSNR() for Pe in Pevals]

    plt.figure()
    plt.plot(nbitlist, ADCSNR, color='r')
    plt.title('quantization SNR')
    plt.xlabel('nbit')
    plt.ylabel('SNR(dB)')
    plt.show()

    plt.figure()
    plt.plot(Pevals, bSnrvals, color='b')
    plt.title('BSC SNR')
    plt.xlabel('Pe')
    plt.xscale('log')
    plt.ylabel('SNR(dB)')
    plt.show()
    pass


def exercise_2():
    Pevals = np.linspace(1e-12, 1, 100)
    nbitlist = [2, 4, 6, 8]
    nbitarray = np.array([2, 4, 8, 16], np.int64)
    plt.figure()
    pTH = []

    for i, el in enumerate(nbitlist):
        OVRSNR = [PCM(1000, el, Pe).snr() for Pe in Pevals]
        plt.plot(OVRSNR, Pevals, label=f'nbit={el}', color=plt.cm.plasma(i / len(nbitlist)))
        pTH.append(PCM(1000, el, 0).critical_pe())  # Aggiunto solo il valore critico per ogni configurazione nbit

    plt.title('PCM overall SNR')
    plt.legend()
    plt.xscale('log')

    QuantSNR = [ADC(nbit).qSNR() for nbit in nbitlist]

    for el in QuantSNR:
        plt.axhline(el, linestyle='--', color='gray', label='Quantization SNR')

    for el in pTH:
        plt.axvline(el, linestyle='--', color='gray', label='Critical Error')

    plt.show()
    pass


def exercise_3():
    def calculate_nbit(dSNR):
        dSNR = 80
        tnbit = int(dSNR / 6)
        return tnbit

    class PCM:
        def __init__(self, Pe, bandwidth):
            self.bandwidth = bandwidth
            self.Pe = Pe
            self.nbit = calculate_nbit(80)
            self.SNR = self.calculate_SNR()

        def calculate_SNR(self):
            return self.nbit * 6

        def calculate_BSC_performance(self):
            Peth = 1 / (4 * ((2 ** self.nbit) - 1))
            if Peth >= self.Pe:
                print("BSC compatible")
            else:
                print("BSC not compatible")

    pass


if __name__ == "__main__":
    print("Laboratory 3 - ADC-BSC")

    exercise_1()
    exercise_2()
    exercise_3()