import json
import sys, os
import subprocess
import re
from glob import glob
from diff_side import *


def exec_cmd(cmd, timeout=20):
    try:
        output = subprocess.check_output(cmd, shell = True, timeout=timeout)
        return True, output.decode()
    except Exception as e:
        return False, e.output.decode()
           
        
def collect_cases():
    my_dir = os.path.dirname(__file__)
    cases = []
    for f in glob('case/*'):
        case_file = f'{my_dir}/{f}'
        cases.append(case_file)
    return cases
     
class Grader:
    
    def __init__(self, lang, func_policy, comment_policy, score) -> None:
        self.lang = lang
        self.func_policy = func_policy
        self.comment_policy = comment_policy
        self.score = score
    
    # only support /* //
    def count_comment(self):
        # 计算注释的行数
        lines = 0
        for file in glob(self.lang):
            with open(file, encoding="utf-8", errors='ignore') as code_file:
                code = code_file.read()
                # 匹配单行注释和多行注释
                comments = re.findall("//.*|/\*.*?\*/", code, re.DOTALL)

                for comment in comments:
                    lines += comment.count("\n") + 1 # 每个注释至少占一行
        return lines
         
         
    def grade_func(self, diff_lines_cnt):
        for p in self.func_policy:
            if diff_lines_cnt >= p[0]:
                score['scores']['function'] -= p[1]
                break
        print(self.func_policy, diff_lines_cnt)
         
           
    def grade_comment(self):
        comment_lines = self.count_comment()
        for p in self.comment_policy:
            if comment_lines >= p[0]:
                score['scores']['comment'] -= p[1]
                break
        print(self.comment_policy, comment_lines)



    def run_code(self, run_cmd, ans_run_cmd, score):
        flag, output = exec_cmd(run_cmd)
        print("[student]: run information\n", flag, output)    
        if not flag:
            score['scores']['function'] = 0
            
        flag, ans = exec_cmd(ans_run_cmd)
        # print("[answer]: run information\n", flag, ans)
        diff_lines_cnt = diff_output(output, ans)
        self.grade_func(diff_lines_cnt)
        # print(ans_run_cmd)


def diff_output(output, ans):
    print("The left side is answer, the right side is your output.")
    print(f"{'=' * 50}")
    # print(better_diff(ans.splitlines(), output.splitlines(),
    #     width=200,
    #     as_string=True,
    #     left_title="  LEFT",
    # ))
    sniff = Sdiffer(max_width=200)
    sniff.print_sdiff(ans.splitlines(), output.splitlines())
    print(f"{'=' * 50}")
    print(f"There are {sniff.diff_lines_cnt} differences.")
    print(f"{'=' * 50}")
    return sniff.diff_lines_cnt

    # # 使用_mdiff方法进行比较
    # diff = difflib.ndiff(ans.splitlines(), output.splitlines())
    # # 打印side-by-side差异
    # for line in list(diff):
    #     code = line[0]
    #     # 根据行的标记决定如何显示
    #     if code == ' ':
    #         # 如果行在两个文件中都存在
    #         print(f"{line[2:].rstrip()} {'':<50} {line[2:].rstrip()}")
    #     elif code == '-':
    #         # 如果行仅在file1中存在
    #         print(f"{line[2:].rstrip()} {'':<50}")
    #     elif code == '+':
    #         # 如果行仅在file2中存在
    #         print(f"{'':<50} {line[2:].rstrip()}")

    # 打印side-by-side差异
    # for (line1, line2, char_changes) in diff:
    #     # print(line1, line2, char_changes)
    #     line1 = line1[0] if line1[0] is not None else ''
    #     line2 = line2[0] if line2[0] is not None else ''
    #     print(f"{line1:<50} {line2}")
    
    # diff = differ.compare(ans.splitlines(), output.splitlines()) # a,b were defined 

    
if __name__ == "__main__":
    config = json.loads(sys.argv[1])
    compile_cmd = config['compile_cmd']
    ans_compile_cmd = config['ans_compile_cmd']
    run_cmd = config['run_cmd']
    ans_run_cmd = config['ans_run_cmd']
    score = config['grade']
    lang = config['lang']

    func_policy_config = config['function']
    func_policy = []
    for p in func_policy_config:
        func_policy.append((p['count'], p['penalty']))
    
    comment_policy_config = config['comment']
    comment_policy = []
    for p in comment_policy_config:
        comment_policy.append((p['count'], p['penalty']))
    
    grader = Grader(lang=lang, func_policy=func_policy, comment_policy=comment_policy, score=score)
    
    flag, output = exec_cmd(ans_compile_cmd)
    
    flag, output = exec_cmd(compile_cmd)
    print("[student]: compile information\n", flag, output)
    if not flag:
        score['scores']['compile'] = 0
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    cases = collect_cases()
    
    if len(cases) == 0:
        grader.run_code(run_cmd, ans_run_cmd, score)
    else:
        for c in cases:
            grader.run_code(run_cmd + f"<< '{c}'", ans_run_cmd + f"<< '{c}'", score)
       
    grader.grade_comment()
    
    print(json.dumps(score))