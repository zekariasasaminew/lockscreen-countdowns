# Countdown lock screens

Three iPhone lock screens that change every day until a real deadline. A static wallpaper cannot count down, so each concept is one image per day, swapped each morning by a Shortcuts automation.

Live: https://zekariasasaminew.github.io/lockscreen-countdowns/

| Concept | Deadline | Page |
| --- | --- | --- |
| Three Rounds | Augustana fall finals, Dec 11 2026, 6 PM | [three-rounds](https://zekariasasaminew.github.io/lockscreen-countdowns/three-rounds/) |
| City Lights | Moving to Chicago, Jan 6 2027 | [chicago](https://zekariasasaminew.github.io/lockscreen-countdowns/chicago/) |
| Merge to Main | Augustana fall finals, Dec 11 2026, 6 PM | [merge-to-main](https://zekariasasaminew.github.io/lockscreen-countdowns/merge-to-main/) |

Each page has a day slider, a download button, and phone setup steps. Frames live at `docs/<concept>/frames/<yyyy-MM-dd>.jpg`.

## Credits

Designed and directed by Zekarias Asaminew. Illustrations, the Merge to Main milestone plan, layout, compositing and rendering made with Gemini.

`build.py` collects frames rendered by each concept's own `render.py --all` and writes `docs/` and `covers/`.
