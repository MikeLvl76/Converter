# What is it ?

A program that computes converted values, it uses maths which is needed for conversion. Nowadays, with many different units in currency, measure, etc, a converter is hugely needed because people does not always use same units and that can lead to a misunderstanding or a mistake.

# Which units does it convert ?

At this time, not many.
Currently ther are 3 types of conversion :</br>

**[ISU](https://en.wikipedia.org/wiki/International_System_of_Units) conversion**
|Unit|meter|liter|gram|
|--|--|--|--|
|meter|implemented|implemented but does not consider meter as cubic meter|implemented|
|liter|implemented but does not consider meter as cubic meter|implemented|implemented|
|gram|implemented|implemented|implemented|

**Temperature conversion**
|Unit|°F|°C|K|
|--|--|--|--|
|°F|implemented|implemented|implemented|
|°C|implemented|implemented|implemented|
|K|implemented|implemented|implemented|

**Currency conversion**
|Unit|euro|dollar|pound|
|--|--|--|--|
|euro|implemented|implemented|implemented|
|dollar|implemented|implemented|implemented|
|pound|implemented|implemented|implemented|

# How does it work ?

It simply use mathematical formulas to convert one value to another. For example converting Celsius to Kelvin :
$$aK=b°C + 273.15$$
With $a$ the result and $b$ the value to convert.

# Where the formulas can be found ?

Here is a list of formulas for conversion :
- ***For ISU conversion*** :
    - gram to liter -> gram value / 1000
    - liter to gram -> liter value * 1000
    - gram to meter -> gram value / 1000
    - meter to gram -> meter value * 1000
    - liter to meter -> liter value / 1000
    - meter to liter -> meter value * 1000
- ***For temperature conversion*** :
    - celsius to fahrenheit -> celsius value * $\frac{9}{5}$ + 32
    - fahrenheit to celsius -> (fahrenheit value - 32) * $\frac{5}{9}$
    - celsius to kelvin -> celsius value + 273.15
    - kelvin to celsius -> kelvin value - 273.15
    - fahrenheit to kelvin -> (fahrenheit value + 459.67) * $\frac{5}{9}$
    - kelvin to fahrenheit -> kelvin value * $\frac{9}{5}$ - 459.67
- ***For currency conversion*** :
    - euro to dollar -> euro value * 1.008065
    - dollar to euro -> dollar value * 0.992000
    - euro to pound -> euro value * 0.850329
    - pound to euro -> pound value * 1.176016
    - dollar to pound -> dollar value * 0.843526
    - pound to dollar -> pound value * 1.185500

# Results

Here is a collection of few screenshots (each screenshot was taken at different time) :

![Currency conversion](/results/converter1.png)
![Classic conversion](/results/converter2.png)
![Temperature conversion](/results/converter3.png)
![Storage](/results/storage.png)
