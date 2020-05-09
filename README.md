# TUM | Machine Learning in Crowd Modelling & Simulation
## Exercise #1
_for Summer Semester 2020_

First, you need define a simple python virtual environment when you pull the project. 

Then run;
```python
pip install -r requirements.txt
```
_Remember that apart from python and pip; the only requirement is numpy, so you can just add that as well._

***

In order to see a simple welcome page, run the command:
```python
python main.py
```

For seeing the test scenarios, run:
```python
python main.py <SCENARIO>
```

From the table below, you can see the available options.

| Scenario              | Argument      |
| ----------------------|:-------------:|
| Chicken Test          | chicken       |
| Circular Pedestrians  | circular      |
| RIMEA Test #1         | 1             |
| RIMEA Test #4         | 4             |
| RIMEA Test #6         | 6             |
| RIMEA Test #7         | 7             |

***

For the case of Test #4, you can also give additional arguments.

You can give a density value in **P/(meters square)** for pedestrians. 

_For better performance, density is divided by 5 and width is 200, height is 7 meters long for this option._

```python
python main.py 4 <DENSITY>
```

***

You can give the **density**, **width** and **height** values for the corridor. 

_Width and height in meters, density in Person/(meters square)_

**You need to be careful with the options since a larger corridor with many pedestrians is very resource consuming!**

```python
python main.py 4 <DENSITY> <WIDTH> <HEIGHT>
```
