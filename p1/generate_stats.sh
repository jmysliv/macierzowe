rm results.txt
touch results.txt
for k in $(seq 0 9);
do
	sed -i -e "s/k = 1 << .*/k = 1 << $k;/" ./src/main.cpp
	echo "#$k" >> results.txt
	for l in $(seq 0 9);
	do
		sed -i -e "s/l = 1 << .*/l = 1 << $l;/" ./src/main.cpp
		make all
		sleep 1
		./app >> results.txt
	done
done
