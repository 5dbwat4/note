<script setup lang="ts">
import { ref, computed } from 'vue'
import { NButton, NInput, NCard, NTag, NInputGroup, NAlert } from 'naive-ui'

const PA2VA_OFFSET = 0xffffffe000000000n - 0x80000000n

const satpInput = ref('0x8000000000080020')
const errorMsg = ref('')
const satpVal = ref<bigint | null>(null)

const mode = ref<number>(0)
const asid = ref<number>(0)
const ppn = ref<bigint | null>(null)
const rootPA = ref<bigint | null>(null)
const rootVA = ref<bigint | null>(null)

function bnHex(v: bigint, pad = 16): string {
  return '0x' + v.toString(16).padStart(pad, '0')
}

interface FieldRow {
  name: string
  desc: string
  bits: string
  hex: string
  bin: string
}

const fields = computed<FieldRow[] | null>(() => {
  if (satpVal.value === null || ppn.value === null) return null
  const val = satpVal.value

  const m = Number((val >> 60n) & 0xfn)
  const a = Number((val >> 44n) & 0xffffn)
  const p = val & 0xfffffffffffn   // 44-bit PPN

  const format = (v: bigint, w: number) => ({
    hex: bnHex(v, Math.ceil(w / 4)),
    bin: v.toString(2).padStart(w, '0')
  })

  return [
    { name: 'MODE', desc: 'Sv39', bits: '63:60', ...format(BigInt(m), 4) },
    { name: 'ASID', desc: '地址空间ID', bits: '59:44', ...format(BigInt(a), 16) },
    { name: 'PPN',  desc: '根页表物理页号', bits: '43:0', ...format(p, 44) },
  ]
})

function parseSATp() {
  errorMsg.value = ''
  try {
    const raw = satpInput.value.trim()
    const val = BigInt(raw)
    if (val < 0n || val > 0xffffffffffffffffn) throw new Error()
    satpVal.value = val

    mode.value = Number((val >> 60n) & 0xfn)
    asid.value = Number((val >> 44n) & 0xffffn)
    ppn.value = val & 0xfffffffffffn

    rootPA.value = ppn.value << 12n
    rootVA.value = rootPA.value + PA2VA_OFFSET
  } catch {
    errorMsg.value = '无效的 SATP 值，请输入类似 0x8000000000080020'
    satpVal.value = null
    ppn.value = null
    rootPA.value = null
    rootVA.value = null
  }
}
</script>

