import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.pyplot import cm
# Constants
rho = 1.29 # air density
cd = 0.47 #dragcoefficient
g = 9.81  # Acceleration due to gravity (m/s^2)
A = (np.pi * 0.04 ** 2)/4  # Cross-sectional area of ping pong ball (m^2)
m = 0.0027  # Mass of ping pong ball (kg)
cup_diameter = 0.08  # Diameter of cup opening (m)
cup_radius = cup_diameter / 2  # Radius of cup opening (m)
cup_height = 0.12  # Height of cup opening (m)
launch_distance = 1 # Distance from ball launch point to cup opening (m)
launch_height = 0.24
dt = 0.001 #s
plottenxtyt = False
arriving_angles = np.array([45])

totalelengteAfvuringsMechanisme = 0.15
#deze gegevens kloppen
rustlengteveer = 0.057
veerconstante = 327


def calculate_conditions(_yb,_xb,_ya,_theta_b):
    _time = math.sqrt((2*_xb*math.tan(math.radians(180-_theta_b))+2*(_ya-_yb))/(-g))
    _vbx = _xb/_time
    _vby = (-(g*_time**2+2*(_ya-_yb)))/(2*_time)
    _vax = _vbx
    _vay = _vby + g*_time
    _theta_a = math.degrees(math.atan(_vay/_vax))
    return _time, _vax,_vay, _theta_a,_vbx,_vby

# dikke bron: https://www.eng.mu.edu/nagurka/Nagurka_Aerodynamic%20Effects_IJEE1433.pdf
def cal_initial_conditions_with_air_resistance(_cd, _rho, _A, _m, _vx, _vy, _t):
    # effect of air resistance of xspeed of the ball
    # vx0 =vxA
    _k1 = (0.5*_cd*_rho*_A)/_m
    _vx0_teller = -2 * _m * _vx
    _vx0_noemer = _A*_rho*_cd*_vx*_t-2*_m
    _vx0 = _vx0_teller/_vx0_noemer
    # vy0 = vyA
    _k = (0.5*_cd*_rho*_A)/(_m*g)
    _vy0_teller = (np.sqrt(_k) * _vy +1) * np.exp(2 * g * np.sqrt(_k) * _t) + np.sqrt(_k) * _vy - 1
    _vy0_noemer = np.sqrt(_k)*((np.sqrt(_k) * _vy +1) * np.exp(2 * g * np.sqrt(_k) * _t) - np.sqrt(_k) * _vy + 1)
    _vy0 = _vy0_teller / _vy0_noemer
    return _vx0, _vy0

def horizontaal(v,t):
    dvdt = - ((0.5 * cd * rho * A) / m) * v ** 2
    return dvdt

def opwaarts(v,t):
    dvdt = -g-((0.5*cd*rho*A)/m)*v**2
    return dvdt

def neerwaarts(v,t):
    dvdt = -g+((0.5*cd*rho*A)/m)*v**2
    return dvdt

def lengteveerIngedrukt(_m,_theta,_lenteloop,_rustlengteveer,_veerconstante,_snehlheid):
    _veerconstante = _veerconstante*2 #2 identieke veren in parallel!!
    _lveerind = -(math.sqrt((g*_m*(math.sin(_theta))**2-2*g*_veerconstante*(_rustlengteveer-_lenteloop)*math.sin(_theta)+_veerconstante*_snehlheid**2)*_m)-g*m*math.sin(_theta)-_veerconstante*_rustlengteveer)/_veerconstante
    _indrukking = _rustlengteveer-_lveerind
    return _lveerind,_indrukking

