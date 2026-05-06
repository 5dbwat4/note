<script setup lang="ts">
import { ref, computed, reactive, nextTick } from 'vue'
import {
  NButton, NInput, NCard, NTag, NSpace, NInputGroup,
  NAlert, NGrid, NGi
} from 'naive-ui'

const PA2VA_OFFSET = 0xffffffe000000000n - 0x80000000n

const vaInput = ref('')
const parsedVA = ref<bigint | null>(null)
const errorMsg = ref('')
const currentStep = ref(0)

const vpn = reactive({ vpn2: -1n, vpn1: -1n, vpn0: -1n, offset: -1n })

const pte2Input = ref('0x200b2401')
const pte1Input = ref('0x200b2801')
const pte0Input = ref('0x200800cb')

const pte2Raw = ref<bigint | null>(null)
const pte1Raw = ref<bigint | null>(null)
const pte0Raw = ref<bigint | null>(null)

const pte2Error = ref('')
const pte1Error = ref('')
const pte0Error = ref('')

const pmdPa = ref<bigint | null>(null)
const pmdVa = ref<bigint | null>(null)
const ptePa = ref<bigint | null>(null)
const pteVa = ref<bigint | null>(null)

const step1Card = ref<InstanceType<typeof NCard> | null>(null)
const step2Card = ref<InstanceType<typeof NCard> | null>(null)
const step3Card = ref<InstanceType<typeof NCard> | null>(null)
const resultCard = ref<InstanceType<typeof NCard> | null>(null)

function bnHex(v: bigint, pad = 16): string {
  return '0x' + v.toString(16).padStart(pad, '0')
}

function parsePTE(raw: bigint) {
  const V = !!(raw & 1n)
  const R = !!(raw & (1n << 1n))
  const W = !!(raw & (1n << 2n))
  const X = !!(raw & (1n << 3n))
  const PFN = raw >> 10n
  const PA = PFN << 12n
  return { hex: bnHex(raw), V, R, W, X, PFN, PA }
}

const pte2Info = computed(() => (pte2Raw.value !== null ? parsePTE(pte2Raw.value) : null))
const pte1Info = computed(() => (pte1Raw.value !== null ? parsePTE(pte1Raw.value) : null))
const pte0Info = computed(() => (pte0Raw.value !== null ? parsePTE(pte0Raw.value) : null))

interface PTEFieldRow {
  name: string
  bits: string
  hex: string
  bin: string
  highlight: boolean
}

function pteFields(raw: bigint): PTEFieldRow[] {
  const mask = (hi: number, lo: number) => ((1n << BigInt(hi - lo + 1)) - 1n) << BigInt(lo)
  const extr = (hi: number, lo: number) => {
    const v = (raw & mask(hi, lo)) >> BigInt(lo)
    const w = hi - lo + 1
    return { hex: bnHex(v, Math.ceil(w / 4)), bin: v.toString(2).padStart(w, '0') }
  }
  const e1 = (bit: number) => extr(bit, bit)
  return [
    { name: 'N',   bits: '63',    ...e1(63), highlight: false },
    { name: 'PBMT', bits: '62:61', ...extr(62, 61), highlight: false },
    { name: 'Reserved', bits: '60:54', ...extr(60, 54), highlight: false },
    { name: 'PPN[2]', bits: '53:28', ...extr(53, 28), highlight: false },
    { name: 'PPN[1]', bits: '27:19', ...extr(27, 19), highlight: false },
    { name: 'PPN[0]', bits: '18:10', ...extr(18, 10), highlight: false },
    { name: 'RSW',  bits: '9:8',  ...extr(9, 8), highlight: false },
    { name: 'D',    bits: '7',    ...e1(7),  highlight: true },
    { name: 'A',    bits: '6',    ...e1(6),  highlight: true },
    { name: 'G',    bits: '5',    ...e1(5),  highlight: true },
    { name: 'U',    bits: '4',    ...e1(4),  highlight: true },
    { name: 'X',    bits: '3',    ...e1(3),  highlight: true },
    { name: 'W',    bits: '2',    ...e1(2),  highlight: true },
    { name: 'R',    bits: '1',    ...e1(1),  highlight: true },
    { name: 'V',    bits: '0',    ...e1(0),  highlight: true },
  ]
}

const pte2Fields = computed(() => pte2Raw.value !== null ? pteFields(pte2Raw.value) : null)
const pte1Fields = computed(() => pte1Raw.value !== null ? pteFields(pte1Raw.value) : null)
const pte0Fields = computed(() => pte0Raw.value !== null ? pteFields(pte0Raw.value) : null)

