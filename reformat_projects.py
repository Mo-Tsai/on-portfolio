"""
reformat_projects.py v3
4 sections per page, ~2 photos per text break, EN translations included.
Reads meta from template .txt files; text from TEXTS dict (with all translations).
"""
import os, re, glob, shutil
from bs4 import BeautifulSoup

TEMPLATE_DIR = "project_content_template"

COMMERCIAL = [
    "commercial/de-nuit","commercial/monte","commercial/r-sanderson",
    "commercial/lezun","commercial/mu-clinic","commercial/dunhua-32f",
    "commercial/elle-cafe","commercial/fire-play","commercial/iron-chef",
    "commercial/cava-baja","commercial/retrodandy","commercial/wave-flower",
    "commercial/yun-jiao","commercial/dunnan-9f","commercial/new-vision",
    "commercial/lalaport",
]
RESIDENTIAL = [
    "residential/residence-h","residential/residence-r","residential/residence-c",
    "residential/residence-l","residential/residence-g","residential/residence-s",
    "residential/residence-o","residential/residence-k","residential/residence-v",
    "residential/residence-m","residential/residence-p",
]

SECTION_TO_FOLDER = {
    "denuit":"commercial/de-nuit","rsanderson":"commercial/r-sanderson",
    "lezun":"commercial/lezun","muclinic":"commercial/mu-clinic",
    "dunhua32f":"commercial/dunhua-32f","ellecafe":"commercial/elle-cafe",
    "fireplay":"commercial/fire-play","ironchef":"commercial/iron-chef",
    "cavabaja":"commercial/cava-baja","retrodandy":"commercial/retrodandy",
    "waveflower":"commercial/wave-flower","yunjiao":"commercial/yun-jiao",
    "dunnan9f":"commercial/dunnan-9f","newvision":"commercial/new-vision",
    "lalaport":"commercial/lalaport",
    "residenceh":"residential/residence-h","residencer":"residential/residence-r",
    "residencec":"residential/residence-c","residencel":"residential/residence-l",
    "residenceg":"residential/residence-g","residences":"residential/residence-s",
    "residenceo":"residential/residence-o","residencek":"residential/residence-k",
    "residencev":"residential/residence-v","residencem":"residential/residence-m",
    "residencep":"residential/residence-p",
}

# ═══════════════════════════════════════════════════════════════════
#  TEXT CONTENT — quote (zh,en) + sections [(zh,en), ...]
# ═══════════════════════════════════════════════════════════════════

TEXTS = {}

# ── de nuit (4 sections) ──────────────────────────────────────────
TEXTS["commercial/de-nuit"] = {
 "q":("侍酒師的工作動線和客人的感受動線，可以同時成立嗎？",
      "Can the sommelier's working logic and the guest's experiential logic coexist?"),
 "s":[
  ("入口處的弧形吧台，是整個空間的第一個問答。它既是侍酒師的工作站，也是客人進入用餐狀態的過渡地帶。材質選用深色石材與拉絲銅件，在光線的映照下，讓邊界變得模糊而有層次。",
   "The curved bar at the entrance is the space's first question and answer — both the sommelier's workstation and the threshold through which guests transition into the dining state. Dark stone and brushed brass blur boundaries under light, creating depth."),
  ("主用餐區採用訂製半圓形卡座，將私密性與開放感並置。座位的弧度讓每一組客人都有屬於自己的角落，卻不被完全隔離。",
   "Custom semi-circular banquettes in the main dining area place intimacy and openness side by side. The curvature gives each group its own corner without full enclosure."),
  ("天花板以手工折件的金屬波浪板收尾，呼應酒窖的意象，同時創造出獨特的聲學環境，讓對話在喧囂中保有隱私。",
   "Hand-folded metal wave panels on the ceiling echo the wine cellar while creating an acoustic environment where conversation holds its privacy within the surrounding noise."),
  ("燈光設計是整個空間最重要的敘事工具。暖白光源以不同角度和強度分層佈置，讓每一張桌子都擁有屬於自己的光環境，而整體氛圍仍保持一致的深沉與專注。",
   "Lighting is the primary narrative instrument. Warm-white sources layered at varying angles and intensities give each table its own light environment, while the overall atmosphere holds its depth and focus."),
]}

# ── Monte (4 sections) ────────────────────────────────────────────
TEXTS["commercial/monte"] = {
 "q":("設計不是在寬裕的時候才開始工作，是在限制中，為了精確的解法而產出。",
      "Design doesn't begin with abundance. It begins with the pressure to be exact."),
 "s":[
  ("13坪。第一個決定是廚房的位置。確定了，開放式廚房的面才有方向，確定了，弧形吧台才能思考如何迎接坐下來的人。弧形把兩端的線條向內收攏，讓最左與最右的人自然往中間靠近——坐在吧台的人彼此之間有距離，但同時有聚攏感，像圓桌，不像排隊。",
   "Thirteen pings. The first decision was the kitchen position. Once fixed, the open kitchen had a direction; once that was set, the bar could receive the people sitting down. The arc draws the ends inward so the leftmost and rightmost guests naturally converge — distance between seats, but a sense of gathering, like a round table, not a queue."),
  ("天花板不封板——四套系統留在視線裡，但以設計的方式存在。訂製弧形燈帶的曲線跟吧台半徑一致，管線走向與結構邏輯對齊，系統不是要被藏起來的問題，是可以被設計的材料。整合，是比設計更難的事。",
   "The ceiling stays open — four systems remain in view, but exist by design. The custom arc light follows the bar's radius; pipe routes align with structural logic. Systems are not problems to be hidden — they are materials to be designed. Integration is harder than design."),
  ("吧台檯面選用深色石材，表面不拋光——料理在上面被看見的方式，取決於檯面反射多少光。霧面讓食物安靜地成立，而不是被光搶走。燈光從弧形燈帶均勻落下，色溫偏暖，讓食材的顏色在檯面上被正確地閱讀。",
   "The bar top is dark stone, unpolished — how food is seen depends on how much light the surface reflects. Matte lets the dish exist quietly rather than competing with glare. Light falls evenly from the arc fixture, warm in temperature, so ingredients read true on the surface."),
  ("13坪的限制，最後成了這個空間最清楚的語言。沒有多餘的牆、沒有裝飾性的隔間，每一個元素都在回應同一個問題：怎麼讓六個人在這裡，同時感覺到親密和自在。答案不在面積，在比例。",
   "The 13-ping constraint became the space's clearest language. No extra walls, no decorative partitions — every element answers the same question: how to make six people feel both intimate and at ease. The answer is not in area, but in proportion."),
]}

# ── R. Sanderson (4 sections) ─────────────────────────────────────
TEXTS["commercial/r-sanderson"] = {
 "q":("你不是走進一個空間，你是被引導進去的。",
      "You are not walking into a space — you are being guided in."),
 "s":[
  ("R. Sanderson 的入口刻意內縮。這個縮口不是美學決定，是一個讓身體先於眼睛進場的策略——當你的腳先移動，你的注意力才會跟上。",
   "R. Sanderson's entrance is deliberately compressed. This constriction is not an aesthetic decision — it is a strategy that lets the body enter before the eyes. When your feet move first, your attention follows."),
  ("零售空間最常把所有答案擺在入口，但一眼看完，就不需要移動了；不移動，就沒有更多的慾望。路徑才是零售設計真正的產品。進門後，動線導向三個節點，構成一個內縮的三角環，每次轉向都有一個未曾預期的展示在等著你。",
   "Retail spaces typically place all answers at the entrance, but once everything is seen, movement stops — and without movement, desire cannot accumulate. The path is the real product. Inside, the route leads through three nodes forming an inward triangle; at each turn, an unexpected display waits."),
  ("動線末端是 VIP 試穿區，曲面牆圍塑，尺度稍稍放大，讓人在不自覺間放慢、坐下、停留。空間不是容器，是節奏。決策發生在最放鬆的時刻。",
   "At the end of the path sits the VIP fitting area — curved walls, expanded scale, a place where people slow without knowing why. Space is not a container; it is rhythm. Decisions happen in the most relaxed moment."),
  ("材質從入口到內部逐漸轉暖。外部立面以金屬與玻璃建立理性的第一印象，進入後木質與皮革接手，觸感從冷轉溫。這個轉變不是刻意的風格切換，是動線本身的情緒曲線——從街道的速度，到試穿時的靜止。",
   "Materials warm progressively from entrance to interior. The facade — metal and glass — establishes a rational first impression; inside, wood and leather take over, touch shifting from cool to warm. This transition is not a deliberate style change; it is the emotional curve of the path itself — from the speed of the street to the stillness of trying on."),
]}

# ── 樂樽爐端燒 (4 sections) ───────────────────────────────────────
TEXTS["commercial/lezun"] = {
 "q":("爐端燒的核心是食物和火，每個決定都在清除無關的視覺干擾。",
      "The core of robatayaki is fire and food. Every decision removes visual noise."),
 "s":[
  ("周圍是老公寓、鐵捲門、電線，街道在說很多話。樂樽選擇白色立面。不是風格，是特殊塗料——抗汙、乾淨、帶著界線感。立面不做多餘的事，只讓室內的暖光從大面玻璃透出來，讓人在還沒推門之前，先看見裡面的木構與火光。",
   "The surroundings speak loudly — old apartment blocks, shutters, overhead wires. Lezun chose white. Not as style, but as a material decision: anti-stain, clean, boundary-defining. The facade does nothing extra, only lets warm interior light pass through the glass, so before you push the door, you see wood structure and firelight inside."),
  ("推門之後，色溫轉暖，墨色天花把設備收進背景，視線回到餐檯與料理檯。吧台不選石材，霧沙面特殊漆料降低反光度，讓食物在檯面上安靜地成立。",
   "Inside, the color temperature shifts warm. A dark ceiling absorbs equipment into the background; the eye returns to counter and cooking surface. The bar is not stone — a matte sand-finish coating reduces reflectivity, letting food exist quietly on the surface."),
  ("天花板那組木格柵，發想於「堆、疊」的構造感，燈藏在第二層，光從縫隙透出，陰影有了厚度。",
   "The wooden grille on the ceiling draws from a logic of stacking. Lights hide in the second layer; light passes through the gaps, and shadow gains depth."),
  ("座位安排回應爐端燒「圍著火吃」的本質。吧台座位面向料理檯，讓客人看見食物從火到盤的完整過程。後方座位退開一步，保有觀看的距離但不失參與感。每一個位置都跟火有關係，只是遠近不同。",
   "Seating responds to robatayaki's essence — eating around fire. Bar seats face the cooking station, letting guests witness the full journey from flame to plate. Rear seats step back, keeping a viewing distance without losing participation. Every position relates to the fire; only the distance differs."),
]}