def plot_xt_yt(_plot):
    if _plot == True:
        # x(t):
        fig1, axs1 = plt.subplots(nrows=1, ncols=2, figsize=(6, 5))
        axs1[0].plot(tijd_anal_np, x_analy_ar_np, '-')
        axs1[0].plot(tijd_num_np, x_num_ar_np, '--')
        axs1[0].plot(tijd_df_np, x_df_ar_np, '-.')
        axs1[0].set_xlabel('tijd t [s]')
        axs1[0].set_ylabel('Afstand x [m]')
        axs1[0].grid()
        # y(t)
        axs1[1].plot(tijd_anal_np, y_analy_ar_np, '-', label='Analytisch')
        axs1[1].plot(tijd_num_np, y_num_ar_np, '--', label='Numeriek')
        axs1[1].plot(tijd_df_np, y_df_ar_np, '-.', label='differential')
        axs1[1].set_xlabel('tijd t [s]')
        axs1[1].set_ylabel('Afstand y [m]')
        axs1[1].grid()
        fig1.legend()
        fig1.suptitle('fx(t) en y(t) voor hoek= {:.0f}°'.format(angle))

        fouty = np.abs(y_df_ar_np[:len(y_analy_ar_np)] - y_analy_ar_np[:len(y_df_ar_np)])
        plt.figure()
        plt.plot(tijd_df_np[:len(y_analy_ar_np)], fouty)
        plt.ylabel('Fout tussen y(t)_analytisch en y(t)_met differentiaal')
        plt.xlabel('Tijd [s]')

        foutx = np.abs(x_df_ar_np[:len(x_analy_ar_np)] - x_analy_ar_np[:len(x_df_ar_np)])
        plt.figure()
        plt.plot(tijd_df_np[:len(y_analy_ar_np)], foutx)
        plt.ylabel('Fout tussen x(t)_analytisch en x(t)_met differentiaal')
        plt.xlabel('Tijd [s]')


