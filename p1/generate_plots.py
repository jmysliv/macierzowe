import matplotlib.pyplot as plt
import numpy as np

NUM_OF_EXPERIMENTS = 10
EXPERIMENT = "TIME [S]"
file_name = "results.txt"
results = [[] for _ in range(NUM_OF_EXPERIMENTS)]


if __name__ == "__main__":
	with open(file_name, "r") as f:
		for line in f.readlines():
			line = line.strip()
			if line[0] == "#": 
				k = int(line[1:])
			else:
				results[k].append(float(line))
	results = np.array(results)
	results = results.T
	plt.figure(figsize=(30, 30))
	for l in range(0, NUM_OF_EXPERIMENTS):
		plt.subplot(2, 2, 1)
		plt.plot(np.arange(0, NUM_OF_EXPERIMENTS), results[l], label=f"L={l}")
		plt.xlabel("K")
		plt.ylabel("Time [s]")
		plt.legend()
		plt.subplot(2, 2, 2)
		plt.plot(np.arange(0, NUM_OF_EXPERIMENTS), results[:, l], label=f"K={l}")
		plt.xlabel("L")
		plt.ylabel("Time [s]")
		plt.legend()
		plt.subplot(2, 2, 3)
		plt.plot(np.arange(0, NUM_OF_EXPERIMENTS), np.log(results[l]), label=f"L={l}")
		plt.xlabel("K")
		plt.ylabel("Log Time [s]")
		plt.legend()
		plt.subplot(2, 2, 4)
		plt.plot(np.arange(0, NUM_OF_EXPERIMENTS), np.log(results[:, l]), label=f"K={l}")
		plt.xlabel("L")
		plt.ylabel("Log Time [s]")
		plt.legend()
	
	plt.savefig("./time.jpg")
	


	
