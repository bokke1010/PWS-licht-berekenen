import matplotlib.pyplot as plt
import calculator

globe = calculator.Globe()
dt = 0.02
data = [globe.calculatePointIncl0(t*dt,0) for t in range(0,round(1/dt))]
plt.plot(data)
plt.show()
