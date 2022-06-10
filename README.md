# Vocal Tube Estimation 2   

Estimation of three tube model from peak frequency.  
This version uses peak frequency ratio instead of absoulte value.  


## usage   

make precomputed data of grid search to set initial value of downhill simplex method to estimate tube area and tube length.    
```
python pre_compute3.py   
```
It will save pks_dpks_stack_tube_use_ratio3.npz.  


estimate three tubes model from peak frequency.  
```
python pks2tube3.py   
```
It will show an example of three tube area and tube length.    


## License    
MIT  


