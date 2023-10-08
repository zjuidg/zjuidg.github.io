import json
import os
import shutil
from copy import deepcopy
from typing import List, Dict, Optional

from flask import Flask, request, send_from_directory


def load_file(path):
    with open(path, encoding='utf8') as f:
        return json.load(f)


def save_file(path, content):
    with open(path, 'w+', encoding='utf8') as f:
        json.dump(content, f)


def render_text_input(label, value, key, note='', tag='input'):
    ipt = f'<input style="width:800px" type="text" value="{value}" \
                   onchange="fetch(\'http://127.0.0.1:5000/set_cache/{key}/\'+this.value)\
                                                                 .then(res => res.text())\
                                                                 .then(res => res != \'success\' && alert(res))"></input>' \
        if tag == 'input' else \
        f'<textarea rows="10" style="width:800px" \
                      onchange="fetch(\'http://127.0.0.1:5000/set_cache/{key}/\'+this.innerText)\
                          .then(res => res.text())\
                          .then(res => res != \'success\' && alert(res))">{value}</textarea>'
    return f'<div style="display:flex;align-items:start;margin:10px 0;">\
        <label style="width:100px">{label}</label>\
        {ipt}\
        <div style="width:400px">{note}</div>\
    </div>'


def render_file_input(label, value, key):
    func = f'var input = document.createElement(\'input\'); \
        input.type = \'file\'; \
        input.onchange = () => \
            fetch(\
                \'http://127.0.0.1:5000/set_cache/{key}/\'+input.files[0].name, \
                {{method:\'POST\',body:input.files[0]}}\
            ).then(res => res.text()).then(res => res != \'success\' && alert(res)); \
        input.click();'
    drop_func = f'event.preventDefault();\
        var file = event.dataTransfer.files[0];\
        fetch(\
            \'http://127.0.0.1:5000/set_cache/{key}/\'+file.name, \
            {{method:\'POST\',body:file}}\
        ).then(res => res.text()).then(res => res != \'success\' && alert(res));'
    return f'<div style="display:flex;align-items:start;margin:10px 0;">\
        <label style="width:100px">{label}</label>\
        <div style="width:100px;height:50px;{btn_style}" \
             ondragover="event.preventDefault();" ondrop="{drop_func}"\
             onclick="{func}">选择文件<br>(或拖拽至此)</div>\
        <div style="width:700px">{value}</div>\
    </div>'


app = Flask(__name__)
config: List[any] = load_file('./source/publications.json')
cache_pub: Optional[Dict[str, any]] = None
btn_style = 'display:inline-block;border:1px solid black;text-align:center;cursor:pointer;'
necessary_keys = ['id',
                  'title',
                  'authors',
                  'teaser',
                  'paper',
                  'source',
                  'transaction',
                  'year',
                  'DOI',
                  'abstract', ]


@app.route('/')
def pub_list_page():
    global cache_pub
    cache_pub = None
    return '<div>\
        <h1>Publication List</h1>\
        <a href="/add">add new</a>\
        <div style="{1}" onclick="fetch(\'http://127.0.0.1:5000/backup\').then(res => res.text()).then(alert)">backup</div>\
        <ul>{0}</ul>\
    </div>'.format(''.join([
        '<li><a href="/pub/{0}">{1}</a></li>'.format(pub['id'], pub['id'])
        for pub in config
    ]), btn_style)


