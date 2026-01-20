python 3.10

使用uv添加ltp包是会报错，初步判断是默认的tokenizers==0.10.3导致
uv add ltp 会提示安装rust进行编译，但安装rust后编译过程仍旧会报错
最后实行的解决办法是：uv add ltp "tokenizers>=0.11.0"

此项目使用用了`src/`布局，需要执行editable安装：
```bash
uv pip install -e .
```
否则无法导入`src/`下的包