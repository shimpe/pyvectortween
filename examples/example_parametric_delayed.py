if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy
    import math
    import random

    from vectortween.ParametricAnimation import ParametricAnimation


    def random_color():
        return (random.uniform(0, 1) for _ in range(3))


    H = 250
    W = 500
    duration = 15
    fps = 25

    # a heart
    no_of_balls = 30
    xs = []
    ys = []
    for b in range(no_of_balls):
        trans = random.uniform(-10,10)
        xs.append(ParametricAnimation(equation="250+ 7*16*(sin(2*pi*t)**3)", tween=["linear"]).delayed_version(
            2 * b * math.pi / no_of_balls).speedup_version(b * math.pi/(no_of_balls/2)).translated_version(trans))
        ys.append(ParametricAnimation(equation="125-7*(13*cos(2*pi*t)-5*cos(2*2*pi*t)-2*cos(3*2*pi*t)-cos(4*2*pi*t))",
                                      tween=["linear"]).delayed_version(2 * b * math.pi / no_of_balls).speedup_version(
            b * math.pi/(no_of_balls/2)).translated_version(trans))

    colors = [tuple(random_color()) for _ in range(no_of_balls)]


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        for i, (x, y) in enumerate(zip(xs, ys)):
            xval = x.make_frame(t, 0, 0, duration, duration)
            yval = y.make_frame(t, 0, 0, duration, duration)
            if xval is not None and yval is not None:
                gizeh.circle(5, xy=[xval, yval], fill=colors[i]).draw(surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_parametric_delayed.mp4", fps=fps, codec="libx264")
