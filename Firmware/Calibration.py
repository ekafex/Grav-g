import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit

# #####################################################
# # Distance Calibration HC-SR04 

# d = np.array([[2,1.97],[3,2.97],[3.5,3.28],[4,3.5],
#               [5,4.26],[6,5.55],[7,6.53],[8,7.49],
#               [9,8.47],[10,9.85],[11,10.88],[12,11.86],
#               [15,14.63],[16,15.33],[17,16.60],
#               [19,18.20],[20,19.20],[25,24.60],
#               [30,29.30],[32,30.33],[35,33.44],
#               [38,36.4],[40,38.52],[45,43.60],
#               [50,48.25],[55,52.85],[60,57.18],
#               [65,62.25],[70,67.58],[75,72.21],
#               [80,76.06],[85,82.15],[90,87.04],
#               [95,92.15],[100,96.92],[110,106.75],
#               [120,116.30],[130,126.94],[140,136.91]])


# def Calibrated_HC_SR04(d_in):
#    # Measures distances >10cm with better than 1.5% 
#     return -0.59 + 1.07*d_in - 3.1e-4*d_in*d_in

# def D_fit(x,*p):
#     return p[0]+ p[1]*x + p[2]*x*x 

# p = curve_fit(D_fit, d[9:,1], d[9:,0], p0=(0,1,0))[0]

# ddd = np.linspace(0, 140,150)

# # pl.plot(d[9:,1], d[9:,0],'-ok',lw=2)
# # pl.plot(ddd, D_fit(ddd,*p),'-r',lw=2)

# pl.plot(d[9:,1], 1-D_fit(d[9:,1],*p)/d[9:,0],'-r',lw=2)
# pl.plot(d[9:,1], 1-Calibrated_HC_SR04(d[9:,1])/d[9:,0],'-k',lw=2)

#####################################################
# Time Calibration KY-037

DT = np.array([[10.26e-2,193.25e-3],[15.34e-2,239.56e-3],
   [25.02e-2,285.49e-3],[43.04e-2,348.63e-3],[56.82e-2,390.67e-3]])


dt = DT[:,1]
H  = DT[:,0]

def Calibrated_Time(dt):
    return dt - 53.7

def funfit(x,*p):
    return 9.807/2*(x-p[0])**2


p = curve_fit(funfit, dt, H, p0=(0,))[0]
tt = np.linspace(0.1,0.5,40)

pl.plot(dt, H,'-ok',lw=2)
pl.plot(tt, funfit(tt,*p),'-r',lw=2)

#####################################################
# # D = [H, dt]
# D=np.array([[10.52e-2,218.34e-3],[20.1e-2,259.52e-3],
#             [30.03e-2,315.32e-3],[40.34e-2,347.58e-3],
#             [50.09e-2,388.75e-3],[60.26e-2,403.02e-3],
#             [70.15e-2,438.18e-3],[80.77e-2,455.56e-3]])

# dt = D[:,1]
# H  = D[:,0]

# def funfit(x,*p):
#     return 9.8/2*(x-p[0])**2 + p[1]

# p = curve_fit(funfit, dt, H, p0=(0,0))[0]

# # h0  = 4.194 #cm
# # dt0 = 45.486 # ms
# # H* = H + h0; 
# # dt* = dt-dt0;

# # H = g*dt^2/2

# pl.plot(dt, H,'-ok',lw=2)

# tt = np.linspace(0.1,0.5,40)
# pl.plot(tt, funfit(tt,*p),'-r',lw=2)

