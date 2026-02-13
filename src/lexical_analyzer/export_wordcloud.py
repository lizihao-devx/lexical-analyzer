from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path
from lexical_analyzer.result import AnalysisResult
import numpy as np
from PIL import Image

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
        background_color=None,
    ):
        self.font_path = font_path
        self.width = width
        self.height = height
        self.background_color = background_color

    def generate_circle_mask(self, height=960, width=1280):
        y, x = np.ogrid[:height, :width]
        center_x = width / 2
        center_y = height / 2

        a = width / 2
        b = height / 2

        ellipse = ((x - center_x) ** 2) / (a ** 2) + \
                  ((y - center_y) ** 2) / (b ** 2) > 1
        
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[ellipse] = 255
        
        return mask
    
    def _apply_circle_white(self, wc: WordCloud, mask: np.ndarray) -> Image.Image:
        """
        将词云图像处理为：
        - 圆内白色背景
        - 圆外透明
        """

        # 1️⃣ 获取 RGBA 词云图像
        wc_img = wc.to_image().convert("RGBA")

        width, height = wc_img.size

        # 2️⃣ 创建透明底图
        transparent_base = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # 3️⃣ 创建 mask 的 PIL 版本
        # 当前规则：
        #   mask == 0 → 圆内（允许）
        #   mask == 255 → 圆外（禁止）
        mask_img = Image.fromarray(mask).convert("L")

        # 4️⃣ 反转 mask
        # 因为 PIL paste 规则：
        #   255 → 贴
        #   0 → 不贴
        inverted_mask = Image.eval(mask_img, lambda x: 255 - x)

        # 5️⃣ 创建纯白圆层
        white_layer = Image.new("RGBA", (width, height), (255, 255, 255, 255))

        # 6️⃣ 在透明底图上贴白色圆
        transparent_base.paste(white_layer, mask=inverted_mask)

        # 7️⃣ 把词云图叠加到白色圆上
        final_img = Image.alpha_composite(transparent_base, wc_img)

        return final_img


    def export(
        self,
        result: AnalysisResult,
        out_path: str = "output/wordcloud.png",
        pos: str | None = None,
        shape = "circle",
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
        
        if shape == "circle":
            mask = self.generate_circle_mask()
        else:
            mask = None
        
        wc = WordCloud(
            font_path=self.font_path,
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            # max_font_size=150,
            mode='RGBA',
            mask=mask,
            prefer_horizontal=1.0,
            # color_func=black_saturation_color_func,
            # contour_width=2,
            # contour_color="black"
        )
        
        # print("font_path =", repr(self.font_path))

        wc.generate_from_frequencies(freq_dict)

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if shape == "circle":
            final_img = self._apply_circle_white(wc, mask)
            final_img.save(out_path)
        else:
            wc.to_file(out_path)

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