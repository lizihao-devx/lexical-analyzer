from wordcloud import WordCloud
from pathlib import Path
import numpy as np
from PIL import Image


class CSVWordCloudExporter:
    def __init__(
        self,
        font_path="fonts/MSYH.TTC",
        width: int = 1280,
        height: int = 960,
        background_color=None,
    ):
        self.font_path = font_path
        self.width = width
        self.height = height
        self.background_color = background_color

    # ==========================
    # 椭圆 mask（与原逻辑一致）
    # ==========================
    def generate_circle_mask(self):
        y, x = np.ogrid[:self.height, :self.width]

        center_x = self.width / 2
        center_y = self.height / 2

        a = self.width / 2
        b = self.height / 2

        ellipse = ((x - center_x) ** 2) / (a ** 2) + \
                  ((y - center_y) ** 2) / (b ** 2) > 1

        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        mask[ellipse] = 255

        return mask

    # ==========================
    # 白底 + 外部透明
    # ==========================
    def _apply_circle_white(self, wc: WordCloud, mask: np.ndarray) -> Image.Image:
        wc_img = wc.to_image().convert("RGBA")

        width, height = wc_img.size

        transparent_base = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        mask_img = Image.fromarray(mask).convert("L")
        inverted_mask = Image.eval(mask_img, lambda x: 255 - x)

        white_layer = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        transparent_base.paste(white_layer, mask=inverted_mask)

        final_img = Image.alpha_composite(transparent_base, wc_img)

        return final_img

    # ==========================
    # 从 CSV 构建词频字典
    # ==========================
    def _build_freq_dict_from_csv(self, csv_path: str) -> dict[str, int]:
        freq: dict[str, int] = {}

        with open(csv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")

                if len(parts) < 2:
                    continue

                word = parts[0].strip()
                try:
                    count = int(parts[1].strip())
                except ValueError:
                    # 跳过表头或非法行
                    continue

                freq[word] = freq.get(word, 0) + count

        return freq

    # ==========================
    # 导出词云
    # ==========================
    def export(
        self,
        csv_path: str,
        out_path: str = "output/wordcloud.png",
        shape="circle",
    ):
        freq_dict = self._build_freq_dict_from_csv(csv_path)

        if not freq_dict:
            raise ValueError("No valid word-frequency data found in CSV.")

        if shape == "circle":
            mask = self.generate_circle_mask()
        else:
            mask = None

        wc = WordCloud(
            font_path=self.font_path,
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            mode="RGBA",
            mask=mask,
            prefer_horizontal=1.0,
        )

        wc.generate_from_frequencies(freq_dict)

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if shape == "circle":
            final_img = self._apply_circle_white(wc, mask)
            final_img.save(out_path)
        else:
            wc.to_file(out_path)


# ==========================
# CLI 入口
# ==========================
if __name__ == "__main__":
    exporter = CSVWordCloudExporter(
        font_path="fonts/MSYH.TTC",
        width=1280,
        height=960,
        background_color=None,
    )

    exporter.export(
        csv_path="data/abstract.csv",
        out_path="output/wordcloud_ab.png",
        shape="circle",
    )

    print("Word cloud generated successfully.")
