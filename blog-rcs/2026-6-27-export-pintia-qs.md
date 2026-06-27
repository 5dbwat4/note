---
title: 从pintia中提取题目
---

Paste the code to devtools to start fetch and download:**【THIS CODE IS WORKING, VERIFIED】**

```js
/**
 * Pintia (PTA) Problem Crawler - Run in browser DevTools console.
 *
 * Crawls all problem sets and their quiz-type problems, marking correct
 * answers for ACCEPTED problems. Downloads result as JSON.
 *
 * Usage:
 *   1. Log in to https://pintia.cn
 *   2. Open DevTools (F12) → Console
 *   3. Paste this entire script and press Enter
 *   4. Wait for download to trigger
 *
 * Configurable constants below.
 */

const CONFIG = {
  /** Delay between API calls (ms) - increase if getting 429 errors */
  DELAY: 500,
  /** Max problem sets to crawl (null = all) */
  MAX_SETS: null,
  /** Fetch all problem sets (true) or only active (false) */
  ALL_SETS: true,
  /** Sort order for problem sets: END_AT (default), CREATE_AT, UPDATE_AT, START_AT */
  ORDER_BY: "END_AT",
  /** Ascending order (true = oldest first) */
  ASC: false,
  /** Max retries on 429 rate limit */
  MAX_RETRIES: 3,
  /** Backoff multiplier for 429 (ms) */
  RETRY_BACKOFF: 2000,
  /** Save intermediate progress every N sets (0 = disabled) */
  SAVE_EVERY: 20,
  /** Problem types for which we should extract correct answers */
  ANSWERABLE_TYPES: [
    "TRUE_OR_FALSE",
    "MULTIPLE_CHOICE",
    "FILL_IN_THE_BLANK_FOR_PROGRAMMING",
    "CODE_COMPLETION",
  ],
  /** Problem types to skip entirely */
  SKIP_TYPES: [],
};

const BASE_URL = "https://pintia.cn/api";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function apiGet(path, params = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= CONFIG.MAX_RETRIES; attempt++) {
    const qs = new URLSearchParams(params).toString();
    const url = `${BASE_URL}${path}${qs ? "?" + qs : ""}`;
    const resp = await fetch(url, {
      headers: {
        accept: "application/json;charset=UTF-8",
        "content-type": "application/json;charset=UTF-8",
        "x-lollipop": localStorage["pta-lollipop"] || "",
      },
      credentials: "include",
    });
    if (resp.ok) return resp.json();
    lastErr = new Error(`${resp.status} ${resp.statusText} on ${path}`);
    if (resp.status === 429 && attempt < CONFIG.MAX_RETRIES) {
      const wait = CONFIG.RETRY_BACKOFF * (attempt + 1);
      console.warn(`  Rate limited (429), waiting ${wait}ms...`);
      await sleep(wait);
      continue;
    }
    throw lastErr;
  }
  throw lastErr;
}

async function getAllProblemSets(filterObj = {}) {
  const all = [];
  let page = 0;
  const limit = 30;
  while (true) {
    const data = await apiGet("/problem-sets", {
      filter: JSON.stringify(filterObj),
      page: String(page),
      limit: String(limit),
      order_by: CONFIG.ORDER_BY,
      asc: CONFIG.ASC ? "true" : "false",
    });
    const sets = data.problemSets || [];
    all.push(...sets);
    console.log(`  Page ${page}: ${sets.length} sets (total: ${data.total})`);
    if (sets.length < limit) break;
    page++;
    await sleep(CONFIG.DELAY);
  }
  return all;
}

function extractAnswersFromSubmissions(submissions) {
  const answers = {};
  for (const sub of submissions) {
    const judgeMap = {};
    for (const j of sub.judgeResponseContents || []) {
      judgeMap[j.problemSetProblemId] = j.status;
    }
    for (const d of sub.submissionDetails || []) {
      const pid = d.problemSetProblemId;
      let ans = null;
      if (d.trueOrFalseSubmissionDetail) {
        ans = d.trueOrFalseSubmissionDetail.answer;
      } else if (d.multipleChoiceSubmissionDetail) {
        ans = d.multipleChoiceSubmissionDetail.answer;
      } else if (d.fillInTheBlankForProgrammingSubmissionDetail) {
        ans = d.fillInTheBlankForProgrammingSubmissionDetail.answers;
      } else if (d.codeCompletionSubmissionDetail) {
        ans = d.codeCompletionSubmissionDetail.program;
      }
      if (ans === null) continue;
      const status = judgeMap[pid];
      if (status === "ACCEPTED") {
        answers[pid] = { answer: ans, status: "ACCEPTED" };
      } else if (!answers[pid]) {
        answers[pid] = { answer: ans, status: status || "UNKNOWN" };
      }
    }
  }
  return answers;
}

async function crawlProblemSet(ps) {
  const psId = ps.id;
  const psName = ps.name;
  console.log(`\nProcessing: ${psName} (${psId})`);

  let examId;
  try {
    const ed = await apiGet(`/problem-sets/${psId}/exams`);
    examId = ed.exam?.id;
    if (!examId) { console.log("  No exam, skip"); return null; }
  } catch (e) { console.log(`  ERROR exams: ${e.message}`); return null; }

  // Problem summaries (types)
  const summaries = (await apiGet(`/problem-sets/${psId}/problem-summaries`)).summaries || {};

  // Problem statuses
  let statusData;
  try {
    statusData = await apiGet(`/exams/${examId}/problem-sets/${psId}/problem-status`);
  } catch (e) {
    console.log(`  ERROR status: ${e.message}`);
    return null;
  }

  const statusById = {};
  for (const p of statusData.problemStatus || []) {
    statusById[p.id] = p.problemSubmissionStatus;
  }
  const labelMap = statusData.examLabelByProblemSetProblemId || {};

  const allTypes = Object.keys(summaries).filter((t) => !CONFIG.SKIP_TYPES.includes(t));
  const answerableTypes = allTypes.filter((t) => CONFIG.ANSWERABLE_TYPES.includes(t));

  // Get answers: try valid-submissions first, then last-submissions
  let answers = {};
  try {
    const vs = await apiGet(`/exams/${examId}/valid-submissions`, { problem_set_id: psId });
    answers = extractAnswersFromSubmissions(vs.submissions || []);
  } catch (e) { /* valid-submissions may not be available */ }

  for (const ptype of answerableTypes) {
    try {
      const ls = await apiGet(`/exams/${examId}/problem-sets/${psId}/last-submissions`, { problem_type: ptype });
      const subAns = extractAnswersFromSubmissions(ls.submission ? [ls.submission] : []);
      for (const [k, v] of Object.entries(subAns)) {
        if (!answers[k] || v.status === "ACCEPTED") answers[k] = v;
      }
    } catch (e) { /* skip */ }
  }

  // Fetch problems by type (ALL types, including SUBJECTIVE/PROGRAMMING)
  const problems = [];
  for (const ptype of allTypes) {
    console.log(`  Fetching ${ptype}...`);
    await sleep(CONFIG.DELAY);
    let probData;
    try {
      probData = await apiGet(`/problem-sets/${psId}/exam-problems`, {
        exam_id: examId,
        problem_type: ptype,
      });
    } catch (e) { console.log(`    ERROR: ${e.message}`); continue; }

    const orgMap = probData.organizationById || {};
    for (const psp of probData.problemSetProblems || []) {
      const pspId = psp.id;
      const pspStatus = statusById[pspId] || "UNKNOWN";

      let choices = null;
      const pc = psp.problemConfig || {};
      const mcpc = pc.multipleChoiceProblemConfig;
      if (mcpc) choices = mcpc.choices;

      const org = orgMap[psp.authorOrganizationId] || {};

      const entry = {
        problemSetProblemId: pspId,
        problemId: psp.problemId || "",
        label: labelMap[pspId] || psp.label || "",
        title: psp.title || "",
        content: psp.content || "",
        description: psp.description || "",
        type: psp.type,
        score: psp.score || 0,
        author: psp.author || "",
        authorOrganization: org.name || "",
        difficulty: psp.difficulty || 0,
        submissionStatus: pspStatus,
        choices: choices,
        solution: psp.solution || "",
      };

      const ansData = answers[pspId];
      if (pspStatus === "PROBLEM_ACCEPTED" && ansData?.status === "ACCEPTED") {
        entry.correctAnswer = ansData.answer;
      } else if (pspStatus === "PROBLEM_WRONG_ANSWER" && ansData) {
        entry.submittedAnswer = ansData.answer;
      }

      problems.push(entry);
    }
  }

  console.log(`  Got ${problems.length} problems`);
  return {
    id: psId,
    name: psName,
    type: ps.type,
    status: ps.status,
    organization: ps.organizationName || "",
    owner: ps.ownerNickname || "",
    createAt: ps.createAt,
    startAt: ps.startAt,
    endAt: ps.endAt,
    problemSummaries: summaries,
    problems,
  };
}

function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.style.display = "none";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  console.log(`Download started: ${filename}`);
}

async function main() {
  console.log("=== Pintia Problem Crawler ===");
  console.log("Config:", CONFIG);
  console.log("Fetching problem sets...");

  const filterObj = CONFIG.ALL_SETS
    ? {}
    : { endAtAfter: new Date().toISOString() };
  let allSets = await getAllProblemSets(filterObj);
  console.log(`Total problem sets: ${allSets.length}`);

  if (CONFIG.MAX_SETS) allSets = allSets.slice(0, CONFIG.MAX_SETS);

  const results = [];
  const skipped = [];
  const failed = [];
  for (let i = 0; i < allSets.length; i++) {
    console.log(`\n[${i + 1}/${allSets.length}]`);
    try {
      const r = await crawlProblemSet(allSets[i]);
      if (r) results.push(r);
      else skipped.push(allSets[i].name);
    } catch (e) {
      console.error(`  FATAL: ${e.message}`);
      failed.push(allSets[i].name + ": " + e.message);
    }
    await sleep(CONFIG.DELAY);

    if (CONFIG.SAVE_EVERY > 0 && results.length > 0 && (i + 1) % CONFIG.SAVE_EVERY === 0) {
      const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
      downloadJSON(results, `pintia_partial_${ts}.json`);
    }
  }

  const totalProblems = results.reduce((sum, r) => sum + (r.problems || []).length, 0);
  console.log(`\n=== DONE: ${results.length} sets, ${totalProblems} problems ===`);
  if (skipped.length) console.log(`Skipped (no exam): ${skipped.length}`);
  if (failed.length) console.log(`Failed: ${failed.length}`);

  const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  downloadJSON(results, `pintia_problems_${ts}.json`);
}

main().catch((e) => console.error("FATAL:", e));

```

