import subprocess

val = 'python ' + r'C:\Users\86182\Desktop\tt\ocr_text.py'
subprocess.call(val,shell=True)
val = 'python ' + r'D:\xiangmu\dianfu_classifier\model_classify\run_classifier_tiny.py'
subprocess.call(val,shell=True)
val = 'python ' + r'C:\Users\86182\Desktop\tt\tupian_classify.py'
subprocess.call(val,shell=True)