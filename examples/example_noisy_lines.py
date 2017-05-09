if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.PointAnimation import PointAnimation
    from vectortween.SequentialAnimation import SequentialAnimation
    from vectortween.BezierCurveAnimation import BezierCurveAnimation
    from vectortween.PolarAnimation import PolarAnimation

    import noise

    H = 250
    W = 500
    duration = 30
    fps = 25


    def my_noise(x, t):
        return 2 * noise.snoise2(x, 0)


    def my_noise2(x, t):
        #print("x = {}, t = {}".format(x, t))
        return 30 * noise.snoise2(x, t)


    a1 = PointAnimation(frm=(0, 0), to=(500, 250), tween=["easeOutQuad"])
    a2 = PointAnimation(to=(0, 0), frm=(500, 250), tween=["easeOutQuad"], noise_fn=my_noise, y_noise_fn=my_noise)
    a3 = PointAnimation(frm=(0, 0), to=(500, 250), tween=["easeOutQuad"], noise_fn=my_noise, y_noise_fn=None)
    a4 = PointAnimation(to=(0, 0), frm=(500, 250), tween=["easeOutQuad"], noise_fn=None, y_noise_fn=my_noise)
    a5 = BezierCurveAnimation([[0, 0], [500, 250]], tween=["easeOutQuad"], noise_fn=my_noise2, y_noise_fn=my_noise2)
    a6 = BezierCurveAnimation([[500, 250], [0, 0]], tween=["easeOutQuad"], noise_fn=my_noise2, y_noise_fn=my_noise2)
    a7 = PolarAnimation(equation="6*theta*sin(6*theta)", offset=[250, 125], scale=[5, 5], noise_fn=my_noise2,
                        y_noise_fn=my_noise2)
    s = SequentialAnimation([a1, a2, a3, a4, a5, a6, a7])


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        xy = s.make_frame(t, 0, 0, duration, duration)
        trail = s.curve_points(t - 1.5, t, 0.01, 0, 0, duration, duration, noiseframe=t)
        if trail and None not in trail:
            gizeh.polyline(trail, stroke=(t / duration, 1 - t / duration, t / duration), stroke_width=5,
                           fill=None).draw(surface)
        if xy is not None and None not in xy:
            gizeh.circle(r=5, xy=xy, stroke=(0, 1, 0), stroke_width=2, fill=None).draw(surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_noisy_lines.mp4", fps=fps, codec="libx264")
