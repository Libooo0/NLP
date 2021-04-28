from paddleocr import PaddleOCR

ocr = PaddleOCR(use_pdserving=False, use_angle_cls=False, det=True, cls=True, use_gpu=True, lang="ch",
                                    det_max_side_len=1500, det_db_thresh=0.2, det_db_box_thresh=0.3,
                                    det_db_unclip_ratio=2.0,
                                    gpu_mem=4000, rec_batch_num=10, cls_batch_num=10)
img2 = r'C:\Users\86182\Desktop\202002\202002\00b6a7dc890445bba59cfc8fb60a3c90\11edd47a1c47467ab27a2379e9562e46_1.png'
result = ocr.ocr(img2, det=True, rec=True, cls=False)
print(result)