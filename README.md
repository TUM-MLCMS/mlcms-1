# TUM | Machine Learning in Crowd Modelling & Simulation
## Exercise #1
_for Summer Semester 2020_

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

_Remember that this value is divided by 10 for a better performance._

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