# ── 慕診所 (4 sections) ───────────────────────────────────────────
TEXTS["commercial/mu-clinic"] = {
 "q":("不是讓診所看起來比較美，而是讓走近的人，身體先鬆一點。",
      "Not to make the clinic more beautiful, but to let the approaching person relax first."),
 "s":[
  ("設計主軸圍繞「城市森林」展開：庭院平台上規劃六顆樹木作為核心景觀，森林圖像輸出在玻璃格柵後面。前景的真實綠意與背景抽象化的森林圖像相互呼應，兩個景深疊在一起，製造出一種錯覺：你不是在走進一棟建築，你是在走進一個地方。",
   "The design centers on an urban forest: six trees anchor the courtyard terrace as the primary landscape; a forest image is printed behind the glass grille. Real green in the foreground, abstracted forest in the background — two depths overlapping to create an illusion. You are not walking into a building. You are walking into a place."),
  ("真實的植栽選擇落地種植，不是盆栽。格柵後的森林圖像刻意抽象化——放鬆不來自「像真的自然」，而來自「讓人脫離當下的城市感」。這兩個選擇加在一起，讓庭院的意象超過它實際的尺寸，讓一個過渡空間有了真正的重量。",
   "The real plants are ground-planted, not potted. The forest image behind the grille is deliberately abstracted — relaxation comes not from resembling real nature, but from detaching you from the urban present. Together, these choices make the courtyard's presence exceed its actual size, giving a transitional space real weight."),
  ("庭院是一個緩衝帶，讓進入診所這件事有了節奏。在你推開門之前，你已經在另一個語境裡了。這個設計不是在美化診所，而是在重新設計「走進去之前的那幾秒」。",
   "The courtyard is a buffer zone, giving the act of entering a clinic its own rhythm. Before you push the door, you are already in a different context. This design does not beautify the clinic — it redesigns those few seconds before you walk in."),
  ("這個空間不只是等候區的前奏，它本身就是品牌體驗的一部分——在任何診療發生之前，品牌就已經對你說了一件事：我們在乎你走進來的感受。",
   "This space is not merely a prelude to the waiting room — it is part of the brand experience itself. Before any treatment begins, the brand has already said one thing: we care how you feel walking in."),
]}

# ── 敦化32F (4 sections) ──────────────────────────────────────────
TEXTS["commercial/dunhua-32f"] = {
 "q":("時間壓力讓設計變純粹了——保留的東西，都是真正需要的。",
      "Time pressure made the design pure — what remained was what was truly needed."),
 "s":[
  ("臨時接手，一個月完工。這是一個從一開始就沒有「試試看」空間的案子。在有限時間裡，決策的順序完全改變——你沒辦法先做出來再改，只能先想清楚，讓工廠做完，到現場組裝。",
   "Handed over mid-process, one month to completion. No room to try and revise — only to think clearly, then execute. The decision sequence was inverted: everything resolved in the factory before anything reached the site."),
  ("所有隔屏、鐵件、櫃體全部場外預製，每一段牆體、每一處孔位，在工廠裡就確定尺寸。現場只有一件工作：精準定位，接上配件。",
   "Every partition, steel element, and cabinet was fabricated off-site. Every wall segment, every socket position confirmed in the factory. On-site, one task only: precise positioning, connect the pieces."),
  ("32 樓的視野是這個空間最大的資產。設計的工作不是在室內創造風景，而是把窗外的風景拉進來。傢俱配置、隔屏高度、材質反射率——每一個決定都在確保視線可以不被打斷地抵達窗邊。",
   "The 32nd-floor view is the space's greatest asset. The design task is not to create scenery indoors, but to pull the view in. Furniture layout, partition height, material reflectivity — every decision ensures the eye reaches the window uninterrupted."),
  ("切掉的東西，都是原本可能只是「感覺不錯」的決定。保留的東西，都是真正需要的。時間壓力反而讓這個空間比大部分案子更誠實。",
   "What was cut was what only ever felt like a good idea. What remained was what was truly needed. Time pressure made this space more honest than most."),
]}

# ── ELLE Café (4 sections) ────────────────────────────────────────
TEXTS["commercial/elle-cafe"] = {
 "q":("品牌的個性不只存在於它說了什麼，而在於它選擇用什麼說話。",
      "A brand's identity lives not in what it says, but in what it chooses to say it with."),
 "s":[
  ("黑、灰、桃紅，水泥牆與金屬結構建立理性的底，入口的層層框景讓街景、立面與內部動線在同一條軸線上展開。設計的軸心是可變色的中島吧台——白天白光滲入灰階結構，空間輕盈透明；夜晚燈光轉暗，吧台成為唯一的發光體，桃紅光自內部滲出。同一個空間，在不同時段說兩種語言。",
   "Black, grey, blush pink — concrete walls and metal structure establish a rational base. Layered frames at the entrance align street, facade, and interior along a single axis. The design pivots on a color-shifting central bar: by day, white light enters the grey structure; by night, the bar becomes the only source, glowing blush from within. One space, two languages at different hours."),
  ("入口的層層框景是整個空間最安靜的設計手法，也是最有力的。街景、立面、內部動線被放在同一條軸線上，讓進入成為一個有景深的過程。在你踏進來之前，空間已經開始說話了。",
   "The layered frames at the entrance are the quietest design gesture in the space, and the most powerful. Street, facade, and interior circulation placed on a single axis — entry becomes a process with depth of field. Before you step inside, the space has already begun to speak."),
  ("白天，光從外部滲入，在水泥牆與金屬結構上形成柔和的漫反射，勾勒出材質的層次與紋理。空間保持輕盈，像是一本在自然光下被翻閱的雜誌。夜晚，環境暗下來，中島吧台的桃紅光從內部滲出，整個空間的重心轉移。同一個地方，白天是一種人，夜晚是另一種人。",
   "By day, light seeps in from outside, forming soft diffuse reflections on concrete and metal. The space stays light — a magazine browsed under natural light. At night the ambient dims, blush-pink light bleeds from within the central bar, and the space's center of gravity shifts. Same place, different people by day and night."),
  ("空間中的所有表面都服從於結構。天花的橫樑延伸出節奏感，牆面以塗抹紋理取代裝飾，材質之間保持距離，又在邊界處對話。在秩序中流動的，是品牌的性格，也是生活的節奏。",
   "Every surface defers to structure. Ceiling beams extend into rhythm; walls trade decoration for applied texture; materials keep distance yet converse at the edges. What flows through the order is the brand's character and the rhythm of daily life."),
]}

# ── Fire Play (4 sections) ────────────────────────────────────────
TEXTS["commercial/fire-play"] = {
 "q":("從現實旅程走向奇幻，櫥窗成為空間敘事的第一個轉折。",
      "From real journeys to imagined ones, the window became the first turn in the narrative."),
 "s":[
  ("Fire Play 的第二次改裝，發生在疫情把邊界關起來的那幾年。第一次開幕時，用「旅行」做為主題。當世界忽然按下暫停鍵，我們決定把視線從地表拉到宇宙——太空梭、行星與片段的機械構造，組合成一個帶有科幻感的場景，回應那段「不知道未來在哪裡」的時間感。",
   "Fire Play's second renovation happened during the years the pandemic sealed the borders. The first opening used travel as its theme. When the world hit pause, we pulled the gaze upward — a spacecraft, planets, fragments of mechanical structure assembled into a scene with science-fiction quality, responding to that period of not knowing where the future was."),
  ("重新調整軌道燈與色溫後，吧台與爐火保持明確焦點，其餘區域則壓低亮度，塑造接近電影光的對比。這樣的配置，讓餐盤色彩更被看見，也讓客人坐在吧台前時，能被安穩地包在陰影與光之間。",
   "After recalibrating track lights and color temperature, the bar and open flame hold a clear focus; the rest dims, creating contrast close to cinematic light. This lets the colors on each plate stand out, wrapping guests at the bar in a steady boundary between shadow and light."),
  ("吧台檯面在原有人造石上疊加金屬漆處理。這層金屬感不是亮晶晶的「新」，而是刻意拉出時間感的痕跡，讓整個吧台從平滑的表面，轉為具有厚度的載體，呼應 Fire Play 對「玩火」與「熟成」的堅持。",
   "A metallic paint finish layered over the existing engineered stone. The metallic quality is not the brightness of new — it deliberately pulls out traces of time, turning the bar from a smooth surface into a carrier with depth, echoing Fire Play's commitment to fire and maturation."),
  ("天花與牆面間加入的鐵件結構，像一組壓印在空間裡的標記。這些透空的金屬肢體，在視線高度形成節奏，把吧台區與座位區緊扣在一起。空間改變了，但語法還是同一個。",
   "Steel elements between ceiling and wall act as stamps pressed into the space. These open metal forms create rhythm at eye level, visually locking the bar and seating areas together. The space changed, but the grammar stayed the same."),
]}

# ── Cava Baja (4 sections) ────────────────────────────────────────
TEXTS["commercial/cava-baja"] = {
 "q":("讓人感覺這個地方「已經存在很久了」。",
      "Making a place feel like it has always been here."),
 "s":[
  ("Cava Baja 要做的不是「西班牙風格」，而是那種走進老酒館之後身體自然鬆下來的感受。磚牆、木門、馬賽克吧台、鑄鐵格柵——每個材質都在服務同一件事。庭院作為緩衝區，讓進入成為一個有節奏的過程，而不是直接沖進室內。",
   "Cava Baja is not about Spanish style — it is about the feeling of walking into an old bar and having your body relax without being asked. Brick walls, wooden doors, mosaic bar top, cast-iron grilles — every material serves the same purpose. The courtyard acts as a buffer, giving entrance a rhythm rather than an abrupt arrival."),
  ("磚牆和鑄鐵格柵不是風格選擇，是時間感的建構。讓一個空間看起來「已經存在很久了」，需要的不是仿舊，而是材質本身的厚度。",
   "Brick walls and cast-iron grilles are not a style choice — they are the construction of a sense of time. Making a space feel like it has always been here requires not imitation of age, but the inherent weight of the materials themselves."),
  ("馬賽克吧台是整個空間最具操作力的元素。馬賽克不是展示性的材料，它的解讀方式是觸覺的、跟手指有關的。吧台的高度和寬度放寬，讓人坐下來之後手自然落在台面上。這不是設計細節，是放鬆的序列。",
   "The mosaic bar top is the space's most operative element. Mosaic is not a visual material — it is read by touch, by fingertips. The bar is widened and lowered so when you sit, your hands naturally rest on the surface. This is not a design detail; it is a sequence of relaxation."),
  ("庭院的存在讓進入有了層次。庭院將一步切成兩段：先進來，停一下，再進去。這個停頓讓座位的期待能夠累積，而不是被直接消耗。",
   "The courtyard gives entrance its layers. One step becomes two: enter, pause, then go in. That pause lets anticipation accumulate rather than being spent at once."),
]}

