# coding=utf-8
"""
The core of this code-obfuscation
Licensed under MIT license:
MIT License

Copyright (c) 2025 Holiday-Zhuyichen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

A great "thank you" to DouBao here
"""

import ast
from typing import override


class FStringSimplifier(ast.NodeTransformer):
    """
    Simplize f string
    """
    @override
    def visit_JoinedStr(self, node):
        """
        Joined String = f string
        """
        new_values = []
        for value in node.values:
            if isinstance(value, ast.FormattedValue) and isinstance(value.value, ast.Call):
                # 将函数调用提取到单独的变量 (修复变量重复定义问题)
                var_name = f"_fstr_{id(value)}"

                # 创建赋值语句
                assign = ast.Assign(
                    targets=[ast.Name(id=var_name, ctx=ast.Store())],
                    value=value.value
                )

                # 创建新的格式化值节点，使用变量名 (修复类型不兼容问题)
                new_value = ast.FormattedValue(
                    value=ast.Name(id=var_name, ctx=ast.Load()),
                    conversion=value.conversion,
                    format_spec=value.format_spec
                )

                # 保存新的节点
                # noinspection PyUnresolvedReferences
                self.assignments.append(assign)  # type: ignore[attr-defined]
                new_values.append(new_value)
            else:
                new_values.append(value)

        # 创建新的JoinedStr节点
        return ast.JoinedStr(values=new_values)  # type: ignore[arg-type]
