if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from vectortween.PointAnimation import NumberAnimation
    from vectortween.SequentialAnimation import SequentialAnimation
    from functools import partial

    W, H = 250, 250  # width, height, in pixels
    duration = 5  # duration of the clip, in seconds
    fps = 25

    def n2z(v):
        """
        convert None to 0
        :param v: a value or None 
        :return: value if v is not None, else 0
        """
        return v if v is not None else 0

    def make_frame(t):
        surface = gizeh.Surface(W, H)

        x1 = NumberAnimation(50,200,tween=['easeOutElastic', 1, 0.2])
        x2 = NumberAnimation(200,200,tween=['linear'])
        x3 = NumberAnimation(200, 50, tween=['easeOutQuad'])
        x4 = NumberAnimation(50, 50, tween=['linear'])
        xs = SequentialAnimation([x1,x2,x3,x4])
        x = partial(xs.make_frame, birthframe=0, startframe=1, stopframe=4, deathframe=5)

        y1 = NumberAnimation(50, 200, tween=['easeInOutQuint'])
        y2 = NumberAnimation(200, 50, tween=['easeInOutQuad'])
        ys = SequentialAnimation([y1,y2,y1,y2,y1,y2,y1,y2],[8,4,2,1,1,2,4,8])
        y = partial(ys.make_frame, startframe=0, birthframe=0, stopframe=5, deathframe=5)

        xy = [x(t), y(t)]
        if None not in xy:
            gizeh.circle(30, xy=xy, fill=(1, 1, 0)).draw(surface)

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example-sequence.mp4", fps=fps, codec="libx264")