# ── 浪花花藝 (4 sections) ─────────────────────────────────────────
TEXTS["commercial/wave-flower"] = {
 "q":("空間的工作，是讓花浮起來，而不是讓空間好看。",
      "The space exists to make the flowers float, not to make itself beautiful."),
 "s":[
  ("花藝品牌最常見的錯誤，是讓空間本身太有設計感，把花搶掉了。浪花的策略是退場。鋼構格柵天花引入漫射光，牆面以白色為底，室外庭院作為第一個視線落點。進入後的核心是一張石頭桌，花在其上。",
   "The most common mistake in floral retail is making the space too designed — stealing the show from the flowers. Wave Flower's strategy is to disappear. A steel-grid ceiling diffuses light; walls stay white; the courtyard anchors the first line of sight. Inside, a stone table holds the arrangement."),
  ("鋼構格柵天花的設計，不是工業風的選擇，是光的決定。格柵讓自然光在進入室內之前先被打散，落在地面和牆面的光沒有硬邊，像在植物生長的環境裡。花在這樣的光線下，不是被「打亮」的，是自然存在的。",
   "The steel-grid ceiling is not an industrial-style choice — it is a decision about light. The grid scatters natural light before it enters; what reaches floor and wall has no hard edge, like the environment where plants grow. Under this light, flowers simply exist."),
  ("室外庭院是空間序列的第一步。在你走進陳列室之前，你先停在外面，視線落在植物上。這個停頓不是等待，是一個讓身體從街道節奏切換到花藝節奏的過渡帶。",
   "The outdoor courtyard is the first step in the spatial sequence. Before entering the showroom, you pause outside, gaze landing on plants. This pause is not waiting — it is a transition zone shifting the body from street rhythm to floral rhythm."),
  ("石頭桌是整個空間的重心。它的材質有重量感，但表面沒有干擾，花放上去之後，桌子本身就隱退了。這是空間設計最難的一件事：讓一個物件在場，但不搶話。",
   "The stone table is the space's center of gravity. Its material carries weight, but its surface offers no distraction — once flowers are placed, the table recedes. This is the hardest thing in spatial design: making an object present without letting it take over."),
]}

# ── 耘角 (4 sections) ─────────────────────────────────────────────
TEXTS["commercial/yun-jiao"] = {
 "q":("設計師退居其次，讓材質與品牌自身說話。",
      "The designer steps back. Material and brand speak for themselves."),
 "s":[
  ("耘角展示間的核心，不是形體的誇張，而是材質本身的語言。特殊塗料在牆面與立體結構上鋪展，每一道轉角、每一處反射，都是塗料與空間共同書寫的語彙。牆面不再是被動的背景，而成為主角。",
   "The core of Yun Jiao's showroom is not formal exaggeration — it is the language of material itself. Specialty coatings spread across walls and structures; every corner, every reflection is a vocabulary written jointly by coating and space. The wall is no longer background — it is the subject."),
  ("線性的結構框架與大面積留白牆面形成對話。留白不是空缺，而是讓塗料有呼吸的空間。當材質需要被感受，它需要沉默的鄰居，而不是競爭的背景。框架是節奏，留白是停頓，塗料是聲音。",
   "Linear structural frames and large blank walls form a dialogue. The void is not emptiness — it is room for the coating to breathe. When a material needs to be felt, it needs a silent neighbor, not a competing background. The frame is rhythm, the blank is pause, the coating is voice."),
  ("塗料的多樣性在這裡被轉化為場域的表情。冷色與暖色、啞光與亮面，在同一空間裡並陳，不是為了展示產品的種類，而是為了讓訪者親身經歷材質如何因光線而改變。移動，才是展示的媒介。",
   "The diversity of coatings is translated into the expression of the field. Cool and warm, matte and gloss, side by side — not to showcase variety, but to let visitors experience firsthand how material changes with light. Movement is the medium of display."),
  ("家具與光線在這個展示間裡是輔助的語境，不是主角。耘角的設計工作，是持續地把視線推回牆面，推回材質，推回那個問題：你感受到了什麼？",
   "Furniture and light serve as supporting context, not protagonists. Yun Jiao's design work is to continuously push the gaze back to the wall, back to the material, back to the question: what do you feel?"),
]}

# ── 敦南9F (4 sections) ───────────────────────────────────────────
TEXTS["commercial/dunnan-9f"] = {
 "q":("沒有一個選擇是只做一件事的。",
      "No decision was made to do only one thing."),
 "s":[
  ("走進來，百歲磚沒有上漆。從入口到隔間牆，都是它。磚的顏色是磚本來的顏色。",
   "Walk in and the century-old brick is unpainted. From the entrance to the partition walls — its color is its own."),
  ("天花板沒有封板——舊管線太多，日後維修不能再拆一次天花，留著就讓它留著，管線噴上品牌藍，抬頭看見的是公司的顏色。",
   "The ceiling stays open — too many old pipes to tear out again, so they stay, sprayed in the brand's blue. Look up and you see the company's color."),
  ("接待在外，電話亭和會議室在中間，辦公室在最裡面——對外的事在前面解決，工作的人不被打斷。",
   "Reception at the front, phone booths and meeting rooms in the middle, workstations at the back — outward-facing business resolved before it reaches the people who need to focus."),
  ("電話亭用鐵件與玻璃圍塑，不封頂。隔音靠材質的厚度，而不是密閉。這個決定讓電話亭在空間裡保持透明感，不會變成一個跟整體斷開的盒子。每個選擇都同時在回應兩件事：功能，和空間的整體感。",
   "Phone booths are framed in steel and glass, open-topped. Sound isolation relies on material mass, not enclosure. This keeps the booths transparent within the space — they never become boxes disconnected from the whole. Every choice answers two things at once: function, and the coherence of the space."),
]}

# ── 新創視眼鏡 (4 sections) ───────────────────────────────────────
TEXTS["commercial/new-vision"] = {
 "q":("讓眼鏡成為唯一的主角。",
      "Making the eyewear the only subject."),
 "s":[
  ("眼鏡的展示，最常見的錯誤是把商品放進一個太有自己主張的空間。新創視的選材從這個問題出發：水泥粉光、台灣製水磨石、原色橡木皮，三種材質有質感，但沒有聲音。展示邏輯從傳統櫃檯轉向開放式中島，銷售變成一件可以移動、可以靠近的事。",
   "The most common mistake in eyewear retail is placing the product in a space with too strong a voice. New Vision's materials begin from this problem: cement finish, Taiwanese terrazzo, natural oak veneer — texture without personality. Display logic shifts from traditional counters to open islands, making sales something that can move and approach."),
  ("地面預埋的線性光源，沿著空間的輪廓走。這條光不是裝飾，是建築線條的強調——讓空間的邊界在視線高度之外也能被感知。光源藏起來，效果才能站出來。",
   "In-floor linear light traces the spatial outline. This line is not decoration — it emphasizes architectural edges, making boundaries perceptible beyond eye level. The source hides so the effect can stand."),
  ("開放式中島取代傳統玻璃櫃台，改變的不只是陳列方式，而是銷售關係。當商品可以被拿起、被直接觸碰，店員與客人之間的距離從「隔著玻璃」變成「站在同一側」。",
   "Open island units replace glass counters, changing not just display but the sales relationship. When products can be picked up and touched directly, the distance between staff and customer shifts from across the glass to standing on the same side."),
  ("水泥粉光、水磨石、橡木皮——三種選材的共同邏輯是「有性格但不搶話」。它們各自有肌理，但放在一起不互相競爭，讓視線回到商品。選材不是風格決定，是展示策略的延伸。",
   "Cement finish, terrazzo, oak veneer — three materials sharing one logic: character without volume. Each has texture, but together they don't compete, returning the eye to the product. Material selection is not style; it is display strategy."),
]}

# ── 恆隆行 南港LaLaport (4 sections) ──────────────────────────────
TEXTS["commercial/lalaport"] = {
 "q":("以體驗為先，讓示範引出對話、對話轉成成交。",
      "Experience first — demonstration generates conversation, conversation generates conversion."),
 "s":[
  ("在家電量販的場域裡，我們把主要的展演區當作一座「亭」來思考——讓人願意停下、靠近、實際操作，對話才會發生。空間分為三個層次：前場為展演區，中段為展售區，後場為庫存動線。",
   "In a consumer electronics retail environment, we designed the main display as a pavilion — a place where people stop, approach, and actually try. Conversation follows. The space divides into three layers: front for demonstration, middle for browsing and sale, back for inventory flow."),
  ("磚紅色系斜向地坪是整個空間最安靜的設計決定，也是最有力的。斜向鋪排製造了方向性，不需要任何標誌，人流自然被帶向體驗島。顏色是磚紅，不是品牌色，這個選擇讓地坪成為空間的語言。",
   "The diagonally laid brick-red flooring is the quietest design decision, and the most powerful. The diagonal creates directionality — no signage needed; foot traffic naturally flows to the experience island. Brick-red, not any brand color — the floor speaks the space's own language."),
  ("展演工作面一律使用鈦鋼石——乾淨、好清理、低反射，讓操作被看得更清楚。展售區回到黑與白作為中性背景，統一不同品牌的視覺。選材的邏輯只有一個：讓商品站出來，空間退後。",
   "All demonstration surfaces use titanium sintered stone — clean, easy to maintain, low reflectivity, making operations more visible. The sales zone returns to black and white as neutral background. One material logic: products step forward, space steps back."),
  ("上方不做完整天花，改以大面積燈板取代，均勻補光、降低眩光，視線更乾淨。在一個以操作體驗為核心的空間裡，任何搶話的設計都是干擾。燈板退場，商品的細節才能被看見。",
   "Large-format light panels replace a full ceiling — even fill, reduced glare, cleaner visual field. In a space built around hands-on experience, any design that demands attention is interference. The panels recede so product details can be seen."),
]}

# ── Residence H (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-h"] = {
 "q":("留白不是空，是一種比例的安排，讓日常的呼吸被保留下來。",
      "Emptiness here is not absence — it is a proportional arrangement that preserves room to breathe."),
 "s":[
  ("這個案子從衛浴開始。排水移位、糞管納入增厚牆體、壁龕與鏡櫃嵌入牆內——設備退到看不見的地方。公共空間取消了餐桌，讓被功能佔據的區域釋放出來。行走更鬆、停留更長、視線更安定。",
   "This project starts in the bathroom. Drainage relocated, pipes absorbed into thickened walls, niches and mirror cabinets embedded flush — equipment retreated below visibility. In the common areas, the dining table was removed, freeing territory. Movement easier, stays longer, the eye at rest."),
  ("魚缸三面可視，讓玄關的第一眼先讀到透明與深度。石材牆的重點不在弧線，而在厚度怎麼被做出來——界面採凹凸層次的立體轉折，進門後的視線在這裡被導向、被緩衝。",
   "The aquarium is visible from three sides, giving the entrance its first reading of transparency and depth. The stone wall's focus is not its curve but how thickness is achieved — layered three-dimensional folds that guide and buffer the eye upon entry."),
  ("石材牆與木作形成材質的呼應，重與輕、亮與暗在同一個節奏裡被安放。厚度不是裝飾，是結構與比例完成後自然成立的重心。",
   "Stone and woodwork form a material echo — heavy and light, bright and dark, placed within the same rhythm. Thickness is not decoration; it is the center of gravity that emerges once structure and proportion are resolved."),
  ("吧台以折線回應圍聚的需求。它不是一條直線，而是透過折線的展開與回折，讓四個人的面向更自然地靠近。整潔來自結構性的整合——乾淨不是表面極簡，是把複雜提前整理好。",
   "The bar counter responds to gathering with a folded line — not straight, but opening and returning so four people face each other naturally. Neatness comes from structural integration: cleanliness is not surface minimalism but complexity sorted in advance."),
]}

