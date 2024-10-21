# Code to observe the rate of change of molar concentrations of the given elements "H2O, O2, OH" with respect to the time 10 seconds
# CH4 + 2(O2 + 3.76N2) = CO2 + 2H20 + 7.52N2
#states.X[:,gas.species_index('species')])
#species
import sys
import numpy as np 
import cantera as ct 
import matplotlib.pyplot as plt 

gas = ct.Solution('gri30.xml')

temp = [1000, 500]
P = 5*101325

incre = 10e-3
end_time = 10 #in seconds

sim_time = end_time/incre 

species = {'CH4':1, 'O2':2, 'N2':7.52}

for T in temp:
	gas.TPX = T, P, 
	r = ct.IdealGasReactor(gas) # Reactor
	sim = ct.ReactorNet([r]) # Reactor Network

	time = 0.0 # Initial Time

	states = ct.SolutionArray(gas, extra = ['t_ms','t']) # States of Reactor---> attribiutes of the reactor

	for n in range(int(sim_time)):
		time += incre

		sim.advance(time) # Advancing the reactor w.r.t the time step

		states.append(r.thermo.state, t_ms = time*1e3, t = time)

	plt.subplot(1,3,1)
	plt.plot(states.t, states.X[:,gas.species_index('H2O')])
	plt.xlabel('Time [s]')
	plt.ylabel('H2O Mole Fraction')

	plt.subplot(1,3,2)
	plt.plot(states.t, states.X[:,gas.species_index('O2')])
	plt.suptitle('Rate of Change of H2O, O2, OH Molar Concentration at '+str(T)+' Kelvin')
	plt.xlabel('Time [s]')
	plt.ylabel('O2 Mole Fraction')
	
	plt.subplot(1,3,3)
	plt.plot(states.t, states.X[:,gas.species_index('OH')])
	plt.xlabel('Time [s]')
	plt.ylabel('OH Mole Fraction')
    plt.title('Molar Concentrations over Time')
	plt.show()