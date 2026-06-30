# CLAUDE.md - MyNotes

## 项目简介

MyNotes 是一个纯前端个人笔记与日常规划工具。项目无需后端、无需构建，直接用浏览器打开 `MyNotes.html` 即可运行。数据保存在浏览器 `localStorage` 中。

## 技术栈

- 原生 HTML、CSS、JavaScript
- 非 ES Module，脚本通过 `<script>` 顺序加载
- 无框架、无包管理器、无构建工具
- 本地存储：`localStorage`

## 入口与结构

```text
MyNotes.html
README.md
AGENTS.md
CLAUDE.md
assets/
css/
  base.css
  nav.css
  calendar.css
  panel.css
  time-picker.css
js/
  helpers.js
  state.js
  storage.js
  lang.js
  notes.js
  timepicker.js
  calendar.js
  plans.js
  app.js
```

## 开发约定

- 保持原生前端实现，不引入框架或构建流程。
- JS 文件依赖加载顺序见 `MyNotes.html`，新增脚本时必须注意顺序。
- 全局状态集中在 `js/state.js`。
- 数据读写统一走 `js/storage.js`。
- 多语言文案维护在 `js/lang.js`，静态文本使用 `data-i18n` 和 `data-i18n-placeholder`。
- CSS 按模块维护，避免无关样式混入。
- README 中引用的截图放在 `assets/`。

## 数据键

- `my_notes_data`：每日规划数据
- `my_notes_lang`：语言偏好
- `note_{year}_{month}`：月备注

## 设计方向

整体风格参考 Apple Human Interface Guidelines：浅灰背景、毛玻璃卡片、清晰层级、克制动效。主色为 Apple Blue，完成状态使用绿色，删除/危险状态使用红色。

## 运行方式

直接打开：

```text
MyNotes.html
```

也可以用 VS Code Live Server 预览。

## Git

- 默认分支：`main`
- 远程仓库：`https://github.com/ab2956955606-cmyk/MyNotes`
- 提交前检查 `git status --short --branch`