# ── Residence G (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-g"] = {
 "q":("材質不喧嘩，而自成秩序。",
      "Materials that don't announce themselves but form their own order."),
 "s":[
  ("屋主長年旅居歐洲，回台灣後，希望把記憶中的氣質帶回家——講究比例，材質不喧嘩而自成秩序。色調以自調灰綠為主，穿插深木與亮金屬，沉著而不厚重。",
   "The owner had lived in Europe for many years. Returning to Taiwan, the request was to bring back a remembered quality — attention to proportion, materials that form their own order. The palette is self-mixed grey-green, with dark wood and bright metal threaded through — composed without being heavy."),
  ("金屬格柵選鍍鈦與細緻拉絲，光在表面緩慢游移不刺眼。白天窗紗過濾自然光，肌理逐層顯現；夜間間接光勾勒線腳、格柵與琴身的曲線。",
   "The metal grille is titanium-plated with fine brushing — light drifts slowly without glare. By day, sheer curtains filter natural light and textures emerge layer by layer; at night, indirect light traces molding, grille, and the piano's curves."),
  ("局部線腳與轉折採傳統手工貼金箔：先以遮蔽與打底確立邊界，再將金箔一片片貼覆於收邊與陰影交界。反射被壓低，只在邊界留下一道光。這道光不是裝飾，是工藝本身留下的痕跡。",
   "Selected moldings use traditional hand-applied gold leaf — boundaries established by masking and priming, then leaf laid piece by piece at the junction of trim and shadow. Reflection is subdued; only a thread of light remains at the edge. Not ornament — the trace craft leaves behind."),
  ("鋼琴留在臥室裡，不是裝飾，是尺度的參照。一個有年份的物件，會讓新做的東西安靜下來——不是因為對比，而是因為它提供了一個已經存在的重心，讓空間不需要再去尋找自己的位置。",
   "The piano stays in the bedroom — not as decoration, but as a scale reference. An object with history quiets everything new around it, not by contrast but by offering a center of gravity that already exists, so the space need not search for its own."),
]}

# ── Residence S (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-s"] = {
 "q":("一條線，統一所有材質的關係。",
      "One line unifies everything."),
 "s":[
  ("這個案子用一條線統一所有材質的關係。從走道到臥室到浴室，半高切線把每一個材質交界壓在同一基準上——節奏不因轉折而斷。不用單一主材塑造風格，用光澤、觸感與施作方式的對比，讓材料之間自然找到秩序。",
   "One line unifies every material relationship. From corridor to bedroom to bathroom, a half-height datum holds every boundary at the same level — rhythm doesn't break at transitions. No single dominant material sets the style; contrasts in sheen, texture, and application let materials find their own order."),
  ("壁紙的熱帶森林圖像密度高，本身有敘事。礦物塗料在下半段接住它——牆面因此有了上下的呼吸。喧囂和安靜同時在場，也同時被整理好。",
   "The wallpaper's tropical-forest imagery is dense, carrying its own narrative. Mineral paint in the lower half catches it — the wall breathes vertically. Exuberance and quiet coexist, both organized."),
  ("浴室用深綠手工磚包牆，釉面不規則，光在上面形成波動。礦物塗料在下半段延續亮度，浴缸因此成為焦點。低彩度的底，細節卻很豐富。",
   "The bathroom is wrapped in deep-green handmade tile — uneven glaze, light rippling across it. Mineral paint below continues the luminosity; the bathtub becomes the focal point. Low chroma at the base, yet rich in detail."),
  ("水平界線是這個案子最安靜的決定，也是控制力最強的。它不製造焦點，它讓所有材質在同一個基準上共存。每一道轉折都回到同一條線，節奏就不被打斷。",
   "The horizontal datum is the quietest decision and the most controlling. It creates no focal point — it lets every material coexist on the same baseline. Each transition returns to the same line; rhythm never breaks."),
]}

# ── Residence O (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-o"] = {
 "q":("一個門的位置改變，空間的呼吸方式就跟著改變。",
      "One door moved, and the way the space breathes changed with it."),
 "s":[
  ("這是一個雙面採光的實品屋。主臥格局開闊，但門的位置讓空間被侷限了。我們把靠牆的門移到窗側，讓行走路徑圍繞窗邊展開，形成一條新的動線與空間感。",
   "A double-aspect show unit. The master bedroom was generous, but door placement confined the space. We relocated the door from wall to window side, so the path unfolds around the glazing — a new circulation, a new spatial quality."),
  ("動線決定空間被感知的方式。門靠牆，進入主臥之後視線直接被牆面截停。移到窗側，身體移動中感受到的是光，而不是邊界。這個調整不改變任何一個房間的尺寸，卻改變了整個空間的開放感。",
   "Circulation determines how space is perceived. With the door against the wall, the eye hits a dead end. Moved to the window side, what the body registers in motion is light, not boundary. No room dimension changes, yet the sense of openness transforms."),
  ("書牆的燈光用工程手法解決。軌道燈倒裝在層板內，改裝為可滑動的小立燈——光源可以沿著層架移動，不需要額外插座。燈具因此是陳列的一部分，可以跟著書的位置一起移動。",
   "Bookshelf lighting solved with engineering, not decoration. Track lights inverted into shelf boards become sliding mini-lamps — the source travels along the shelving without extra sockets. The fixture is part of the display, moving with the books."),
  ("法國進口壁紙讓牆面保有手感而不失秩序。低飽和的綠灰不是設計師的偏好，是讓家具與物件能在其中自然成立的底色——讓住進去的人帶著自己的生活進來，而不是被空間的風格限定。",
   "French imported wallpaper gives the walls hand-quality without losing order. The low-saturation grey-green is not a preference — it is the backdrop that lets furniture and objects exist naturally, inviting residents to bring their own life in rather than being defined by the space."),
]}

# ── Residence K (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-k"] = {
 "q":("設計從看不見的地方開始。",
      "The design begins in the invisible."),
 "s":[
  ("重新整合排煙與空調的主幹線，結構沿著兩側收整，釋放出空間的高度與節奏。系統被理順之後，光線重新獲得方向，氣流自然流動，空間因此變得純粹。",
   "Exhaust and air conditioning trunk lines reorganized, consolidated along both sides — releasing the space's height and rhythm. Once systems were resolved, light found direction, air moved naturally, and the space became clear."),
  ("半高牆是這個格局最關鍵的決定。它不是在隔間與開放之間找妥協，而是同時對兩件事負責：讓光穿透，同時讓空間感知到自己的邊界。門軌藏進結構，因為看見軌道會讓人意識到空間可以被關起來——這個意識本身就是束縛。",
   "The half-height wall is the most critical decision. It does not compromise between partition and openness — it takes responsibility for both: letting light pass while the space perceives its own boundary. The track is hidden because seeing it makes you aware the space can be closed — that awareness itself is confinement."),
  ("銅紅色的金屬漆不是風格選擇，是邊界的語言。在一個以霧面礦物塗料為主調的浴室裡，銅紅色作為分色的界線，告訴視線哪裡是轉折、哪裡是收束。它的功能更接近建築線腳——不是裝飾，是比例的標記。",
   "The copper-red metallic paint is not a style choice — it is the language of boundary. In a bathroom dominated by matte mineral finish, copper-red serves as a color division, telling the eye where things turn and close. Its function is closer to architectural molding — not decoration, but a marker of proportion."),
  ("進口壁紙讓客廳與臥室有材質的手感和深度。紋理在光影下自己說話——白天一種閱讀，夜間另一種。這是一種安靜的豐富，不依賴視覺衝擊，而依賴材質本身的時間感。",
   "Imported wallpaper gives the living room and bedroom material texture and depth. The pattern speaks under changing light — one reading by day, another by night. A quiet richness dependent not on visual impact but on the material's own sense of time."),
]}

# ── Residence V (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-v"] = {
 "q":("色彩對調——綠放在桌面，金屬光澤留給燈具。",
      "A color inversion — green belongs to the table, metallic sheen to the light."),
 "s":[
  ("公區以弧形沙發界定起居邊界，餐桌形成第二重心，牆線以金屬收邊拉出一條水平視線，統一場域節奏。玄關與重點立面選用「佛羅倫茲」，深淺紋路交織成雲霧般肌理，粗獷的材質被時間研磨，凝成安靜的力量。",
   "A curved sofa defines the living boundary; the dining table anchors a second center of gravity; metal trim pulls a horizontal sightline that unifies the field. The entrance uses Florentz stone — dark and light veins woven into clouded texture, a material once rough, ground by time into quiet force."),
  ("佛羅倫茲的選擇不是為了豪華感，是為了時間感。石材表面的深淺紋路之間，有一種不可被複製的偶然性。半高分色加上極細金屬條，讓牆面在「整體」與「層次」之間保持張力。",
   "Florentz stone is chosen not for luxury but for the sense of time. Between the dark and light veins there is an unrepeatable contingency. Mid-height color split with ultra-fine metal strips keeps the wall in tension between whole and layered."),
  ("翠玉白菜桌面與葉形燈具的關係，是這個空間裡最精細的對話。桌面的綠是石材天然的顏色，燈具的金屬是人工的光澤——放在同一條軸線上，綠與金互相定義了對方的邊界。",
   "The dialogue between the Jade Cabbage table and leaf-form pendant is the finest conversation here. The table's green is stone's natural color; the pendant's metal is artificial sheen — placed on the same axis, green and gold define each other's boundary."),
  ("茶室結合書房，不只是機能的整合，而是一種儀式性的安排。從公共領域走向臥室，這個空間要你先停下來，讓步伐換節奏，讓視線換景。",
   "The tea room combined with the study is not just functional — it is ceremonial. Moving from public to bedroom, this space asks you to pause, shift your pace, change your view."),
]}

# ── Iron Chef (4 sections) ────────────────────────────────────────
TEXTS["commercial/iron-chef"] = {
 "q":("玻璃隔出層次，石材壓住重心，威士忌牆是整個空間的錨點。",
      "Glass creates layers, stone holds the center of gravity, and the whisky wall anchors the entire space."),
 "s":[
  ("入口的紅橘色玻璃隔屏，不是裝飾，是情緒的轉場。從街道走進來，視線先被一層暖色過濾，身體的節奏在這裡被放慢。透過玻璃看見的室內，帶著一層琥珀色的濾鏡——還沒坐下，氣氛已經開始了。",
   "The red-orange glass partition at the entrance is not decoration — it is an emotional transition. Walking in from the street, the eye is filtered through warm color, the body's pace slows. The interior seen through the glass carries an amber cast — the atmosphere begins before you sit."),
  ("威士忌展示牆以黑色鐵件格柵構成，背光均勻打亮每一支酒瓶。展示不是炫耀收藏量，而是讓每一支酒在架上有自己的位置和光線。格柵的節奏感讓牆面從陳列變成空間的立面語言。",
   "The whisky display wall is structured in black steel grille, backlit to illuminate each bottle evenly. Display is not about showing volume — it is about giving every bottle its own position and light. The grille's rhythm turns the wall from a shelf into the space's facade language."),
  ("大理石與深色皮革定義了休息區的重量感。石材選用帶紋路的天然石，不拋光處理，讓表面保留觸覺的溫度。座椅的間距經過計算——足夠私密，但不封閉，讓對話可以發生，也可以不發生。",
   "Marble and dark leather define the lounge's sense of weight. Natural veined stone, unpolished, retains warmth to the touch. Seat spacing is calculated — private enough, but not enclosed, allowing conversation to happen or not."),
  ("山水意象的藝術作品被嵌入玻璃隔間的視線軸上，成為空間的視覺終點。它不是附加的裝飾，而是動線的句點——當你走完這個空間，最後看見的是一幅安靜的風景，讓整個體驗的情緒在這裡收束。",
   "The landscape artwork is embedded along the glass partition's sight axis, becoming the visual terminus. It is not added decoration but the period at the end of circulation — when you finish the space, the last thing you see is a quiet landscape, gathering the experience's emotion to a close."),
]}

