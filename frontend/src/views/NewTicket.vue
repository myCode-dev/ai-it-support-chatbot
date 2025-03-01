<template>
  <div class="support-container">
    <el-card class="support-card">
      <h2>📩 IT Support Ticket</h2>

      <el-form ref="formRef" :model="formData" label-width="140px" :rules="rules">
        <!-- 👤 使用者姓名 -->
        <el-form-item label="Your Name" prop="name">
          <el-input v-model="formData.name" placeholder="Enter your name..." />
        </el-form-item>

        <!-- 📧 Email -->
        <el-form-item label="Email" prop="email">
          <el-input v-model="formData.email" placeholder="Enter your email..." />
        </el-form-item>

        <!-- 💻 設備類型 -->
        <el-form-item label="Device Type" prop="device">
          <el-select v-model="formData.device" placeholder="Select a device">
            <el-option label="Laptop" value="Laptop" />
            <el-option label="Desktop" value="Desktop" />
            <el-option label="Printer" value="Printer" />
            <el-option label="Network" value="Network" />
            <el-option label="Software Issue" value="Software" />
            <el-option label="Other" value="Other" />
          </el-select>
        </el-form-item>

        <!-- 📝 問題描述 -->
        <el-form-item label="Issue Description" prop="issue">
          <el-input v-model="formData.issue" type="textarea" :rows="4" placeholder="Describe your issue..." />
        </el-form-item>

        <!-- 📎 附加檔案 -->
        <el-form-item label="Attach Screenshot">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :before-upload="handleFileUpload"
          >
            <el-button type="primary">Upload File</el-button>
          </el-upload>
        </el-form-item>

        <br>
        <!-- 📨 提交按鈕 -->
        <el-button style='float:right;' type='primary'>submit</el-button>
      </el-form>

      <!-- 🎟️ 顯示報修單號 -->
      <el-alert v-if="ticketId" type="success" show-icon class="ticket-alert">
        ✅ Ticket Submitted! Your Ticket ID: <strong>{{ ticketId }}</strong>
      </el-alert>
    </el-card>
  </div>
</template>


<script setup>
import { ref } from "vue";
import axios from "axios";

const formRef = ref(null);
const formData = ref({
  name: "",
  email: "",
  phone: "",
  device: "",
  issue: "",
  screenshot: null,
});

const ticketId = ref(null);
const loading = ref(false);

// **📌 表單驗證規則**
const rules = {
  name: [{ required: true, message: "Please enter your name", trigger: "blur" }],
  email: [{ required: true, message: "Please enter your email", trigger: "blur" }],
  device: [{ required: true, message: "Please select a device type", trigger: "change" }],
  issue: [{ required: true, message: "Please describe your issue", trigger: "blur" }],
};

// **📌 檔案上傳處理**
const handleFileUpload = (file) => {
  formData.value.screenshot = file;
  return false; // 阻止 Element UI 自動上傳
};

// **📌 提交報修單**
const submitTicket = async () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return;

    loading.value = true;

    try {
      const formDataObj = new FormData();
      formDataObj.append("user_id", "user123");
      formDataObj.append("name", formData.value.name);
      formDataObj.append("email", formData.value.email);
      formDataObj.append("phone", formData.value.phone);
      formDataObj.append("device", formData.value.device);
      formDataObj.append("issue", formData.value.issue);

      if (formData.value.screenshot) {
        formDataObj.append("screenshot", formData.value.screenshot);
      }

      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/ticket`, formDataObj, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      ticketId.value = res.data.ticket_id;
    } catch (error) {
      console.error("Error submitting ticket:", error);
      ElMessage.error("Failed to submit the ticket. Please try again.");
    } finally {
      loading.value = false;
    }
  });
};
</script>


<style scoped>
.support-container {
  max-width: 600px;
  margin: 0px auto;
}

.support-card {
  padding: 20px;
  border-radius: 8px;
}

.ticket-alert {
  margin-top: 15px;
}

.upload-demo {
  display: flex;
  justify-content: center;
}
</style>