function bnBin(v: bigint, width: number): string {
  return v.toString(2).padStart(width, '0')
}

const vpnBin = computed(() => {
  if (parsedVA.value === null) return null
  return {
    vpn2: bnBin(vpn.vpn2, 9),
    vpn1: bnBin(vpn.vpn1, 9),
    vpn0: bnBin(vpn.vpn0, 9),
    offset: bnBin(vpn.offset, 12),
  }
})

const vpnHex = computed(() => {
  if (parsedVA.value === null) return null
  return {
    vpn2: bnHex(vpn.vpn2, 3),
    vpn1: bnHex(vpn.vpn1, 3),
    vpn0: bnHex(vpn.vpn0, 3),
    offset: bnHex(vpn.offset, 3),
  }
})

const gdbCmdL2 = computed(() => {
  if (parsedVA.value === null) return ''
  return `p/x *(swapper_pg_dir + ${bnHex(vpn.vpn2 > 0n ? vpn.vpn2 : 0n, 2)})`
})

const gdbCmdL1 = computed(() => {
  if (pmdVa.value === null) return ''
  return `p/x ((uint64_t*)0x${pmdVa.value.toString(16)})[${bnHex(vpn.vpn1 > 0n ? vpn.vpn1 : 0n, 2)}]`
})

const gdbCmdL0 = computed(() => {
  if (pteVa.value === null) return ''
  return `p/x ((uint64_t*)0x${pteVa.value.toString(16)})[${bnHex(vpn.vpn0 > 0n ? vpn.vpn0 : 0n, 2)}]`
})

function parseVA() {
  errorMsg.value = ''
  try {
    const raw = vaInput.value.trim()
    let val: bigint
    if (raw.startsWith('0x') || raw.startsWith('0X')) {
      val = BigInt(raw)
    } else {
      val = BigInt(raw)
    }
    if (val < 0n || val > 0xffffffffffffffffn) throw new Error()
    parsedVA.value = val
    vpn.vpn2 = (val >> 30n) & 0x1ffn
    vpn.vpn1 = (val >> 21n) & 0x1ffn
    vpn.vpn0 = (val >> 12n) & 0x1ffn
    vpn.offset = val & 0xfffn
    currentStep.value = 1
    pte2Raw.value = null; pte1Raw.value = null; pte0Raw.value = null
    pmdPa.value = null; pmdVa.value = null; ptePa.value = null; pteVa.value = null
    pte2Input.value = '0x200b2401'; pte1Input.value = '0x200b2801'; pte0Input.value = '0x200800cb'
    pte2Error.value = ''; pte1Error.value = ''; pte0Error.value = ''
  } catch {
    errorMsg.value = '无效的虚拟地址，请输入类似 0xffffffe000200000'
    parsedVA.value = null
    currentStep.value = 0
  }
}

async function fetchL2() {
  pte2Error.value = ''
  try {
    const raw = BigInt(pte2Input.value.trim())
    pte2Raw.value = raw
    pmdPa.value = (raw >> 10n) << 12n
    pmdVa.value = pmdPa.value + PA2VA_OFFSET
    currentStep.value = 2
    await nextTick()
    step2Card.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } catch {
    pte2Error.value = '请输入合法的十六进制值'
  }
}

async function fetchL1() {
  pte1Error.value = ''
  try {
    const raw = BigInt(pte1Input.value.trim())
    pte1Raw.value = raw
    ptePa.value = (raw >> 10n) << 12n
    pteVa.value = ptePa.value + PA2VA_OFFSET
    currentStep.value = 3
    await nextTick()
    step3Card.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } catch {
    pte1Error.value = '请输入合法的十六进制值'
  }
}

async function fetchL0() {
  pte0Error.value = ''
  try {
    const raw = BigInt(pte0Input.value.trim())
    pte0Raw.value = raw
    currentStep.value = 4
    await nextTick()
    resultCard.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } catch {
    pte0Error.value = '请输入合法的十六进制值'
  }
}
</script>

