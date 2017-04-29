if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.PolarAnimation import PolarAnimation

    def random_color():
        import random
        return (random.uniform(0,1) for _ in range(3))

    W, H = 250, 250  # width, height, in pixels
    duration = 10  # duration of the clip, in seconds
    fps = 25

    no_of_balls = 10
    p = []
    for i in range(no_of_balls):
        p.append(PolarAnimation(equation="100*sin(5*theta + {0}*2*pi/5)".format(i)))

    colors = [ tuple(random_color()) for _ in range(no_of_balls) ]

    def make_frame(t):
        surface = gizeh.Surface(W, H)

        xys = []
        for i in range(no_of_balls):
            xys.append(p[i].make_frame(t, birthframe=0, startframe=0, stopframe=no_of_balls+2-i, deathframe=no_of_balls+2-i))

        for i, xyval in enumerate(xys):
            if None not in xyval:
                gizeh.circle(3+i, xy=[xyval[0] + 125, xyval[1] + 125], fill=colors[i]).draw(surface)

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_polar.mp4", fps=fps, codec="libx264")
