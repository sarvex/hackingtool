# coding=utf-8
import re

from core import HackingTool
from core import HackingToolsCollection
from hackingtool import all_tools


def sanitize_anchor(s):
    return re.sub(r"\W", "-", s.lower())


def get_toc(tools, indentation = ""):
    md = ""
    for tool in tools:
        if isinstance(tool, HackingToolsCollection):
            md += f"{indentation}- [{tool.TITLE}](#{sanitize_anchor(tool.TITLE)})\n"
            md += get_toc(tool.TOOLS, indentation=f'{indentation}    ')
    return md


def get_tools_toc(tools, indentation = "##"):
    md = ""
    for tool in tools:
        if isinstance(tool, HackingToolsCollection):
            md += f"{indentation}# {tool.TITLE}\n"
            md += get_tools_toc(tool.TOOLS, indentation=f'{indentation}#')
        elif isinstance(tool, HackingTool):
            if tool.PROJECT_URL:
                md += f"- [{tool.TITLE}]({tool.PROJECT_URL})\n"
            else:
                md += f"- {tool.TITLE}\n"
    return md


def generate_readme():
    toc = get_toc(all_tools[:-1])
    tools_desc = get_tools_toc(all_tools[:-1])

    with open("README_template.md") as fh:
        readme_template = fh.read()

    readme_template = readme_template.replace("{{toc}}", toc)
    readme_template = readme_template.replace("{{tools}}", tools_desc)

    with open("README.md", "w") as fh:
        fh.write(readme_template)


if __name__ == '__main__':
    generate_readme()
