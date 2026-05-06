<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { NButton, NInput, NSwitch, NCard, NTag, NSpace, NBadge } from 'naive-ui'

// ---------- 类型 ----------
interface PTEInfo {
  hex: string
  ppn: string
  pa: string
  flags: { V: boolean; R: boolean; W: boolean; X: boolean; A: boolean; D: boolean }
  raw: number
}

interface PageTreeNode {
  name: string
  addr: string
  index: string
  children?: PageTreeNode[]
  leaf?: boolean
  pages?: { name: string; addr: string; perm: string }[]
}

// ---------- 常量 ----------
const VM_START = 0xffffffe000000000
const PA_OFFSET = VM_START - 0x80000000
const PHY_SIZE = 128 * 1024 * 1024
const PAGE_SIZE = 4096

// 预设页表物理地址（虚构，演示用）
const ROOT_PA = 0x80001000       // swapper_pg_dir
const PMD_PA = 0x80002000       // 中间页表 (vpn2=0)
const PTE_TABLE_A_PA = 0x80003000 // 叶子页表 A (text/rodata, vpn1=1)
const PTE_TABLE_B_PA = 0x80004000 // 叶子页表 B (data, vpn1=2)

// 段映射（模拟 setup_vm_final）
const SEGMENTS = [
  {
    name: 'text',
    start: VM_START + 0x200000,
    end:   VM_START + 0x300000,
    perm: 'RX',
    leafFlags: 0xcb, // V R X A D
    physBase: 0x80200000,
    vpn1: 1
  },
  {
    name: 'rodata',
    start: VM_START + 0x300000,
    end:   VM_START + 0x400000,
    perm: 'R',
    leafFlags: 0xc3, // V R A D
    physBase: 0x80300000,
    vpn1: 1
  },
  {
    name: 'data',
    start: VM_START + 0x400000,
    end:   VM_START + PHY_SIZE,
    perm: 'RW',
    leafFlags: 0xc7, // V R W A D
    physBase: 0x80400000,
    vpn1: 2
  }
]

// ---------- 状态 ----------
const vaInput = ref('0xffffffe000200000')
const parsedVA = ref<number | null>(null)
const vpns = reactive({ vpn2: -1, vpn1: -1, vpn0: -1, offset: -1 })
const manualMode = ref(false)
const currentStep = ref(0)      // 0:未开始, 1:L2, 2:L1, 3:L0, 4:结果
const manualPTE = reactive({ l2: '', l1: '', l0: '' })
const pteResult = reactive<{ l2: PTEInfo | null; l1: PTEInfo | null; l0: PTEInfo | null }>({
  l2: null, l1: null, l0: null
})
const errorMsg = ref('')

// ---------- 辅助函数 ----------
function getSegment(va: number) {
  return SEGMENTS.find(s => va >= s.start && va < s.end) || null
}

function parsePTE(raw: number, isLeaf: boolean): PTEInfo {
  const v = !!(raw & 1)
  const r = !!(raw & (1 << 1))
  const w = !!(raw & (1 << 2))
  const x = !!(raw & (1 << 3))
  const a = !!(raw & (1 << 6))
  const d = !!(raw & (1 << 7))
  const ppn = raw >> 10
  const pa = ppn << 12
  return {
    hex: '0x' + raw.toString(16).padStart(16, '0'),
    ppn: '0x' + ppn.toString(16),
    pa:  '0x' + pa.toString(16),
    flags: { V: v, R: r, W: w, X: x, A: a, D: d },
    raw
  }
}

function simulatePTE(level: 2 | 1 | 0): number {
  if (parsedVA.value === null) return 0
  const va = parsedVA.value
  const seg = getSegment(va)

  if (level === 2) {
    if (vpns.vpn2 !== 0 || !seg) return 0
    const ppn = PMD_PA >> 12
    return (ppn << 10) | 0x1
  }
  if (level === 1) {
    if (!seg || vpns.vpn1 !== seg.vpn1) return 0
    const leafPA = seg.vpn1 === 1 ? PTE_TABLE_A_PA : PTE_TABLE_B_PA
    const ppn = leafPA >> 12
    return (ppn << 10) | 0x1
  }
  if (level === 0) {
    if (!seg) return 0
    const offsetInSeg = va - seg.start
    const pageOffset = Math.floor(offsetInSeg / PAGE_SIZE)
    const physAddr = seg.physBase + pageOffset * PAGE_SIZE
    const ppn = physAddr >> 12
    return (ppn << 10) | seg.leafFlags
  }
  return 0
}