# ── Retrodandy (4 sections) ──────────────────────────────────────
TEXTS["commercial/retrodandy"] = {
 "q":("不是做舊，是讓時間住進來。",
      "Not aging artificially — letting time move in."),
 "s":[
  ("Retrodandy 的街角立面用深色木作與手繪金字招牌還原老派紳裝店的語彙。這不是復古風格的模仿，而是對一種已經消失的零售體驗的重建——推門之前，你已經知道這裡賣的不只是衣服。",
   "Retrodandy's corner facade uses dark woodwork and hand-painted gold lettering to reconstruct the vocabulary of an old-world haberdashery. This is not imitation of vintage style — it is the rebuilding of a retail experience that has disappeared. Before you push the door, you already know this place sells more than clothing."),
  ("室內以深色木地板與木作展示架構成主要材質系統。橄欖綠牆面在中段接手，讓視覺有了呼吸。陳列不用現代零售的均質邏輯，而是像老店一樣，每個角落有自己的性格——衣架、書冊、收藏品混在一起，讓人想翻、想碰、想停留。",
   "Inside, dark wood floors and timber display units form the primary material system. Olive-green walls take over midway, giving the eye room to breathe. Display follows not modern retail's uniform logic but the old-shop way — each corner has its own character. Racks, books, and collectibles mingle, making you want to browse, touch, and stay."),
  ("軌道燈從深色天花垂落，光源集中在商品與桌面上，周圍環境退入柔和的暗處。這種打光方式讓每一件商品都像被單獨挑出來展示，而不是淹沒在整片均勻的亮度裡。",
   "Track lights drop from the dark ceiling, concentrating on merchandise and tabletops while the surroundings recede into soft shadow. This lighting makes each product feel individually spotlighted rather than lost in uniform brightness."),
  ("皮沙發與老地毯定義了一個不屬於銷售的區域——一個讓人坐下來的地方。零售空間裡放一張沙發，不是為了舒適，而是為了時間。當客人願意坐下來，停留的時間就不再是他在計算的事。",
   "A leather sofa and vintage rug define a zone that does not belong to selling — a place to sit. Placing a sofa in a retail space is not about comfort; it is about time. When a customer sits down, the length of the stay stops being something they count."),
]}

# ── Residence R (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-r"] = {
 "q":("光與石的對話，定義了這個家的所有表情。",
      "The dialogue between light and stone defines every expression of this home."),
 "s":[
  ("客廳以淺灰皮革沙發與深色木地板建立基調，視線的重心落在餐廳方向——整面背光石材牆成為空間的主角。石材的紋路像夜裡的樹影，光從背後透出，讓一面牆同時擁有重量和透明感。",
   "The living room establishes its tone with light-grey leather and dark wood flooring; the eye's center of gravity falls toward the dining area, where a full backlit stone wall becomes the protagonist. The stone's veining resembles shadows of trees at night — light passing from behind gives the wall both weight and transparency."),
  ("餐桌選用深色石材檯面，與牆面的背光石形成對話。一個是被光穿透的，一個是吸收光的——同樣的材質邏輯，不同的光學表現。燈帶嵌入壁龕，提供間接照明，讓展示物件在柔光中被閱讀。",
   "The dining table's dark stone top dialogues with the backlit wall. One is penetrated by light, the other absorbs it — the same material logic, different optical behavior. LED strips recessed into wall niches provide indirect light, letting displayed objects be read in softness."),
  ("臥室延續公共區域的灰調，但材質轉為織物與壁紙，觸感從硬轉軟。天花板的間接光帶取代了主燈，讓光源從邊緣滲入，整個房間沒有一個明確的光源中心——放鬆，從看不見光源開始。",
   "The bedroom continues the grey tone of the public areas, but materials shift to textiles and wallpaper — touch moves from hard to soft. Indirect light strips replace a central fixture, seeping from the edges. The room has no visible light center — relaxation begins when you cannot see the source."),
  ("這個家的設計語言只有兩個字：石與光。每一個空間都在用不同的方式重述這個主題。客廳是光照亮石，餐廳是光穿透石，臥室是光退到邊緣。同一句話，說了三遍，每次的語氣不同。",
   "This home's design language has only two words: stone and light. Every room restates the theme differently. In the living room, light illuminates stone; in the dining room, light penetrates stone; in the bedroom, light retreats to the edges. The same sentence spoken three times, each with a different tone."),
]}

# ── Residence C (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-c"] = {
 "q":("天花板不是結構的結束，是空間敘事的開始。",
      "The ceiling is not where structure ends — it is where spatial narrative begins."),
 "s":[
  ("這個案子最強烈的手勢是天花板。弧形造型從玄關延伸到公共區域，水泥粉光與石材交接處嵌入燈帶，讓曲面的輪廓在不同角度被光勾勒出來。天花板不再是被動的頂面，而是空間裡最主動的表情。",
   "The strongest gesture here is the ceiling. Curved forms extend from the entrance through the common area; light strips embedded at the junction of cement finish and stone trace the contour from every angle. The ceiling is no longer a passive overhead plane — it is the space's most active expression."),
  ("灰色系的水泥塗料覆蓋了牆面與天花的大部分面積，讓空間保持統一的色調底。深色石材在關鍵位置出現——吧台檯面、玄關落地面——不是為了對比，而是為了給視線一個停靠的重量。",
   "Grey cement coating covers most wall and ceiling surfaces, maintaining a unified tonal base. Dark stone appears at key moments — bar top, entrance flooring — not for contrast, but to give the eye a place to rest with weight."),
  ("弧形不只存在於天花。吧台的邊緣、櫃體的轉角、甚至門框的收邊，都以弧線處理。直角在這個空間裡被系統性地消除——不是為了柔軟的感覺，而是為了讓視線在空間裡移動時不被截斷。",
   "Curves are not limited to the ceiling. The bar's edge, cabinet corners, even door-frame trim — all treated with arcs. Right angles are systematically eliminated, not for softness but so the eye is never interrupted as it moves through the space."),
  ("燈帶是這個家的隱藏主角。它藏在弧形天花的邊緣、石材的接縫、櫃體的底部——從來不直接出現，但它定義了每一個面的輪廓。拿掉燈帶，這些造型就只是造型；有了光，它們才成為空間。",
   "The LED strip is the hidden protagonist. It hides at the edges of curved ceilings, stone joints, cabinet bases — never appearing directly, but defining the contour of every surface. Without the light, these forms are just forms; with light, they become space."),
]}

# ── Residence L (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-l"] = {
 "q":("精確，是這個空間唯一的裝飾。",
      "Precision is the only ornament this space allows."),
 "s":[
  ("整個空間以白色為主體，但白不是單一的——牆面、天花、門片，每一個白都有不同的材質和光澤度。霧面塗料吸收光線，亮面烤漆反射光線，格柵板讓光穿透。同一個顏色，三種說話的方式。",
   "The entire space is white, but not a single white — walls, ceiling, door panels, each a different material and sheen. Matte coating absorbs light, gloss lacquer reflects it, the grille panel lets light pass. One color, three ways of speaking."),
  ("天花板的面板以精密的幾何切割呈現，每一塊面板之間的接縫控制在極窄的溝縫內。弧形轉角處的收邊沒有用矽利康填縫，而是用金屬條精準收口——這個細節決定了整個天花的質感是「精密的」而不是「裝修的」。",
   "Ceiling panels are cut with geometric precision; joints between each panel held to minimal grooves. Curved corners are finished not with silicone but with metal trim — this detail determines whether the ceiling reads as precision or as renovation."),
  ("門片與牆面齊平，把手內嵌。關上門之後，門消失了。這個設計決定讓走道從一系列的「門」變成一個連續的面——視線不會被門框打斷，空間的寬度感因此被放大。",
   "Doors sit flush with walls, handles recessed. When closed, the door disappears. This decision turns the corridor from a series of doors into a continuous surface — the eye is not broken by frames, and the perceived width expands."),
  ("在一個幾乎沒有顏色的空間裡，比例成為唯一的視覺語言。面板的寬高比、溝縫的寬度、弧角的半徑——每一個數字都經過計算。這個家不靠材質的華麗取勝，靠的是每一條線都在它該在的位置。",
   "In a space with almost no color, proportion becomes the only visual language. Panel aspect ratios, groove widths, arc radii — every number calculated. This home does not win with material luxury but with every line in its right place."),
]}

# ── Residence M (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-m"] = {
 "q":("天花板是一條河，空間的節奏跟著它流動。",
      "The ceiling is a river; the space's rhythm flows with it."),
 "s":[
  ("這個案子的天花板不是平面——它是一組連續的弧形曲面，從玄關開始展開，經過客廳，一路延伸到廚房中島上方。曲面的起伏跟著空間機能轉變：在客廳上方稍微抬高，在中島上方壓低，用高度的變化界定區域，而不需要任何隔間。",
   "The ceiling here is not flat — it is a series of continuous curved surfaces unfolding from the entrance through the living room to above the kitchen island. The undulation follows functional shifts: rising slightly over the living area, dipping over the island, defining zones through height rather than partitions."),
  ("中島以深藍色烤漆搭配石材檯面，是整個淺灰空間裡最沉的一筆。這個顏色不是裝飾性的跳色，而是重心——當空間裡大部分的面都在退讓的時候，需要一個元素站出來，讓人知道這裡是廚房的核心。",
   "The island — deep-navy lacquer with stone top — is the heaviest stroke in an otherwise pale-grey space. This color is not a decorative accent but a center of gravity. When most surfaces are receding, one element must step forward to declare itself the kitchen's core."),
  ("礦物塗料與水磨石地坪構成空間的底色。兩種材質都有細微的顆粒感，在不同光線下呈現不同的深淺——白天偏冷，夜間偏暖。這種會隨光線改變的材質，讓空間在一天之內有兩種表情。",
   "Mineral coating and terrazzo flooring form the space's base tone. Both materials carry fine granularity that shifts shade under different light — cooler by day, warmer at night. Materials that change with light give the space two expressions within a single day."),
  ("玄關處的天然石材牆從地面延伸到天花，灰白色紋路在間接光下浮現。黃色單椅與橘色書桌是刻意安排的兩個亮點——在一個以灰階為主的空間裡，色彩的出現需要被控制，少才有效。",
   "Natural stone at the entrance runs floor to ceiling; grey-white veins surface under indirect light. The yellow chair and orange desk are deliberate accents — in a space governed by greyscale, color must be controlled. Less is what makes it work."),
]}

