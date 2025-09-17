<template>
  <n-card hoverable title="小红书分享链接解密">
    <n-p>由于CORS原因，xhslink.com短链接无法在浏览器环境中解析</n-p>
    <n-p
      >请先在浏览器中访问以 xhslink.com 开头的链接，跳转成 www.xiaohongshu.com
      开头的链接后完整粘贴至下方</n-p
    >

    <n-form-item
      label="分享链接"
      :validation-status="inputValidationStatus"
      :feedback="inputFeedback"
    >
      <n-input v-model:value="shareURL" @keyup.enter="submitDecode"></n-input>
    </n-form-item>

    <div v-if="showDecode">
      <n-p>
        分享者ID：{{ shareer }} | 分享者主页：
        <a :href="'https://www.xiaohongshu.com/user/profile/' + shareer">
            link
        </a>
      </n-p>

      <iframe :src="'https://www.xiaohongshu.com/user/profile/' + shareer"
        style="width: 100%;border: aqua dotted;height: 100vh;"></iframe>
    </div>
  </n-card>
</template>
<script setup>
import { ref } from "@vue/runtime-core";
import { computed } from "@vue/runtime-core";

const shareURL = ref("");
const shareer = ref("");
const showDecode = ref(false);
const inputValidationStatus = computed(() => {
  if (shareURL.value == "") {
    return undefined;
  }
  try {
    const url = new URL(shareURL.value);
    if (!url.searchParams?.has("shareRedId")) {
      return "error";
    }
    return "success";
  } catch (e) {
    return "error";
  }
});
const inputFeedback = computed(() => {
  if (shareURL.value == "") {
    return "";
  }
  try {
    const url = new URL(shareURL.value);
    if(url.hostname=="xhslink.com"){
        return "请先访问该链接，获取域名为xiaohongshu.com的链接并输入"
    }
    if (!url.searchParams?.get("shareRedId")) {
      return "不包含分享者信息";
    }
    return "*Press Enter*";
  } catch (e) {
    return "请输入有效的URL";
  }
});

const submitDecode = () => {
  const encoded = new URL(shareURL.value).searchParams?.get("shareRedId");
  if (!encoded) return false;

  const RFC4648_5_base64_decode = (b64) => {
    const DEC = {
      "-": "+",
      _: "/",
      ".": "=",
    };
    return atob(b64.replace(/[-_.]/g, (m) => DEC[m]));
  };
  const toLower = (charCode) => (charCode > 65 ? charCode + 32 : charCode);

  const reshape = [
    2, 6, 2, 0, 3, 5, 4, 9, 6, 7, 5, 2, 9, 8, 0, 6, 6, 3, 9, 7, 4, 5, 6, 9,
  ];
  const decoded = RFC4648_5_base64_decode(encoded)
    .split("")
    .map((char, i) => {
      return String.fromCharCode(toLower(char.charCodeAt(0) - reshape[i]));
    })
    .join("");
  showDecode.value = true;
  shareer.value = decoded;
};
</script>