// ---------- 交互方法 ----------
function parseVA() {
  errorMsg.value = ''
  try {
    const val = BigInt(vaInput.value.trim())
    if (val < 0 || val > 0xffffffffffffffffn) throw new Error()
    const num = Number(val)
    parsedVA.value = num
    vpns.vpn2 = (num >> 30) & 0x1ff
    vpns.vpn1 = (num >> 21) & 0x1ff
    vpns.vpn0 = (num >> 12) & 0x1ff
    vpns.offset = num & 0xfff
    currentStep.value = 1
    pteResult.l2 = pteResult.l1 = pteResult.l0 = null
    manualPTE.l2 = manualPTE.l1 = manualPTE.l0 = ''
  } catch {
    errorMsg.value = '无效的虚拟地址，请输入类似 0xffffffe000200000'
    parsedVA.value = null
    currentStep.value = 0
  }
}

function fetchL2() {
  if (!parsedVA.value) return
  if (manualMode.value) {
    const raw = parseInt(manualPTE.l2, 16)
    if (isNaN(raw)) { errorMsg.value = '请输入合法的十六进制 PTE 值'; return }
    pteResult.l2 = parsePTE(raw, false)
  } else {
    const raw = simulatePTE(2)
    pteResult.l2 = parsePTE(raw, false)
  }
  currentStep.value = 2
}

function fetchL1() {
  if (!parsedVA.value) return
  if (manualMode.value) {
    const raw = parseInt(manualPTE.l1, 16)
    if (isNaN(raw)) { errorMsg.value = '请输入合法的十六进制 PTE 值'; return }
    pteResult.l1 = parsePTE(raw, false)
  } else {
    const raw = simulatePTE(1)
    pteResult.l1 = parsePTE(raw, false)
  }
  currentStep.value = 3
}

function fetchL0() {
  if (!parsedVA.value) return
  if (manualMode.value) {
    const raw = parseInt(manualPTE.l0, 16)
    if (isNaN(raw)) { errorMsg.value = '请输入合法的十六进制 PTE 值'; return }
    pteResult.l0 = parsePTE(raw, true)
  } else {
    const raw = simulatePTE(0)
    pteResult.l0 = parsePTE(raw, true)
  }
  currentStep.value = 4
}

// ---------- 页表树数据 ----------
const treeData = computed<PageTreeNode>(() => ({
  name: 'swapper_pg_dir',
  addr: '0x' + ROOT_PA.toString(16),
  index: `vpn2 = ${vpns.vpn2 >= 0 ? '0x' + vpns.vpn2.toString(16) : '?'}`,
  children: [{
    name: 'PMD (中间页表)',
    addr: '0x' + PMD_PA.toString(16),
    index: `vpn1 = ${vpns.vpn1 >= 0 ? '0x' + vpns.vpn1.toString(16) : '?'}`,
    children: [
      {
        name: 'PTE Table A',
        addr: '0x' + PTE_TABLE_A_PA.toString(16),
        index: 'vpn1=1',
        leaf: true,
        pages: [
          { name: 'Text Page', addr: '0x80200xxx', perm: 'RX' },
          { name: 'Rodata Page', addr: '0x80300xxx', perm: 'R' }
        ]
      },
      {
        name: 'PTE Table B',
        addr: '0x' + PTE_TABLE_B_PA.toString(16),
        index: 'vpn1=2',
        leaf: true,
        pages: [
          { name: 'Data Page', addr: '0x80400xxx', perm: 'RW' }
        ]
      }
    ]
  }]
}))

function isNodeActive(level: number, extra?: { vpn1?: number; leaf?: string }): boolean {
  if (!parsedVA.value) return false
  if (level === 0) return currentStep.value >= 1
  if (level === 1) return currentStep.value >= 2
  if (level === 2 && extra) {
    const seg = getSegment(parsedVA.value)
    if (!seg) return false
    return extra.vpn1 === seg.vpn1 && currentStep.value >= 3
  }
  if (level === 3 && extra) {
    const seg = getSegment(parsedVA.value)
    if (!seg || currentStep.value < 4) return false
    return extra.leaf === seg.name
  }
  return false
}

