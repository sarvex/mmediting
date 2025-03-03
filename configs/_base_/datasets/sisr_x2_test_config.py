test_pipeline = [
    dict(
        type='LoadImageFromFile',
        key='img',
        color_type='color',
        channel_order='rgb',
        imdecode_backend='cv2'),
    dict(
        type='LoadImageFromFile',
        key='gt',
        color_type='color',
        channel_order='rgb',
        imdecode_backend='cv2'),
    dict(type='PackEditInputs')
]

# test config for Set5
set5_data_root = 'data/Set5'
set5_dataloader = dict(
    num_workers=4,
    persistent_workers=False,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='BasicImageDataset',
        metainfo=dict(dataset_type='set5', task_name='sisr'),
        data_root=set5_data_root,
        data_prefix=dict(img='LRbicx2', gt='GTmod12'),
        pipeline=test_pipeline))
set5_evaluator = dict(
    type='EditEvaluator',
    metrics=[
        dict(type='PSNR', crop_border=2, prefix='Set5'),
        dict(type='SSIM', crop_border=2, prefix='Set5'),
    ])

set14_data_root = 'data/Set14'
set14_dataloader = dict(
    num_workers=4,
    persistent_workers=False,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='BasicImageDataset',
        metainfo=dict(dataset_type='set14', task_name='sisr'),
        data_root=set14_data_root,
        data_prefix=dict(img='LRbicx2', gt='GTmod12'),
        pipeline=test_pipeline))
set14_evaluator = dict(
    type='EditEvaluator',
    metrics=[
        dict(type='PSNR', crop_border=2, prefix='Set14'),
        dict(type='SSIM', crop_border=2, prefix='Set14'),
    ])

# test config for DIV2K
div2k_data_root = 'data/DIV2K'
div2k_dataloader = dict(
    num_workers=4,
    persistent_workers=False,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='BasicImageDataset',
        # ann_file='meta_info_DIV2K800sub_GT.txt',
        ann_file='meta_info_DIV2K100sub_GT.txt',
        metainfo=dict(dataset_type='div2k', task_name='sisr'),
        data_root=div2k_data_root,
        data_prefix=dict(
            img='DIV2K_train_LR_bicubic/X2_sub', gt='DIV2K_train_HR_sub'),
        pipeline=test_pipeline))
div2k_evaluator = dict(
    type='EditEvaluator',
    metrics=[
        dict(type='PSNR', crop_border=2, prefix='DIV2K'),
        dict(type='SSIM', crop_border=2, prefix='DIV2K'),
    ])

# test config
test_cfg = dict(type='EditTestLoop')
test_dataloader = [
    set5_dataloader,
    set14_dataloader,
    div2k_dataloader,
]
test_evaluator = [
    set5_evaluator,
    set14_evaluator,
    div2k_evaluator,
]
