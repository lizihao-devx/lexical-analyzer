from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path
from lexical_analyzer.result import AnalysisResult

def black_saturation_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """
    频率高 → 更纯黑
    频率低 → 偏灰
    """
    max_font = 100

    ratio = min(font_size / max_font, 1.0)

    # 从灰到黑
    gray = int(180 - ratio * 180)
    gray = max(gray, 0)

    return f"rgb({gray}, {gray}, {gray})"

class WordCloudExporter:
    def __init__(
        self,
        font_path = "fonts/MSYH.TTC",
        width: int = 1280,
        height: int = 960,
        background_color: str = "white",
    ):
        self.font_path = font_path
        self.width = width
        self.height = height
        self.background_color = background_color

    def export(
        self,
        result: AnalysisResult,
        out_path: str = "output/wordcloud.png",
        pos: str | None = None,
    ):
        """
        生成词云图片

        :param result: AnalysisResult 对象，包含词频分析结果
        :param output_path: 输出图片路径
        :param pos: 指定词性，若为 None 则生成所有词性的词云
        """
        freq_dict = self._build_freq_dict(result, pos)

        if not freq_dict:
            raise ValueError("No words available for word cloud generation.")
        
        wc = WordCloud(
            font_path=self.font_path,
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            # max_font_size=150,
            prefer_horizontal=1.0,
            color_func=black_saturation_color_func,
        )
        
        # print("font_path =", repr(self.font_path))

        wc.generate_from_frequencies(freq_dict)

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(self.width / 100, self.height / 100))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()

    def _build_freq_dict(
        self,
        result: AnalysisResult,
        pos: str | None
    ) -> dict[str, int]:
        """
        从AnalysisResult中构建词频字典
        """
        freq: dict[str, int] = {}

        for p, counter in result.freq_groups.items():
            # 将pos转换为字符串进行比较
            pos_str = p.value if hasattr(p, "value") else str(p)

            # 如果指定词性，只保留对应的
            if pos and pos_str != pos:
                continue

            for word, count in counter.items():
                freq[word] = freq.get(word, 0) + count

        return freq