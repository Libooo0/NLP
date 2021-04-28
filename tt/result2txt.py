

# def txt2result():
"""
test与test_result对应起来
"""
# 模型出来的类别
with open(r'D:\xiangmu\dianfu_classifier\model_classify\text\output_new_bak_tiny_20200908_wo_star\test_results.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    list = [0]
    for line in lines:
        ls = [float(x) for x in line.split()]
        list.append(ls.index(max(ls)))
    print(list)
# ocr出来的文本
with open('test_final.txt', 'w', encoding='utf-8') as t:
    t.write('label\ttext\n')
    with open(r'C:\Users\86182\Desktop\tt\test.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            line = str(list[i]) + lines[i][1:]

            t.write("{}".format(line))