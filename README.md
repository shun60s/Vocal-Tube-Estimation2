# Vocal Tube Estimation 2   

Estimation of three tube model from peak frequency.  
This version uses peak frequency ratio instead of absolute value.  


## usage   

make precomputed data of grid search to set initial value of downhill simplex method to estimate tube area and tube length.    
```
python pre_compute3.py   
```
It will save pks_dpks_stack_tube_use_ratio3.npz.  


estimate three tubes model from peak frequency.  
```
python pks2tube3.py  --peaks [ list of three peak frequency]
```
It will show an example of three tube area and tube length.  
In frequency response figure, red dot mark means target peak frequency, and cyan x mark means estimation result. They may differ some.  

Example 1  
```
python pks2tube3.py  --peaks 523.3 659.358 800
```
 ![figure1](docs/figure_800.png)   

Example 2  
```
python pks2tube3.py  --peaks 523.3 659.358 730
```
 ![figure2](docs/figure_730.png)   



## License    
MIT  


