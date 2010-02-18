from graphics import write_png, gradient, LINEAR_X, LINEAR_Y, RADIAL, NO_NOISE, GAUSSIAN, HSV

write_png("box1.png", 100, 200, gradient(LINEAR_Y, NO_NOISE, [
    (1, (0xF7, 0xF7, 0xF7), (0x98, 0x9A, 0x9E)),
]))

write_png("box2.png", 1, 60, gradient(LINEAR_Y, NO_NOISE, [
    (1, (0xF7, 0xF7, 0xF7), (0xDD, 0xDE, 0xDF)),
]))

write_png("footer.png", 100, 100, gradient(LINEAR_Y, GAUSSIAN(0.01), [
    (0.1, (0x00, 0x00, 0x00), (0x11, 0x11, 0x11)),
    (1, (0x11, 0x11, 0x11), (0x22, 0x22, 0x22)),
]))

write_png("nav.png", 1, 100, gradient(LINEAR_Y, NO_NOISE, [
    (1, (0x11, 0x11, 0x11), (0x66, 0x66, 0x66)),
]))
