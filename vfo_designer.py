import math as m
import numpy as np
import matplotlib.pyplot as plt


def get_parallel_L_C(C_v_min, C_v_max, C_s, f_min, f_max):

    # Circuit schematic
    schematic = """
     -------------------
     |       |        |
    C        {0} C_v    |
    C  L     |        = C_p
    C        |        |
    C        = C_s    |
     |       |        |
     -------------------
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


if __name__=="__main__":

    # Get parameters
    f_min = float(input("Minimum desired frequency in MHz?"))*1e6
    f_max = float(input("Maximum desired frequency in MHz?"))*1e6
    C_v_min = float(input("Minimum variable capacitance in pF?"))*1e-12
    C_v_max = float(input("Maximum variable capacitance in pF?"))*1e-12

    # Series capacitances
    C_s = np.logspace(-12, -10, 10)

    plt.figure()
    print("{0:<20}{1:<20}{2:<20}".format("Series C [pF]", "Parallel C [pF]", "Parallel L [uH]"))
    print("".join(["-"]*60))

    for i in range(10):
        C_p, L, schematic = get_parallel_L_C(C_v_min, C_v_max, C_s[i], f_min, f_max)
        print("{0:<20}{1:<20}{2:<20}".format(C_s[i]*1e12, C_p*1e12, L*1e6))


        # Get frequency over range of C_v
        C_v = np.linspace(C_v_min, C_v_max, 1000)
        C = (1/C_s[i]+1/C_v)**-1+C_p
        f = 1/(2.0*m.pi*np.sqrt(L*C))
        plt.plot(C_v*1e12, f*0.000001, label=str(C_s[i]*1e12))

    print(schematic)
    plt.legend(title="Series C [pF]")
    plt.xlabel('Variable Capacitance [pF]')
    plt.ylabel('Frequency [MHz]')
    plt.show()
