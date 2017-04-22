if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy
    import numpy as np

    from vectortween.TimeConversion import TimeConversion
    from vectortween.NumberAnimation import NumberAnimation

    W, H = 1000, 1000 # width, height, in pixels
    duration = 15 # duration of the clip, in seconds
    fps = 25
    tc = TimeConversion()

    X = 0
    Y = 1

    def draw_rect(upperleft, bottomright, radius, linewidth, cornerfill, linefill, rotation, surface):
        if None not in upperleft and\
                        None not in bottomright and \
                        radius is not None and \
                        linefill is not None and\
                        cornerfill is not None and\
                        linefill is not None and\
                        surface is not None:
            circles = []
            uleft = (upperleft[X],upperleft[Y])
            uright= (bottomright[X], upperleft[Y])
            bleft = (upperleft[X], bottomright[Y])
            bright = (bottomright[X], bottomright[Y])
            circles.append(gizeh.circle(radius, xy=uleft, fill=cornerfill))
            circles.append(gizeh.circle(radius, xy=bleft, fill=cornerfill))
            circles.append(gizeh.circle(radius, xy=bright, fill=cornerfill))
            circles.append(gizeh.circle(radius, xy=uright, fill=cornerfill))
            circles.append(gizeh.polyline([uleft, bleft, bright, uright], True, stroke=linefill, stroke_width=linewidth))
            group = gizeh.Group(circles)
            rotated_group = group.rotate(rotation, [(upperleft[X]+bottomright[X])/2.0,(upperleft[Y]+bottomright[Y])/2.0])
            rotated_group.draw(surface)

    def make_frame(t):
        surface = gizeh.Surface(W, H)
        list_of_ul  = []
        list_of_br = []
        for x in range(30):
            for y in range(30):
                list_of_ul.append((x*24, y*24))
                list_of_br.append((x * 24 + 15, y * 24 + 15))

        #print(t) - t is expressed in seconds for videos; frames for .gifs !!!
        for i, (ul, br) in enumerate(zip(list_of_ul, list_of_br)):
            rot = NumberAnimation(0, np.pi, tween=['easeOutElastic', 0.3+i/len(list_of_br), 1.0/(i/10.0+0.01)])
            rot1 = rot.make_frame(t, None, 0.2, 9.8, None)
            rot3 = np.pi*i*0.1365/180.0
            total_rot = 0
            if rot1 is not None:
                total_rot += rot1
            if rot3 is not None:
                total_rot += rot3
            #print (total_rot)
            draw_rect(ul, br, 3, 2, (1,0,0), (0,1,0), total_rot, surface)

        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example2.mp4", fps=fps, codec='libx264')
