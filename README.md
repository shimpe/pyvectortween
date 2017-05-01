# Vectortween

Some helper classes to generate vector graphics animations with tweening.

This library works wity python 3 only. It depends on the python libraries "pytweening", "numpy", "scipy" and "sympy"

While it can be used in combination with any other library, the examples are made using the libraries "gizeh" and "moviepy".

Documentation is mostly non-existing at the moment, but you can look at the examples to get some inspiration.
 
 #  Basic concept
 An animation is modeled as numbers that evolve over time from a starting point to an end point. 
 Animation specifications do not include start and stop times or durations. 
 These are specified only while realizing the animations. 
 This makes it easy to compose animations into more complex animations.
 
 ## Example
 ```python
 from vectortween.NumberAnimation import NumberAnimation
 
 n = NumberAnimation(frm=0, to=100, tween=["easeOutBounce"])
 
 for i in range(100):
    print (n.make_frame(frame=i/20, birthframe=0, startframe=0, 
                        stopframe=5, deathframe=5))
```

## Discussion

The simplest animation is a NumberAnimation. The specification says that the 
animation will produce values between 0 and 100 and that, as the 
animation progresses towards the end, the numbers will bounce back and forth a bit.

When calling the make_frame method, we must specify a timeline. 
The animation is automatically stretched to fill the time between startframe and stopframe:
 * `frame`: the current frame or timestep for which we want to get a NumberAnimation 
  value.
 * `birthframe`: for frames < birthframe, make_frame returns None 
 (the animation is not yet "alive"). For birthframe <= frame < startframe, 
 the animation returns the initial value.
 * `startframe`: for startframe <= frame <= stopframe, the animation returns values
 as specified in the NumberAnimation parameters.
 * `stopframe`: for stopframe < frame < deathframe, the animation returns
 the final animation value (the animation remains "alive", but doesn't
 evolve further).
 * `deathframe`: for frame >= deathframe, the animation returns None. 
 The animation is "dead".

All frame arguments are floats. So it's perfectly possible to
ask (and get, within machine precision) the animated value for frame 3.52634.

## Not for real-time usage!

Although I try to get a reasonable performance, performance is not the 
first concern. The library is not intended for real-time usage. 
My current interest lies in offline generation/rendering of graphics.
The library will happily sacrifice speed for accuracy when faced with 
the choice. As a result it can be arbitrarily slow 
(especially with heavy parameteric equations).

## Examples

I suggest to look at the examples to get an idea of how the different animation types work.