<template>
  <div class="app-container">
    <h1 class="title">RISC‑V Sv39 三级页表查找模拟</h1>

    <n-card size="small" class="input-card">
      <n-input-group>
        <n-input
          v-model:value="vaInput"
          placeholder="虚拟地址，如 0xffffffe000200000"
          clearable
          style="flex:1"
          @keyup.enter="parseVA"
        />
        <n-button type="primary" @click="parseVA" :disabled="!vaInput.trim()">
          解析地址
        </n-button>
      </n-input-group>
      <n-alert v-if="errorMsg" type="error" style="margin-top:10px">
        {{ errorMsg }}
      </n-alert>
    </n-card>

    <n-card v-if="vpnHex && vpnBin" size="small" class="vpn-card">
      <template #header>解析结果</template>
      <div class="va-display">
        <span class="va-label">虚拟地址</span>
        <code class="va-full">{{ bnHex(parsedVA!) }}</code>
      </div>
      <table class="vpn-table">
        <thead>
          <tr>
            <th class="col-label"></th>
            <th class="col-vpn2">VPN[2]</th>
            <th class="col-vpn1">VPN[1]</th>
            <th class="col-vpn0">VPN[0]</th>
            <th class="col-offset">Offset</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="row-label">字段</td>
            <td>L2 索引</td>
            <td>L1 索引</td>
            <td>L0 索引</td>
            <td>页内偏移</td>
          </tr>
          <tr>
            <td class="row-label">位范围</td>
            <td>[38:30]</td>
            <td>[29:21]</td>
            <td>[20:12]</td>
            <td>[11:0]</td>
          </tr>
          <tr class="row-bits">
            <td class="row-label">位值</td>
            <td><code>{{ vpnBin.vpn2 }}</code></td>
            <td><code>{{ vpnBin.vpn1 }}</code></td>
            <td><code>{{ vpnBin.vpn0 }}</code></td>
            <td><code>{{ vpnBin.offset }}</code></td>
          </tr>
          <tr>
            <td class="row-label">值 (hex)</td>
            <td><code class="val-hex">{{ vpnHex.vpn2 }}</code></td>
            <td><code class="val-hex">{{ vpnHex.vpn1 }}</code></td>
            <td><code class="val-hex">{{ vpnHex.vpn0 }}</code></td>
            <td><code class="val-hex">{{ vpnHex.offset }}</code></td>
          </tr>
        </tbody>
      </table>
    </n-card>

    <div v-if="currentStep >= 1" class="steps-section">
      <n-card
        ref="step1Card"
        size="small"
        :class="['step-card', { active: currentStep === 1 }]"
      >
        <template #header>
          <div class="step-header">
            <span>步骤 1：获取 Level 2 PTE（根页表 swapper_pg_dir）</span>
            <n-tag v-if="currentStep > 1" type="success" size="small">已完成</n-tag>
            <n-tag v-else-if="currentStep === 1" type="info" size="small">当前</n-tag>
          </div>
        </template>

        <div class="gdb-box">
          <span class="gdb-label">GDB 命令：</span>
          <code class="gdb-cmd">{{ gdbCmdL2 }}</code>
        </div>

        <div class="input-action-row">
          <n-input
            v-model:value="pte2Input"
            placeholder="输入 GDB 返回的十六进制值"
            style="flex:1"
            @keyup.enter="fetchL2"
          />
          <n-button type="primary" @click="fetchL2" :disabled="!pte2Input.trim()">
            下一步
          </n-button>
        </div>
        <p v-if="pte2Error" class="step-error">{{ pte2Error }}</p>

        <div v-if="pte2Info" class="pte-result">
          <n-space vertical size="small">
            <div><strong>PTE：</strong>{{ pte2Info.hex }}</div>
            <div><strong>PPN：</strong>{{ bnHex(pte2Info.PFN, 8) }}</div>
            <div><strong>PMD 物理地址：</strong>{{ bnHex(pte2Info.PA) }}</div>
            <div><strong>PMD 虚拟地址：</strong>{{ pmdVa ? bnHex(pmdVa) : '' }}</div>
            <div class="calc-box">
              <div class="calc-title">计算过程</div>
              <div><code>PMD PA = (PTE &gt;&gt; 10) &lt;&lt; 12</code></div>
              <div>= ({{ pte2Info.hex }} &gt;&gt; 10) &lt;&lt; 12</div>
              <div>= {{ bnHex(pte2Info.PFN, 8) }} &lt;&lt; 12</div>
              <div>= <strong>{{ bnHex(pte2Info.PA) }}</strong></div>
              <div style="margin-top:6px"><code>PMD VA = PMD PA + PA2VA_OFFSET</code></div>
              <div>= {{ bnHex(pte2Info.PA) }} + 0xffffffe000000000 − 0x80000000</div>
              <div>= <strong>{{ pmdVa ? bnHex(pmdVa) : '' }}</strong></div>
            </div>
            <n-space :size="4">
              <n-tag :type="pte2Info.V ? 'success' : 'default'" size="tiny">V={{ pte2Info.V ? 1 : 0 }}</n-tag>
              <n-tag :type="pte2Info.R ? 'success' : 'default'" size="tiny">R={{ pte2Info.R ? 1 : 0 }}</n-tag>
              <n-tag :type="pte2Info.W ? 'success' : 'default'" size="tiny">W={{ pte2Info.W ? 1 : 0 }}</n-tag>
              <n-tag :type="pte2Info.X ? 'success' : 'default'" size="tiny">X={{ pte2Info.X ? 1 : 0 }}</n-tag>
            </n-space>
            <table v-if="pte2Fields" class="pte-fields-table">
              <thead>
                <tr>
                  <th>字段</th>
                  <th>位</th>
                  <th>值 (hex)</th>
                  <th>值 (bin)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in pte2Fields" :key="f.name" :class="{ 'row-flags': f.highlight }">
                  <td class="field-name">{{ f.name }}</td>
                  <td>{{ f.bits }}</td>
                  <td><code>{{ f.hex }}</code></td>
                  <td><code class="bin-val">{{ f.bin }}</code></td>
                </tr>
              </tbody>
            </table>
          </n-space>
        </div>
      </n-card>

      <n-card
        ref="step2Card"
        v-if="currentStep >= 2"
        size="small"
        :class="['step-card', { active: currentStep === 2 }]"
      >
        <template #header>
          <div class="step-header">
            <span>步骤 2：获取 Level 1 PTE（中间页表 PMD）</span>
            <n-tag v-if="currentStep > 2" type="success" size="small">已完成</n-tag>
            <n-tag v-else-if="currentStep === 2" type="info" size="small">当前</n-tag>
          </div>
        </template>

        <div class="gdb-box">
          <span class="gdb-label">GDB 命令：</span>
          <code class="gdb-cmd">{{ gdbCmdL1 }}</code>
        </div>

        <div class="input-action-row">
          <n-input
            v-model:value="pte1Input"
            placeholder="输入 GDB 返回的十六进制值"
            style="flex:1"
            @keyup.enter="fetchL1"
          />
          <n-button type="primary" @click="fetchL1" :disabled="!pte1Input.trim()">
            下一步
          </n-button>
        </div>
        <p v-if="pte1Error" class="step-error">{{ pte1Error }}</p>

        <div v-if="pte1Info" class="pte-result">
          <n-space vertical size="small">
            <div><strong>PTE：</strong>{{ pte1Info.hex }}</div>
            <div><strong>PPN：</strong>{{ bnHex(pte1Info.PFN, 8) }}</div>
            <div><strong>PTE 物理地址：</strong>{{ bnHex(pte1Info.PA) }}</div>
            <div><strong>PTE 虚拟地址：</strong>{{ pteVa ? bnHex(pteVa) : '' }}</div>
            <div class="calc-box">
              <div class="calc-title">计算过程</div>
              <div><code>PTE PA = (PTE &gt;&gt; 10) &lt;&lt; 12</code></div>
              <div>= ({{ pte1Info.hex }} &gt;&gt; 10) &lt;&lt; 12</div>
              <div>= {{ bnHex(pte1Info.PFN, 8) }} &lt;&lt; 12</div>
              <div>= <strong>{{ bnHex(pte1Info.PA) }}</strong></div>
              <div style="margin-top:6px"><code>PTE VA = PTE PA + PA2VA_OFFSET</code></div>
              <div>= {{ bnHex(pte1Info.PA) }} + 0xffffffe000000000 − 0x80000000</div>
              <div>= <strong>{{ pteVa ? bnHex(pteVa) : '' }}</strong></div>
            </div>
            <n-space :size="4">
              <n-tag :type="pte1Info.V ? 'success' : 'default'" size="tiny">V={{ pte1Info.V ? 1 : 0 }}</n-tag>
              <n-tag :type="pte1Info.R ? 'success' : 'default'" size="tiny">R={{ pte1Info.R ? 1 : 0 }}</n-tag>
              <n-tag :type="pte1Info.W ? 'success' : 'default'" size="tiny">W={{ pte1Info.W ? 1 : 0 }}</n-tag>
              <n-tag :type="pte1Info.X ? 'success' : 'default'" size="tiny">X={{ pte1Info.X ? 1 : 0 }}</n-tag>
            </n-space>
            <table v-if="pte1Fields" class="pte-fields-table">
              <thead>
                <tr>
                  <th>字段</th>
                  <th>位</th>
                  <th>值 (hex)</th>
                  <th>值 (bin)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in pte1Fields" :key="f.name" :class="{ 'row-flags': f.highlight }">
                  <td class="field-name">{{ f.name }}</td>
                  <td>{{ f.bits }}</td>
                  <td><code>{{ f.hex }}</code></td>
                  <td><code class="bin-val">{{ f.bin }}</code></td>
                </tr>
              </tbody>
            </table>
          </n-space>
        </div>
      </n-card>

      <n-card
        ref="step3Card"
        v-if="currentStep >= 3"
        size="small"
        :class="['step-card', { active: currentStep === 3 }]"
      >
        <template #header>
          <div class="step-header">
            <span>步骤 3：获取 Level 0 PTE（叶子页表）</span>
            <n-tag v-if="currentStep > 3" type="success" size="small">已完成</n-tag>
            <n-tag v-else-if="currentStep === 3" type="info" size="small">当前</n-tag>
          </div>
        </template>

        <div class="gdb-box">
          <span class="gdb-label">GDB 命令：</span>
          <code class="gdb-cmd">{{ gdbCmdL0 }}</code>
        </div>

        <div class="input-action-row">
          <n-input
            v-model:value="pte0Input"
            placeholder="输入 GDB 返回的十六进制值"
            style="flex:1"
            @keyup.enter="fetchL0"
          />
          <n-button type="primary" @click="fetchL0" :disabled="!pte0Input.trim()">
            下一步
          </n-button>
        </div>
        <p v-if="pte0Error" class="step-error">{{ pte0Error }}</p>

        <div v-if="pte0Info" class="pte-result">
          <n-space vertical size="small">
            <div><strong>PTE：</strong>{{ pte0Info.hex }}</div>
            <div><strong>PPN：</strong>{{ bnHex(pte0Info.PFN, 8) }}</div>
            <div><strong>叶子物理地址：</strong>{{ bnHex(pte0Info.PA) }}</div>
            <n-space :size="4">
              <n-tag :type="pte0Info.V ? 'success' : 'default'" size="tiny">V={{ pte0Info.V ? 1 : 0 }}</n-tag>
              <n-tag :type="pte0Info.R ? 'success' : 'default'" size="tiny">R={{ pte0Info.R ? 1 : 0 }}</n-tag>
              <n-tag :type="pte0Info.W ? 'success' : 'default'" size="tiny">W={{ pte0Info.W ? 1 : 0 }}</n-tag>
              <n-tag :type="pte0Info.X ? 'success' : 'default'" size="tiny">X={{ pte0Info.X ? 1 : 0 }}</n-tag>
            </n-space>
            <table v-if="pte0Fields" class="pte-fields-table">
              <thead>
                <tr>
                  <th>字段</th>
                  <th>位</th>
                  <th>值 (hex)</th>
                  <th>值 (bin)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in pte0Fields" :key="f.name" :class="{ 'row-flags': f.highlight }">
                  <td class="field-name">{{ f.name }}</td>
                  <td>{{ f.bits }}</td>
                  <td><code>{{ f.hex }}</code></td>
                  <td><code class="bin-val">{{ f.bin }}</code></td>
                </tr>
              </tbody>
            </table>
          </n-space>
        </div>
      </n-card>

      <n-card ref="resultCard" v-if="currentStep >= 4" size="small" class="result-card">
        <template #header>
          <span style="font-weight:600;color:#065f46">最终结果</span>
        </template>
        <div v-if="pte0Info" class="result-content">
          <n-grid :cols="2" :x-gap="16" :y-gap="8">
            <n-gi>
              <div class="result-label">叶子 PTE 值</div>
              <code class="result-value">{{ pte0Info.hex }}</code>
            </n-gi>
            <n-gi>
              <div class="result-label">PPN</div>
              <code class="result-value">{{ bnHex(pte0Info.PFN, 8) }}</code>
            </n-gi>
            <n-gi>
              <div class="result-label">最终物理地址</div>
              <code class="result-value">{{ bnHex(pte0Info.PA) }}</code>
            </n-gi>
            <n-gi>
              <div class="result-label">权限</div>
              <n-space :size="4">
                <n-tag :type="pte0Info.V ? 'success' : 'default'" size="small">V={{ pte0Info.V ? 1 : 0 }}</n-tag>
                <n-tag :type="pte0Info.R ? 'success' : 'default'" size="small">R={{ pte0Info.R ? 1 : 0 }}</n-tag>
                <n-tag :type="pte0Info.W ? 'success' : 'default'" size="small">W={{ pte0Info.W ? 1 : 0 }}</n-tag>
                <n-tag :type="pte0Info.X ? 'success' : 'default'" size="small">X={{ pte0Info.X ? 1 : 0 }}</n-tag>
              </n-space>
            </n-gi>
          </n-grid>
        </div>
      </n-card>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto Mono', 'LXGW-Wenkai-Screen', monospace;
  color: #1e293b;
}

