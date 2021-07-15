# -*- coding:utf-8 -*-

import os
import time
import shutil
import json

def create_total_json(root_dir='/'):
    save_path = os.path.join(root_dir, 'total.json')
    total_json = {
        'traceEvents': [],
        'beginningOfTime': 0
    }
    temp_map = {}
    unique_pid = 0
    total_compile_time = 0
    total_json_count = 0
    for parent, dirs, files in os.walk(root_dir):
        for _file in files:
            file_path = os.path.join(parent, _file)
            base_dir = os.path.basename(os.path.normpath(parent))
            filename = file_path.replace(base_dir, '')
            file_root, file_extension = os.path.splitext(file_path)
            if file_extension == '.json':
                trace_json = file(file_path)
                json_dic = json.load(trace_json)
                if 'traceEvents' in json_dic :
                    total_json_count += 1
                    for dic in json_dic['traceEvents']:
                        if dic['name'] == 'ExecuteCompiler':
                           total_compile_time += dic['dur']/1000000.0
                           print "{} -----> {}".format(_file, dic['dur']/1000000.0)
                if _file == 'main.json':
                    total_json['beginningOfTime'] = json_dic['beginningOfTime']
                    unique_pid = json_dic['traceEvents'][0]['pid']
    print "total {} files.".format(total_json_count)
    return total_compile_time

    # for key in temp_map:
    #     total_json['traceEvents'].append(temp_map[key])
    # with open(save_path, "w") as newFile:
    #     newFile.write(json.dumps(total_json, indent=4))

if __name__ == '__main__':
    start_time = time.time()
    enable_time = create_total_json('/Users/yao/ClangModule/x86_64_enable_module')
    disable_time = create_total_json('/Users/yao/ClangModule/x86_64_disable_module')
    delta = enable_time - disable_time
    print 'enable: {}'.format(enable_time)
    print 'disable: {}'.format(disable_time)
    print 'enable - disable = {}'.format(delta)

    print("Total Cost: {}".format(time.time() - start_time))