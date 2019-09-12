def collide(box, box2):
    if box[2] < 0:
        box = [box[0]+box[2], box[1], -box[2], box[3]]
    if box[3] < 0:
        box = [box[0], box[1]+box[3], box[2], -box[3]]

    if box2[2] < 0:
        box2 = [box2[0]+box2[2], box2[1], -box2[2], box2[3]]
    if box2[3] < 0:
        box2 = [box2[0], box2[1]+box2[3], box2[2], -box2[3]]

    if box[0] < box2[0] + box2[2] and\
        box[0] + box[2] > box2[0] and\
        box[1] < box2[1] + box2[3] and\
        box[1] + box[3] > box2[1]:
        return True
