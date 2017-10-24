gfortran CalculateCrank.f -o CalculateCrank
./CalculateCrank
gnuplot -e "set terminal png size 800,600; set output 'Displacement.PNG'; plot 's.out'"
gnuplot -e "set terminal png size 800,600; set output 'Max.PNG'; plot 'v.out'"
gfortran CalculateCam.f -o CalculateCam
./CalculateCam
gnuplot -e "set polar; set terminal png size 800,600; set output 'IntakeCam.PNG';plot 'intcams.out'"

