import numpy as np
import cv2


det_config = '/utils/cascade_rcnn_x101_64x4d_fpn_1class.py'
det_checkpoint = '/checkpoints/cascade_rcnn_x101_64x4d_fpn_20e_onehand10k-dac19597_20201030.pth'
pose_config = '/utils/td-hm_mobilenetv2_8xb64-210e_onehand10k-256x256.py'
pose_checkpoint = '/checkpoints/mobilenetv2_onehand10k_256x256-f3a3d90e_20210330.pth'
device = 'cpu'  # 'cuda:0'


def get_models():
    # build detector
    detector = init_detector(det_config, det_checkpoint, device=device)
    detector.cfg = adapt_mmdet_pipeline(detector.cfg)

    # build pose estimator
    pose_estimator = init_pose_estimator(
        pose_config,
        pose_checkpoint,
        device=device,
        cfg_options=dict(model=dict(test_cfg=dict(output_heatmaps=False)))
    )

    return detector, pose_estimator


def get_keypoints(img, detector, pose_estimator):
    results = process_image(img, detector, pose_estimator)
    keypoints = results.keypoints[0]
    bbox = results.bboxes[0]

    return keypoints, bbox


def process_hands(img, detector, pose_estimator, draw=False):
    keypoints, bbox = get_keypoints(img, detector, pose_estimator)

    points = []

    for id, keypoint in enumerate(keypoints):
        h, w, c = img.shape
        cx, cy = int(keypoint[0]), int(keypoint[1])
        points.append([id, cx, cy])
        if draw:
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

    xmin, ymin, xmax, ymax = bbox.astype(int)

    if draw:
        cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), 
                    (0, 255, 0), 2)
        cv2.imwrite('test.jpg', img)

    return points, bbox


def check_fingers(points):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]
    if points[tip_ids[0]][1] > points[tip_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    for id in range(1, 5):
        if points[tip_ids[id]][2] < points[tip_ids[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def process_image(img, detector, pose_estimator):
    # predict bbox
    det_result = inference_detector(detector, img)
    pred_instance = det_result.pred_instances.cpu().numpy()
    bboxes = np.concatenate(
        (pred_instance.bboxes, pred_instance.scores[:, None]), axis=1)
    bboxes = bboxes[np.logical_and(pred_instance.labels == 0,
                                   pred_instance.scores > 0.3)]
    bboxes = bboxes[nms(bboxes, 0.3), :4]

    # predict keypoints
    pose_results = inference_topdown(pose_estimator, img, bboxes)
    data_samples = merge_data_samples(pose_results)

    # show the results
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    out_file = None
    # if output_root:
    #     out_file = f'{output_root}/test.jpg'

    # visualizer.add_datasample(
    #     'result',
    #     img,
    #     data_sample=data_samples,
    #     draw_gt=False,
    #     draw_heatmap=False,
    #     draw_bbox=True,
    #     show_kpt_idx=True,
    #     skeleton_style='mmpose',
    #     show=True,
    #     wait_time=0,
    #     out_file=out_file,
    #     kpt_thr=0.3)

    # if there is no instance detected, return None
    return data_samples.get('pred_instances', None)
