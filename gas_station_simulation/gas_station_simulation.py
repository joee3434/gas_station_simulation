import simpy
import random
import matplotlib.pyplot as plt

# parameters
NUM_PUMPS = 2
SERVICE_MIN = 3
SERVICE_MAX = 5
ARRIVAL_RATE = 2
SIM_TIME = 60

waiting_times = []
queue_lengths = []
time_points = []

def car(env, name, station):
    arrival_time = env.now
    print(f"{name} arrived at {arrival_time:.2f}")

    with station.request() as request:
        yield request

        wait = env.now - arrival_time
        waiting_times.append(wait)

        print(f"{name} starts fueling at {env.now:.2f}")

        service_time = random.randint(SERVICE_MIN, SERVICE_MAX)
        yield env.timeout(service_time)

        print(f"{name} leaves at {env.now:.2f}")

def car_generator(env, station):

    car_id = 0

    while True:
        car_id += 1

        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))

        env.process(car(env, f"Car {car_id}", station))

def monitor_queue(env, station):

    while True:
        queue_lengths.append(len(station.queue))
        time_points.append(env.now)

        yield env.timeout(1)

env = simpy.Environment()

station = simpy.Resource(env, capacity=NUM_PUMPS)

env.process(car_generator(env, station))
env.process(monitor_queue(env, station))

env.run(until=SIM_TIME)

print("\n===== Simulation Results =====")

print("Cars served:", len(waiting_times))

if waiting_times:
    avg_wait = sum(waiting_times)/len(waiting_times)
    print("Average waiting time:", round(avg_wait,2))

print("Max queue length:", max(queue_lengths))

# رسم الجراف
plt.plot(time_points, queue_lengths)

plt.xlabel("Time")
plt.ylabel("Queue Length")
plt.title("Gas Station Queue Simulation")

plt.show()