if __name__ == "__main__":
    import gizeh
    import moviepy.editor as mpy

    from scipy import misc
    from scipy.ndimage import zoom
    from numpy import pi
    from vectortween.NumberAnimation import NumberAnimation
    from vectortween.SequentialAnimation import SequentialAnimation
    from vectortween.ColorAnimation import ColorAnimation

    # heart shape retrieved from https: // commons.wikimedia.org / wiki / File: Heart_coraz % C3 % B3n.svg
    mask = misc.imread("heart.png")
    print("mask.shape = ", mask.shape, " mask.dtype = ", mask.dtype)
    H = mask.shape[0]
    W = mask.shape[1]
    subsample = 20
    subsampled_mask = zoom(mask, (1 / subsample, 1 / subsample, 1))
    print(subsampled_mask.shape)

    #debug code:
    #misc.imsave("heart-subsampled.png", subsampled_mask)

    yrange = subsampled_mask.shape[0]
    xrange = subsampled_mask.shape[1]
    xwidth = subsample
    ywidth = subsample
    stripes = 5
    duration = 15
    fps = 25

    anim = NumberAnimation(frm=2, to=subsample-2, tween=["easeOutBounce"])
    anim = SequentialAnimation([anim], repeats=15)

    def get_color(x, y, subsampled_mask):
        color = subsampled_mask[y][x]/255
        return color

    def get_rotation(x, y, subsampled_mask):
        c = get_color(x, y, subsampled_mask)
        if sum(c) > 2:
            return pi/3
        else:
            return 0

    def make_frame(t):
        surface = gizeh.Surface(W, H)

        for y in range(yrange):
            for x in range(xrange):
                coloranim = SequentialAnimation([
                    ColorAnimation(frm=(1, 1, 1, 1), to=get_color(x, y, subsampled_mask)),
                    ColorAnimation(to=(1, 1, 1, 1), frm=get_color(x, y, subsampled_mask))])
                rotanim = SequentialAnimation([
                    NumberAnimation(frm=0, to=get_rotation(x, y, subsampled_mask)),
                    NumberAnimation(to=0, frm=get_rotation(x, y, subsampled_mask))])
                colorval = coloranim.make_frame(t, 0, 0, duration * 0.90, duration)
                rotval = rotanim.make_frame(t, 0, 0, duration * 0.90, duration)
                for numstripes in range(stripes):
                    val = anim.make_frame(t, 0, 0, duration - numstripes / 3, duration)

                    if val is not None:

                        if x % 2:
                            xy = (x * xwidth, y * ywidth + numstripes * ywidth / stripes)
                            xyrot = (xy[0] + val/2, xy[1])
                            gizeh.polyline([[0, 0], [val, 0]], stroke_width=1, stroke=colorval).translate(
                                xy=xy).rotate(rotval,center=xyrot).draw(surface)
                        else:
                            xy = (x * xwidth + numstripes * ywidth / stripes, y * ywidth)
                            xyrot = (xy[0], xy[1] + val/2)
                            gizeh.polyline([[0, 0], [0, val]], stroke_width=1, stroke=colorval).translate(
                                xy=xy).rotate(rotval,center=xyrot).draw(surface)

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_videofile("example_mask.mp4", fps=fps, codec="libx264")
