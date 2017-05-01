if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.BezierCurveAnimation import BezierCurveAnimation


    def random_color():
        import random
        return (random.uniform(0, 1) for _ in range(3))


    W, H = 250, 250  # width, height, in pixels
    duration = 5  # duration of the clip, in seconds
    fps = 25

    controlpoints = [(120, 160), (35, 200), (220, 240), (220, 40)]
    b = BezierCurveAnimation(controlpoints=controlpoints)


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        xy = b.make_frame(t, 0, 0, duration - 1, duration)
        curve_points = b.curve_points(0, t, 0.01, 0, 0, duration - 1, duration)
        # print (curve_points)
        if xy is not None and None not in xy:
            gizeh.circle(5, xy=xy, fill=(0, 1, 0)).draw(surface)
        gizeh.polyline(curve_points, stroke=(0, 0, 1), stroke_width=2).draw(surface)
        gizeh.polyline(controlpoints, stroke=(1, 0, 0), stroke_width=2).draw(surface)
        for cp in controlpoints:
            gizeh.circle(5, xy=cp, fill=(0, 1, 1)).draw(surface)

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_bezier.mp4", fps=fps, codec="libx264")
