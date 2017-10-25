# boomboom

Very serious engine simulation for very serious people.

## Getting Started

Run the following to install dependencies:
```
pip install -U -r requirements.txt
```

Run the engine model at least once. Among other things, this gives metrics like
mean piston speed and RPM.
```
python engine1.py
```

Once the engine model has run, it will save the cam information for further experimentation. Experiment with different plots and smoothing algorithms in:
```
python cam_processing.py
```
