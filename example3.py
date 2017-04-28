if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy
    import random

    from vectortween.TimeConversion import TimeConversion
    from vectortween.NumberAnimation import NumberAnimation

    W, H = 1000, 1000  # width, height, in pixels
    MARGIN = 100


    def my(y):  # add margin and flip Y-axis
        if y is None:
            return None
        return H - y + MARGIN


    def mx(x):  # add margin x
        if x is None:
            return None
        return x + MARGIN


    duration = 15  # duration of the clip, in seconds
    fps = 25
    tc = TimeConversion()

    X = 0
    Y = 1

    rect_anim = []
    rect_colors = []
    for i in range(10):
        rect_anim.append(NumberAnimation(0, random.uniform(100, 600), tween=["easeInOutQuad"]))
        rect_colors.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))


    def draw_rect(ul, br, linewidth, linefill, surfacefill, surface):
        if None not in ul and \
                        None not in br and \
                        linewidth is not None and \
                        linefill is not None and \
                        surfacefill is not None and \
                        surface is not None:
            width = br[X] - ul[X]
            height = ul[Y] - br[Y]
            cx = (br[X] + ul[X]) / 2.0
            cy = (br[Y] + ul[Y]) / 2.0
            gizeh.rectangle(width, height, xy=[cx, cy], fill=surfacefill,
                            stroke=linefill, stroke_width=linewidth).draw(surface)


    def draw_line(x1, x2, linewidth, linefill, surface):
        if None not in x1 and \
                        None not in x2 and \
                        linewidth is not None and \
                        linefill is not None and \
                        surface is not None:
            gizeh.polyline([x1, x2], False, stroke=linefill, stroke_width=linewidth).draw(surface)


    def draw_text(txt, position, color, surface):
        if txt is not None and \
                        None not in position and \
                        color is not None:
            gizeh.text(txt, "sans-serif", fontsize=20, xy=position, fill=color).draw(surface)


    def make_frame(t):
        surface = gizeh.Surface(W, H)
        axe_anim = NumberAnimation(100, 800, tween=['easeOutElastic', 1, 0.2])
        axe_color = (1, 1, 1)
        axe_width = 2
        # draw axes from second 1 to second 3 (keep alive until second 15)
        draw_line((mx(0), my(-10)), (mx(0), my(axe_anim.make_frame(t, 1, 1, 3, 15))), axe_width, axe_color, surface)
        draw_line((mx(-10), my(0)), (mx(axe_anim.make_frame(t, 1, 1, 3, 15)), my(0)), axe_width, axe_color, surface)
        for i in range(20):
            subdiv_anim = NumberAnimation(0, i * 35, tween=(["easeOutBounce"]))
            x = subdiv_anim.make_frame(t, 1.5, 1.5, 6, 15)
            draw_line((mx(x), my(-10)), (mx(x), my(10)), 1, axe_color, surface)
            draw_line((mx(-10), my(x)), (mx(10), my(x)), 1, axe_color, surface)
            if (i + 1) % 5 == 0:
                txt_x = subdiv_anim.make_frame(t, 2.5, 2.5, 6, 15)
                draw_text("{0}".format(i + 1), (mx(txt_x), my(-20)), (1, 1, 1), surface)
                draw_text("{0}".format(i + 1), (mx(-20), my(txt_x)), (1, 1, 1), surface)
        for i in range(10):
            y = rect_anim[i].make_frame(t, 5, 5, 9, 15)
            draw_rect((mx(i * 70), my(y)),
                      (mx((i + 0.9) * 70), my(0)),
                      2, (0, 0, 1),
                      rect_colors[i],
                      surface)
        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example3.mp4", fps=fps, codec='libx264')
    clip.write_gif("example3.gif", fps=fps, opt='nq')