.title {
  text-align: center;
  font-size: 1.6rem;
  margin-bottom: 20px;
}

.input-card {
  margin-bottom: 16px;
}

.vpn-card {
  margin-bottom: 16px;
}

.va-display {
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.va-label {
  font-size: 0.85rem;
  color: #64748b;
}

.va-full {
  font-family: 'Roboto Mono', monospace;
  font-size: 1rem;
  font-weight: 600;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 4px;
}

.vpn-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  text-align: center;
}

.vpn-table th,
.vpn-table td {
  padding: 8px 10px;
  border: 1px solid #e2e8f0;
}

.vpn-table thead th {
  font-weight: 700;
  font-size: 0.9rem;
}

.col-label { width: 70px; text-align: left; }
.col-vpn2  { background: #eff6ff; }
.col-vpn1  { background: #ecfdf5; }
.col-vpn0  { background: #f5f3ff; }
.col-offset { background: #f8fafc; }

.vpn-table tbody td {
  font-family: 'Roboto Mono', monospace;
}

.vpn-table .row-label {
  font-family: 'Roboto Mono', monospace;
  font-weight: 600;
  color: #475569;
  text-align: left;
  background: #f8fafc;
}

.vpn-table .row-bits td {
  font-family: 'Roboto Mono', monospace;
  letter-spacing: 1px;
  word-break: break-all;
}

.vpn-table .val-hex {
  font-weight: 700;
  color: #0f172a;
  font-size: 0.95rem;
}

.steps-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-card {
  transition: border-color 0.2s;
  border: 1px solid #e2e8f0;
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

.gdb-box {
  background: #1e293b;
  color: #10b981;
  padding: 10px 14px;
  border-radius: 6px;
  margin: 8px 0 12px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
}

.gdb-label {
  color: #94a3b8;
  white-space: nowrap;
  flex-shrink: 0;
}

.gdb-cmd {
  color: #4ade80;
  font-family: 'Roboto Mono', monospace;
  white-space: nowrap;
}

.input-action-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.step-error {
  color: #d03050;
  font-size: 0.85rem;
  margin-top: 6px;
}

.pte-result {
  margin-top: 12px;
  background: #f8fafc;
  padding: 12px;
  border-radius: 6px;
  font-size: 0.9rem;
}

.pte-fields-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
  font-size: 0.8rem;
}

.pte-fields-table th,
.pte-fields-table td {
  padding: 4px 10px;
  border: 1px solid #e2e8f0;
  text-align: center;
  font-family: 'Roboto Mono', monospace;
}

.pte-fields-table th {
  background: #f1f5f9;
  font-weight: 600;
  color: #475569;
}

.pte-fields-table .field-name {
  font-weight: 600;
  color: #0f172a;
  text-align: left;
}

.pte-fields-table .row-flags {
  background: #fefce8;
}

.pte-fields-table .bin-val {
  letter-spacing: 0.5px;
  font-size: 0.78rem;
}

.calc-box {
  background: #fefce8;
  border: 1px solid #fde68a;
  border-radius: 6px;
  padding: 8px 12px;
  margin-top: 8px;
  font-size: 0.82rem;
  font-family: 'Roboto Mono', monospace;
  line-height: 1.8;
}

.calc-title {
  font-weight: 700;
  color: #92400e;
  margin-bottom: 2px;
  font-size: 0.85rem;
}

.calc-box code {
  background: #fef3c7;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 0.8rem;
}

.result-card {
  border: 1px solid #10b981;
  background: #f0fdf4;
}

.result-content {
  font-size: 0.9rem;
}

.result-label {
  color: #475569;
  font-size: 0.8rem;
  margin-bottom: 4px;
}

.result-value {
  font-family: 'Roboto Mono', monospace;
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  background: #e2e8f0;
  padding: 2px 6px;
  border-radius: 3px;
}
</style>
