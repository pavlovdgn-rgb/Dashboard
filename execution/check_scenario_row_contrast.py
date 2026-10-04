"""Reproduce contrast checks from Figma node 136:488, inspected 2026-09-22."""
import json
from pathlib import Path


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


if __name__ == '__main__':
    pairs = [
        ('Primary text', '#22241F', '#ECEEDC', 4.5),
        ('Secondary text', '#66695F', '#ECEEDC', 4.5),
        ('Percentage', '#626E32', '#ECEEDC', 4.5),
        ('Incomplete count', '#66695F', '#F3F3EE', 4.5),
        ('Selected label', '#22241F', '#FFFFFF', 4.5),
        ('Radio dot', '#626E32', '#FFFFFF', 3),
        ('Radio outline', '#626E32', '#ECEEDC', 3),
        ('Progress fill against track', '#626E32', '#E4E5DC', 3),
        ('Selected background against white (supplementary cue)', '#ECEEDC', '#FFFFFF', None),
    ]
    result = [{'element': label, 'foreground': fg, 'background': bg,
               'ratio': contrast(fg, bg), 'threshold': threshold,
               'passes': contrast(fg, bg) >= threshold if threshold else None}
              for label, fg, bg, threshold in pairs]
    out = Path(__file__).resolve().parents[1] / '.tmp/analytics-components/contrast.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
