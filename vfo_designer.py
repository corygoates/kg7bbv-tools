import math as m
import numpy as np
import matplotlib.pyplot as plt


def get_parallel_L_C(C_v_min, C_v_max, C_s, f_min, f_max):

    # Circuit schematic
    schematic = """
     -----------------------
     |       |        |
    C        {0} C_v    |
    C  L     |        = C_p
    C        |        |
    C        = C_s    |
     |       |        |
     -----------------------
     |
     _
     -
    """.format(u"\u2260")

    # Variable capacitance range
    C_v_t_min = (1/C_s+1/C_v_min)**-1
    C_v_t_max = (1/C_s+1/C_v_max)**-1

    # Calculate required parallel capacitance and inductance
    C_v = C_v_t_max-C_v_t_min
    r = (f_min/f_max)**2
    C_f = r/(1-r)*C_v
    C_p = C_f-C_v_t_min
    L = 1/(4*np.pi**2*f_min**2*(C_v_t_max+C_p))

    return C_p, L, schematic


class ProgressiveVFO:
    """VFO from Hayward and Lawson "A Progressive Communications Receiver" QST 1981-11."""


    def __init__(self, L, C1, Cv, f_min, f_max):

        # Store params
        self.L = L
        self.C1 = C1
        self.Cv = Cv

        # Circuit schematic
        self.schematic = """
         ---------------------------
         |       |        |
        C        = C3  C1 =
        C  L     |        |_____
        C        |        |    |
        C        |     C2 =    {0} Cv
         |       |        |    |
         ---------------------------
         |
         _
         -
        """.format(u"\u2260")

        # Calculate required capacitances
        wl = 2.0*np.pi*f_min
        wu = 2.0*np.pi*f_max
        Cl = 1.0/(wl**2*L)
        Cu = 1.0/(wu**2*L)
        dC = Cl-Cu
        x = 2.0*C1+Cv
        y = C1*Cv+C1**2*(1-Cv/dC)
        self.C2 = 0.5*(-x+np.sqrt(x**2-4*y))
        self.C3 = Cv-1.0/(1.0/C1+1.0/self.C2)

    
    def plot_tuning(self):
        """Plots the tuning range of the VFO over a linear variation in Cv."""

        # Calculate frequencies
        Cv_range = np.linspace(0.0, self.Cv, 1000)
        C = self.C3+1.0/(1.0/self.C1+1.0/(self.C2+Cv_range))
        f = 1.0/(2.0*np.pi*np.sqrt(self.L*C))

        # PLot
        plt.figure()
        plt.plot(Cv_range*1e12, f*1e6)
        plt.xlabel('$C_v$ [pF]')
        plt.ylabel('f [MHz]')
        plt.show()


if __name__=="__main__":

    vfo = ProgressiveVFO(0.784e-6, 15.0e-12, 145.0e-12, 14.225e6, 14.350e6)
    vfo.plot_tuning()

    ## Get parameters
    #f_min = float(input("Minimum desired frequency in MHz?"))*1e6
    #f_max = float(input("Maximum desired frequency in MHz?"))*1e6
    #C_v_min = float(input("Minimum variable capacitance in pF?"))*1e-12
    #C_v_max = float(input("Maximum variable capacitance in pF?"))*1e-12

    ## Series capacitances
    #C_s = np.logspace(-12, -10, 10)

    #plt.figure()
    #print("{0:<20}{1:<20}{2:<20}".format("Series C [pF]", "Parallel C [pF]", "Parallel L [uH]"))
    #print("".join(["-"]*60))

    #for i in range(10):
    #    C_p, L, schematic = get_parallel_L_C(C_v_min, C_v_max, C_s[i], f_min, f_max)
    #    print("{0:<20}{1:<20}{2:<20}".format(C_s[i]*1e12, C_p*1e12, L*1e6))


    #    # Get frequency over range of C_v
    #    C_v = np.linspace(C_v_min, C_v_max, 1000)
    #    C = (1/C_s[i]+1/C_v)**-1+C_p
    #    f = 1/(2.0*m.pi*np.sqrt(L*C))
    #    plt.plot(C_v*1e12, f*0.000001, label=str(C_s[i]*1e12))

    #print(schematic)
    #plt.legend(title="Series C [pF]")
    #plt.xlabel('Variable Capacitance [pF]')
    #plt.ylabel('Frequency [MHz]')
    #plt.show()
