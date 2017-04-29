if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.ParametricAnimation import ParametricAnimation

    H = 250
    W = 500
    duration = 15
    fps=25

    def add(a,b):
        if a is None or b is None:
            return None
        return a+b

    def make_frame(t):
        surface = gizeh.Surface(W, H)
        # big ellipse
        x1 = ParametricAnimation(equation="250+200*sin(2*pi*t)", tween=["easeInOutQuad"])
        y1 = ParametricAnimation(equation="125+80*cos(2*pi*t)", tween=["easeInOutQuad"])
        # smaller circles on top of the ellipse
        x2 = ParametricAnimation(equation="10*sin(50*pi*t)", tween=["linear"])
        y2 = ParametricAnimation(equation="10*cos(50*pi*t)", tween=["linear"])
        xy = [ add(x1.make_frame(t, 0.2, 1, 14, 15), x2.make_frame(t, 0.2, 1, 14, 15)),
               add(y1.make_frame(t, 0.2, 1, 14, 15), y2.make_frame(t, 0.2, 1, 14, 15)) ]
        if None not in xy:
            gizeh.circle(5, xy=xy, fill=(1, 1, 0)).draw(surface)
        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_parametric.mp4", fps=fps, codec="libx264")
