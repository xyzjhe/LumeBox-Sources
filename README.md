# LumeBox 源仓库

订阅入口统一放在 `subscriptions/`，分类与分级数据放在 `metadata/`。根目录只保留说明和各功能目录。

订阅格式：总入口是 JSON，分类 TXT 文件列出 JS / Python 脚本地址；TXT 本身是地址清单。实际源文件为 `.js` 或 `.py`，由 App 按运行时标记加载。HTML 网页放在 `web/`，需从网页主页导入，不混入脚本订阅。

## 一次导入

- [国内 CDN 线路](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/all.json)
- [GitHub 原站线路](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/all.json)

在 APP 的“总订阅导入导出”中选择线路或粘贴链接。国内 CDN 线路的清单和脚本都走 CDN；能否直连取决于当前网络，更新可能有 CDN 缓存延迟。两条线路内容相同，选择一条即可。

## PY 合集

用户提供的 PY 合集已去重入库，并作为独立清单接入上方总订阅。也可仅导入 [PY 原站订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/python.json) 或 [PY 国内 CDN 订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/python.json)。当前纳入的 PY 源通过离线宿主加载；未逐站保证播放。13 份加载失败脚本保存在 archive/python，不进入订阅；本地管理工具与示例排除。详见 [合集记录](docs/PY合集入库.md)。

## 按需分类