const currentSegment = computed(() => {
  if (!parsedVA.value) return null
  return getSegment(parsedVA.value)
})
const finalPhysicalAddr = computed(() => pteResult.l0?.pa || '')
</script>

<template>
  <div class="app-container">
    <h1 class="title">RISC‑V Sv39 三级页表查找演示</h1>

    <!-- 输入区域 -->
    <n-card class="input-card" size="small">
      <div class="input-row">
        <n-input
          v-model:value="vaInput"
          placeholder="如 0xffffffe000200000"
          clearable
          style="flex: 1; min-width: 220px;"
        />
        <n-button type="primary" @click="parseVA" :disabled="!vaInput.trim()">解析地址</n-button>
        <div class="switch-box">
          <span class="switch-label">手动模式</span>
          <n-switch v-model:value="manualMode" />
        </div>
      </div>
      <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
    </n-card>

    <!-- VPN / offset 显示 -->
    <n-card v-if="parsedVA !== null" class="vpn-card" size="small">
      <div class="vpn-grid">
        <div class="vpn-item vpn2">VPN[2] (L2)<br><span class="vpn-value">0x{{ vpns.vpn2.toString(16) }}</span></div>
        <div class="vpn-item vpn1">VPN[1] (L1)<br><span class="vpn-value">0x{{ vpns.vpn1.toString(16) }}</span></div>
        <div class="vpn-item vpn0">VPN[0] (L0)<br><span class="vpn-value">0x{{ vpns.vpn0.toString(16) }}</span></div>
        <div class="vpn-item offset">Offset<br><span class="vpn-value">0x{{ vpns.offset.toString(16) }}</span></div>
      </div>
    </n-card>

    <!-- 主内容：步骤 + 树 -->
    <div v-if="currentStep >= 1" class="main-content">
      <!-- 左侧：查找步骤 -->
      <div class="steps-column">
        <!-- 步骤 L2 -->
        <n-card :class="['step-card', { active: currentStep === 1 }]" size="small">
          <template #header>
            <div class="step-header">
              <span>步骤 1：获取 Level 2 PTE (根页表)</span>
              <n-tag v-if="currentStep > 1" type="success" size="small">已完成</n-tag>
              <n-tag v-else-if="currentStep === 1" type="info" size="small">当前</n-tag>
            </div>
          </template>
          <p class="step-desc">索引 <code>swapper_pg_dir[vpn2]</code></p>
          <div v-if="manualMode" class="manual-input">
            <n-input v-model:value="manualPTE.l2" placeholder="PTE 十六进制值" size="small" style="flex:1" />
            <n-button size="small" @click="fetchL2" :disabled="!manualPTE.l2">查询</n-button>
          </div>
          <n-button v-else size="small" @click="fetchL2" :disabled="currentStep !== 1">获取 L2 PTE</n-button>
          <div v-if="pteResult.l2" class="pte-info">
            <div><strong>PTE:</strong> {{ pteResult.l2.hex }}</div>
            <div><strong>PPN:</strong> {{ pteResult.l2.ppn }} → {{ pteResult.l2.pa }}</div>
            <n-space class="flags" size="small">
              <n-tag v-for="(v,k) in pteResult.l2.flags" :key="k" :type="v ? 'success' : 'default'" size="tiny">
                {{ k }}={{ v ? 1 : 0 }}
              </n-tag>
            </n-space>
          </div>
        </n-card>

        <!-- 步骤 L1 -->
        <n-card v-if="currentStep >= 2" :class="['step-card', { active: currentStep === 2 }]" size="small">
          <template #header>
            <div class="step-header">
              <span>步骤 2：获取 Level 1 PTE (中间页表)</span>
              <n-tag v-if="currentStep > 2" type="success" size="small">已完成</n-tag>
              <n-tag v-else-if="currentStep === 2" type="info" size="small">当前</n-tag>
            </div>
          </template>
          <p class="step-desc">中间页表基址 {{ pteResult.l2?.pa }}，索引 <code>[vpn1]</code></p>
          <div v-if="manualMode" class="manual-input">
            <n-input v-model:value="manualPTE.l1" placeholder="PTE 十六进制值" size="small" style="flex:1" />
            <n-button size="small" @click="fetchL1" :disabled="!manualPTE.l1">查询</n-button>
          </div>
          <n-button v-else size="small" @click="fetchL1" :disabled="currentStep !== 2">获取 L1 PTE</n-button>
          <div v-if="pteResult.l1" class="pte-info">
            <div><strong>PTE:</strong> {{ pteResult.l1.hex }}</div>
            <div><strong>PPN:</strong> {{ pteResult.l1.ppn }} → {{ pteResult.l1.pa }}</div>
            <n-space class="flags" size="small">
              <n-tag v-for="(v,k) in pteResult.l1.flags" :key="k" :type="v ? 'success' : 'default'" size="tiny">
                {{ k }}={{ v ? 1 : 0 }}
              </n-tag>
            </n-space>
          </div>
        </n-card>

        <!-- 步骤 L0 -->
        <n-card v-if="currentStep >= 3" :class="['step-card', { active: currentStep === 3 }]" size="small">
          <template #header>
            <div class="step-header">
              <span>步骤 3：获取 Level 0 PTE (叶子页表)</span>
              <n-tag v-if="currentStep > 3" type="success" size="small">已完成</n-tag>
              <n-tag v-else-if="currentStep === 3" type="info" size="small">当前</n-tag>
            </div>
          </template>
          <p class="step-desc">叶子页表基址 {{ pteResult.l1?.pa }}，索引 <code>[vpn0]</code></p>
          <div v-if="manualMode" class="manual-input">
            <n-input v-model:value="manualPTE.l0" placeholder="PTE 十六进制值" size="small" style="flex:1" />
            <n-button size="small" @click="fetchL0" :disabled="!manualPTE.l0">查询</n-button>
          </div>
          <n-button v-else size="small" @click="fetchL0" :disabled="currentStep !== 3">获取 L0 PTE</n-button>
          <div v-if="pteResult.l0" class="pte-info">
            <div><strong>PTE:</strong> {{ pteResult.l0.hex }}</div>
            <div><strong>PPN:</strong> {{ pteResult.l0.ppn }} → {{ pteResult.l0.pa }}</div>
            <n-space class="flags" size="small">
              <n-tag v-for="(v,k) in pteResult.l0.flags" :key="k" :type="v ? 'success' : 'default'" size="tiny">
                {{ k }}={{ v ? 1 : 0 }}
              </n-tag>
            </n-space>
          </div>
        </n-card>

        <!-- 最终结果 -->
        <n-card v-if="currentStep >= 4" class="result-card" size="small">
          <template #header>
            <span class="result-title">✅ 最终物理地址及权限</span>
          </template>
          <div class="result-content">
            <div class="result-item">
              <span>物理地址：</span>
              <strong>{{ finalPhysicalAddr }}</strong>
            </div>
            <div class="result-item">
              <span>权限：</span>
              <n-tag v-if="currentSegment" type="warning">{{ currentSegment.perm }}</n-tag>
            </div>
            <div class="result-item">
              <span>段：</span>
              <strong>{{ currentSegment?.name || '未知' }}</strong>
            </div>
          </div>
        </n-card>
      </div>

      <!-- 右侧：页表树 -->
      <n-card class="tree-card" size="small">
        <template #header>
          <span class="tree-title">🌳 页表树 (swapper_pg_dir)</span>
        </template>
        <div class="tree-container">
          <!-- 根节点 -->
          <div :class="['tree-node', 'root', { active: isNodeActive(0) }]">
            <div class="node-name">{{ treeData.name }}</div>
            <div class="node-addr">{{ treeData.addr }} | {{ treeData.index }}</div>
          </div>
          <!-- 中间页表 -->
          <div :class="['tree-node', 'pmd', { active: isNodeActive(1) }]">
            <div class="node-name">{{ treeData.children[0].name }}</div>
            <div class="node-addr">{{ treeData.children[0].addr }} | {{ treeData.children[0].index }}</div>
            <!-- 叶子表 A -->
            <div :class="['tree-node', 'leaf', { active: isNodeActive(2, {vpn1:1}) }]">
              <div class="node-name">{{ treeData.children[0].children[0].name }}</div>
              <div class="node-addr">{{ treeData.children[0].children[0].addr }}</div>
              <div
                v-for="page in treeData.children[0].children[0].pages"
                :key="page.perm"
                :class="['tree-node', 'page', { active: isNodeActive(3, {leaf: page.perm==='RX'?'text':page.perm==='R'?'rodata':'data'}) }]"
              >
                <div class="node-name">{{ page.name }} ({{ page.perm }})</div>
                <div class="node-addr">{{ page.addr }}</div>
              </div>
            </div>
            <!-- 叶子表 B -->
            <div :class="['tree-node', 'leaf', { active: isNodeActive(2, {vpn1:2}) }]">
              <div class="node-name">{{ treeData.children[0].children[1].name }}</div>
              <div class="node-addr">{{ treeData.children[0].children[1].addr }}</div>
              <div
                v-for="page in treeData.children[0].children[1].pages"
                :key="page.perm"
                :class="['tree-node', 'page', { active: isNodeActive(3, {leaf:'data'}) }]"
              >
                <div class="node-name">{{ page.name }} ({{ page.perm }})</div>
                <div class="node-addr">{{ page.addr }}</div>
              </div>
            </div>
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<style scoped>
/* ---------- 全局布局 ---------- */
.app-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto Mono', sans-serif;
  color: #1e293b;
}
.title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 24px;
}