# ── Residence P (4 sections) ──────────────────────────────────────
TEXTS["residential/residence-p"] = {
 "q":("讓舊的東西定義新的空間，而不是反過來。",
      "Letting old objects define the new space, not the other way around."),
 "s":[
  ("這個家的核心收藏是屋主多年蒐集的老件——手工雕花木門、清代屏風、波斯地毯、盆栽。設計的起點不是風格，而是一個問題：怎麼讓這些已經有故事的物件，在一個新空間裡繼續說話？",
   "The heart of this home is the owner's collection gathered over many years — hand-carved wooden doors, Qing dynasty screens, Persian rugs, bonsai. The design starts not from style but from a question: how to let objects that already carry stories continue speaking in a new space?"),
  ("玄關的收納櫃嵌入手工雕花老木門，新做的白色框體退到背景，讓木門的紋路和色澤成為走道的主角。波斯地毯從腳下延伸，把傳統工藝的密度帶進一個現代的平面裡。新與舊的交界不用過渡，直接並置。",
   "Carved antique wooden doors are set into the entrance storage; new white frames recede, letting the wood's grain and patina command the corridor. A Persian rug extends underfoot, carrying the density of traditional craft into a modern plane. No transition between new and old — they are placed side by side."),
  ("客廳以傳統中式屏風作為空間的視覺焦點，藍色布面沙發與紅木傢俱並陳。這個配色不是「中式風格」的公式，而是屋主生活的真實反映——每一件傢俱都有來歷，設計的工作是讓它們在同一個空間裡不打架。",
   "The living room uses a traditional Chinese screen as its visual anchor; blue upholstered sofa and rosewood furniture sit together. This palette is not a Chinese-style formula — it is the true reflection of the owner's life. Every piece of furniture has a provenance; the design work is making them coexist without conflict."),
  ("大理石地面的光澤度與老木件的啞光形成自然的對比。這個對比不是設計師製造的張力，而是時間的差距——新的材料會反光，老的材料吸收光。讓這個差距存在，而不是試圖統一它，才是這個家的設計態度。",
   "The polished marble floor contrasts naturally with the matte patina of antique wood. This contrast is not designed tension — it is the gap of time. New materials reflect; old materials absorb. Letting this gap exist rather than trying to unify it is this home's design attitude."),
]}

# ── Add 5th section to ALL projects ───────────────────────────────
TEXTS["commercial/de-nuit"]["s"].append(
 ("酒與空間的關係，最終是時間的關係。侍酒師的手在吧台上移動，客人的對話在座位間流動，燈光隨著時間推移慢慢改變色溫。de nuit 不是一個靜態的場景，是一個會隨著夜晚深入而逐漸改變的空間。",
  "The relationship between wine and space is ultimately one of time. The sommelier's hands move across the bar, conversation flows between seats, and color temperature shifts as the evening deepens. de nuit is not a static scene — it is a space that evolves as the night goes on."))

TEXTS["commercial/monte"]["s"].append(
 ("在這樣的尺度裡，每一個感官細節都會被放大。料理的香氣在 13 坪裡比在 50 坪裡更強烈，吧台對面的表情比在大餐廳裡更清楚。小，不是限制——小，是一種親密的放大器。",
  "At this scale, every sensory detail is amplified. The aroma of cooking is stronger in 13 pings than in 50; the expression across the bar is clearer than in a large dining room. Small is not a limitation — small is an amplifier of intimacy."))

TEXTS["commercial/r-sanderson"]["s"].append(
 ("整個空間的燈光沒有使用主燈。軌道燈沿著動線方向排列，每一組光源只照亮一個節點的展示。走在路徑上的人不會意識到光在引導自己——這就是好的零售燈光：讓人以為自己是自由移動的，但每一步都在設計裡。",
  "The space uses no main fixture. Track lights align with the circulation path; each group illuminates only one node's display. The person on the path never realizes light is guiding them — this is what good retail lighting does: making people believe they move freely while every step stays within the design."))

TEXTS["commercial/lezun"]["s"].append(
 ("最後一個決定是音量。爐端燒的料理聲——火的聲音、刀的聲音、食材落在鐵板上的聲音——是空間體驗的一部分。吸音材只用在座位區的天花，讓料理區的聲音被保留，座位區的對話被保護。聲音也需要被設計。",
  "The last decision was about sound. The sounds of robatayaki — fire, knife, ingredients hitting iron — are part of the spatial experience. Acoustic absorption is applied only to the ceiling above seating, preserving cooking sounds while protecting conversation. Sound, too, must be designed."))

TEXTS["commercial/mu-clinic"]["s"].append(
 ("從庭院到候診區的地坪使用同一種材質，沒有門檻、沒有高差。這個連續性讓「進入診所」這件事失去了明確的分界——你不是在某一刻「走進醫療空間」，而是在不知不覺間已經在裡面了。焦慮感的降低，從消除邊界開始。",
  "The flooring from courtyard to waiting room uses the same material — no threshold, no level change. This continuity erases the clear boundary of entering a clinic. You do not walk into a medical space at a specific moment; you find yourself already inside. Reducing anxiety starts with dissolving borders."))

TEXTS["commercial/dunhua-32f"]["s"].append(
 ("完工後回頭看，一個月的時間反而讓團隊學到一件事：設計最花時間的部分，往往是猶豫。當猶豫被拿掉，每一個決定都更果斷，空間也因此更乾淨。這不是速度的勝利，是專注力的勝利。",
  "Looking back, the one-month timeline taught the team something: the most time-consuming part of design is often hesitation. When hesitation is removed, every decision becomes more decisive and the space cleaner. This is not a victory of speed — it is a victory of focus."))

TEXTS["commercial/elle-cafe"]["s"].append(
 ("ELLE Café 最後做到的事情是：讓一個品牌的空間不只是品牌的容器，而是品牌本身的延伸。走進來的人不需要看到任何 logo，就已經知道這是 ELLE——因為空間的態度、光線的選擇、材質的比例，都在說同一句話。",
  "What ELLE Café ultimately achieves is making a brand's space not merely a container for the brand, but an extension of the brand itself. No one needs to see a logo to know this is ELLE — the space's attitude, lighting choices, and material proportions all speak the same sentence."))

TEXTS["commercial/fire-play"]["s"].append(
 ("兩次改裝，同一個品牌，不同的故事。第一次是地面上的旅行，第二次是太空的想像。但空間的底層邏輯沒有改變——吧台永遠是核心，火永遠是焦點，客人永遠坐在最好的位置看廚師工作。故事換了，骨架沒有換。",
  "Two renovations, one brand, different stories. The first was earthbound travel; the second, space. But the underlying spatial logic never changed — the bar is always the core, fire always the focus, guests always seated at the best vantage to watch the chef. The story changed; the skeleton did not."))

TEXTS["commercial/iron-chef"]["s"].append(
 ("這個空間要做到的，是讓商務與放鬆同時成立。玻璃隔間讓視線穿透，但聲音被控制在各自的區域裡。你可以在吧台獨飲，也可以在沙發區談事情——兩種狀態在同一個空間裡不互相干擾。這不是複合空間，是同一個空間的兩種閱讀方式。",
  "The space achieves business and relaxation simultaneously. Glass partitions let sight pass through while sound is contained in each zone. You can drink alone at the bar or discuss business in the lounge — two states coexisting without interference. Not a hybrid space, but one space with two ways of reading."))

TEXTS["commercial/cava-baja"]["s"].append(
 ("Cava Baja 最後要回答的問題不是「怎麼做出西班牙風格」，而是「怎麼讓一個新的空間擁有老地方才有的自在」。答案不在裝飾裡，在材質的選擇、座位的間距、光線的溫度——這些加在一起，讓人的身體比腦子更早知道：可以放鬆了。",
  "Cava Baja's final question is not how to create Spanish style but how to give a new space the ease only old places possess. The answer is not in decoration — it is in material choice, seat spacing, light temperature. Together, they let the body know before the mind: you can relax."))

TEXTS["commercial/retrodandy"]["s"].append(
 ("Retrodandy 不是在賣復古，是在賣一種已經不存在的購物體驗——慢的、有溫度的、可以跟店主聊天的。空間設計的工作是讓這種體驗有一個可信的場景。當場景夠真實，故事就不需要解釋。",
  "Retrodandy does not sell vintage — it sells a shopping experience that no longer exists: slow, warm, conversational. The design's job is to give that experience a believable setting. When the setting is real enough, the story needs no explanation."))

TEXTS["commercial/wave-flower"]["s"].append(
 ("花是有時間性的材料——今天和明天看到的不一樣。空間設計必須回應這個特性：不能用固定的展示邏輯去框住一個每天都在變化的主角。石桌、白牆、漫射光——這三個不變的元素，讓花的每一次變化都被好好地承接。",
  "Flowers are a time-based material — today and tomorrow look different. Spatial design must respond to this: a changing protagonist cannot be confined by fixed display logic. Stone table, white wall, diffused light — three constants that properly receive every change the flowers undergo."))

TEXTS["commercial/yun-jiao"]["s"].append(
 ("展示間的成功不在於來的人看了多少產品，而在於他離開之後記得什麼感覺。塗料是一種需要被「感受」而不是被「看見」的材料——當空間讓人慢下來、讓光線有機會在牆面上停留，材質的語言才能被聽見。",
  "A showroom's success is not how many products visitors see but what feeling they carry when they leave. Coating is a material that must be felt, not merely seen — when the space slows people down and gives light a chance to linger on the wall, the material's language can finally be heard."))

TEXTS["commercial/dunnan-9f"]["s"].append(
 ("這個空間用了三種主要材料：百歲磚、品牌藍管線、黑色鐵件。三個選擇都不是風格的選擇——磚是建築本來的，藍是品牌本來的，鐵件是結構本來的。設計的工作不是加東西進來，是讓已經在那裡的東西被看見。",
  "Three primary materials: century-old brick, brand-blue pipes, black steel. None are style choices — the brick belongs to the building, the blue to the brand, the steel to the structure. The design work is not adding things in, but making what is already there visible."))

TEXTS["commercial/new-vision"]["s"].append(
 ("眼鏡的試戴是一個需要鏡子和光線同時配合的行為。中島旁的立鏡角度經過計算，確保試戴時臉部的光線均勻、無陰影。這個細節不會被客人注意到，但他們會覺得「在這裡試戴的時候，鏡子裡的自己看起來比較好看」——這就夠了。",
  "Trying on eyewear requires mirror and light to work together. The standing mirror beside the island is angled so facial lighting is even and shadowless during try-on. Customers will not notice this detail, but they will feel that the person in the mirror looks better here — that is enough."))

TEXTS["commercial/lalaport"]["s"].append(
 ("一個好的展售空間，最後的檢驗標準是：客人願不願意多待五分鐘。不是因為還有東西沒看完，而是因為待在這裡的感覺是好的。磚紅地坪、均勻光板、操作島——這些選擇加在一起，讓一個家電賣場變成一個讓人想留下來的地方。",
  "The final test of a good retail space is whether the customer stays five minutes longer — not because there is more to see, but because being here feels right. Brick-red floor, even light panels, experience island — together they turn an appliance store into a place people want to remain."))

TEXTS["residential/residence-h"]["s"].append(
 ("這個家最安靜的設計，是所有設備的消失。空調出風口藏進天花板的線條裡，開關面板與牆面齊平，插座退到傢俱後方。當技術設備從視線中消失，空間才能真正安靜下來——整潔不是風格，是系統性的整合。",
  "The quietest design in this home is the disappearance of all equipment. Air vents hide within ceiling lines, switch plates sit flush with walls, outlets retreat behind furniture. When technical equipment vanishes from sight, the space can truly be quiet — neatness is not a style; it is systematic integration."))

