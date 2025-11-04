from PIL import Image, ImageDraw


a = []
answer_1, answer_2 = 0, 0
min_x, min_y = 0, 0
max_x, max_y = -10 ** 10, -10 ** 10
for i in range(int(input())):
    x, y = [int(j) for j in input().split()]
    a.append((x, y))
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
points = []
for i in a:
    points.append((i[0] - min_x, i[1] - min_y))
im = Image.new('RGB', (max_x - min_x + 10, max_y - min_y + 10), '#000000')
draw = ImageDraw.Draw(im)
draw.polygon(points, fill='#FFC000')
for i in range(len(points) - 1):
    draw.line((points[i], points[i + 1]), fill='#FFFFFF')
draw.line((points[-1], points[0]), fill='#FFFFFF')
pixels = im.load()
for i in range(max_x - min_x + 10):
    for j in range(max_y - min_y + 10):
        if (0, 0, 0) != pixels[i, j]:
            if pixels[i, j] == (255, 255, 255):
                answer_2 += 1
            else:
                answer_1 += 1
print(answer_1, answer_2)




