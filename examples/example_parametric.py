if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.ParametricAnimation import ParametricAnimation

    H = 250
    W = 500
    duration = 5
    fps=25

    def make_frame(t):
        surface = gizeh.Surface(W, H)
        x = ParametricAnimation(equation="250+200*sin(2*pi*t)", tween=["easeOutQuad"])
        y = ParametricAnimation(equation="125+80*cos(2*pi*t)", tween=["easeOutQuad"])
        xy = [ x.make_frame(t, 0.2, 1, 4, 5),
               y.make_frame(t, 0.2, 1, 4, 5) ]
        if None not in xy:
            gizeh.circle(30, xy=xy, fill=(1, 1, 0)).draw(surface)
        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_parametric.mp4", fps=fps, codec="libx264")