@app.route('/pub/<pub_id>')
def pub_detail_page(pub_id):
    pub = None
    for p in config:
        if p['id'] == pub_id:
            pub = p
    if pub is None:
        return '<div><h1>Not Found!</h1><a href="/">Back</a></div>'
    global cache_pub
    if cache_pub is None:
        cache_pub = deepcopy(pub)
    return '<div>\
        <h1><a href="/"><-</a>Update Publication</h1>\
        <form>\
            {2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}{20}\
            <div style="{0}" onclick="fetch(\'http://127.0.0.1:5000/update/{1}\').then(res => res.text()).then(alert)">submit</div>\
        </form>\
    </div>'.format(
        btn_style, pub_id,
        render_text_input('*ID', pub['id'], 'id', '简写名，尽量短，且可以作为网址的一部分'),
        render_text_input('*Title', pub['title'], 'title', '论文标题'),
        render_text_input('*Authors', ', '.join(pub['authors']), 'authors', '逗号分隔，如San Zhang, Si Li'),
        render_file_input('*Teaser', pub['teaser'], 'teaser'),
        render_file_input('*Paper', pub['paper'], 'paper'),
        render_text_input('*Source', pub['source'], 'source', '投的期刊/会议名，简写，如IEEE TVCG'),
        render_text_input('*Transaction', pub['transaction'], 'transaction', '投的期刊/会议名，如IEEE Transactions on '
                                                                             'Intelligent Transportation Systems ('
                                                                             'TITS 2020)'),
        render_text_input('*Year', pub['year'], 'year', '年份'),
        render_text_input('*DOI', pub['DOI'], 'DOI'),
        render_text_input('*Abstract', pub['abstract'], 'abstract', '摘要', 'textarea'),
        render_text_input('Video',
                          pub['video'].split('/')[-1] if 'video' in pub and pub['video'] != '' else '',
                          'video',
                          '请上传到YouTube，并填写hash码，如J1P2VSn8ge4'),
        render_text_input('Volume',
                          pub['volume'] if 'volume' in pub else '',
                          'volume'),
        render_text_input('Issue', pub['issue'] if 'issue' in pub else '', 'issue'),
        render_text_input('Article No', pub['articleNo'] if 'articleNo' in pub else '', 'articleNo', '论文序号'),
        render_text_input('Start Page', pub['page'][0] if 'page' in pub else '', 'page1'),
        render_text_input('End Page', pub['page'][1] if 'page' in pub else '', 'page2'),
        render_text_input('Demo', pub['demo'] if 'demo' in pub else '', 'demo', 'A web link for your demo.'),
        render_text_input('System', pub['system'] if 'system' in pub else '', 'system', 'A web link for your system.'),
        render_text_input('Title Key', ', '.join(pub['titleKey']) if 'titleKey' in pub else '', 'titleKey',
                          '逗号分隔，如Honorable Mention, Preview'),
    )


@app.route('/add')
def add_pub_page():
    global cache_pub
    cache_pub = {}
    return '<div>\
        <h1><a href="/"><-</a>Add New Publication</h1>\
        <form>\
            {1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}\
            <div style="{0}" onclick="fetch(\'http://127.0.0.1:5000/add\').then(res => res.text()).then(alert)">submit</div>\
        </form>\
    </div>'.format(
        btn_style,
        render_text_input('*ID', '', 'id', '简写名，尽量短，且可以作为网址的一部分'),
        render_text_input('*Title', '', 'title', '论文标题'),
        render_text_input('*Authors', '', 'authors', '逗号分隔，如San Zhang, Si Li'),
        render_file_input('*Teaser', '', 'teaser'),
        render_file_input('*Paper', '', 'paper'),
        render_text_input('*Source', '', 'source', '投的期刊/会议名，简写，如IEEE TVCG'),
        render_text_input('*Transaction', '', 'transaction', '投的期刊/会议名，如IEEE Transactions on '
                                                             'Intelligent Transportation Systems ('
                                                             'TITS 2020)'),
        render_text_input('*Year', '', 'year', '年份'),
        render_text_input('*DOI', '', 'DOI'),
        render_text_input('*Abstract', '', 'abstract', '摘要', 'textarea'),
        render_text_input('Video',
                          '',
                          'video',
                          '请上传到YouTube，并填写hash码，如J1P2VSn8ge4'),
        render_text_input('Volume',
                          '',
                          'volume'),
        render_text_input('Issue', '', 'issue'),
        render_text_input('Article No', '', 'articleNo', '论文序号'),
        render_text_input('Start Page', '', 'page1'),
        render_text_input('End Page', '', 'page2'),
        render_text_input('Demo', '', 'demo', 'A web link for your demo.'),
        render_text_input('System', '', 'system', 'A web link for your system.'),
        render_text_input('Title Key', '', 'titleKey', '逗号分隔，如Honorable Mention, Preview'),
    )