/* 输入卡片 */
.input-card {
  margin-bottom: 20px;
}
.input-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.switch-box {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.switch-label {
  font-size: 0.9rem;
  white-space: nowrap;
}
.error-text {
  color: #d03050;
  margin-top: 8px;
  font-size: 0.85rem;
}

/* VPN 展示 */
.vpn-card {
  margin-bottom: 24px;
}
.vpn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}
.vpn-item {
  text-align: center;
  padding: 12px 8px;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 0.85rem;
  line-height: 1.4;
}
.vpn-item.vpn2 { border-bottom: 3px solid #3b82f6; }
.vpn-item.vpn1 { border-bottom: 3px solid #10b981; }
.vpn-item.vpn0 { border-bottom: 3px solid #8b5cf6; }
.vpn-item.offset { border-bottom: 3px solid #6b7280; }
.vpn-value {
  font-family: 'Roboto Mono', monospace;
  font-weight: 700;
  font-size: 1.4rem;
  display: block;
  margin-top: 4px;
}

/* 主内容区域 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 20px;
  align-items: start;
}

/* 步骤卡片 */
.steps-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.step-card {
  border: 1px solid #e2e8f0;
  transition: border-color 0.2s;
}
.step-card.active {
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}
.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}
.step-desc {
  font-size: 0.9rem;
  color: #475569;
  margin: 4px 0 8px;
}
.step-desc code {
  background: #f1f5f9;
  padding: 1px 4px;
  border-radius: 3px;
  font-family: monospace;
}
.manual-input {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
.pte-info {
  margin-top: 12px;
  font-size: 0.9rem;
  background: #f8fafc;
  padding: 10px;
  border-radius: 6px;
}
.pte-info div {
  margin-bottom: 4px;
}
.flags {
  margin-top: 8px;
  flex-wrap: wrap;
}

/* 结果卡片 */
.result-card {
  border: 1px solid #10b981;
  background: #f0fdf4;
}
.result-title {
  font-weight: 600;
  color: #065f46;
}
.result-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.result-item {
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ---------- 页表树 ---------- */
.tree-card {
  position: sticky;
  top: 20px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}
.tree-title {
  font-weight: 600;
}
.tree-container {
  padding-left: 12px;
  font-size: 0.9rem;
}
.tree-node {
  position: relative;
  padding: 6px 0 6px 20px;
  border-left: 2px solid #cbd5e1;
  margin-bottom: 2px;
}
.tree-node.root {
  border-left-color: #3b82f6;
}
.tree-node.pmd {
  margin-left: 16px;
}
.tree-node.leaf {
  margin-left: 16px;
  border-left-color: #a78bfa;
}
.tree-node.page {
  margin-left: 16px;
  border-left-color: #f59e0b;
}
.tree-node.active {
  background: #eff6ff;
  border-left-color: #2563eb !important;
  border-radius: 0 6px 6px 0;
}
.tree-node.active .node-name {
  font-weight: 700;
}
.node-name {
  font-family: 'Roboto Mono', monospace;
  color: #0f172a;
}
.node-addr {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 2px;
}

/* 小屏幕适配 */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  .tree-card {
    position: static;
    max-height: none;
  }
}
</style>