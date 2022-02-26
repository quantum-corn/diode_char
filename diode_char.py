# %% md
# # Ohm's Law
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v1.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing(file='diode_char_ckt.svg')
d+=elm.Battery().reverse().up().label(('-','V','+'))
d+=elm.MeterI().right()
d+=elm.ResistorVar().down().label(('+','R','-'))
d+=elm.Diode().left()
d+=elm.Ground()
d.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% circuit
circuit = Circuit("Diode Characteristic Curve")
circuit.include('../model_library/diode.lib')
circuit.V('', 1, circuit.gnd, 10@u_V)
circuit.D('', 1, circuit.gnd, model='1N4148')

# %% simulate
simulator = circuit.simulator()
analysis = simulator.dc(V=slice(-1.5, 1.5, 0.01))

# %% scale the current data
i=-analysis.v
i*=(i>=0@u_A)+((i<0@u_A)*1e8)

# %% md
# ### Now let's plot the data
# For this I will use matplotlib

# %% import
import matplotlib.pyplot as plt

# %% plot data
fig, ax=plt.subplots()
ax.set(title="Diode Characteristic Curve", xlabel='Voltage in V', ylabel='Current in A (V>0) & x1e8 A (V<0)')
ax.grid()
ax.axhline(y=0, color='black')
ax.axvline(x=0, color='black')
ax.plot(analysis['v-sweep'], i)
plt.show()
plt.savefig('diode_char_plt.svg')