@app.route('/set_cache/<key>/<value>', methods=['GET', 'POST'])
def set_cache(key, value):
    global cache_pub
    if cache_pub is None:
        return 'failed'
    if key in ['id', 'title', 'DOI', 'source', 'transaction', 'abstract', 'demo', 'system']:
        cache_pub[key] = value
    elif key in ['year', 'volume', 'issue', 'articleNo']:
        cache_pub[key] = int(value)
    elif key in ['authors', 'titleKey']:
        cache_pub[key] = list(map(lambda x: x.strip(), value.split(',')))
    elif key == 'page1':
        if 'page' not in cache_pub:
            cache_pub['page'] = [0, 0]
        cache_pub['page'][0] = int(value)
    elif key == 'page2':
        if 'page' not in cache_pub:
            cache_pub['page'] = [0, 0]
        cache_pub['page'][1] = int(value)
    elif key == 'video':
        cache_pub["video"] = f"https://youtu.be/{value}"
        cache_pub["embedVideo"] = f"https://www.youtube.com/embed/{value}"
    elif key in ['teaser', 'paper']:
        with open(value, 'wb+') as f:
            f.write(request.data)
        cache_pub[key] = value
        return 'success'
    else:
        return 'failed'
    return 'success'


@app.route('/update/<pub_id>')
def upd_pub(pub_id):
    global config, cache_pub

    # check for necessary information
    if cache_pub is None or '' in [cache_pub[key] for key in necessary_keys]:
        return 'Failed! Some necessary information is not filled!'

    # check for duplicate id
    new_pub_id = cache_pub['id']
    if new_pub_id != pub_id:
        for pub in config:
            if pub['id'] == new_pub_id:
                return 'Failed! Duplicated Pub ID!'

    # find ori pub
    ori_pub = None
    for pub in config:
        if pub['id'] == pub_id:
            ori_pub = pub
    if ori_pub is None:
        return 'Failed! Original Pub Not Found!'

    # manage id change
    ori_folder = f'source/projects/{pub_id}'
    tgt_folder = f'source/projects/{new_pub_id}'
    if pub_id != new_pub_id:
        shutil.move(ori_folder, tgt_folder)  # change folder name
        for key in ['teaser', 'paper']:  # change filepath in config
            if cache_pub[key].startswith(ori_folder):
                cache_pub[key] = cache_pub[key].replace(ori_folder, tgt_folder)

    # manage files
    for key in ['teaser', 'paper']:
        if not cache_pub[key].startswith(tgt_folder) and os.path.isfile(cache_pub[key]):
            tgt_path = f'source/projects/{new_pub_id}/{cache_pub[key]}'
            shutil.move(cache_pub[key], tgt_path)
            cache_pub[key] = tgt_path

    # update config
    for key in cache_pub:
        ori_pub[key] = cache_pub[key]
    save_file(f'./source/publications.json', config)

    return 'success'


@app.route('/add')
def add_pub():
    global config, cache_pub

    # check for necessary information
    if cache_pub is None or '' in [cache_pub[key] for key in necessary_keys]:
        return 'Failed! Some necessary information is not filled!'

    # check for duplicate id
    pub_id = cache_pub['id']
    for pub in config:
        if pub['id'] == pub_id:
            return 'Failed! Duplicated Pub ID!'

    # manage files
    folder = f'source/projects/{pub_id}'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    teaser_path = f'{folder}/{cache_pub["teaser"]}'
    paper_path = f'{folder}/{cache_pub["paper"]}'
    shutil.move(cache_pub['teaser'], teaser_path)
    shutil.move(cache_pub['paper'], paper_path)
    cache_pub['teaser'] = teaser_path
    cache_pub['paper'] = paper_path

    # manage config
    config.insert(0, deepcopy(cache_pub))
    save_file(f'./source/publications.json', config)
    return 'success'


@app.route('/backup')
def backup():
    save_file("./source/publications.json.bak", config)
    return 'success'


@app.route('/test')
def test():
    return send_from_directory('./', 'index.html')


@app.route('/source/<path:path>')
def static_file(path):
    return send_from_directory('./source', path)


if __name__ == "__main__":
    app.run(debug=True)