<template>
  <div class="app-container">
    <h1 class="title">RISC‑V Sv39 SATP 寄存器解析</h1>

    <n-card size="small" class="input-card">
      <n-input-group>
        <n-input
          v-model:value="satpInput"
          placeholder="SATP 值，如 0x8000000000080020"
          clearable
          style="flex:1"
          @keyup.enter="parseSATp"
        />
        <n-button type="primary" @click="parseSATp" :disabled="!satpInput.trim()">
          解析
        </n-button>
      </n-input-group>
      <n-alert v-if="errorMsg" type="error" style="margin-top:10px">
        {{ errorMsg }}
      </n-alert>
    </n-card>

    <template v-if="fields && satpVal !== null">
      <n-card size="small" class="vpn-card">
        <template #header>SATP 位域分解</template>

        <div class="formula-box">
          <code>satp = (MODE &lt;&lt; 60) | (ASID &lt;&lt; 44) | PPN</code>
        </div>

        <table class="vpn-table">
          <thead>
            <tr>
              <th class="col-label"></th>
              <th class="col-mode">MODE</th>
              <th class="col-asid">ASID</th>
              <th class="col-ppn">PPN</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="row-label">字段</td>
              <td>地址转换模式</td>
              <td>地址空间 ID</td>
              <td>根页表物理页号</td>
            </tr>
            <tr>
              <td class="row-label">位范围</td>
              <td>[63:60]</td>
              <td>[59:44]</td>
              <td>[43:0]</td>
            </tr>
            <tr class="row-bits">
              <td class="row-label">位值</td>
              <td><code>{{ fields[0].bin }}</code></td>
              <td><code>{{ fields[1].bin }}</code></td>
              <td><code>{{ fields[2].bin }}</code></td>
            </tr>
            <tr>
              <td class="row-label">值 (hex)</td>
              <td><code class="val-hex">{{ fields[0].hex }}</code></td>
              <td><code class="val-hex">{{ fields[1].hex }}</code></td>
              <td><code class="val-hex">{{ fields[2].hex }}</code></td>
            </tr>
            <tr class="row-desc">
              <td class="row-label"></td>
              <td>8 = Sv39</td>
              <td></td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </n-card>

      <n-card size="small" class="calc-card">
        <template #header>计算过程</template>

        <div class="calc-steps">
          <div class="calc-step">
            <n-tag type="info" size="small">1</n-tag>
            <span class="calc-text">
              MODE = (satp &gt;&gt; 60) &amp; 0xf = <code>{{ mode }}</code>
              <template v-if="mode === 8">
                <n-tag type="success" size="small" style="margin-left:6px">Sv39</n-tag>
              </template>
              <template v-else>
                <n-tag type="warning" size="small" style="margin-left:6px">非 Sv39</n-tag>
              </template>
            </span>
          </div>

          <div class="calc-step">
            <n-tag type="info" size="small">2</n-tag>
            <span class="calc-text">
              ASID = (satp &gt;&gt; 44) &amp; 0xffff = <code>{{ asid }}</code>
            </span>
          </div>

          <div class="calc-step">
            <n-tag type="info" size="small">3</n-tag>
            <span class="calc-text">
              PPN = satp &amp; 0xfffffffffff = <code>{{ bnHex(ppn!, 11) }}</code>
            </span>
          </div>

          <div class="calc-step">
            <n-tag type="info" size="small">4</n-tag>
            <span class="calc-text">
              根页表物理地址 = PPN &lt;&lt; 12 = <code>{{ bnHex(rootPA!) }}</code>
            </span>
          </div>

          <div class="calc-step">
            <n-tag type="info" size="small">5</n-tag>
            <span class="calc-text">
              根页表虚拟地址 = PA + PA2VA_OFFSET = <code>{{ bnHex(rootVA!) }}</code>
            </span>
          </div>
        </div>
      </n-card>

      <n-card size="small" class="result-card">
        <template #header>
          <span class="result-title">结果</span>
        </template>
        <table class="result-table">
          <tr>
            <td>根页表物理地址</td>
            <td><code class="result-value">{{ bnHex(rootPA!) }}</code></td>
          </tr>
          <tr>
            <td>根页表虚拟地址</td>
            <td><code class="result-value">{{ bnHex(rootVA!) }}</code></td>
          </tr>
          <tr>
            <td>构造公式</td>
            <td><code class="result-value">(8 &lt;&lt; 60) | ({{ bnHex(rootPA!, 11) }} &gt;&gt; 12)</code></td>
          </tr>
        </table>
      </n-card>
    </template>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 800px;
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

.formula-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 14px;
  text-align: center;
}

.formula-box code {
  font-family: 'Roboto Mono', monospace;
  font-size: 0.95rem;
  color: #0f172a;
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
.col-mode  { background: #eff6ff; }
.col-asid  { background: #fefce8; }
.col-ppn   { background: #ecfdf5; }

.vpn-table tbody td {
  font-family: 'Roboto Mono', monospace;
}

.vpn-table .row-label {
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

.vpn-table .row-desc td {
  color: #64748b;
  font-size: 0.8rem;
}

.calc-card {
  margin-bottom: 16px;
}

.calc-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.calc-step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 0.9rem;
}

.calc-text {
  line-height: 1.6;
}

.calc-text code {
  font-family: 'Roboto Mono', monospace;
  font-weight: 700;
  color: #0f172a;
  background: #e2e8f0;
  padding: 1px 5px;
  border-radius: 3px;
}

.result-card {
  border: 1px solid #10b981;
  background: #f0fdf4;
}

.result-title {
  font-weight: 600;
  color: #065f46;
}

.result-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.result-table td {
  padding: 8px 12px;
  border: 1px solid #a7f3d0;
}

.result-table td:first-child {
  font-weight: 600;
  color: #475569;
  width: 180px;
  background: #ecfdf5;
}

.result-value {
  font-family: 'Roboto Mono', monospace;
  font-weight: 700;
  color: #0f172a;
}
</style>