| 分类 | 独立源数 | 原站 | 国内 CDN |
| --- | ---: | --- | --- |
| 漫画 | 52 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/comic.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/comic.txt) |
| 美图 | 5 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/photo.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/photo.txt) |
| 影视 | 34 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/movie.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/movie.txt) |
| 视频与直播 | 128 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/video.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/video.txt) |
| 有声小说 | 7 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/audiobook.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/audiobook.txt) |
| 文字小说 | 0 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/novel.txt) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/novel.txt) |
| PY 合集 | 83 | [订阅](https://raw.githubusercontent.com/teng662858/LumeBox-Sources/main/subscriptions/python.json) | [订阅](https://cdn.jsdelivr.net/gh/teng662858/LumeBox-Sources@main/subscriptions/cdn/python.json) |

共 **309 个独立源**，同 ID 不重复收录。漫画、美图、文字小说、有声导入 APP 漫画板块；影视、视频导入视频板块。

## 2026-11-03 懂片帝（video/懂片帝.js）

`dongpiandi.ai`（懂片帝AI：AI 找片 + 片单 + 播放）是聚合前端，自己不存片：把各家聚合资源站
（红牛 / 新浪 / 极速 / 豪华 / ikun / 魔都 / 西瓜…）与官方 CDN 的线路编到同一部作品上。
形态是 React SPA + 同源 `/v1/*` JSON 接口，首页 HTML 只有 4 KB。

- **每个请求都要 HMAC-SHA256 签名**：`x-ai-movie-timestamp`（毫秒）、`x-ai-movie-nonce`（16 字节 hex）、
  `x-ai-movie-signature = HMAC(SIGN_KEY, "METHOD\npath?query\nts\nnonce")`。实测只校验这三个头，
  客户端版本号之类的随便填也能过，所以站点换前端版本不影响本源；换 key 时把新
  `main-*.js` 里的 `Jo="…"` 抄进源即可。源里优先用宿主原生 `tools.hmac`，失败退回纯 JS，
  并按响应 `Date` 对设备时钟偏差做一次校正重试。
- 接口：`/v1/feed/home`（首页板块）、`/v1/browse/catalog`（`q`/`kind`/`genre`/`area`/`language`/
  `year`/`sort`/`hot_list_key`/`page`/`limit≤20`）、`/v1/runtime/bootstrap`（分类与筛选表）、
  `/v1/catalog/{id}`（详情 + `episodes[].token`）、`/v1/playback/resolve/{token}`（线路表）、
  `POST /v1/playback/resolve-line`（票券换址）。
- 分类 id 直接用站点查询串（`kind=movie`、`sort=trending&window=day`、`hot_list_key=tv_korean`…），
  首页板块的「更多」由 `section.browse.params` 转成同一套编码，点进去就是普通列表分页。
- 分类 / 筛选 / 排序（v1.3.0 补全，17 个分类全部出内容、15 个首条唯一）：
  - kind 分类显式带 `sort=heat_desc`（bootstrap 的 `default_sort`）；实测「不带 sort」站点按最新出，
    不显式给就和「最近更新」撞首屏。筛选里的「排序」能覆盖（实测《空枪》→ 选「最新」变《半山腰的索玛花》）。
  - 筛选组：bootstrap 5 个 kind 走 `catalog_ui`；**documentary / sports 在 bootstrap 里没有，
    但参数照样生效**，补本地表（genre 从片库反查）；`all` 与两个热播分类给通用组（实测「不带 kind」
    时 area/year/genre 也生效）；7 个榜单不给组（实测榜单丢附加参数：`hot_list_key + area` 的 area
    不生效、`+ sort` 反而把榜单顶掉）。
  - **多选只有地区支持**：`area=中国大陆,中国香港` 混出两地；`genre=喜剧,爱情`、`language=国语,粤语`
    都回 0 条，所以只对 area 做逗号拼接。
  - 没有的维度（实测静默忽略）：`rating_gte`/`score_gte`/`duration_lte`/`is_finished`/`status`/
    `free`/`playable_only`/`actor`/`channel`/`region`/`lang`；短剧「状态」「形式」站点自标 `enabled:false`。
- 播放默认走第三方直链（`resolve_mode:"direct"` 的 m3u8/mp4，免费不扣额度），官方
  `resolve://` 票券线路只在直链一条都没有时兜底。**不逐条探活**：32 条线路里总有一两条
  CDN 已挂、要等宿主 6 秒超时，串行探活会把 `content` 拖到 16 秒被判超时；改成按
  「站点权重 + 资源站实测稳定性」排序后直接给地址，前 5 条进 `qualities` 供切换。
- 实测：`content` 213–899 ms、直链 206 + `#EXTM3U`；真 QuickJS 沙箱里签名头与 Dart 侧 HMAC 逐字一致。
- **v1.4.0 午夜剧场接成第 18 个分类**（`midnight`）：走 `discovery → play → timeline`，
  `chapters()` 把 `timeline.segments` 展开成章节、`content()` 按段取 `media_sources[].url`，
  `play` 缓存 10 分钟避免重复扣词元。**请求侧实测打通**：`play_request_id` 必须标准 UUID v4
  （纯随机 hex 回 `400 Invalid UUID`；改成 8-4-4-12、第三段首字符 `4`、第四段 `8/9/a/b` 后，
  `random/play`、`top/play`、`playlists/{id}/play` 三个都从 400 变 403 资格拦截，说明 body 被接受）。
  **响应结构还没有真实样本**（账号练气1层 `access`/`discovery`/`play` 全 403
  `midnight_theater_not_eligible`），结构取自 `/assets/MidnightTheaterRoute-*.js` 的消费代码，
  解析防御式；没资格时分类会明确回报原因，不静默返回空。
- **v1.1.0 账号（可选）+ 线路偏好**：用真实账号实测过 —— **不填账号也能用全部片库**，登录前后
  线路表逐条一致（34 条：25 直链 + 9 官方票券），连「新4K-限时等级专属」「4K海外-官方C」
  匿名换也返回 201 + 真地址；登录只多出站内那套（`/v1/users/me/quota` 每日词元、收藏、历史、
  午夜剧场且要先确认 18+）。所以账号做成可选：`POST /v1/users/password/login`（字段名是
  `account` 不是 `username`，登录不要验证码，注册才要），会话取 `ai_movie_session=ums2_…`
  （同一条响应里还有几个 `Max-Age=0` 的空 cookie，必须按 `ums2_` 前缀取）存 `fs` 复用，
  401 重登一次，密码错只写 30 分钟 TTL 的 `login_fail.json` 不阻塞播放。另加 `lineMode`
  （直链优先 / 官方优先）与设置页动作「检查账号与额度」「退出站点登录」——前者实测输出
  `账号：teng233（林间小太阳2017）／等级：练气1层（member）／今日词元：已用 0 / 上限 100 万`。
- **v1.2.0：午夜剧场没接**（有实测依据）。它是「AI 现生成今晚片单」而不是片库：
  `POST /v1/midnight-theater/playlists`（前端超时 45 秒）→ 轮询 `/generations/{id}` →
  `POST .../playlists/{id}/play` → 再进 `/v1/playback`，每次按次扣大量词元。而且**这个账号没资格**：
  走完站点自己的成年确认（`PUT /v1/users/me/preferences {"adult_confirmed":true}` → 200 带
  `adult_confirmed_at`）后，`GET /v1/midnight-theater/access` 仍回
  `403 {"code":"midnight_theater_not_eligible","message":"当前账号暂不符合开放条件"}`，
  `discovery` 同 403、`eligibility` 是 `{eligible:false}`。没资格就拿不到可验证的响应结构，
  按写源规则不猜。所以只加两个能验证的动作：「确认已满 18 岁（站点账号）」「查午夜剧场资格」。
  同时修了线路选择：头几条偶尔是 403/404 的资源站（`dytt-tvs` 403、`bfeng11` 404），
  现在单条探活 1 秒、总预算 2.2 秒、命中即停，全不通转票券，`content` 仍在 2.5 秒内。

## 2026-11-03 爱丽丝书屋（comic/爱丽丝书屋.js）

`alicesw.com` 成人网络小说站（全站 18+，diyquge 模板的静态 HTML，无接口无加密）。本源按**文字小说**交付：
列表/详情声明 `mediaType:"novel"`，正文返回 `kind:"text"`，App 归入漫画板块的「小说」分类并打开文字阅读器。

- 结构：题材分类 `/lists/{id}.html?page=N`、总列表 `/all/order/{排序}+desc.html?page=N`、
  题材+排序 `/all/id/{id}/order/{排序}+desc.html`、原创专区 `/original.html`、
  排行 `/other/rank_hits/order/hits_day|hits_week|hits_month|hits.html`（单页 30 条、不分页）、
  搜索 `/search.html?q={词}&f=_all&sort=relevance&p=N`（10 条/页）、详情 `/novel/{id}.html`、
  目录 `/other/chapters/id/{id}.html`（**一次给全**，实测 6972 章 / 666 KB 单页）、
  正文 `/book/{书号}/{章节hash}.html`。
- 注意 `/novel/{id}` 与 `/book/{书号}` 的编号**不是同一个**，章节地址只能从目录页取。
- 35 个分类（最近更新 / 四个排行 / 原创专区 / 29 个题材）+ 排序筛选（最近更新 / 人气最高 / 字数最多）；
  排行与原创专区走站点固定路径，排序对它们不生效。
- 发布页 `alicesw.click`（另有 `www.asw5.cc`）写进源设置；镜像 `alicesw.com`（海外主站）、
  `alicesw1.homes`（大陆备用，简体同源）、`alicesw.tw`（繁体站，结构一致）。发布页给出的
  `alicesw.quest` 只是另一个发布页（没有正文）。源站按 IP 拒美国 Utah，源标注 `network:"proxy"`。
- **1.1.0 列表封面**：站点列表页没有封面，源里按 id 并发抓详情页取 `.imgbox img`
  （32 并发、单请求 1500ms 超时、列表 2400ms / 首页 3200ms 预算），封面 URL 用 `LumeSource.fs`
  缓存 12 小时、最多 380 条。冷启动 `list()` 2.5s 覆盖 31/31，缓存命中 0.78s；`home()` 2.7s 覆盖 34/48。
- 验证：`node tools/lume-source-check.mjs sources/comic/alicesw.js` → PASS
  （home 6 板块 34/48 有封面 / list 31 条 31/31 有封面 / detail 封面+标签 / chapters 8 / content 13693 字正文约 390ms）。

## 2026-11-01 漫蛙 v2.0.0（comic/漫蛙.js）

原源打 `manwa.me`，整站 403「Just a moment…」（Cloudflare），App 里打开是空白；`/book/<id>`、`/booklist?gender=` 这些老路径也已不存在。
本版换到实测可用的 **manwa2.com**，并把章节正文的加密解开了：

- 详情 `/comic/<数字>`、章节 `/chapter/<漫画>/<话>`、正文在章节页 `var params='<base64>'` 里，
  AES-128-CBC（key `9S8$vJnU2ANeSRoF`）解出 `{"images":[…80 张…]}`；明文前 16 字节是随机填充，
  按 16 字节块边界试 JSON.parse；图片本身是明文 webp（旧版那层 `my2ecret782ecret` 图片加密已不需要）。
- **镜像自动切换**：`H.get` 先用手选/默认域名，403 / 非 200 / 连不上就换下一个（manwa2.com ↔ manwa.me），成功即记住。
- 实测：manwa2.com 可用；manwa.me 官方域名有 Cloudflare（留作手选）；manwa3/4/5、manwa1/7/9 全 302 到
  `gotowww.aipages.dev` 广告页（已废）；manwa2.top / manwa360.cc 只是导航壳（1.2 KB SPA）。
- 验证：`node tools/lume-source-check.mjs` → PASS（home 12 / list 40 / chapters 21 / content 80 张图 / 首图 200 webp）；
  镜像切换单测：domain 指到 manwa.me（403）→ 自动落到 manwa2.com 拿到 30 条。

## 仓库目录

| 目录 | 内容 |
| --- | --- |
| `subscriptions/` | 所有订阅入口；`cdn/` 是国内 CDN 线路；`legacy/` 为迁移用旧子集 |
| `metadata/` | 唯一源目录、18+ 分级与旧地址迁移表 |
| `comic/`、`photo/` | 漫画、美图源脚本 |
| `movie/`、`video/`、`audiobook/` | 影视、视频、有声源脚本，分别存放 |
| `web/` | 可下载导入的 HTML 网页主页（不进入脚本订阅） |
| `docs/` | 使用与维护说明 |
| `tools/`、`snapshots/`、`licenses/` | 工具、回归样本、授权 |

[完整源目录](docs/源目录.md) · [地址迁移说明](docs/源分类与兼容地址.md) · [维护说明](docs/README.md)

旧根目录订阅文件已收起，需要配套新版 APP 自动迁移旧地址，或使用上方新入口。18+ 是内容分级；未分级不代表全年龄。目录整理与离线检查不代表所有封面、图标和播放当前可用。