fig, axs = plt.subplots(figsize=(6,5))
for angle in arriving_angles:
    ########################################
    ########################################
    # initial conditions:
    ########################################
    ########################################
    tb,vax,vay,theta_a,vbx,vby = calculate_conditions(cup_height,launch_distance,launch_height,angle)
    beginsnelheid = math.sqrt(vay**2+vax**2)

    ########################################
    ########################################
    #traject without air resistance:
    ########################################
    ########################################
    tijd_np = np.arange(0, tb, dt)
    xtraject_np =vax*tijd_np
    ytraject_np = launch_height+vay*tijd_np-0.5*g*(tijd_np**2)

    ########################################
    ########################################
    #traject with air resistance analytically
    ########################################
    ########################################

    kx = (0.5*cd*rho*A)/m
    x_analy_ar_np =  np.log(np.abs(kx*vax*tijd_np+1))/kx

    ky = (0.5*cd*rho*A)/(m*g)
    y_analy_ar_np = np.zeros(len(tijd_np))
    t1 = np.arctan(vay*ky**0.5)/(g*ky**0.5)
    verschil = np.abs(tijd_np-t1)
    index_t1 = verschil.argmin()-1
    for i in range(0,len(tijd_np)):
        if tijd_np[i]<=t1:
            y_analy_ar_np[i]=launch_height + (2*np.log(np.cos(g*ky**0.5*tijd_np[i] - np.arctan(ky**0.5*vay))) - np.log(1/(ky*vay**2+1)))/(2*g*ky)
        else:
            y_analy_ar_np[i]= y_analy_ar_np[index_t1] - np.log(np.cosh(ky**0.5*g*(tijd_np[i]-t1)))/(g*ky)
        if y_analy_ar_np[i]<=cup_height or x_analy_ar_np[i]>=launch_distance:
            x_analy_ar_np = x_analy_ar_np[:i+1]
            y_analy_ar_np = y_analy_ar_np[:i+1]
            tijd_anal_np = tijd_np[:i+1]
            break
    ########################################
    ########################################
    #traject with air resistance numerically:
    ########################################
    ########################################
    x_num_ar_np = np.zeros(len(tijd_np))
    x_num_ar_np[0]= 0
    y_num_ar_np = np.zeros(len(tijd_np))
    y_num_ar_np[0]=launch_height

    vx_ar_np = np.zeros(len(tijd_np))
    vx_ar_np[0]= vax
    vy_ar_np = np.zeros(len(tijd_np))
    vy_ar_np[0] = vay

    for i in range(1,len(tijd_np)):
        ax = (-0.5*cd*rho*A*(vx_ar_np[i-1]**2))/m
        if vy_ar_np[i-1]>=0:
            ay = (-0.5 * cd * rho * A * (vx_ar_np[i - 1] ** 2) - m * g) / m
        else:
            ay = (0.5 * cd * rho * A * (vx_ar_np[i - 1] ** 2) - m * g) / m

        vx_ar_np[i] = vx_ar_np[i-1]+ax*dt
        vy_ar_np[i] = vy_ar_np[i-1]+ay*dt

        x_num_ar_np[i]= x_num_ar_np[i - 1] + vx_ar_np[i] * dt
        y_num_ar_np[i]= y_num_ar_np[i - 1] + vy_ar_np[i] * dt

        if y_num_ar_np[i]<=cup_height or x_num_ar_np[i]>=launch_distance:
            x_num_ar_np = x_num_ar_np[:i]
            y_num_ar_np = y_num_ar_np[:i]
            tijd_num_np=tijd_np[:i]
            break

    ########################################
    ########################################
    # traject with air resistance with partial solver:
    ########################################
    ########################################

    tijd_opwaarts_np = np.arange(0,t1,dt)
    tijd_neerwaarts_np = np.arange(t1,tb,dt)
    tijd_df_np = np.concatenate((tijd_opwaarts_np,tijd_neerwaarts_np))

    vx_df_np = odeint(horizontaal,vax,tijd_df_np)

    vy_opwaarts_np = odeint(opwaarts,vay,tijd_opwaarts_np)
    vy_neerwaarts_np = odeint(neerwaarts,0,tijd_neerwaarts_np)
    vy_df_np = np.concatenate((vy_opwaarts_np,vy_neerwaarts_np))

    x_df_ar_np = np.zeros(len(tijd_np))
    x_df_ar_np[0] = 0
    y_df_ar_np = np.zeros(len(tijd_df_np))
    y_df_ar_np[0] = launch_height

    for i in range(1, len(tijd_df_np)):
        y_df_ar_np[i] = y_df_ar_np[i-1]+vy_df_np[i]*dt
        x_df_ar_np[i] = x_df_ar_np[i - 1] + vx_df_np[i] * dt

        if y_df_ar_np[i]<=cup_height or x_df_ar_np[i]>=launch_distance:
            x_df_ar_np = x_df_ar_np[:i]
            y_df_ar_np = y_df_ar_np[:i]
            tijd_df_np=tijd_df_np[:i]
            break

    ########################################
    ########################################
    # new traject to get in the cup
    ########################################
    ########################################
    tijd_new_np = np.arange(0,5, dt)

    x_new_np = np.zeros(len(tijd_new_np))
    vx_new_np = np.zeros(len(tijd_new_np))

    y_new_np = np.zeros(len(tijd_new_np))
    y_new_np[0] = launch_height
    vy_new_np = np.zeros(len(tijd_new_np))

    vx0 = vax
    vy0 = vay
    num_loops = 0
    while (abs(x_new_np[-1]-launch_distance)>0.0001 and num_loops<10000) or (abs(y_new_np[-1]-cup_height)>0.0001 and num_loops<10000):
        if abs(x_new_np[-1]-launch_distance)>0.0001:
            vx0 = vx0 + 0.0001
        elif abs(y_new_np[-1]-cup_height)>0.0001:
            vy0 = vy0 + 0.0001

        tijd_new_np = np.arange(0,5,dt)
        x_new_np = np.zeros(len(tijd_new_np))
        vx_new_np = np.zeros(len(tijd_new_np))

        y_new_np = np.zeros(len(tijd_new_np))
        y_new_np[0] = launch_height
        vy_new_np = np.zeros(len(tijd_new_np))

        num_loops = num_loops+1

        vx_new_np[0] = vx0
        vy_new_np[0] = vy0

        kx = (0.5 * cd * rho * A) / m
        x_new_np = np.log(np.abs(kx * vx0 * tijd_new_np + 1)) / kx
        vx_new_np = vx0/(vx0*kx*tijd_new_np+1)

        ky = (0.5 * cd * rho * A) / (m * g)
        t1_new = np.arctan(vy0 * ky ** 0.5) / (g * ky ** 0.5)
        verschil_new = np.abs(tijd_new_np - t1_new)
        index_t1_new = verschil_new.argmin() - 1
        for i in range(1, len(tijd_new_np)):
            if tijd_new_np[i] <= t1_new:
                vy_new_np[i] = np.tan(np.arctan(vy0*ky**0.5)-g*tijd_new_np[i]*ky**0.5)/ky**0.5
                y_new_np[i] = launch_height + (2 * np.log(np.cos(g * ky ** 0.5 * tijd_new_np[i] - np.arctan(ky ** 0.5 * vy0))) - np.log(1 / (ky * vy0 ** 2 + 1))) / (2 * g * ky)
            else:
                vy_new_np[i] = np.tanh(ky**0.5*g*(t1_new-tijd_new_np[i]))/ky**0.5
                y_new_np[i] = y_new_np[index_t1_new] - np.log(np.cosh(ky ** 0.5 * g * (tijd_new_np[i] - t1_new))) / (g * ky)

            if y_new_np[i]<=cup_height:
                x_new_np = x_new_np[:i + 1]
                vx_new_np = vx_new_np[:i+1]

                y_new_np = y_new_np[:i + 1]
                vy_new_np = vy_new_np[:i+1]

                tijd_new_np = tijd_new_np[:i + 1]
                break
    new_angle = np.abs(np.arctan(vy_new_np[-1]/vx_new_np[-1])*180/np.pi)
    new_theta_a = np.abs(np.arctan(vy_new_np[0]/vx_new_np[0])*180/np.pi)
    new_beginssnelheid = math.sqrt(vy_new_np[0]**2+vx_new_np[0]**2)
    new_trajectduur = tijd_new_np[-1]

    if 'tijd_anal_np' not in locals() or 'tijd_anal_np' not in globals():
        tijd_anal_np = tijd_np
    if 'tijd_num_np' not in locals() or 'tijd_num_np' not in globals():
        tijd_num_np =tijd_np

    ################
    ################
    # x-y traject
    if len(arriving_angles)==1:
        axs.plot(xtraject_np, ytraject_np, '-',
                 label=f'Zonder luchtweerstand: Voor landingshoek= {round(angle, 3)}° is beginhoek= {round(theta_a, 3)}° en beginsnelheid= {round(beginsnelheid, 3)}m/s en trajectduur= {round(tb, 3)}s')
        # axs.plot(x_num_ar_np, y_num_ar_np, '--', label=f'Met luchtweerstand en dezelfde condities en numeriek')
        axs.plot(x_analy_ar_np, y_analy_ar_np, '-.', label=f'Met luchtweerstand en analytisch')
        axs.plot(x_df_ar_np, y_df_ar_np, '-.', label=f'Met luchtweerstand en differentiaal')
        axs.plot(x_new_np, y_new_np, '--',
                 label=f'Met luchtweerstand: Voor landingshoek= {round(new_angle, 3)}° is beginhoek= {round(new_theta_a, 3)}° en beginsnelheid= {round(new_beginssnelheid, 3)}m/s en trajectduur= {round(new_trajectduur, 3)}s')
    else:
        axs.plot(xtraject_np, ytraject_np, '-',label=f'Zonder luchtweerstand: Voor landingshoek= {round(angle, 3)}° is beginhoek= {round(theta_a, 3)}° en beginsnelheid= {round(beginsnelheid, 3)}m/s en trajectduur= {round(tb, 3)}s')
        axs.plot(x_new_np, y_new_np, '--',label=f'Met luchtweerstand: Voor landingshoek= {round(new_angle, 3)}° is beginhoek= {round(new_theta_a, 3)}° en beginsnelheid= {round(new_beginssnelheid, 3)}m/s en trajectduur= {round(new_trajectduur, 3)}s')
    plot_xt_yt(plottenxtyt)
    ################
    ################

    veerIngedrukt,lengteverschil = lengteveerIngedrukt(m,new_theta_a,totalelengteAfvuringsMechanisme,rustlengteveer,veerconstante,new_beginssnelheid)
    print(f'Voor hoek: {round(new_angle,2)}° is moet de veer: {round(lengteverschil,4)}m ingedrukt worden, waardoor lengte veer = {round(veerIngedrukt,4)}m')


axs.set_xlabel('Afstand x [m]')
axs.set_ylabel('Afstand y [m]')
fig.suptitle('y(x)')
axs.grid()
fig.legend(bbox_to_anchor=(1,1),loc='upper right')
fig.tight_layout()