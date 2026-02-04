from ilovepdf import Iloveimg


def test_iloveimg_aliases():
    client = Iloveimg("pub", "secret")
    task = client.new_task("compress", make_start=False)
    assert task.tool == "compressimage"

    task = client.new_task("rotate", make_start=False)
    assert task.tool == "rotateimage"

    task = client.new_task("watermark", make_start=False)
    assert task.tool == "watermarkimage"

    task = client.new_task("upscale", make_start=False)
    assert task.tool == "upscaleimage"

    task = client.new_task("removebackground", make_start=False)
    assert task.tool == "removebackgroundimage"
