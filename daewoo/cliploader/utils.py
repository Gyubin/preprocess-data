import numpy as np

def stack_images(images):
    images = [np.expand_dims(img, axis=0) for img in images]
    while len(images) > 1:
        result = []
        for i in range(0, len(images), 2):
            if i != len(images)-1:
                result.append(np.vstack((images[i], images[i+1])))
            elif i == len(images)-1:
                result.append(images[i])
        images = result
    return images[0]


def make_label_custom(labels, window, n_class=360):
    label_dist = np.zeros((len(labels), n_class), dtype=float)
    label_digitized = label_digitize(labels, n_class)
    interval = round(1.0 / window, 4)

    for row, cur in enumerate(label_digitized):
        label_dist[row][cur] = 1
        for context, weight in enumerate(np.arange(interval/1, 1.0+interval, interval)):

            right_idx = cur + context + 1
            left_idx = cur - context - 1

            if right_idx >= n_class: right_idx -= n_class
            label_dist[row][right_idx] = (1 - weight) ** 2

            if left_idx < 0: left_idx += n_class
            label_dist[row][left_idx] = (1 - weight) ** 2
    return label_dist


def make_label_normal(labels, std, n_class=360):
    label_norm = np.zeros((len(labels), n_class), dtype=float)
    temp_norm = [norm.pdf(i, scale=std) for i in range(-int(n_class/2), int(n_class/2))]
    label_digitized = label_digitize(labels, n_class)

    for row, cur in enumerate(label_digitized):
        if cur < (n_class/2): where_zero = cur+int(n_class/2)
        else: where_zero = cur-int(n_class/2)
        label_norm[row, where_zero:n_class] = temp_norm[:n_class-where_zero]
        label_norm[row, 0:where_zero] = temp_norm[n_class-where_zero:]
    return label_norm