TEXTS["residential/residence-g"]["s"].append(
 ("這個家不追求某一種風格的完成度，而是追求一種「住過很久」的自在感。新做的櫃體刻意不搶戲，讓屋主帶回來的老件和旅行記憶有足夠的位置。設計的完成，不是交屋那天，是住進去之後，屋主把自己的東西一件件放進來的時候。",
  "This home does not pursue the completeness of any style — it pursues the ease of having lived here a long time. New cabinetry is deliberately understated, leaving room for the owner's antiques and travel memories. The design is not finished on handover day — it is finished when the owner places their belongings, one by one, inside."))

TEXTS["residential/residence-s"]["s"].append(
 ("這個案子最後的完成度，不在於某一個空間的亮點，而在於整體的連貫性。從走道走到臥室、從臥室走到浴室，你不會感覺到「換了一個房間」——你感覺到的是同一首歌的不同樂章，節奏在變，但旋律從未斷過。",
  "The final measure of this project is not any single room's highlight but the coherence of the whole. Walking from corridor to bedroom to bathroom, you never feel you have entered a different room — you feel different movements of the same song. The rhythm changes, but the melody never breaks."))

TEXTS["residential/residence-o"]["s"].append(
 ("實品屋的設計挑戰是：住的人還不存在。你不能為一個特定的人設計，但你可以為一種生活方式設計。這個案子選擇的生活方式是「有閱讀習慣、喜歡自然光、需要安靜的獨處時間」——讓看屋的人走進來，覺得這就是自己想要的日常。",
  "The challenge of a show unit: the resident does not yet exist. You cannot design for a specific person, but you can design for a way of living. This project chose a life of reading habits, natural light, and quiet solitude — so the visitor walks in and feels this is the daily life they want."))

TEXTS["residential/residence-k"]["s"].append(
 ("這個家的設計邏輯是「先整理看不見的，再處理看得見的」。當管線、設備、結構被重新整合之後，空間自然變得乾淨。表面上的極簡不是刻意追求的風格，而是底層整理完之後的自然結果。",
  "The design logic here is to organize the invisible before addressing the visible. Once pipes, equipment, and structure are reintegrated, the space naturally becomes clean. Surface minimalism is not a pursued style — it is the natural result of having sorted out what lies beneath."))

TEXTS["residential/residence-v"]["s"].append(
 ("從玄關的佛羅倫茲到餐桌的翠玉白菜，從葉形燈具到茶室的木作——每一個材質都有自己的重量和時間感。這個家不追求統一，追求的是和聲。不同的聲音，在同一個空間裡，找到彼此可以共存的音調。",
  "From entrance Florentz stone to Jade Cabbage table, from leaf pendant to tearoom woodwork — every material carries its own weight and sense of time. This home does not seek uniformity; it seeks harmony. Different voices, in the same space, finding a pitch at which they can coexist."))

TEXTS["residential/residence-r"]["s"].append(
 ("背光石材的選擇不只是視覺上的決定，也是空間尺度的策略。當一面牆會發光，它就不只是牆——它成為光源的一部分，讓空間的邊界變得模糊。房間因此感覺比實際更大，因為你的眼睛無法精確判斷牆在哪裡結束、光從哪裡開始。",
  "Backlit stone is not just a visual decision — it is a spatial strategy. When a wall emits light, it becomes part of the light source, blurring the space's boundary. The room feels larger than it is because the eye cannot precisely judge where wall ends and light begins."))

TEXTS["residential/residence-c"]["s"].append(
 ("這個家的設計態度是：讓建築語言進入室內。弧形天花、水泥塗料、嵌入式燈帶——這些原本屬於建築尺度的手法，被縮放到住宅的尺度裡。結果是一個不像「裝修」的家——它看起來像是被建造出來的，而不是被裝飾出來的。",
  "The design attitude here is bringing architectural language indoors. Curved ceilings, cement coating, recessed light strips — gestures that belong to architectural scale, rescaled to residential dimensions. The result is a home that does not look decorated — it looks constructed."))

TEXTS["residential/residence-l"]["s"].append(
 ("住進這個家之後，屋主會開始注意到一件事：每一個東西放進來，都很容易找到它的位置。這不是因為收納做得多，而是因為空間的秩序感讓物件自然歸位。當背景夠安靜，前景的每一個選擇都會變得清楚。",
  "After moving in, the owner begins to notice: everything brought in finds its place easily. Not because storage is abundant, but because the space's sense of order lets objects settle naturally. When the background is quiet enough, every choice in the foreground becomes clear."))

TEXTS["residential/residence-m"]["s"].append(
 ("這個家的設計用一條連續的天花曲線，取代了傳統的隔間邏輯。你不會在走動的時候經過門框或感覺到空間的切換——只有天花的高度在變化，光線在跟著轉彎，地坪的材質在腳下安靜地過渡。整個家是一條路徑，不是一組房間。",
  "This home replaces traditional partition logic with one continuous ceiling curve. You never pass through a door frame or feel the space switch — only the ceiling height changes, light turns with it, and the floor transitions quietly underfoot. The entire home is a path, not a set of rooms."))

TEXTS["residential/residence-p"]["s"].append(
 ("這個家最終要說的是：收藏不需要展示廳，它需要的是一個日常。當雕花木門變成收納的門片、波斯地毯變成每天踩過的地面、盆栽在陽台上繼續生長——老件不再是被觀看的物品，而是生活的一部分。這才是收藏最好的歸宿。",
  "What this home ultimately says is: a collection does not need a gallery — it needs a daily life. When carved doors become storage panels, Persian rugs become the floor you walk on every day, and bonsai keep growing on the balcony — antiques are no longer objects to be viewed but part of living. That is the best home a collection can find."))

# ═══════════════════════════════════════════════════════════════════
#  TEMPLATE READING (for meta: title, type, city, hero, plan, nav)
# ═══════════════════════════════════════════════════════════════════

def parse_kv(text):
    data = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("[") or line.startswith("#") or line.startswith("="):
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)", line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data

