if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.ParametricAnimation import ParametricAnimation
    from vectortween.SequentialAnimation import SequentialAnimation

    H = 250
    W = 500
    duration = 15
    fps = 25


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        # big ellipse with local smaller circles
        x1 = ParametricAnimation(equation="250+200*sin(2*pi*t) + 10*sin(50*pi*t)", tween=["easeInOutQuad"])
        y1 = ParametricAnimation(equation="125+ 80*cos(2*pi*t) + 10*cos(50*pi*t)", tween=["easeInOutQuad"])

        # a heart
        x2 = ParametricAnimation(equation="250+ 7*16*(sin(2*pi*t)**3)", tween=["linear"])
        y2 = ParametricAnimation(equation="125 - 7*(13*cos(2*pi*t)-5*cos(2*2*pi*t)-2*cos(3*2*pi*t)-cos(4*2*pi*t))",
                                 tween=["linear"])

        xseq = SequentialAnimation([x1, x2])
        yseq = SequentialAnimation([y1, y2])

        xy = [xseq.make_frame(t, 0.2, 1, 14, 15), yseq.make_frame(t, 0.2, 1, 14, 15)]

        if None not in xy:
            gizeh.circle(5, xy=xy, fill=(1, 1, 0)).draw(surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_parametric.mp4", fps=fps, codec="libx264")
