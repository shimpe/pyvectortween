if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.PointAnimation import PointAnimation

    W, H = 250, 250  # width, height, in pixels
    duration = 5  # duration of the clip, in seconds
    fps = 25


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        gizeh.circle(30, xy=((t * 22), (t * 22)), fill=(1, 1, 0)).draw(surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_gif("example_blogentry_plain.gif", fps=fps, fuzz=10)


    def make_frame_tween(t):
        surface = gizeh.Surface(W, H)
        p = PointAnimation((0, 0), (110, 110), tween=['easeOutElastic', 1, 0.2])
        xy = p.make_frame(t, 0.2, 1, 4, 5)  # appear at second 0.2, animate between seconds 1-4,
        # then stay until disappearance second 5
        if None not in xy:
            gizeh.circle(30, xy=xy, fill=(1, 1, 0)).draw(surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame_tween, duration=duration)
    clip.write_gif("example_blogentry_tween.gif", fps=fps, fuzz=10)