def load_all_templates():
    templates = {}
    singles = {
        "commercial/de-nuit": os.path.join(TEMPLATE_DIR, "denuit-project_content_template.txt"),
        "commercial/monte": os.path.join(TEMPLATE_DIR, "txt_monte.txt"),
    }
    for folder, path in singles.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                templates[folder] = parse_kv(f.read())
    for fname in ["txt_others.txt", "txt_residential_all.txt"]:
        path = os.path.join(TEMPLATE_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        parts = re.split(r"={5,}\s*(\S+?)-content\.txt\s*={5,}", content)
        for i in range(1, len(parts), 2):
            name = parts[i].strip()
            block = parts[i + 1] if i + 1 < len(parts) else ""
            folder = SECTION_TO_FOLDER.get(name)
            if folder:
                templates[folder] = parse_kv(block)
    return templates

# ═══════════════════════════════════════════════════════════════════
#  IMAGE HANDLING
# ═══════════════════════════════════════════════════════════════════

def get_content_images(folder, hero_path, plan_path):
    project = folder.split("/")[-1]
    img_dir = os.path.join("images", project)
    if not os.path.isdir(img_dir):
        return []
    files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
    skip = set()
    if hero_path:
        skip.add(os.path.basename(hero_path.split("/")[-1]))
    if plan_path:
        skip.add(os.path.basename(plan_path.split("/")[-1]))
    skip.add("00.jpg")
    imgs = []
    for f in files:
        b = os.path.basename(f)
        if b in skip or "plan" in b.lower():
            continue
        imgs.append(f"/images/{project}/{b}")
    return imgs

def img_exists(p):
    return os.path.isfile(p.lstrip("/"))

def rel(p):
    return "../../" + p.lstrip("/")

# ═══════════════════════════════════════════════════════════════════
#  HTML GENERATION
# ═══════════════════════════════════════════════════════════════════

def render_row(layout, imgs):
    cls_map = {"full":"wide","6040":"tall","half":"sq","third":"sq"}
    cls = cls_map.get(layout, "sq")
    cells = "\n".join(
        f'    <div class="mag-cell {cls}"><img src="{img}" loading="lazy" alt=""></div>'
        for img in imgs
    )
    return f'  <div class="mag-row r-{layout}">\n{cells}\n  </div>'


def layout_for_group(imgs_rel, cycle_idx):
    """Given a list of relative image paths, return rows HTML using varied layouts."""
    ROW_CYCLE = ["half", "6040", "full", "third", "half", "full", "6040"]
    ROW_NEED  = {"full":1, "half":2, "6040":2, "third":3}
    rows = ""
    ri, rc = 0, cycle_idx
    while ri < len(imgs_rel):
        lay = ROW_CYCLE[rc % len(ROW_CYCLE)]
        need = ROW_NEED[lay]
        left = len(imgs_rel) - ri
        if left < need:
            lay = "full" if left == 1 else ("half" if left == 2 else "third")
            need = min(left, ROW_NEED[lay])
        chunk = imgs_rel[ri:ri+need]
        rows += "\n" + render_row(lay, chunk)
        ri += need
        rc += 1
    return rows, rc


def build_page(folder, tpl, is_res):
    txt = TEXTS.get(folder, {"q":("",""), "s":[]})
    quote_zh, quote_en = txt["q"]
    sections = txt["s"]
    num_secs = len(sections)

    # Meta
    title = tpl.get("H2_NAME", folder.split("/")[-1])
    type_val = tpl.get("H3_TYPE", "住家空間" if is_res else "空間設計")
    city = tpl.get("H4_CITY", "Taipei, Taiwan").split(",")[0].strip()
    hero_path = tpl.get("H1_IMAGE", f'/images/{folder.split("/")[-1]}/00.jpg')
    hero_src = rel(hero_path)
    hero_full = "https://ondesignlabltd.com/" + hero_path.lstrip("/")

    # Plan
    plan_raw = tpl.get("P1_IMAGE", "")
    if plan_raw and plan_raw != "NONE" and img_exists(plan_raw):
        plan_src = rel(plan_raw)
        plan_class = "plan-section"
    else:
        plan_src = ""
        plan_class = "plan-section hidden"

    # Images
    all_imgs = get_content_images(folder, hero_path, plan_raw)

    # ── Distribute images EVENLY across sections ──
    # e.g. 22 imgs / 5 secs → [5, 5, 4, 4, 4]
    if num_secs > 0 and len(all_imgs) > 0:
        base = len(all_imgs) // num_secs
        extra = len(all_imgs) % num_secs
        counts = [base + (1 if i < extra else 0) for i in range(num_secs)]
    else:
        counts = [0] * max(num_secs, 1)

    # Split images into per-section groups
    sec_imgs = []
    idx = 0
    for c in counts:
        sec_imgs.append([rel(p) for p in all_imgs[idx:idx+c]])
        idx += c

    # Build sections HTML
    sections_html = ""
    cycle_idx = 0
    for i in range(num_secs):
        # Images before text
        if sec_imgs[i]:
            rows, cycle_idx = layout_for_group(sec_imgs[i], cycle_idx)
            sections_html += rows

        # Text break
        zh, en = sections[i]
        num_label = f"0{i+1}" if i < 9 else str(i+1)
        sections_html += f"""
  <div class="text-break">
    <p class="tb-num">{num_label}</p>
    <p class="tb-zh">{zh}</p>
    <p class="tb-en">{en}</p>
  </div>"""

    # Nav
    back_href = "/residential/index.html" if is_res else "/commercial/index.html"
    back_label = "Residential" if is_res else "Commercial"
    prev_name = tpl.get("N1_PREV_NAME", "")
    prev_path = tpl.get("N1_PREV_PATH", "")
    next_name = tpl.get("N2_NEXT_NAME", "")
    next_path = tpl.get("N2_NEXT_PATH", "")
    prev_link = f'<a href="{prev_path}">&larr; {prev_name}</a>' if prev_path else "<span></span>"
    next_link = f'<a href="{next_path}">{next_name} &rarr;</a>' if next_path else "<span></span>"

    desc = f"{title} {type_val} | ON Design Lab"

    # Quote HTML (handle line breaks)
    q_zh = quote_zh.replace("\\n", "<br>")

    # Thumb strip
    thumb_html = ""
    for img_path in all_imgs:
        thumb_html += f'    <div class="thumb"><img loading="lazy" src="{rel(img_path)}" alt=""></div>\n'

    plan_block = ""
    if plan_class == "plan-section":
        plan_block = f"""
  <!-- PLAN -->
  <div class="plan-section">
    <p class="plan-eyebrow">Floor Plan</p>
    <img src="{plan_src}" loading="lazy" alt="Floor Plan">
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &mdash; ON Design Lab</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} &mdash; ON Design Lab">
<meta property="og:image" content="{hero_full}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--black:#0a0a0a;--white:#fafaf8;--dim:rgba(255,255,255,.07)}}
html,body{{background:var(--black);color:var(--white);font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}}
a{{color:inherit;text-decoration:none}}

nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:1.5rem 2.5rem;background:rgba(10,10,10,.88);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.06)}}
nav .logo{{font-size:12px;letter-spacing:.18em}}
nav ul{{list-style:none;display:flex;gap:2.5rem}}
nav ul li a{{font-size:11px;letter-spacing:.12em;opacity:.4;transition:opacity .2s}}
nav ul li a:hover{{opacity:1}}

.hero{{position:relative;width:100%;height:100vh;overflow:hidden;display:flex;align-items:flex-end}}
.hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.55)}}
.hero-caption{{position:relative;z-index:2;padding:3rem 2.5rem;width:100%;border-top:1px solid rgba(255,255,255,.1)}}
.hero-title{{font-size:clamp(2.5rem,7vw,6rem);font-weight:200;letter-spacing:-.02em;line-height:.95;margin-bottom:.6rem}}
.hero-tags{{font-size:11px;letter-spacing:.12em;opacity:.35}}

.content{{max-width:1100px;margin:0 auto}}
.intro{{max-width:720px;padding:5rem 2.5rem;border-bottom:1px solid var(--dim)}}
.intro-zh{{font-size:16px;line-height:2.05;opacity:.75;margin-bottom:2.5rem}}
.intro-en{{font-size:13px;line-height:1.95;opacity:.28;font-style:italic}}

.plan-section{{padding:4rem 2.5rem;border-bottom:1px solid var(--dim)}}
.plan-section.hidden{{display:none}}
.plan-eyebrow{{font-size:9px;letter-spacing:.22em;opacity:.22;text-transform:uppercase;margin-bottom:2rem}}
.plan-section img{{width:100%;display:block;filter:brightness(.85);cursor:zoom-in}}
.plan-section img:hover{{filter:brightness(1)}}

.mag-row{{display:grid;gap:1px;background:var(--dim);border-bottom:1px solid var(--dim)}}
.mag-row.r-full{{grid-template-columns:1fr}}
.mag-row.r-6040{{grid-template-columns:6fr 4fr}}
.mag-row.r-half{{grid-template-columns:1fr 1fr}}
.mag-row.r-third{{grid-template-columns:1fr 1fr 1fr}}
@media(max-width:600px){{.mag-row.r-6040,.mag-row.r-half,.mag-row.r-third{{grid-template-columns:1fr}}}}
.mag-cell{{background:var(--black);overflow:hidden}}
.mag-cell img{{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.82);transition:filter .4s,transform .55s;cursor:zoom-in}}
.mag-cell:hover img{{filter:brightness(1);transform:scale(1.03)}}
.mag-cell.tall{{aspect-ratio:3/4}}
.mag-cell.wide{{aspect-ratio:16/9}}
.mag-cell.sq{{aspect-ratio:1}}

.text-break{{max-width:720px;padding:4rem 2.5rem;border-bottom:1px solid var(--dim)}}
.tb-num{{font-size:9px;letter-spacing:.2em;opacity:.2;text-transform:uppercase;margin-bottom:1.5rem}}
.tb-zh{{font-size:14px;line-height:2.05;opacity:.68;margin-bottom:1.8rem}}
.tb-en{{font-size:12px;line-height:1.95;opacity:.27;font-style:italic}}

.proj-nav{{display:flex;justify-content:space-between;align-items:center;padding:2.5rem;border-top:1px solid var(--dim)}}
.proj-nav a{{font-size:11px;letter-spacing:.1em;opacity:.3;transition:opacity .2s}}
.proj-nav a:hover{{opacity:.9}}
.proj-nav .back{{font-size:10px;letter-spacing:.15em;opacity:.2}}

#lb{{display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,.95);align-items:center;justify-content:center}}
#lb.open{{display:flex}}
#lb img{{max-width:92vw;max-height:90vh;object-fit:contain}}
#lb-close{{position:absolute;top:1.5rem;right:2rem;font-size:22px;opacity:.4;cursor:pointer;background:none;border:none;color:var(--white)}}
#lb-close:hover{{opacity:1}}
#lb-prev,#lb-next{{position:absolute;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--white);font-size:2rem;opacity:.25;cursor:pointer;padding:1rem;transition:opacity .2s}}
#lb-prev:hover,#lb-next:hover{{opacity:.9}}
#lb-prev{{left:.5rem}}
#lb-next{{right:.5rem}}
#lb-counter{{position:absolute;bottom:1.5rem;left:50%;transform:translateX(-50%);font-size:10px;opacity:.3;letter-spacing:.1em}}

.thumb-label{{font-size:9px;letter-spacing:.22em;opacity:.22;text-transform:uppercase;padding:2.5rem 2.5rem 1rem;max-width:1100px;margin:0 auto}}
.thumb-strip{{display:flex;gap:2px;overflow-x:auto;padding:0 2.5rem 2rem;max-width:1100px;margin:0 auto;scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.15) transparent}}
.thumb-strip::-webkit-scrollbar{{height:4px}}
.thumb-strip::-webkit-scrollbar-track{{background:transparent}}
.thumb-strip::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.15);border-radius:2px}}
.thumb{{flex:0 0 auto;width:100px;height:68px;overflow:hidden;cursor:zoom-in;opacity:.5;transition:opacity .3s}}
.thumb:hover{{opacity:1}}
.thumb img{{width:100%;height:100%;object-fit:cover;display:block}}
</style>
</head>
<body>

<nav>
  <a href="/index.html" class="logo">ON DESIGN LAB</a>
  <ul>
    <li><a href="/commercial/index.html">Commercial</a></li>
    <li><a href="/residential/index.html">Residential</a></li>
    <li><a href="/info/index.html">Info</a></li>
  </ul>
</nav>

<div class="hero">
  <img src="{hero_src}" fetchpriority="high" loading="eager" decoding="async" alt="{title}">
  <div class="hero-caption">
    <h1 class="hero-title">{title}</h1>
    <p class="hero-tags">{type_val} &middot; {city}</p>
  </div>
</div>

<div class="content">

  <div class="intro">
    <p class="intro-zh">{q_zh}</p>
    <p class="intro-en">{quote_en}</p>
  </div>
{plan_block}

{sections_html}

  <p class="thumb-label">All Photos</p>
  <div class="thumb-strip">
{thumb_html}  </div>

  <div class="proj-nav">
    {prev_link}
    <a href="{back_href}" class="back">{back_label}</a>
    {next_link}
  </div>

</div>

<div id="lb">
  <button id="lb-close">&#10005;</button>
  <button id="lb-prev">&#8249;</button>
  <img id="lb-img" src="" alt="">
  <button id="lb-next">&#8250;</button>
  <span id="lb-counter"></span>
</div>
<script>
(function(){{
  var imgs=[].slice.call(document.querySelectorAll('.mag-cell img, .plan-section:not(.hidden) img'));
  var srcs=imgs.map(function(i){{return i.src}});
  var lb=document.getElementById('lb');
  var lbImg=document.getElementById('lb-img');
  var lbC=document.getElementById('lb-counter');
  var cur=0;
  function show(i){{cur=i;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;lb.classList.add('open')}}
  function close(){{lb.classList.remove('open');lbImg.src=''}}
  imgs.forEach(function(img,i){{img.addEventListener('click',function(){{show(i)}})}});
  [].slice.call(document.querySelectorAll('.thumb-strip .thumb')).forEach(function(t){{
    t.addEventListener('click',function(){{
      var s=t.querySelector('img').src;
      var i=srcs.findIndex(function(x){{return x===s}});
      if(i>=0)show(i);else{{srcs.push(s);show(srcs.length-1)}}
    }});
  }});
  document.getElementById('lb-close').onclick=close;
  document.getElementById('lb-prev').onclick=function(){{cur=(cur-1+srcs.length)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length}};
  document.getElementById('lb-next').onclick=function(){{cur=(cur+1)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length}};
  lb.addEventListener('click',function(e){{if(e.target===lb)close()}});
  document.addEventListener('keydown',function(e){{
    if(!lb.classList.contains('open'))return;
    if(e.key==='ArrowLeft')document.getElementById('lb-prev').click();
    if(e.key==='ArrowRight')document.getElementById('lb-next').click();
    if(e.key==='Escape')close();
  }});
}})();
</script>

</body>
</html>"""

    return html, num_secs


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    templates = load_all_templates()
    print(f"Loaded {len(templates)} templates\n")

    all_projects = [(f, False) for f in COMMERCIAL] + [(f, True) for f in RESIDENTIAL]
    empty_pages = []

    for folder, is_res in all_projects:
        path = os.path.join(folder, "index.html")
        if not os.path.exists(path):
            print(f"[SKIP] {folder} - no index.html")
            continue

        tpl = templates.get(folder)
        if not tpl:
            print(f"[SKIP] {folder} - no template")
            continue

        backup = path.replace("index.html", "index_backup.html")
        if not os.path.exists(backup):
            shutil.copy(path, backup)

        try:
            html, num_secs = build_page(folder, tpl, is_res)
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

            img_count = html.count('class="mag-cell')
            if num_secs == 0:
                empty_pages.append(folder)
                print(f"[OK-EMPTY] {folder} ({img_count} imgs, 0 sections)")
            else:
                print(f"[OK] {folder} ({img_count} imgs, {num_secs} sections)")

        except Exception as e:
            print(f"[ERR] {folder} - {e}")
            import traceback
            traceback.print_exc()
            if os.path.exists(backup):
                shutil.copy(backup, path)

    print(f"\n--- Done: {len(all_projects)} projects ---")
    if empty_pages:
        print(f"\nEmpty (no copy yet):")
        for p in empty_pages:
            print(f"  {p}")


if __name__ == "__main__":
    main()