【AIGC】【Unverified】以下内容仅供给AI参考。


# Pintia (PTA) API Reference

> 基于 2026-06 逆向分析。Base URL: `https://pintia.cn/api`

## 1. 鉴权

| 方式 | 说明 |
|------|------|
| Cookie | `PTASession=xxx; JSESSIONID=xxx`（HttpOnly） |
| Header | `x-lollipop`（客户端 token，可留空或用固定值 `9f6605...`） |
| Header | `x-marshmallow`（可为空） |
| CORS | `same-origin`，需 `credentials: "include"` |

登录流程通过 `https://passport.pintia.cn/api/u/current` 获取当前用户信息。

---

## 2. 题目集列表

```
GET /api/problem-sets
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `filter` | JSON string | 过滤条件，见下方 |
| `page` | int (0-based) | 页码 |
| `limit` | int | 每页数量，最大 30 |
| `order_by` | enum | `END_AT` / `CREATE_AT` / `UPDATE_AT` / `START_AT` |
| `asc` | "true"\|"false" | 升序/降序 |

### filter 示例

| 用途 | 值 |
|------|---|
| 活跃题目集 | `{"endAtAfter":"2026-06-26T16:00:00.000Z"}` |
| 所有题目集 | `{}` |

### Response

```json
{
  "total": 111,
  "problemSets": [
    {
      "id": "2029403182994202624",
      "name": "面向对象程序设计2025-2026习题集",
      "type": "EXERCISE",
      "timeType": "FIXED_TIME",
      "status": "PENDING",
      "organizationName": "浙江大学",
      "ownerNickname": "wwxuzju",
      "manageable": false,
      "createAt": "2026-03-05T03:46:37Z",
      "updateAt": "2026-03-06T01:53:12Z",
      "startAt": "2026-03-05T03:45:00Z",
      "endAt": "2026-06-30T05:45:00Z",
      "scoringRule": "NORMAL",
      "feature": "NONE",
      "sourceProblemSetId": "1892388524373225472"
    }
  ],
  "homeworkByProblemSetId": {}
}
```

---

## 3. 当前用户

```
GET https://passport.pintia.cn/api/u/current
```

返回当前登录用户信息（id, nickname, studentNumber 等）。

---

## 4. 题目集的考试 / 答题

```
GET /api/problem-sets/{problemSetId}/exams
```

### Response

```json
{
  "exam": {
    "id": "2029561959292456960",
    "score": 0.0,
    "startAt": "2026-03-05T03:45:00Z",
    "endAt": "2026-06-30T05:45:00Z",
    "status": "PROCESSING",
    "userId": "1832401778745544704",
    "problemSetId": "2029403182994202624",
    "ended": false
  },
  "problemSet": {
    "id": "2029403182994202624",
    "name": "...",
    "problemSetConfig": { "compilers": [...] }
  },
  "status": "PROCESSING"
}
```

`exam.id` 是后续所有题目相关 API 的必要参数。

---

## 5. 题目类型统计

```
GET /api/problem-sets/{problemSetId}/problem-summaries
```

### Response

```json
{
  "summaries": {
    "TRUE_OR_FALSE": {"total": 13, "totalScore": 26},
    "MULTIPLE_CHOICE": {"total": 20, "totalScore": 60},
    "FILL_IN_THE_BLANK_FOR_PROGRAMMING": {"total": 1, "totalScore": 6},
    "CODE_COMPLETION": {"total": 1, "totalScore": 8},
    "SUBJECTIVE": {"total": 7, "totalScore": 150}
  }
}
```

---

## 6. 题目状态列表

```
GET /api/exams/{examId}/problem-sets/{problemSetId}/problem-status
```

### Response

```json
{
  "problemStatus": [
    {
      "id": "2029403183010979840",
      "label": "8-1",
      "score": 10,
      "problemSubmissionStatus": "PROBLEM_ACCEPTED",
      "problemType": "SUBJECTIVE",
      "problemPoolIndex": 1,
      "indexInProblemPool": 1
    }
  ],
  "examLabelByProblemSetProblemId": {
    "2029403183010979840": "8-1"
  }
}
```

### problemSubmissionStatus 枚举

| 值 | 含义 |
|---|------|
| `PROBLEM_ACCEPTED` | 答案正确 |
| `PROBLEM_WRONG_ANSWER` | 答案错误（提交过但未通过） |
| `PROBLEM_NO_ANSWER` | 未作答 |
| `PROBLEM_SUBMITTED` | 已提交但尚未判题 |

---

## 7. 题目详情

```
GET /api/problem-sets/{problemSetId}/exam-problems?exam_id={examId}&problem_type={TYPE}
```

获取某一题型下的所有题目详情。

### Response（单选题示例）

```json
{
  "organizationById": {
    "14": {"id": "14", "name": "福州大学", "code": "fzu", "type": "SCHOOL"}
  },
  "problemSetProblems": [
    {
      "id": "2062420119713849349",
      "label": "2-1",
      "score": 2,
      "problemConfig": {
        "solutionVisible": false,
        "answerVisible": false,
        "multipleChoiceProblemConfig": {
          "choices": [
            "接受消息的对象",
            "要执行的函数的名字",
            "要执行的函数的内部结构",
            "函数需要的参数"
          ],
          "maxDisplayChoicesPerLine": 1
        }
      },
      "title": "对象之间的相互作用和通信是通过消息...",
      "content": "对象之间的相互作用和通信是通过消息。（ ）不是消息的组成部分。 @[](2)\n\nA. ...\nB. ...\nC. ...\nD. ...",
      "type": "MULTIPLE_CHOICE",
      "author": "王秀",
      "difficulty": 0,
      "compiler": "NO_COMPILER",
      "problemStatus": "REVIEWED",
      "lastSubmissionId": "0",
      "solution": "",
      "problemSetId": "2062420119697072128",
      "problemId": "2652",
      "description": "对象之间的相互作用和通信是通过消息。（ ）不是消息的组成部分。",
      "problemPoolIndex": 1,
      "indexInProblemPool": 1,
      "authorOrganizationId": "14"
    }
  ],
  "examLabelByProblemSetProblemId": {
    "2062420119713849349": "2-1"
  }
}
```

### 单题详情

```
GET /api/problem-sets/{problemSetId}/exam-problems/{problemSetProblemId}
```

---

## 8. 作答记录与正确答案

### 已结束的考试：valid-submissions

```
GET /api/exams/{examId}/valid-submissions?problem_set_id={problemSetId}
```

#### Response

```json
{
  "submissions": [
    {
      "id": "2009054280852127744",
      "userId": "1832401778745544704",
      "problemType": "TRUE_OR_FALSE",
      "submitAt": "2026-01-08T00:07:21Z",
      "status": "PARTIAL_ACCEPTED",
      "score": 18.0,
      "submissionDetails": [
        {
          "problemSetProblemId": "2004027359105167360",
          "trueOrFalseSubmissionDetail": { "answer": "TRUE" }
        },
        {
          "problemSetProblemId": "2004153228956086273",
          "trueOrFalseSubmissionDetail": { "answer": "TRUE" }
        }
      ],
      "judgeResponseContents": [
        { "status": "ACCEPTED", "score": 2.0, "problemSetProblemId": "2004027359105167360" },
        { "status": "WRONG_ANSWER", "score": 0.0, "problemSetProblemId": "2004153228956086273" }
      ]
    }
  ]
}
```

通过匹配 `judgeResponseContents[*].status === "ACCEPTED"` 的题目与 `submissionDetails`，即可得到**正确答案**。

### 进行中的考试：last-submissions

```
GET /api/exams/{examId}/problem-sets/{problemSetId}/last-submissions?problem_type={TYPE}
GET /api/exams/{examId}/problem-sets/{problemSetId}/last-submissions?problem_set_problem_id={PSP_ID}
```

返回格式同上（单次提交对象 `submission`）。

---

## 9. 提交答案

```
POST /api/exams/{examId}/exam-submissions
```

> 谨慎使用，会实际提交答案。

---

## 10. 题目类型表

| API 枚举值 | 中文名 | 答案格式 |
|-----------|--------|---------|
| `TRUE_OR_FALSE` | 判断题 | `"TRUE"` / `"FALSE"` |
| `MULTIPLE_CHOICE` | 单选题 | `"A"` ~ `"D"` |
| `FILL_IN_THE_BLANK_FOR_PROGRAMMING` | 程序填空题 | `["answer1", "answer2"]` |
| `CODE_COMPLETION` | 代码补全 | `"code string"` |
| `SUBJECTIVE` | 主观题/编程题 | `{answer:"", file:"uuid.zip"}` |
| `PROGRAMMING` | 编程题 | 同上 |
| `MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER` | 多选题 | 选项数组 |
| `FILL_IN_THE_BLANK` | 填空题 | 答案数组 |

### 答案字段映射

| 题型 | submissionDetail 字段 |
|------|----------------------|
| TRUE_OR_FALSE | `trueOrFalseSubmissionDetail.answer` |
| MULTIPLE_CHOICE | `multipleChoiceSubmissionDetail.answer` |
| FILL_IN_THE_BLANK_FOR_PROGRAMMING | `fillInTheBlankForProgrammingSubmissionDetail.answers` |
| CODE_COMPLETION | `codeCompletionSubmissionDetail.program` |
| SUBJECTIVE / PROGRAMMING | `subjectiveSubmissionDetail.file`（忽略） |

---

## 11. 注意事项

- **429 rate limit**：请求过快会触发，建议每次请求间隔 ≥ 500ms，遇到 429 时指数退避重试。
- **403**：无权限访问该题目集（如未加入班级）。
- **无 exam**：PENDING 状态的题目集可能尚未开始，此时 `exams` 接口不返回数据。
- 不同 problem set 的题型组合不同，应先查 `problem-summaries` 再按类型逐一获取。
- `exam-problems` 的 `content` 字段包含 `@[]()` 标记，是页面渲染用的占位符。
