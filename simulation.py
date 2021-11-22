from elements import *
from port import *


simulations = 1000
results = []
for _ in range(simulations):
    print(1)
    d = [Dock(1),Dock(2),Dock(3)]
    t = TugBoat(1)
    p = Port(d,t)
    p.run()
    if p.ships == []:
        continue
    m = 0
    for s in p.ships:
        m+= s.leave_time-s.arrival_time
        print(s.arrival_time, s.leave_time,s.leave_time-s.arrival_time)
    results.append(m/len(p.ships))

ans = f'''Tras {len(results)} simulaciones analizadas se concluye que el tiempo promedio de un barco en el puerto es
{(sum(results)/len(results))} horas'''
print(ans)
    