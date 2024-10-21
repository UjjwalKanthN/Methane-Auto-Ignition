import sys
import numpy as np 
import cantera as ct 
import matplotlib.pyplot as plt 

gas = ct.Solution('gri30.xml')

T = 1250
P_start = 101325
P_end = 5*101325

sim_time = 10*1000  #10 seconds

n = 8 # Number of values for pressure
press = np.linspace(P_start,P_end,n)
Ignition_delay = []

for P in press:

	gas.TPX = T, P, {'CH4':1, 'O2':2, 'N2':7.52}
	r = ct.IdealGasReactor(gas) # Reactor
	sim = ct.ReactorNet([r]) # Reactor Network

	time = 0.0 # Initial Time

	# States of Reactor which include all attribiutes of the reactor
	states = ct.SolutionArray(gas, extra = ['t_ms','t'])

	T_old = T

	i = 1
	for i in range(sim_time+1):
		time += 1e-03

		sim.advance(time) # Advancing the reactor w.r.t the time step

		states.append(r.thermo.state, t_ms = time*1e3, t = time)

		T_new = states.T
		T_new = T_new[i-1]

		if ((T_new - T_old)>=400):
			Ignition_delay.append(time)

		T_old = states.T
		T_old = T_old[i-1]

	plt.subplot(2,1,1)
	plt.plot(states.t_ms, states.T)

plt.legend(['P_start = ' + str(P/101325) + '[atm]' for P in press])
plt.xlabel('Time [ms]')
plt.ylabel('Temperature [K]')
#plt.title('Ignition Delay with Temperature Variation')

plt.subplot(2,1,2)
plt.plot(press/101325, Ignition_delay, '-o')
plt.xlabel('Initial Pressure [Pa]')
plt.ylabel('Ignition Delay [ms]')
plt.title('Ignition Delay with Temperature Variation')

print('Ignition Delay = ', Ignition_delay)
print('Pressure = ', press)
plt.show()