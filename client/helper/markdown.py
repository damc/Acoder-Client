from typing import Dict

from .files import content


def load_markdown(file_path: str) -> Dict[str, str]:
    content_ = content(file_path)
    lines = content_.splitlines()
    data = {'title': lines[0].strip("# ") if lines else ""}
    lines = lines[1:]
    subtitles = []
    subtitles_start = {}
    for key, line in enumerate(lines):
        if line.startswith("##"):
            subtitle = line.strip("# ").lower()
            subtitles.append(subtitle)
            subtitles_start[subtitle] = key
    for i in range(0, len(subtitles)):
        start = subtitles_start[subtitles[i]] + 1
        end = (
            subtitles_start[subtitles[i + 1]]
            if i + 1 < len(subtitles)
            else len(lines)
        )
        subtitle_content = "\n".join(lines[start:end]).strip()
        data[subtitles[i]] = subtitle_content
    return data
