if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.TimeConversion import TimeConversion
    from vectortween.PointAnimation import PointAnimation
    from vectortween.ColorAnimation import ColorAnimation

    W, H = 250, 250  # width, height, in pixels
    duration = 10  # duration of the clip, in seconds
    fps = 25
    tc = TimeConversion()

    def draw_line(startpoint, endpoint, radius, linewidth, startpointfill, linefill, surface):
        if None not in startpoint and None not in endpoint and linefill is not None \
                and startpointfill is not None and radius is not None and linewidth is not None:
            circle = gizeh.circle(radius, xy=(startpoint[0], startpoint[1]), fill=startpointfill)
            circle2 = gizeh.circle(radius, xy=(endpoint[0], endpoint[1]), fill=startpointfill)
            line = gizeh.polyline([startpoint, endpoint], False, stroke=linefill, stroke_width=linewidth)
            circle.draw(surface)
            circle2.draw(surface)
            line.draw(surface)

    def make_frame(t):
        p = PointAnimation((0 + 75, 0 + 75),
                           (100 + 75, 0 + 75),
                           tween=['easeOutElastic', 0.1, 0.1])
        p2 = PointAnimation((100 + 75, 0 + 75),
                            (0 + 75, 100 + 75),
                            tween=['easeOutElastic', 0.1, 0.5])
        p3 = PointAnimation((100 + 75 + 10, 0 + 75 + 10),
                            (0 + 75 + 10, 100 + 75 + 10),
                            tween=['easeOutCubic'])
        c = ColorAnimation((1,0,0),
                           (0.3,0.6,0.2),
                           tween=['easeOutElastic',0.1,0.1])

        surface = gizeh.Surface(W, H)
        f = p.make_frame(frame=tc.sec2frame(t, fps),
                         birthframe=None,
                         startframe=tc.sec2frame(0.2, fps),
                         stopframe=tc.sec2frame(9.8, fps),
                         deathframe=None)
        f2 = p2.make_frame(frame=tc.sec2frame(t, fps),
                         birthframe=None,
                         startframe=tc.sec2frame(0.2, fps),
                         stopframe=tc.sec2frame(9.8, fps),
                         deathframe=None)
        f3 = p3.make_frame(frame=tc.sec2frame(t, fps),
                         birthframe=None,
                         startframe=tc.sec2frame(0.2, fps),
                         stopframe=tc.sec2frame(9.8, fps),
                         deathframe=None)
        coloranim = c.make_frame(frame=tc.sec2frame(t, fps),
                         birthframe=tc.sec2frame(0.2, fps),
                         startframe=tc.sec2frame(2, fps),
                         stopframe=tc.sec2frame(8, fps),
                         deathframe=tc.sec2frame(9.8, fps))

        red = (1,0,0)
        green = (0,1,0)
        blue = (0,0,1)

        draw_line(f, f2, 10, 3, red, green, surface)
        draw_line(f, f3, 10, 3, blue, coloranim, surface)

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_gif("example.gif", fps=fps, opt="OptimizePlus", fuzz=10)