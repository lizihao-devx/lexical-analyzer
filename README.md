python 3.10

使用uv添加ltp包是会报错，初步判断是默认的tokenizers==0.10.3导致

uv add ltp 会提示安装rust进行编译，但安装rust后编译过程仍旧会报错

最后实行的解决办法是：uv add ltp "tokenizers>=0.11.0"

本项目使用用了`src/`布局，已经在`pyproject.toml`中添加了`hatchling`以便`src/`下的包被顺利识别。

如果导入仍然报错，可执行editable安装：
```bash
uv pip install -e .
```
否则无法导入`src/`下的包